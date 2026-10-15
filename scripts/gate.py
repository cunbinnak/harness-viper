#!/usr/bin/env python3
"""gate.py — kiểm điều kiện rời phase. In ✓/✗ từng mục, exit 1 nếu còn thiếu.

KHÔNG chặn tool, KHÔNG sửa gì. Chỉ báo. Quyết định đi tiếp vẫn là của người.
Nguồn chuẩn của gate: PROTOCOL.md §6. Lệch nhau thì PROTOCOL thắng.

Usage:
    python scripts/gate.py                      # tự đọc phase từ STATE.md
    python scripts/gate.py DOCUMENT|BUILD|VERIFY|SHIP|NEXT-WAVE

Exit: 0 qua · 1 còn thiếu · 2 sai tham số.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "STATE.md"

# kind chạy dưới dạng container (có health qua docker) — mobile chạy emulator, không proof qua docker.
CONTAINERIZED = {"backend", "bff", "web"}

# Windows console (cp1252) không in được Unicode — ép UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------- readers ----

def read(rel: str) -> str:
    p = ROOT / rel
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


def read_live(rel_or_text: str, *, is_text: bool = False) -> str:
    """Bỏ HTML comment <!-- --> trước khi đếm (guidance không tính)."""
    text = rel_or_text if is_text else read(rel_or_text)
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def filled(rel: str) -> bool:
    """File tồn tại, có nội dung, và không còn placeholder {{...}} (ngoài comment)."""
    live = read_live(rel).strip()
    return bool(live) and "{{" not in live


def count_rows(rel: str, pattern: str) -> int:
    return len(re.findall(pattern, read_live(rel), flags=re.MULTILINE))


def section(rel: str, header: str) -> str:
    """Cắt nội dung một `## header` (tới `## ` kế tiếp)."""
    text = read_live(rel)
    m = re.search(rf"^#{{1,4}}\s*{re.escape(header)}.*?$(.*?)(?=^#{{1,4}}\s|\Z)",
                  text, flags=re.MULTILINE | re.DOTALL)
    return m.group(1) if m else ""


def table_rows(text: str) -> list[list[str]]:
    """Parse các dòng bảng markdown → list ô (bỏ header + separator)."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= {"-", ":", " "} for c in cells):  # separator
            continue
        rows.append(cells)
    return rows[1:] if rows else []  # bỏ header


def state_field(name: str) -> str:
    m = re.search(rf"{re.escape(name)}\s*:\s*(.+)", read("STATE.md"))
    return m.group(1).strip() if m else ""


def phase_from_state() -> str:
    return state_field("Phase hiện tại").upper().replace(" ", "-") or ""


def state_wave() -> str:
    return state_field("Wave").strip()


def scope_locked() -> bool:
    return bool(re.search(r"- \[[xX]\].*Scope khoá", read("STATE.md")))


def challenge_count(phase: str) -> int:
    """Số dòng §Challenge log của phase này có kết quả PASS (1 dòng = 1 câu hỏi)."""
    return sum(1 for cells in table_rows(section("STATE.md", "Challenge log"))
               if len(cells) >= 4 and cells[1].upper().startswith(phase[:3]) and "PASS" in cells[3].upper())


def challenge_pass(phase: str) -> bool:
    return challenge_count(phase) >= 1


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=20).stdout.strip()
    except Exception:
        return ""


def last_code_commit() -> str:
    """Commit mới nhất chạm `services/` — proof.json phải chụp đúng commit này."""
    return _git("log", "-1", "--format=%H", "--", "services")


def roadmap_wave_row(wave: str) -> list[str]:
    for cells in table_rows(section("docs/ROADMAP.md", "§1")):
        if cells and cells[0].strip() == str(wave):
            return cells
    return []


def parse_wave_targets(wave: str) -> list[tuple[str, str]]:
    """ROADMAP §1 cột Target → [(name, kind)]. Ô dạng `name (kind), name (kind)`."""
    row = roadmap_wave_row(wave)
    idx = _col_index("Target")
    if not row or idx is None or idx >= len(row):
        return []
    return [(n, k.lower()) for n, k in re.findall(r"([\w.\-]+)\s*\(\s*(\w+)\s*\)", row[idx])]


def parse_wave_feats(wave: str) -> set[str]:
    """FEAT id in-scope của wave — từ ROADMAP §1 cột AC in-scope."""
    row = roadmap_wave_row(wave)
    idx = _col_index("AC in-scope")
    if not row or idx is None or idx >= len(row):
        return set()
    return set(re.findall(r"FEAT-[\w-]+", row[idx]))


def _screen_map_rows() -> list[dict]:
    """SCREEN-MAP -> list dict theo header (mỗi bảng con tự dò header lại). Bỏ dòng tách + dòng nhóm."""
    rows, head = [], None
    for ln in read("docs/ux/SCREEN-MAP.md").splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            head = None if not s else head
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if re.match(r"^[\s:|-]+$", s):
            continue
        if any(c.lower() == "mockup" for c in cells):          # dòng header
            head = [c.lower() for c in cells]
            continue
        if head and len(cells) == len(head):
            rows.append(dict(zip(head, cells)))
    return rows


def wave_screens(wave: str) -> list[dict]:
    """Màn UI in-scope wave. Format mới (cột `wave` + `mã màn`): lọc theo cột Wave.
    Format cũ: tag `(Wave N)` ô Mockup > FEAT in-scope > tên màn nêu trong hàng ROADMAP."""
    feats = parse_wave_feats(wave)
    wave_text = " ".join(roadmap_wave_row(wave))
    out = []
    for r in _screen_map_rows():
        text = " ".join(r.values())
        if "wave" in r:
            in_scope = re.sub(r"\D", "", r["wave"]) == str(wave)
        else:
            tag = re.search(r"\(\s*Wave\s*(\d+)", r.get("mockup", ""), re.I)
            stems = [h[:-5] for h in re.findall(r"([\w\-]+\.html)", text)]
            in_scope = (tag.group(1) == str(wave)) if tag else (
                any(f in text for f in feats)
                or any(re.search(rf"(?<![\w-]){re.escape(s)}(?![\w-])", wave_text) for s in stems))
        if in_scope and re.search(r"\b(web|mobile)\b", text):
            r["_code"] = r.get("mã màn") or next(iter(r.values()), "?")
            out.append(r)
    return out


def missing_wave_mockups(wave: str) -> list[str]:
    """Màn UI in-scope wave mà ô Mockup KHÔNG trỏ tới mockup tồn tại — file, và (nếu có `#Mã`) section
    `id` đúng mã trong file. Bắt "khai màn/màn con (tab/modal/form) nhưng lười không vẽ" — lỗ lan chuỗi:
    picky không có gì để so + arch §3 không ai đòi API cho nó."""
    files = {p.name: p for p in (ROOT / "docs" / "ux" / "mockups").rglob("*.html")}
    missing = []
    for r in wave_screens(wave):
        refs = re.findall(r"([\w\-]+\.html)(?:#([\w\-]+))?", r.get("mockup", ""))
        ok = False
        for fname, anchor in refs:
            f = files.get(fname)
            html = f.read_text(encoding="utf-8", errors="ignore") if f else ""
            if f and (not anchor or re.search(r"id=[\"']" + re.escape(anchor) + r"[\"']", html)):
                ok = True
                break
        if not ok:
            missing.append(r["_code"])
    return missing


_COLOR_REF = r"`?(#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b|--[\w-]+)`?"
_PAIR = re.compile(_COLOR_REF + r"[^`|\n#]{0,40}?\btrên\s+" + _COLOR_REF)


def _luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    chans = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        chans.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * chans[0] + 0.7152 * chans[1] + 0.0722 * chans[2]


def contrast_ratio(fg: str, bg: str) -> float:
    """Tỉ số tương phản WCAG 2.x giữa hai mã hex (#rgb / #rrggbb)."""
    a, b = sorted((_luminance(fg), _luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def contrast_pairs(rel: str = "docs/DESIGN-SYSTEM.md") -> tuple[list[tuple], list[str]]:
    """Đọc khối "cặp tương phản" của DESIGN-SYSTEM → [(chữ, nền, hex chữ, hex nền, tỉ số, ngưỡng)] + lỗi tra token.
    Token tra từ `:root` (`--x: #hex;` hoặc `var(--y)`) và bảng §2 (| `--x` | `#hex` |). Ghi `lớn` trong cùng vế → ngưỡng 3:1."""
    text = read_live(rel)
    tokens: dict[str, str] = {}
    for name, val in re.findall(r"(--[\w-]+)\s*:\s*([^;\n]+);", text):
        tokens.setdefault(name, val.strip())
    for name, val in re.findall(r"\|\s*`(--[\w-]+)`\s*\|\s*`?([^`|]+?)`?\s*\|", text):
        tokens.setdefault(name, val.strip())

    def resolve(ref: str, depth: int = 0) -> str | None:
        if ref.startswith("#"):
            return ref
        val = tokens.get(ref, "")
        m = re.match(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b", val)
        if m:
            return m.group(0)
        v = re.match(r"var\(\s*(--[\w-]+)", val)
        return resolve(v.group(1), depth + 1) if v and depth < 5 else None

    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if re.search(r"cặp tương phản", ln, re.I)), None)
    if start is None:
        return [], []
    block = [lines[start]]
    for ln in lines[start + 1:]:
        if ln.lstrip().startswith("#"):
            break
        block.append(ln)
    pairs, errs = [], []
    for ln in block:
        if not _PAIR.search(ln) and re.search(r"\btrên\b", ln) and re.search(r"#[0-9a-fA-F]{3}|--[\w-]+", ln):
            errs.append(f"dòng chưa đúng dạng `<chữ>` trên `<nền>` (máy không đọc được): {ln.strip()[:70]}")
        for m in _PAIR.finditer(ln):
            fg, bg = m.group(1), m.group(2)
            clause = re.split(r"[·;]", ln[m.end():], maxsplit=1)[0]
            need = 3.0 if re.search(r"\blớn\b|large", clause, re.I) else 4.5
            hf, hb = resolve(fg), resolve(bg)
            if not hf or not hb:
                errs.append(f"{fg} trên {bg}: không tra được mã hex")
                continue
            pairs.append((fg, bg, hf, hb, contrast_ratio(hf, hb), need))
    return pairs, errs


def _check_contrast(r: "Report") -> None:
    """DESIGN-SYSTEM cặp tương phản — gate TỰ TÍNH tỉ số WCAG AA. CẢNH BÁO, không chặn: nguồn chuẩn cuối là
    file thiết kế (Figma); đây chỉ để thấy sớm cặp màu khai sai số, không ép đổi màu ở DOCUMENT."""
    if not (ROOT / "docs" / "DESIGN-SYSTEM.md").exists():
        return                                    # backend-only (KHÔNG CÓ UI) — không có design system
    pairs, errs = contrast_pairs()
    bad = [f"{fg} trên {bg} = {ratio:.2f}:1 (WCAG AA cần ≥ {need:g}:1)" for fg, bg, _, _, ratio, need in pairs if ratio < need]
    if bad or errs:
        r.note("[cảnh báo tương phản] " + "; ".join(bad + errs))
    elif pairs:
        r.note(f"tương phản: {len(pairs)} cặp đạt WCAG AA (gate tự tính)")


# phần tử mockup gọi server hoặc hiển thị dữ liệu server → phải khai `data-api` (tĩnh = "none")
API_TAGS = re.compile(r"<(?:button|form|table|select)\b[^>]*>|<a\b[^>]*\bdownload\b[^>]*>"
                      r"|<input\b[^>]*type=[\"']file[\"'][^>]*>", re.I)


def _norm_api(s: str) -> str:
    """`GET /api/v1/leave/{id}?x=1` → `GET /leave/{}` (bỏ tiền tố /api[/vN], query, tên tham số)."""
    m = re.match(r"\s*(GET|POST|PUT|PATCH|DELETE)\s+(\S+)", s, re.I)
    if not m:
        return ""
    path = re.sub(r"^/api(/v\d+)?", "", m.group(2).split("?")[0].rstrip("/"))
    path = re.sub(r"\{[^}]*\}|:\w+|(?<=/)\d+(?=/|$)", "{}", path) or "/"
    return f"{m.group(1).upper()} {path}"


def arch_endpoints() -> set[str]:
    eps = set()
    for p in (ROOT / "docs" / "arch").glob("*.md"):
        for m in re.finditer(r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[^\s`|]*)", p.read_text(encoding="utf-8", errors="ignore")):
            eps.add(_norm_api(f"{m.group(1)} {m.group(2)}"))
    return eps


def mockup_api_gaps(wave: str) -> tuple[list[str], list[str]]:
    """Mockup của màn in-scope wave: (phần tử thiếu `data-api`, `data-api` không có trong arch §3).
    Bắt "màn có nút Tải xuống / bảng / dropdown nhưng arch §3 không có API nuôi nó"."""
    files = {p.name: p for p in (ROOT / "docs" / "ux" / "mockups").rglob("*.html")}
    names = {f for r in wave_screens(wave) for f in re.findall(r"([\w\-]+\.html)", r.get("mockup", ""))}
    eps, untagged, unknown = arch_endpoints(), [], []
    for n in sorted(names):
        if n not in files:
            continue   # thiếu file đã báo ở missing_wave_mockups
        for m in API_TAGS.finditer(files[n].read_text(encoding="utf-8", errors="ignore")):
            api = re.search(r"data-api=[\"']([^\"']*)[\"']", m.group(0))
            if not api:
                untagged.append(f"{n}: {m.group(0)[:60]}")
                continue
            for one in (a.strip() for a in api.group(1).split(";")):
                if one and one.lower() != "none" and _norm_api(one) not in eps:
                    unknown.append(f"{n}: {one}")
    return untagged, unknown


def _check_mockup_api(r: Report, wave: str) -> None:
    untagged, unknown = mockup_api_gaps(wave)
    r.check(not untagged, f"mockup wave {wave}: mọi nút/form/bảng/dropdown/tải file khai `data-api`"
            + (f" — THIẾU {len(untagged)}: {' | '.join(untagged[:3])}" if untagged else ""))
    r.check(not unknown, f"mockup wave {wave}: mọi `data-api` có endpoint trong arch §3"
            + (f" — KHÔNG CÓ {len(unknown)}: {' | '.join(unknown[:5])} (→ bổ sung arch §3)" if unknown else ""))


def fidelity_gaps(wave: str) -> tuple[list[str], list[str]]:
    """tracking/wave-N/fidelity.md (MAIN ghi từ báo cáo picky, 1 dòng/Mã màn): (mã in-scope THIẾU dòng, mã còn LỆCH)."""
    rows = table_rows(read(f"tracking/wave-{wave}/fidelity.md"))
    seen = {c[0].strip(): " ".join(c).upper() for c in rows if c}
    codes = [r["_code"] for r in wave_screens(wave)]
    absent = [c for c in codes if c not in seen]
    off = [c for c, txt in seen.items() if "LỆCH" in txt]
    return absent, off


def pending_topup(wave: str) -> list[str]:
    """ROADMAP §backlog: item xếp vào wave này mà CẦN top-up doc (tag `thiếu AC` hoặc Xử đòi `top-up`)
    nhưng cột Xử chưa ghi `đã top-up` = sắp code thứ không có spec/mockup đỡ."""
    out = []
    m = re.search(r"^#{1,4}[^\n]*Backlog[^\n]*$(.*?)(?=^#{1,4}\s|\Z)",
                  read_live("docs/ROADMAP.md"), flags=re.MULTILINE | re.DOTALL)
    for cells in table_rows(m.group(1) if m else ""):
        if len(cells) < 4:
            continue
        what, xu = cells[1], cells[-1]
        needs = "thiếu ac" in (what + xu).lower() or "top-up" in xu.lower()
        if needs and re.search(rf"\bwave\s*{re.escape(str(wave))}\b", xu, re.I) and "đã top-up" not in xu.lower():
            out.append(what[:60])
    return out


def tc_rows(text: str) -> list[dict]:
    """test-cases.md → [{tc, ac, tag, res}] đọc theo TÊN cột (khung TEMPLATE.test-cases.md; cột cũ `kết quả` vẫn đọc được)."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
    if not lines:
        return []
    head = [c.strip().lower() for c in lines[0].strip("|").split("|")]
    col = lambda name: next((i for i, h in enumerate(head) if h.startswith(name)), None)
    i_tc, i_ac, i_tag, i_res = col("tc"), col("ac"), col("tag"), col("kết quả")
    out = []
    for row in table_rows("\n".join(lines)):
        get = lambda i: row[i].strip() if i is not None and i < len(row) else ""
        out.append({"tc": get(i_tc), "ac": get(i_ac), "tag": get(i_tag).lower(),
                    "res": get(i_res).upper().replace("`", "")})
    return out


def in_scope_acs(wave: str) -> list[tuple[str, str]]:
    """AC in-scope wave (ROADMAP §1 cột AC in-scope) → [(FEAT-id, số AC)]."""
    row = roadmap_wave_row(wave)
    idx = _col_index("AC in-scope")
    return parse_ac_cell(row[idx] if row and idx is not None and idx < len(row) else "")


def parse_ac_cell(cell: str, expand: bool = True) -> list[tuple[str, str]]:
    """Ô dạng `FEAT-x AC-1..3, FEAT-y AC-2,4` → [(FEAT-id, số AC)] — AC gắn đúng FEAT đứng trước nó.
    FEAT không ghi AC: expand → mọi `### AC-n` trong docs/feat/<FEAT-id>.md · không expand (ô AC của TC) → không AC nào."""
    out = []
    for part in re.split(r"(?=FEAT-)", cell):
        m = re.match(r"(FEAT-[\w-]+?)(?=[\s:,;(]|AC-|$)(.*)", part.strip(), flags=re.S)
        if not m:
            continue
        feat, rest = m.group(1), re.sub(r"(\.\.|–|-)\s*AC-", r"\1", m.group(2))   # AC-1..AC-3 → AC-1..3
        nums: list[str] = []
        for spec in re.findall(r"AC-([\d\s,.\-–]+)", rest):
            for piece in re.split(r"\s*,\s*", spec.strip(" ,")):
                rng = re.match(r"(\d+)\s*(?:\.\.|-|–)\s*(\d+)$", piece)
                if rng:
                    nums += [str(n) for n in range(int(rng.group(1)), int(rng.group(2)) + 1)]
                elif piece.isdigit():
                    nums.append(piece)
        if not nums and expand:
            nums = re.findall(r"^#{2,4}\s*AC-(\d+)", read_live(f"docs/feat/{feat}.md"), flags=re.M)
        out += [(feat, n) for n in dict.fromkeys(nums)]
    return out


def regression_ids(wave: int) -> list[str]:
    """Mã TC gắn @regression trong test-cases.md của mọi wave đã đóng (archive/wave-k, k < wave)."""
    ids = []
    for k in range(1, wave):
        for p in sorted((ROOT / "archive" / f"wave-{k}").glob("tracking/wave-*/test-cases.md")):
            ids += [x["tc"] for x in tc_rows(p.read_text(encoding="utf-8", errors="ignore"))
                    if "@regression" in x["tag"] and x["tc"]]
    return list(dict.fromkeys(ids))


def _wave_ac_cell(wave: str, roadmap: str) -> str:
    """Ô AC in-scope của `wave` trong một bản ROADMAP (text) — để đọc bản ở commit cũ."""
    m = re.search(r"^#{1,4}\s*§1.*?$(.*?)(?=^#{1,4}\s|\Z)", read_live(roadmap, is_text=True), flags=re.M | re.S)
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")]
            for ln in (m.group(1) if m else "").splitlines() if ln.strip().startswith("|")]
    idx = next((i for i, h in enumerate(rows[0]) if "AC in-scope" in h), None) if rows else None
    row = next((c for c in rows[1:] if c and c[0] == str(wave)), [])
    return row[idx] if row and idx is not None and idx < len(row) else ""


def _check_ac_baseline(r: "Report", wave: str) -> None:
    """AC bị RÚT khỏi wave so với bản chốt (commit đóng wave trước · wave 1: commit tick Scope khoá) mà ROADMAP §2
    không có dòng điều chỉnh của wave này = hoãn ngầm để gate VERIFY đếm ít AC hơn."""
    if not wave.isdigit():
        return
    n = int(wave)
    base = (_git("log", "-1", "--format=%H", "--", f"archive/wave-{n - 1}") if n >= 2
            else _git("log", "-1", "--format=%H", "-S", "[x] **Scope khoá", "--", "STATE.md"))
    if not base:
        return
    now = set(in_scope_acs(wave))
    gone = [f"{f} AC-{a}" for f, a in parse_ac_cell(_wave_ac_cell(wave, _git("show", f"{base}:docs/ROADMAP.md")))
            if (f, a) not in now]
    logged = any(len(c) >= 2 and re.sub(r"\D", "", c[1]) == wave for c in table_rows(section("docs/ROADMAP.md", "§2")))
    r.check(not gone or logged, f"AC in-scope wave {wave} không bị rút so với bản chốt"
            + (f" — RÚT: {', '.join(gone[:6])} mà ROADMAP §2 không có dòng wave {wave}" if gone and not logged else ""))


def policy_rows(flows: str) -> list[list[str]]:
    """Bảng 'Chính sách từng hành động' (domain-ba A.6) — mọi bảng ngay sau dòng nhãn đó trong §Luồng nghiệp vụ."""
    rows, take, buf = [], False, []
    for ln in flows.splitlines() + [""]:
        s = ln.strip()
        if s.startswith("Chính sách từng hành động"):
            take, buf = True, []
            continue
        if take and s.startswith("|"):
            buf.append(s)
        elif take and buf:            # hết bảng
            rows += table_rows("\n".join(buf))
            take, buf = False, []
    return rows


def wave_declares_ship(wave: str) -> bool:
    """Chỉ đọc cột `phases` (không bắt nhầm chữ SHIP trong tên FEAT/target)."""
    row, idx = roadmap_wave_row(wave), _col_index("phases")
    return bool(row) and idx is not None and idx < len(row) and "SHIP" in row[idx].upper()


# ------------------------------------------------------------------ report ---

class Report:
    def __init__(self) -> None:
        self.ok = True

    def check(self, cond: bool, msg: str) -> None:
        mark = "✓" if cond else "✗"
        print(f"  {mark} {msg}")
        if not cond:
            self.ok = False

    def note(self, msg: str) -> None:
        print(f"  • {msg}")


# ------------------------------------------------------------------ gates ----

def read_proof(wave: str) -> dict | None:
    p = ROOT / "tracking" / f"wave-{wave}" / "proof.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def gate_document(r: Report) -> None:
    for f in ("docs/PRD.md", "docs/PERSONAS.md", "docs/CAPABILITIES-MAP.md", "docs/TECHSTACK.md"):
        r.check(filled(f), f"{f} tồn tại + điền hết (không còn {{{{)")
    r.check(count_rows_glob("docs/feat", r"FEAT-.*\.md") >= 1, "≥1 docs/feat/FEAT-*.md")
    r.check(filled("docs/arch/OVERVIEW.md"), "docs/arch/OVERVIEW.md điền")
    arch_targets = [p for p in (ROOT / "docs/arch").glob("*.md")
                    if p.name != "OVERVIEW.md" and not p.name.startswith("TEMPLATE")]
    r.check(len(arch_targets) >= 1, "≥1 docs/arch/{name}.md (per-target)")
    # system-design (SA) — OVERVIEW §5 đủ 5.1–5.9; 5.7 phân loại dữ liệu + 5.8 triển khai luôn có dòng (kể cả dự án nhỏ)
    ov = read_live("docs/arch/OVERVIEW.md")
    miss_sd = [f"5.{i}" for i in range(1, 10) if not re.search(rf"^#{{2,4}}\s*5\.{i}\b", ov, flags=re.M)]
    r.check(not miss_sd, "OVERVIEW §5 System design đủ 5.1–5.9"
            + (f" — THIẾU: {', '.join(miss_sd)}" if miss_sd else ""))
    for key, label in (("5.7", "phân loại dữ liệu"), ("5.8", "triển khai — số instance · đứng sau proxy")):
        r.check(bool(table_rows(section("docs/arch/OVERVIEW.md", key))), f"OVERVIEW §{key} {label}: có ≥1 dòng")
    # ma trận vai×hành động — không ô trống
    matrix = table_rows(section("docs/PERSONAS.md", "§2"))
    empty = [c for row in matrix for c in row[1:] if not c]
    r.check(bool(matrix) and not empty, "PERSONAS §2 ma trận không ô trống")
    # mọi dòng CAPABILITIES có CAP-
    caps = table_rows(section("docs/CAPABILITIES-MAP.md", "§1"))
    r.check(bool(caps) and all("CAP-" in row[0] for row in caps), "CAPABILITIES: mọi dòng có CAP-")
    # ROADMAP có wave + phases
    waves = roadmap_all_waves()
    r.check(bool(waves), "ROADMAP §1 có ≥1 wave")
    r.check(bool(waves) and all(any("BUILD" in c.upper() for c in row) for row in waves),
            "mỗi wave khai phases (≥ BUILD)")
    # domain-ba A — bảng luồng nghiệp vụ: có, Authority ký, không còn ô CHƯA HỎI (chống suy diễn actor)
    flows = section("docs/INTERVIEW.md", "Luồng nghiệp vụ đã xác nhận")
    n_flow = len(re.findall(r"^\*\*Luồng:", flows, flags=re.M))
    unsigned = len(re.findall(r"chốt bởi Authority:\s*(\{\{|\s*$|—)", flows, flags=re.M))
    unasked = len(re.findall(r"CHƯA HỎI", flows))
    r.check(n_flow >= 1 and unsigned == 0 and unasked == 0,
            f"INTERVIEW §Luồng nghiệp vụ: {n_flow} bảng, Authority ký, không ô CHƯA HỎI"
            + (f" — chưa ký: {unsigned}" if unsigned else "") + (f" — CHƯA HỎI: {unasked}" if unasked else ""))
    # domain-ba A.6 — bảng chính sách từng hành động: có dòng, không ô trống (chống "tài liệu im lặng" về luật)
    policy = policy_rows(flows)
    blank = sum(1 for row in policy for c in row if not c)
    r.check(bool(policy) and not blank,
            f"INTERVIEW bảng chính sách từng hành động: {len(policy)} dòng, không ô trống"
            + (f" — {blank} ô trống (không áp dụng → ghi `n/a — <lý do>`)" if blank else "")
            + ("" if policy else " — CHƯA có bảng (domain-ba A.6)"))
    # mockup wave đầu (wave 1 dựng lúc DOCUMENT) — màn UI in-scope đều có file, không khai suông
    first_wave = waves[0][0].strip() if waves and waves[0] else "1"
    miss = missing_wave_mockups(first_wave)
    r.check(not miss, f"mockup màn UI in-scope wave {first_wave} đều có file"
            + (f" — THIẾU: {', '.join(miss)} (khai trong SCREEN-MAP nhưng chưa dựng .html)" if miss else ""))
    _check_mockup_api(r, first_wave)
    _check_contrast(r)
    n_ch = challenge_count("DOCUMENT")
    r.check(n_ch >= 3, f"Challenge DOCUMENT: {n_ch} câu PASS (cần ≥3, trong đó ≥1 journey-walk) — §Challenge log")
    dec_rows = [ln for ln in read_live("docs/DECISIONS.md").splitlines()
                if ln.strip().startswith("| DEC-") and "{{" not in ln]
    r.check(len(dec_rows) >= 2, "≥2 dòng DECISIONS (đã điền, không placeholder)")
    sec = section("STATE.md", "DOCUMENT")
    for item in re.findall(r"- \[ \] (.+)", sec):
        if "Scope khoá" not in item:
            r.check(False, f"[STATE chưa tick] {item[:70]}")
    # Scope khoá là ô CUỐI: tick sau khi mọi mục trên xanh (document.md Bước cuối) → đỏ ở đây trước lúc đó là đúng
    r.check(scope_locked(), "Scope khoá (STATE tick) — ô cuối, tick sau khi mọi mục trên xanh")


def gate_build(r: Report) -> None:
    wave = state_wave()
    if wave.isdigit() and int(wave) >= 2:
        _check_reviewed(r, wave)
    else:
        r.note("wave 1 — miễn wave_reviewed (fresh từ DOCUMENT)")
    # bất biến chuyển wave: đang BUILD thì VERIFY/SHIP chưa thể xong; wave trước phải đóng bằng next_wave.py + commit
    leftover = [ph for ph in ("VERIFY", "SHIP") if re.search(r"- \[[xX]\]", section("STATE.md", ph))]
    r.check(not leftover, "không còn ô VERIFY/SHIP đã tick khi đang BUILD"
            + (f" — CÒN tick ở {', '.join(leftover)}: sót từ wave trước (đóng wave làm tay?) → chạy lại reset" if leftover else ""))
    if wave.isdigit() and int(wave) >= 2:
        prev = f"archive/wave-{int(wave) - 1}"
        tracked = subprocess.run(["git", "ls-files", prev], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        r.check(bool(tracked), f"{prev} tồn tại + đã commit (đóng wave bằng next_wave.py)")
    miss = missing_wave_mockups(wave)
    r.check(not miss, f"màn UI in-scope wave {wave} đều có mockup"
            + (f" — THIẾU: {', '.join(miss)} (→ /document top-up dựng mockup TRƯỚC khi code)" if miss else ""))
    _check_mockup_api(r, wave)
    todo = pending_topup(wave)
    r.check(not todo, f"backlog xếp wave {wave} cần top-up đều đã top-up"
            + (f" — CHƯA: {' | '.join(todo)} (→ /document top-up, xong ghi `đã top-up → …` ở cột Xử)" if todo else ""))
    _check_proof(r, wave)
    _state_checkboxes(r, "BUILD")


def _check_reviewed(r: Report, wave: str) -> None:
    row = roadmap_wave_row(wave)
    idx = _col_index("Rà lại")
    val = row[idx] if row and idx is not None and idx < len(row) else ""
    r.check(bool(val) and val not in ("—", "-"), f"ROADMAP wave {wave} có `Rà lại` (wave_reviewed)")


def _check_proof(r: Report, wave: str) -> None:
    """proof.json MÁY-sinh (capture_proof.py) — không tin tick tay: make check xanh · chụp trên code ĐÃ commit, đúng
    commit mới nhất của services/ (sửa code sau lần chụp = proof cũ) · mọi target container hoá wave khai healthy."""
    proof = read_proof(wave)
    if not proof:
        r.check(False, "thiếu tracking/wave-N/proof.json — chạy `python scripts/capture_proof.py`")
        return
    r.check(bool(proof.get("check", {}).get("ok")), "make check xanh (proof.json — máy sinh)")
    code = proof.get("code") or {}
    fresh = not code.get("dirty", True) and code.get("commit") == last_code_commit()
    r.check(fresh, "proof chụp trên code đã commit, đúng commit mới nhất của services/"
            + ("" if fresh else " — còn sửa dở hoặc code đổi sau lần chụp → commit rồi chạy lại capture_proof"))
    # target phủ đủ wave — đối chiếu ROADMAP §1 cột Target ↔ proof.targets (chống "khai 2 làm 1")
    declared = parse_wave_targets(wave)
    if not declared:
        r.check(False, f"ROADMAP §1 wave {wave}: cột Target không parse được target nào (không xác nhận được phủ đủ)")
    ptargets = {t.get("target"): t for t in proof.get("targets", [])}
    for name, kind in declared:
        if kind in CONTAINERIZED:
            t = ptargets.get(name)
            r.check(bool(t) and bool(t.get("healthy")), f"target `{name}` ({kind}) chạy thật — proof healthy")
        else:  # mobile — không proof qua docker, dựa tick STATE (emulator)
            r.note(f"target `{name}` ({kind}) — emulator, không proof docker; dựa ô tick STATE")


def gate_verify(r: Report) -> None:
    wave = state_wave()
    tc = f"tracking/wave-{wave}/test-cases.md"
    rows = tc_rows(read(tc))   # khung templates/TEMPLATE.test-cases.md — đọc theo TÊN cột
    r.check(exists(tc) and bool(rows), f"{tc}: có bảng TC (khung TEMPLATE.test-cases.md)")
    # không còn TC chưa xong: FAIL · BLOCKED · CHƯA CHẠY · trống (CHƯA CÓ QUY ĐỊNH không tính — không phải bug, đi backlog)
    bad = [f"{x['tc']}:{x['res'] or 'trống'}" for x in rows
           if not x["res"] or x["res"].startswith(("FAIL", "BLOCKED", "CHƯA CHẠY"))]
    r.check(not bad, "không còn TC FAIL / BLOCKED / CHƯA CHẠY (kết quả trống = CHƯA CHẠY)"
            + (f" — {len(bad)}: {', '.join(bad[:6])}" if bad else ""))
    # mọi AC in-scope có ≥1 TC PASS (tính TỪNG AC — 1 TC PASS cho cả wave không đủ)
    acs = in_scope_acs(wave)
    passed = {p for x in rows if x["res"].startswith("PASS") for p in parse_ac_cell(x["ac"], expand=False)}
    uncovered = [f"{f} AC-{n}" for f, n in acs if (f, n) not in passed]
    r.check(bool(acs) and not uncovered, f"mọi AC in-scope wave {wave} có TC PASS ({len(acs)} AC)"
            + (f" — CHƯA: {', '.join(uncovered[:8])}" if uncovered else "")
            + ("" if acs else " — không đọc được AC in-scope (ROADMAP §1 cột AC in-scope + docs/feat/)"))
    _check_ac_baseline(r, wave)
    # regression: mọi TC @regression của wave đã đóng phải được chạy lại + PASS ở wave này
    if wave.isdigit() and int(wave) >= 2:
        cur = {x["tc"]: x["res"] for x in rows}
        # ĐÃ THAY = TC hết hợp lệ vì AC đổi qua top-up, có TC thay thế (bug-hunter rà đề test kiểm TC thay có thật)
        miss = [t for t in regression_ids(int(wave)) if not cur.get(t, "").startswith(("PASS", "ĐÃ THAY"))]
        r.check(not miss, "TC @regression của wave trước đã chạy lại + PASS (hoặc ĐÃ THAY)"
                + (f" — CHƯA/ĐỎ: {', '.join(miss[:8])}" if miss else ""))
    gap = [x["tc"] for x in rows if x["res"].startswith("CHƯA CÓ QUY ĐỊNH")]
    if gap:
        r.note(f"CHƯA CÓ QUY ĐỊNH: {len(gap)} TC ({', '.join(gap[:6])}) — không chặn gate; báo Authority + ROADMAP §backlog")
    # §Findings: BLOCKER/MAJOR chỉ coi là đã xử khi agent xác nhận đã sửa, hoặc đã đẩy backlog
    open_major = [row for row in table_rows(section("STATE.md", "Findings"))
                  if len(row) >= 5 and re.search(r"BLOCKER|MAJOR", row[2].upper())
                  and not re.search(r"fixed.*xác nhận|backlog", row[4], re.I)]
    r.check(not open_major, "§Findings: hết BLOCKER/MAJOR chưa xử (Xử lý = `fixed — <agent> xác nhận` hoặc `backlog`)"
            + (f" — CÒN {len(open_major)}" if open_major else ""))
    if wave_screens(wave):   # có màn UI in-scope → picky phải phủ đủ + khớp (bằng chứng ở fidelity.md)
        absent, off = fidelity_gaps(wave)
        r.check(not absent, f"tracking/wave-{wave}/fidelity.md phủ đủ màn in-scope"
                + (f" — THIẾU dòng: {', '.join(absent)} (picky chưa soi)" if absent else ""))
        r.check(not off, "fidelity.md không còn màn LỆCH mockup"
                + (f" — LỆCH: {', '.join(off)}" if off else ""))
    _check_proof(r, wave)   # vòng sửa đổi code → proof phải chụp lại đúng commit mới nhất
    _state_checkboxes(r, "VERIFY")


def gate_ship(r: Report) -> None:
    wave = state_wave()
    if not wave_declares_ship(wave):
        r.note(f"wave {wave} không khai SHIP → bỏ qua, đi /next-wave")
        return
    # gate SHIP chạy SAU deploy (Bước cuối) → đòi đủ cả mục (sau deploy); trước deploy guard_bc mới miễn các mục đó
    unchecked = count_rows("docs/PRODUCTION-READY.md", r"^- \[ \]")
    r.check(exists("docs/PRODUCTION-READY.md") and unchecked == 0,
            "PRODUCTION-READY 4 nhóm xanh — kể cả mục (sau deploy)" + (f" — CÒN {unchecked} mục" if unchecked else ""))
    if wave.isdigit() and int(wave) >= 2:
        bc3 = len(re.findall(r"^- \[ \]", section("docs/BACKWARD-COMPAT.md", "§3"), flags=re.MULTILINE))
        r.check(bc3 == 0, "BACKWARD-COMPAT §3 xanh (guard_bc)")
    _state_checkboxes(r, "SHIP")   # deploy/smoke/rollback tick tay — gate soi như BUILD/VERIFY


def gate_next_wave(r: Report) -> None:
    """Chấm SAU `next_wave.py --go` (STATE đã sang wave N+1). Chốt TRƯỚC khi đóng (VERIFY/SHIP xanh) nằm trong script."""
    wave = state_wave()
    prev = str(int(wave) - 1) if wave.isdigit() else ""
    r.check(bool(prev) and bool(_git("ls-files", f"archive/wave-{prev}")),
            f"archive/wave-{prev or 'N'} đã snapshot + commit (`next_wave.py --go` → git commit)")
    backlog = table_rows(section("docs/ROADMAP.md", "§3"))
    undisposed = [row for row in backlog if len(row) >= 4 and not row[3].strip()]
    r.check(not undisposed, "ROADMAP §3 backlog: mọi item đã định đoạt (cột Xử không trống)")
    if roadmap_wave_row(wave):
        _check_reviewed(r, wave)
    else:
        r.note(f"ROADMAP không còn wave {wave} → hết wave: teardown `docker compose down --volumes`, báo dự án xong")


# --------------------------------------------------------------- helpers -----

def count_rows_glob(dir_rel: str, pattern: str) -> int:
    d = ROOT / dir_rel
    if not d.exists():
        return 0
    return sum(1 for p in d.glob("*.md")
               if re.match(pattern, p.name) and not p.name.startswith("TEMPLATE"))


def roadmap_all_waves() -> list[list[str]]:
    return [row for row in table_rows(section("docs/ROADMAP.md", "§1"))
            if row and row[0].strip().isdigit()]


def _col_index(name: str) -> int | None:
    for line in section("docs/ROADMAP.md", "§1").splitlines():
        if line.strip().startswith("|") and name in line:
            headers = [c.strip() for c in line.strip("|").split("|")]
            for i, h in enumerate(headers):
                if name in h:
                    return i
    return None


def _state_checkboxes(r: Report, phase: str) -> None:
    sec = section("STATE.md", f"{phase} (wave") or section("STATE.md", phase)
    unchecked = re.findall(r"- \[ \] (.+)", sec)
    for item in unchecked:
        r.check(False, f"[STATE chưa tick] {item[:70]}")
    # tick mang số wave KHÁC wave đang chạy = tick cũ không được reset (đóng wave làm tay) → không tin
    wave = state_wave()
    for item in re.findall(r"- \[[xX]\] (.+)", sec):
        old = [w for w in re.findall(r"wave-(\d+)/", item) if w != wave]   # chỉ đường dẫn bằng chứng (tracking/wave-N/…), không bắt lời ghi chú
        if wave.isdigit() and old:
            r.check(False, f"[STATE tick cũ wave {old[0]}] {item[:60]} — bỏ tick, đo lại cho wave {wave}")
    if not unchecked and sec:
        r.note(f"STATE gate {phase}: mọi mục đã tick")


def _state_shape(r: Report) -> None:
    """STATE.md phải giữ khung templates/TEMPLATE.state.md: heading · chữ ô gate · trường đầu."""
    tpl = read("templates/TEMPLATE.state.md")
    if not tpl:
        return
    live = read("STATE.md")
    lines, bad, sec = {ln.strip() for ln in live.splitlines()}, [], ""
    for ln in tpl.splitlines():
        s = ln.strip()
        if s.startswith("## ") or s.startswith("### "):
            sec = s
            if s not in lines:
                bad.append(f"heading thiếu/bị sửa: {s[:60]}")
        box = re.match(r"- \[ \] (.+)", s)
        # ô DOCUMENT tick 1 lần cho cả dự án (giữ chữ bản lúc chạy) → chỉ soi chữ ô wave-scoped (next_wave dựng lại mỗi wave)
        if box and "DOCUMENT" not in sec and not re.search(rf"^\s*- \[[ xX]\] {re.escape(box.group(1))}", live, flags=re.M):
            bad.append(f"ô gate thiếu/bị sửa chữ: {box.group(1)[:50]}")
        fld = re.match(r"^([^\s:`>#|\-][^:]*?)\s+:\s", ln)
        if fld and not re.search(rf"^{re.escape(fld.group(1))}\s+:", live, flags=re.M):
            bad.append(f"thiếu trường đầu: {fld.group(1)}")
    for b in bad:
        r.check(False, f"[STATE lệch khung template] {b}")
    if not bad:
        r.note("STATE giữ đúng khung templates/TEMPLATE.state.md")
    else:
        r.note("→ trả heading/chữ ô/trường về đúng template; bằng chứng ghi dòng con dưới ô hoặc vào log")


GATES = {
    "DOCUMENT": gate_document, "BUILD": gate_build, "VERIFY": gate_verify,
    "SHIP": gate_ship, "NEXT-WAVE": gate_next_wave,
}


def main(argv: list[str]) -> int:
    phase = (argv[1].upper() if len(argv) > 1 else phase_from_state()).replace(" ", "-")
    if phase not in GATES:
        print(f"Phase không rõ: {phase!r}. Chọn: {', '.join(GATES)}", file=sys.stderr)
        return 2
    print(f"[gate {phase}]  (nguồn: PROTOCOL.md §6)")
    r = Report()
    _state_shape(r)
    GATES[phase](r)
    print(f"\n{'PASS — rời phase được' if r.ok else 'CÒN THIẾU — chưa rời phase'}")
    return 0 if r.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
