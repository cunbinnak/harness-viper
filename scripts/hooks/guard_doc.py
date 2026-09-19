#!/usr/bin/env python3
"""guard_doc — chặn Write/Edit vào SPEC doc đã khoá scope (ngoài phase DOCUMENT).

Sau khoá scope (BUILD/VERIFY/SHIP/NEXT-WAVE) doc spec ĐÓNG BĂNG: vấn đề dồn sang wave sau
(`docs/ROADMAP.md §backlog` → `/next-wave` → `/document` top-up = re-lock). Không "vừa code vừa vặn
doc" — giữ hợp đồng ổn định cho review/dogfood đánh. (Ngoại lệ đồng bộ tên field trong AC khoá cũng
KHÔNG sửa tại chỗ — ghi backlog, wave sau top-up.)

CHO SỬA lúc BUILD (sổ SỐNG, append): DECISIONS.md · ROADMAP.md (§backlog + tick tiến độ) ·
BACKWARD-COMPAT.md · PRODUCTION-READY.md. Ngoài `docs/` (services/ · knowledge-base/ · tracking/ · STATE)
không đụng. Phase DOCUMENT (author + top-up) → cho sửa mọi doc.

PreToolUse(Write|Edit|MultiEdit): exit 2 nếu spec doc + phase != DOCUMENT. Fail-open.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIVING = {"DECISIONS.md", "ROADMAP.md", "BACKWARD-COMPAT.md", "PRODUCTION-READY.md"}

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def phase() -> str:
    try:
        t = (ROOT / "STATE.md").read_text(encoding="utf-8")
    except OSError:
        return ""
    m = re.search(r"Phase hiện tại\s*:\s*([A-Za-z-]+)", t)
    return m.group(1).upper().replace(" ", "-") if m else ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
        fp = str((data.get("tool_input") or {}).get("file_path", "")).replace("\\", "/")
    except Exception:
        return 0  # fail-open
    if "docs/" not in fp:                 # chỉ canh docs/
        return 0
    if fp.rsplit("/", 1)[-1] in LIVING:   # sổ sống — luôn cho append
        return 0
    p = phase()
    if p in ("", "DOCUMENT"):             # DOCUMENT author/top-up → cho sửa
        return 0
    sys.stderr.write(
        f"[guard_doc] Pha {p}: doc SPEC đã KHOÁ — không sửa lúc BUILD/VERIFY.\n"
        "Thiếu/lệch → `docs/ROADMAP.md §backlog` → wave sau `/document` top-up (re-lock). "
        "Mơ hồ trong AC → `docs/DECISIONS.md` (được sửa).\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
