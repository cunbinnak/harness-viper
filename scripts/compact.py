#!/usr/bin/env python3
"""compact.py — báo cáo doc phình (sổ append-only dài dần qua nhiều wave). CHỈ ĐỌC, không sửa.

Vì sao có: docs KHÔNG reset qua wave (trí nhớ) → DECISIONS.md, ROADMAP §backlog cứ dài ra;
sau 5–7 wave phần đọc được lẫn phần hết hiệu lực → không ai đọc nữa. Gợi ý gấp dòng cũ sang
`archive/ledger/`. KHÔNG `--go`: tự sửa sổ append-only đoán sai một lần là mất vĩnh viễn.

Usage: python scripts/compact.py   (luôn exit 0 — báo cáo, không chặn)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def rows(rel: str, section: str | None = None) -> int:
    text = (ROOT / rel).read_text(encoding="utf-8") if (ROOT / rel).exists() else ""
    if section:
        m = re.search(rf"## [^\n]*{section}.*?(?=\n## |\Z)", text, flags=re.DOTALL)
        text = m.group(0) if m else ""
    return sum(1 for ln in text.splitlines()
               if ln.strip().startswith("|") and set(ln.strip()) - set("|-: "))


def main() -> int:
    print("[compact] báo cáo doc phình (CHỈ ĐỌC — gấp bằng tay sang archive/ledger/, không có --go)\n")
    dec = rows("docs/DECISIONS.md") - 1  # trừ header
    backlog = rows("docs/ROADMAP.md", "Backlog") - 1
    waves_closed = len(list((ROOT / "archive").glob("wave-*"))) if (ROOT / "archive").exists() else 0

    print(f"  DECISIONS.md      : ~{max(dec,0)} dòng quyết định")
    print(f"  ROADMAP §Backlog  : ~{max(backlog,0)} dòng")
    print(f"  Wave đã đóng      : {waves_closed}")
    print()
    if waves_closed >= 3 and dec > 25:
        print("  ⚠ Nên gấp: DECISIONS của các wave ĐÃ ĐÓNG (có trong archive/) → cắt sang")
        print("    archive/ledger/DECISIONS.md, để lại 1 dòng trỏ. Giữ dòng quyết định còn hiệu lực.")
    else:
        print("  ✓ Chưa cần gấp (ít wave / sổ còn ngắn).")
    print("\n  Ba luật gấp tay: (1) không xoá dòng gate đang đọc · (2) không bọc <!-- --> (biến khỏi phép đếm)")
    print("  (3) không đổi tiêu đề ## (mỏ neo). Gấp = CẮT khỏi file sống, DÁN sang ledger, để lại dòng trỏ.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
