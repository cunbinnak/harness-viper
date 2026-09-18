#!/usr/bin/env python3
"""bootstrap.py — khởi tạo project mới từ fork: thay placeholder DANH TÍNH + leftover-check.

Thay `{{PROJECT_NAME}} {{PROJECT_CODE}} {{DATE}} {{AUTHORITY_NAME}} {{AUTHORITY_EMAIL}}` khắp file text.
GIỮ NGUYÊN marker định dạng (`{{name}} {{boundary}} {{slug}} {{N}} {{CAP-…}} {{FEAT-…}}` … — điền lúc authoring).
Leftover-check: còn placeholder danh tính = lỗi (exit 1).

Usage: python scripts/bootstrap.py --name "Tên dự án" [--code CODE] [--authority "Tên <email>"]
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

IDENTITY = ("PROJECT_NAME", "PROJECT_CODE", "DATE", "AUTHORITY_NAME", "AUTHORITY_EMAIL")
TEXT_EXT = {".md", ".py", ".json", ".yml", ".yaml", ".toml", ".txt", ".css", ".html"}
SKIP_DIR = {".git", "node_modules", "target", "build", "dist", ".gradle", "__pycache__", "archive", ".next", ".venv"}
UNFILLED = "_CHƯA ĐIỀN_"


SELF = Path(__file__).resolve()


def text_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*"):
        if any(part in SKIP_DIR for part in p.parts):
            continue
        if p.resolve() == SELF:   # tool tự chứa {{PROJECT_NAME}}… trong docstring làm ví dụ — không thay, không flag
            continue
        if p.is_file() and (p.suffix in TEXT_EXT or p.name in ("Makefile", ".gitignore")):
            out.append(p)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--code", default=None)
    ap.add_argument("--authority", default=None)  # "Tên <email>"
    ap.add_argument("--check", action="store_true", help="chỉ leftover-check, không thay")
    args = ap.parse_args(argv[1:])

    name, email = UNFILLED, UNFILLED
    if args.authority:
        m = re.match(r"(.*?)\s*<(.+?)>", args.authority)
        if m:
            name, email = m.group(1).strip(), m.group(2).strip()
        else:
            name = args.authority.strip()
    subs = {
        "PROJECT_NAME": args.name,
        "PROJECT_CODE": args.code or re.sub(r"\W+", "-", args.name.lower()).strip("-"),
        "DATE": date.today().isoformat(),
        "AUTHORITY_NAME": name,
        "AUTHORITY_EMAIL": email,
    }

    files = text_files()
    if not args.check:
        changed = 0
        for p in files:
            t = p.read_text(encoding="utf-8", errors="ignore")
            new = t
            for k, v in subs.items():
                new = new.replace("{{" + k + "}}", v)
            if new != t:
                p.write_text(new, encoding="utf-8")
                changed += 1
        print(f"[bootstrap] thay danh tính ({args.name}) trong {changed} file.")

    pat = re.compile(r"\{\{(" + "|".join(IDENTITY) + r")\}\}")
    leftover = [p.relative_to(ROOT) for p in files if pat.search(p.read_text(encoding="utf-8", errors="ignore"))]
    if leftover:
        print("  ✗ còn placeholder DANH TÍNH ở:", file=sys.stderr)
        for p in leftover:
            print(f"      {p}", file=sys.stderr)
        return 1
    print("  ✓ không còn placeholder danh tính. (marker định dạng {{name}}/{{boundary}}… giữ nguyên, điền lúc authoring)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
