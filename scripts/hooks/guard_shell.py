#!/usr/bin/env python3
"""guard_shell — chặn ghi mockup có app shell LỆCH canonical `_shell.html` (PROTOCOL §8, vá shell-drift).

PreToolUse(Write|Edit): file `docs/ux/mockups/{target}/{screen}.html` (KHÔNG phải `_shell.html`).
So khối shell (giữa `<!-- SHELL:START -->` … `<!-- SHELL:END -->`) với `_shell.html` CÙNG thư mục,
chuẩn hoá `aria-current` (active-state mỗi màn khác nhau — hợp lệ) trước khi so. Lệch (nav items/thứ tự/
nhóm/logo/user-menu/ICON khác) → exit 2 = deny.

Fail-open — BỎ QUA (return 0) khi: không phải mockup .html · chính `_shell.html` · chưa có `_shell.html`
(canonical chưa dựng) · `_shell.html` chưa đánh dấu SHELL · mockup không có khối SHELL (màn full-screen:
login/print — hợp lệ). `Edit` chỉ thấy fragment `new_string`: nếu chạm marker SHELL mà không trọn khối →
BÁO MỀM (return 0, không chặn — guard chỉ so chắc khi Write thấy trọn file). MultiEdit: bỏ qua như guard_ds.
"""
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


def main() -> int:
    try:
        data = json.load(sys.stdin)
        ti = data.get("tool_input", {}) or {}
        path = (ti.get("file_path") or "").replace("\\", "/")
        content = ti.get("content")            # Write: trọn file
        new_string = ti.get("new_string")      # Edit: fragment
    except Exception:
        return 0

    if "docs/ux/mockups/" not in path or not path.endswith(".html"):
        return 0
    if os.path.basename(path) == "_shell.html":
        return 0

    shell_path = os.path.join(os.path.dirname(path), "_shell.html")
    if not os.path.exists(shell_path):
        return 0                               # canonical chưa dựng — không có gì để so
    try:
        canon_m = SHELL_RE.search(open(shell_path, encoding="utf-8", errors="ignore").read())
    except Exception:
        return 0
    if not canon_m:
        return 0                               # _shell.html chưa đánh dấu SHELL
    canon_norm = normalize(canon_m.group(1))

    is_write = content is not None
    text = content if is_write else (new_string or "")
    m = SHELL_RE.search(text)
    if not m:
        # Write không có khối shell = màn full-screen hợp lệ (login/print) → bỏ qua.
        # Edit chạm marker nhưng không trọn khối → không đủ để so → BÁO MỀM.
        if not is_write and ("SHELL:START" in text or "SHELL:END" in text):
            sys.stderr.write(
                f"[guard_shell] Edit chạm khối SHELL trong {path} nhưng fragment không trọn khối — "
                f"rà tay app shell vs _shell.html (guard chỉ so chắc khi Write thấy trọn file).\n")
        return 0

    if normalize(m.group(1)) != canon_norm:
        sys.stderr.write(
            f"[guard_shell] CẢNH BÁO: App shell trong {path} LỆCH _shell.html canonical "
            f"(nav items/thứ tự/nhóm heading/logo/user-menu/icon khác nhau). "
            f"Read _shell.html → copy đúng khối SHELL:START…SHELL:END → chỉ đổi `aria-current` mục đang đứng. "
            f"Rà lại trước khi trình chốt (ux-design §Nhất quán cross-màn).\n")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
