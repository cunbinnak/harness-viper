#!/usr/bin/env python3
"""reanchor — sau compact, nhồi lại PROTOCOL §2 (luật nền) + TRẠNG THÁI SỐNG vào context.

Van an toàn cho MAIN-code-hết: phiên dài bị compact → bản tóm tắt giữ "đang làm gì" nhưng đánh rơi
"đang bị cấm gì" + "đang tắc gì". Hook đọc THẲNG TỪ FILE (không chép cứng luật — sửa luật quên hook thì
nhồi luật cũ còn hại hơn) → nhồi lại: luật §2 + phase/wave + Blocker mở + Finding chưa xử + AC wave đang bám.

CHẠY: Claude Code gọi qua hook SessionStart matcher "compact" (.claude/settings.json).
  stdout: JSON hookSpecificOutput.additionalContext (CHỈ xử khi exit 0). Mỗi lần bắn ghi 1 dòng .reanchor.log.
ĐO HIỆU QUẢ: python scripts/hooks/reanchor.py --audit
  Đọc log + transcript, đếm số lần compact + soi SAU mỗi lần có gọi AskUserQuestion sai phase không.
exit 0 luôn ở chế độ hook — hook lỗi KHÔNG được chặn phiên.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / ".reanchor.log"

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Vi phạm soi được bằng máy trong transcript (phần còn lại của luật đọc tay).
VIOLATION_TOOLS = {"AskUserQuestion": "luật #2 — AskUserQuestion ngoài DOCUMENT"}
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
SEP = re.compile(r"^\|[\s|:-]+\|$")


# ---------------------------------------------------------------- readers ----

def read(rel: str) -> str:
    try:
        return (ROOT / rel).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def field(name: str) -> str:
    m = re.search(rf"{re.escape(name)}\s*:\s*(.+)", read("STATE.md"))
    return m.group(1).strip() if m else "?"


def phase() -> str:
    return field("Phase hiện tại").upper().replace(" ", "-")


def section(text: str, header: str, stop: str = "\n## ") -> str:
    """Một mục của file, đã bỏ khối <!-- --> (hướng dẫn cho người điền, không phải nội dung)."""
    i = text.find(header)
    if i < 0:
        return ""
    j = text.find(stop, i + len(header))
    return COMMENT.sub("", text[i: j if j > 0 else len(text)]).strip()


def table_rows(block: str) -> list[str]:
    """Dòng dữ liệu thật của bảng markdown (bỏ separator + đúng 1 dòng tiêu đề)."""
    lines = [l for l in block.splitlines() if l.strip().startswith("|")]
    lines = [l for l in lines if not SEP.match(l.strip())]
    return [r for r in lines[1:] if r.strip("| ").strip()]


# --------------------------------------------------------- hook: nhồi lại ----

def targets_owed(wave: str, target_cell: str) -> list[str]:
    """Target container hoá (backend/bff/web) khai ở ROADMAP nhưng CHƯA healthy trong proof.json."""
    healthy = set()
    p = ROOT / "tracking" / f"wave-{wave}" / "proof.json"
    try:
        proof = json.loads(p.read_text(encoding="utf-8"))
        healthy = {t.get("target") for t in proof.get("targets", []) if t.get("healthy")}
    except (OSError, ValueError):
        pass
    owed = []
    for name, kind in re.findall(r"([\w.\-]+)\s*\(\s*(\w+)\s*\)", target_cell):
        if kind.lower() in ("backend", "bff", "web") and name not in healthy:
            owed.append(f"{name} ({kind})")
    return owed


def laws() -> str:
    body = section(read("PROTOCOL.md"), "## §2 — Luật nền", stop="\n---")
    return body or "_Không đọc được `PROTOCOL.md §2` — mở file đọc luật nền trước khi làm tiếp._"


def live_state() -> str:
    """Trạng thái sống lấy từ file: phase/wave + Blocker mở + Finding chưa xử + AC wave đang bám."""
    st = read("STATE.md")
    out = [f"Phase: **{field('Phase hiện tại')}** · Wave: **{field('Wave')}** · Đường vào: {field('Đường vào')}"]

    blockers = table_rows(section(st, "## Blocker"))
    if blockers:
        out.append(f"**Blocker đang mở ({len(blockers)}) — đã thử hết mới dồn vào đây:**\n" + "\n".join(blockers))

    findings = table_rows(section(st, "## Findings"))
    if findings:
        out.append(f"**Finding chưa xử ({len(findings)}) — BLOCKER/MAJOR phải xử trước khi rời VERIFY:**\n" + "\n".join(findings))

    w = field("Wave")
    if w.isdigit():
        for r in table_rows(section(read("docs/ROADMAP.md"), "## §1")):
            cells = [c.strip() for c in r.strip("|").split("|")]
            if cells and cells[0] == w:
                out.append(f"**Wave {w} đang bám (ROADMAP §1):** {r.strip()}")
                if phase() == "BUILD" and len(cells) > 1:
                    owed = targets_owed(w, cells[1])   # cột Target = col 1 (sau Wave)
                    if owed:
                        out.append("**Target CÒN NỢ (chưa có proof chạy thật) — BUILD chưa xong, "
                                   "làm nốt rồi mới /verify:** " + ", ".join(owed))
                break
    return "\n\n".join(out)


def build_context(source: str) -> str:
    return "\n".join([
        f"[reanchor sau `{source}`] Context vừa nén — bản tóm tắt hay đánh rơi *đang bị cấm gì* + *đang tắc gì*.",
        "Luật + trạng thái dưới đây đọc THẲNG TỪ FILE (không phải từ tóm tắt):",
        "",
        "## Luật nền (PROTOCOL §2)",
        laws(),
        "",
        "## Trạng thái sống",
        live_state() or "_(chưa đọc được STATE.md)_",
        "",
        f"→ Chạy `python scripts/gate.py` xem gate phase {phase()} còn thiếu gì. Làm nốt việc dở, đừng mở việc mới.",
    ])


def log_fire(payload: dict) -> None:
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "source": payload.get("source", "?"),
                "session_id": payload.get("session_id", "?"),
                "transcript": payload.get("transcript_path", ""),
                "phase": phase(),
            }, ensure_ascii=False) + "\n")
    except OSError:
        pass  # log hỏng thì kệ, không được để hook chặn phiên


def run_hook() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}
    log_fire(payload)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": build_context(payload.get("source", "compact")),
    }}, ensure_ascii=False))
    return 0


# --------------------------------------------------------- --audit: đo -------

def iter_records(path: Path):
    try:
        with path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    yield json.loads(line)
                except (json.JSONDecodeError, ValueError):
                    continue
    except OSError:
        return


def parse_ts(s: str):
    try:
        d = datetime.fromisoformat((s or "").replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def tools_after(transcript: Path, after_iso: str) -> list[tuple[str, str]]:
    mark = parse_ts(after_iso)
    if mark is None:
        return []
    found = []
    for rec in iter_records(transcript):
        if rec.get("type") != "assistant":
            continue
        t = parse_ts(rec.get("timestamp", ""))
        if t is None or t <= mark:
            continue
        for block in (rec.get("message") or {}).get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                found.append((rec.get("timestamp", ""), block.get("name", "?")))
    return found


def audit() -> int:
    if not LOG.exists():
        print("Chưa có .reanchor.log — hook chưa chạy lần nào (phiên chưa từng compact, hoặc hook chưa nối).")
        print("Kiểm nối hook: grep -A6 SessionStart .claude/settings.json")
        return 0
    fires = [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"\n=== Đã compact {len(fires)} lần ===\n")
    total = 0
    for i, fire in enumerate(fires, 1):
        print(f"[{i}] {fire['at']}  ·  phase {fire['phase']}  ·  {fire['source']}")
        tp = Path(fire.get("transcript") or "")
        if not tp.is_file():
            print("    (không đọc được transcript — bỏ qua)\n")
            continue
        after = tools_after(tp, fire["at"])
        print(f"    {len(after)} lượt gọi tool sau mốc này")
        # Luật #2 chỉ có hiệu lực NGOÀI DOCUMENT — ở DOCUMENT hỏi Authority là đúng, không soi.
        if fire["phase"] == "DOCUMENT":
            print("    · phase DOCUMENT — AskUserQuestion là đúng luật, không soi\n")
            continue
        viol = [(ts, n) for ts, n in after if n in VIOLATION_TOOLS]
        total += len(viol)
        for ts, n in viol:
            print(f"    ✗ {ts}  {n} — {VIOLATION_TOOLS[n]}")
        if not viol:
            print("    ✓ không có dấu hiệu phá luật đo được bằng máy")
        print()
    print("=" * 56)
    print(f"Tổng vi phạm đo được bằng máy: {total}")
    print("Lưu ý: máy chỉ soi AskUserQuestion. 3 thứ nặng hơn phải đọc tay: "
          "quyết định thiếu dòng DECISIONS · báo 'xong' khi chưa dogfood · lặng lẽ nới scope đã khoá.")
    return 0


if __name__ == "__main__":
    if "--audit" in sys.argv:
        raise SystemExit(audit())
    try:
        raise SystemExit(run_hook())
    except SystemExit:
        raise
    except Exception as e:                       # hook KHÔNG BAO GIỜ được làm hỏng phiên
        print(f"reanchor.py: {e}", file=sys.stderr)
        raise SystemExit(0)
