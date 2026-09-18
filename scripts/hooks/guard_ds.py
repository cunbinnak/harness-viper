#!/usr/bin/env python3
"""guard_ds — chặn ghi mockup/design-system lệch token (PROTOCOL §8, vá E1/A3).

PreToolUse(Write|Edit): file trong docs/ux/mockups/**.html hoặc docs/DESIGN-SYSTEM.md —
cấm mã màu hex THÔ ngoài khối `:root {}` (phải dùng `var(--color-*)`; token là SoT). exit 2 = deny. Fail-open.
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
        content = ti.get("content") or ti.get("new_string") or ""
    except Exception:
        return 0
    if "docs/ux/mockups/" not in path and not path.endswith("DESIGN-SYSTEM.md"):
        return 0
    body = re.sub(r":root\s*\{.*?\}", "", content, flags=re.DOTALL)      # bỏ khối định nghĩa token
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.DOTALL)              # bỏ comment CSS
    hexes = re.findall(r"[:\s]#[0-9a-fA-F]{3,8}\b", body)
    if hexes:
        sys.stderr.write(
            f"[guard_ds] Hex thô ngoài :root trong {path} ({[h.strip() for h in hexes[:3]]}…) — "
            f"phải dùng `var(--color-*)` (PROTOCOL §8; token DESIGN-SYSTEM là nguồn sự thật, chống demo-đẹp-chạy-xấu E1).\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
