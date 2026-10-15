#!/usr/bin/env python3
"""next_wave.py — đóng wave hiện tại (snapshot, KHÔNG reset docs) + mở wave kế.

- Snapshot `archive/wave-N/` (copy HẾT, không chọn lọc) → sự tồn tại = cờ "đã đóng" (từ chối đóng 2 lần).
- Dựng lại phần **WAVE-SCOPED** của `STATE.md` từ `templates/TEMPLATE.state.md` (gate BUILD/VERIFY/SHIP/NEXT-WAVE ·
  3 log) — xoá luôn đuôi heading/chữ ô bị sửa tay · set `Wave: N+1` + `Phases wave này` từ ROADMAP §1.
- **KHÔNG reset `docs/`** (trí nhớ qua wave). RÀ LẠI kế hoạch + stamp ngày vào ô `Rà lại` của wave N+1 do MAIN làm ở `/next-wave`.

Usage: python scripts/next_wave.py [--go] [--accept-red=DEC-x]
  (không --go = xem trước, không sửa gì · gate VERIFY/SHIP đỏ → từ chối, trừ --accept-red do Authority quyết)
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "STATE.md"
TEMPLATE = ROOT / "templates" / "TEMPLATE.state.md"
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def state_field(text: str, name: str) -> str:
    m = re.search(rf"{re.escape(name)}\s*:\s*(.+)", text)
    return m.group(1).strip() if m else ""


def _block(t: str, head: str) -> re.Match | None:
    """Khối từ dòng `head…` tới heading cùng cấp/`---` kế tiếp (đuôi heading sửa tay vẫn bắt được)."""
    lvl = head.split(" ")[0]
    return re.search(rf"^{re.escape(head)}[^\n]*\n.*?(?=^{lvl} |^## |^---|\Z)", t, flags=re.M | re.S)


def roadmap_phases(wave: int) -> str:
    rm = ROOT / "docs" / "ROADMAP.md"
    if not rm.exists():
        return ""
    for ln in rm.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if ln.strip().startswith("|") and cells[0] == str(wave):
            return next((c for c in cells[1:] if re.fullmatch(r"[A-Z, \-\[\]]*BUILD[A-Z, \-\[\]]*", c)), "")
    return ""


def gate_ok(phase: str) -> bool:
    """Chạy `gate.py <phase>` — exit 0 = xanh."""
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "gate.py"), phase], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode == 0


def reset_state(text: str, next_wave: int) -> str:
    if not TEMPLATE.exists():
        return _reset_state_legacy(text, next_wave)
    tpl = TEMPLATE.read_text(encoding="utf-8")
    for head in ("### BUILD", "### VERIFY", "### SHIP", "### NEXT-WAVE", "## Challenge log", "## Blocker", "## Findings"):
        m, mt = _block(text, head), _block(tpl, head)
        if m and mt:
            text = text[:m.start()] + mt.group(0) + text[m.end():]
    text = re.sub(r"(Wave\s*:\s*).+", rf"\g<1>{next_wave}", text, count=1)
    phases = roadmap_phases(next_wave) or "—            (khai khi mở wave: BUILD,VERIFY[,SHIP])"
    return re.sub(r"(Phases wave này\s*:\s*).+", lambda m: m.group(1) + phases, text, count=1)


def _reset_state_legacy(text: str, next_wave: int) -> str:
    """Dự án chưa có templates/TEMPLATE.state.md — bỏ tick + xoá dòng log như cũ."""
    def uncheck_section(t: str, header: str) -> str:
        m = re.search(rf"(### {header}.*?)(?=\n### |\n---|\Z)", t, flags=re.DOTALL)
        if not m:
            return t
        block = m.group(1).replace("- [x]", "- [ ]").replace("- [X]", "- [ ]")
        return t[:m.start()] + block + t[m.end():]

    for h in ("BUILD", "VERIFY", "SHIP", "NEXT-WAVE"):
        text = uncheck_section(text, h)
    for header in ("Challenge log", "Blocker", "Findings"):
        m = re.search(rf"(## [^\n]*{header}[^\n]*\n)(.*?)(?=\n## |\Z)", text, flags=re.DOTALL)
        if not m:
            continue
        lines, kept, seen_sep = m.group(2).splitlines(), [], False
        for ln in lines:
            s = ln.strip()
            is_row = s.startswith("|")
            is_sep = is_row and set(s) <= set("|-: ")
            if is_sep:
                seen_sep = True
                kept.append(ln)
            elif is_row and seen_sep:
                continue
            else:
                kept.append(ln)
        text = text[:m.start(2)] + "\n".join(kept) + text[m.end(2):]
    text = re.sub(r"(Wave\s*:\s*).+", rf"\g<1>{next_wave}", text, count=1)
    text = re.sub(r"(Phases wave này\s*:\s*).+", r"\g<1>—            (khai khi mở wave: BUILD,VERIFY[,SHIP])", text, count=1)
    return text


def main(argv: list[str]) -> int:
    go = "--go" in argv
    text = STATE.read_text(encoding="utf-8")
    wave = state_field(text, "Wave")
    if not wave.isdigit():
        print(f"Wave hiện tại không phải số ({wave!r}) — chưa mở wave nào? Không đóng được.")
        return 1
    n = int(wave)
    arch = ROOT / "archive" / f"wave-{n}"
    if arch.exists():
        print(f"✗ archive/wave-{n}/ ĐÃ tồn tại = cờ 'wave {n} đã đóng'. Từ chối đóng lại (tránh mất vết).")
        return 1

    # wave chỉ đóng khi gate VERIFY (+ SHIP nếu khai) xanh — trừ Authority quyết đóng dù KHÔNG ĐẠT (dòng DECISIONS)
    red = [ph for ph in ["VERIFY"] + (["SHIP"] if "SHIP" in roadmap_phases(n) else []) if not gate_ok(ph)]
    accept = next((a.split("=", 1)[1] for a in argv if a.startswith("--accept-red=")), "")
    if red:
        dec = ROOT / "docs" / "DECISIONS.md"
        if not accept or accept not in (dec.read_text(encoding="utf-8") if dec.exists() else ""):
            print(f"✗ gate {' + '.join(red)} wave {n} còn ĐỎ — từ chối đóng wave.\n"
                  f"  Authority quyết đóng dù KHÔNG ĐẠT → 1 dòng docs/DECISIONS.md (DEC-x) + chuyển mọi TC FAIL/BLOCKED"
                  f" + finding BLOCKER/MAJOR còn mở vào ROADMAP §3 (Xử = wave {n+1}) → chạy lại với --accept-red=DEC-x")
            return 1
        print(f"! gate {' + '.join(red)} còn đỏ — đóng theo {accept} (Authority quyết; phần đỏ đã sang backlog wave {n+1})")

    srcs = ["STATE.md", f"tracking/wave-{n}", "docs"]   # chép HẾT docs/ — bản đã giao (mockup · bảng chính sách…) nằm nguyên
    srcs = [s for s in srcs if (ROOT / s).exists()]
    print(f"[next-wave] đóng wave {n} → mở wave {n+1}   ({'THỰC THI' if go else 'xem trước — thêm --go để chạy'})")
    print(f"  Snapshot → archive/wave-{n}/ :")
    for s in srcs:
        print(f"    · {s}")
    print(f"  Reset STATE: dựng lại gate BUILD/VERIFY/SHIP/NEXT-WAVE + 3 log từ template · Wave → {n+1}")
    print("  KHÔNG đụng: docs/ sống · archive cũ · knowledge-base · DECISIONS")
    if not go:
        return 0

    arch.mkdir(parents=True)
    for s in srcs:
        src, dst = ROOT / s, arch / s
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst) if src.is_dir() else shutil.copy2(src, dst)
    STATE.write_text(reset_state(text, n + 1), encoding="utf-8")
    print(f"\n✓ Đã snapshot + mở wave {n+1}. Bước kế (MAIN): RÀ LẠI kế hoạch wave {n+1} + stamp ngày vào ô `Rà lại` của wave {n+1} (ROADMAP §1) + `git commit` archive → /build hoặc /document top-up.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
