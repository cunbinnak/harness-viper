#!/usr/bin/env python3
"""guard_makefile — chặn Write/Edit vào ROOT Makefile (hợp đồng 6 lệnh, bất biến).

Root Makefile chỉ ĐIỀU PHỐI (viết 1 lần). Lúc BUILD, MAIN điền THÂN ở per-target
`services/<nhóm>/<tên>/Makefile` (stack skill §4) — KHÔNG sửa root. Chống "đang triển khai lại
sửa hợp đồng" (đổi tên/thân verb ở root = phá gate.py + capture_proof).

PreToolUse(Write|Edit|MultiEdit): exit 2 nếu file_path là Makefile KHÔNG nằm dưới services/. Fail-open.
"""
import json
import sys

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    try:
        data = json.load(sys.stdin)
        fp = (data.get("tool_input") or {}).get("file_path", "")
    except Exception:
        return 0  # fail-open
    norm = str(fp).replace("\\", "/").strip()
    name = norm.rsplit("/", 1)[-1]
    if name == "Makefile" and "services/" not in norm:
        sys.stderr.write(
            "[guard_makefile] Root Makefile là HỢP ĐỒNG 6 lệnh — KHÔNG sửa (dù đang BUILD).\n"
            "Điền THÂN ở per-target `services/<nhóm>/<tên>/Makefile` (stack skill §4). "
            "Cần đổi hợp đồng = việc framework, không phải BUILD.\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
