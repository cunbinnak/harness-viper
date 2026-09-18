#!/usr/bin/env python3
"""next_wave.py — đóng wave hiện tại (snapshot, KHÔNG reset docs) + mở wave kế.

- Snapshot `archive/wave-N/` (copy HẾT, không chọn lọc) → sự tồn tại = cờ "đã đóng" (từ chối đóng 2 lần).
- Reset phần **WAVE-SCOPED** của `STATE.md`: bỏ tick gate BUILD/VERIFY/SHIP · xoá dòng log · set `Wave: N+1`.
- **KHÔNG reset `docs/`** (trí nhớ qua wave). RÀ LẠI kế hoạch + stamp `Rà lại wave N+1` do MAIN làm ở `/next-wave`.

Usage: python scripts/next_wave.py [--go]   (không --go = xem trước, không sửa gì)
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "STATE.md"
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def state_field(text: str, name: str) -> str:
    m = re.search(rf"{re.escape(name)}\s*:\s*(.+)", text)
    return m.group(1).strip() if m else ""


def reset_state(text: str, next_wave: int) -> str:
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

    srcs = ["STATE.md", f"tracking/wave-{n}", "docs/feat", "docs/arch", "docs/ROADMAP.md", "docs/CAPABILITIES-MAP.md"]
    srcs = [s for s in srcs if (ROOT / s).exists()]
    print(f"[next-wave] đóng wave {n} → mở wave {n+1}   ({'THỰC THI' if go else 'xem trước — thêm --go để chạy'})")
    print(f"  Snapshot → archive/wave-{n}/ :")
    for s in srcs:
        print(f"    · {s}")
    print(f"  Reset STATE: bỏ tick BUILD/VERIFY/SHIP · xoá 3 log · Wave → {n+1}")
    print("  KHÔNG đụng: docs/ sống · archive cũ · knowledge-base · DECISIONS")
    if not go:
        return 0

    arch.mkdir(parents=True)
    for s in srcs:
        src, dst = ROOT / s, arch / s
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst) if src.is_dir() else shutil.copy2(src, dst)
    STATE.write_text(reset_state(text, n + 1), encoding="utf-8")
    print(f"\n✓ Đã snapshot + mở wave {n+1}. Bước kế (MAIN): RÀ LẠI kế hoạch wave {n+1} + stamp `Rà lại wave {n+1}` vào ROADMAP → /build hoặc /document top-up.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
