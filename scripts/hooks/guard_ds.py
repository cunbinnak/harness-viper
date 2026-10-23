#!/usr/bin/env python3
"""guard_ds — chặn ghi mockup/design-system lệch token (PROTOCOL §8).

PreToolUse(Write|Edit): file trong docs/ux/mockups/**.html hoặc docs/DESIGN-SYSTEM.md —
cấm mã màu hex THÔ ngoài khối `:root {}` (phải dùng `var(--color-*)`; token là SoT). exit 2 = deny. Fail-open.
Mockup .html có thẻ HTML: chỉ soi vùng CSS (`<style>`, thuộc tính `style=`) — chữ hiển thị như "Đơn #1042" không phải mã màu.
"""
import json
import re
import sys

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    try:
        data = json.load(sys.stdin)
        ti = data.get("tool_input", {}) or {}
        path = (ti.get("file_path") or "").replace("\\", "/")
        content = ti.get("content") or ti.get("new_string") or "\n".join(
            e.get("new_string", "") for e in ti.get("edits") or [])   # MultiEdit
    except Exception:
        return 0
    if "docs/ux/mockups/" not in path and not path.endswith("DESIGN-SYSTEM.md"):
        return 0
    body = re.sub(r":root\s*\{.*?\}", "", content, flags=re.DOTALL)      # bỏ khối định nghĩa token
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.DOTALL)              # bỏ comment CSS
    body = re.sub(r"^\s*\|\s*`?--[\w-]+`?\s*\|.*$", "", body, flags=re.MULTILINE)  # dòng bảng token §2 (| --x | #hex |) = chỗ định nghĩa
    if path.endswith(".html") and re.search(r"<[a-zA-Z]", body):
        body = "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", body, flags=re.DOTALL | re.I)
                         + re.findall(r'\bstyle\s*=\s*"([^"]*)"', body, flags=re.I)
                         + re.findall(r"\bstyle\s*=\s*'([^']*)'", body, flags=re.I))
    hexes = re.findall(r"[:\s]#[0-9a-fA-F]{3,8}\b", body)
    if hexes:
        sys.stderr.write(
            f"[guard_ds] Hex thô ngoài :root trong {path} ({[h.strip() for h in hexes[:3]]}…) — "
            f"phải dùng `var(--color-*)` (PROTOCOL §8; token DESIGN-SYSTEM là nguồn sự thật, chống demo-đẹp-chạy-xấu).\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
