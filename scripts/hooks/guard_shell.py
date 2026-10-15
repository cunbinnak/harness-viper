#!/usr/bin/env python3
"""guard_shell — CẢNH BÁO mockup có app shell LỆCH canonical `_shell.html` (PROTOCOL §8, chống shell trôi).

PostToolUse(Write|Edit|MultiEdit) — chạy SAU khi ghi: đọc TRỌN file mockup trên đĩa (nên bắt được cả Write lẫn
Edit/MultiEdit), so khối shell (giữa `<!-- SHELL:START -->` … `<!-- SHELL:END -->`) với `_shell.html` CÙNG thư mục,
chuẩn hoá `aria-current` (active-state mỗi màn khác nhau — hợp lệ) trước khi so. Lệch (nav items/thứ tự/nhóm/logo/
user-menu/ICON khác) → exit 2 = đưa cảnh báo cho model (file ĐÃ ghi, KHÔNG undo) để tự sửa. Cảnh báo, không chặn.

Bỏ qua (exit 0) khi: không phải mockup .html · chính `_shell.html` · chưa có `_shell.html` (canonical chưa dựng) ·
`_shell.html` chưa đánh dấu SHELL · mockup không có khối SHELL (màn full-screen: login/print — hợp lệ). Fail-open.
"""
from __future__ import annotations

import json
import os
import re
import sys

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SHELL_RE = re.compile(r"<!--\s*SHELL:START\s*-->(.*?)<!--\s*SHELL:END\s*-->", re.DOTALL)


def normalize(block: str) -> str:
    """Xoá active-state (mỗi màn đánh dấu `aria-current` ở đúng mục đang đứng — hợp lệ) + gộp whitespace."""
    b = re.sub(r'\s*aria-current="[^"]*"', "", block)
    b = re.sub(r"\s+", " ", b)
    return b.strip()


def shell_of(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            m = SHELL_RE.search(f.read())
    except OSError:
        return None
    return normalize(m.group(1)) if m else None


def main() -> int:
    try:
        data = json.load(sys.stdin)
        path = ((data.get("tool_input", {}) or {}).get("file_path") or "").replace("\\", "/")
    except Exception:
        return 0
    if "docs/ux/mockups/" not in path or not path.endswith(".html") or os.path.basename(path) == "_shell.html":
        return 0
    canon = shell_of(os.path.join(os.path.dirname(path), "_shell.html"))
    mine = shell_of(path)
    if canon is None or mine is None or mine == canon:
        return 0
    sys.stderr.write(
        f"[guard_shell] CẢNH BÁO: App shell trong {path} LỆCH _shell.html canonical "
        f"(nav items/thứ tự/nhóm heading/logo/user-menu/icon khác nhau). File ĐÃ ghi — sửa ngay: "
        f"Read _shell.html → copy đúng khối SHELL:START…SHELL:END → chỉ đổi `aria-current` mục đang đứng "
        f"(ux-design §Nhất quán cross-màn).\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
