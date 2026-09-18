#!/usr/bin/env python3
"""guard_proof — chặn Write/Edit vào `*proof.json` (bằng chứng runtime CHỈ do capture_proof.py sinh).

gate đọc proof.json để verify make-check + health THẬT (không tin tick tay). Nếu agent/MAIN sửa tay được
proof.json thì cơ chế mất tác dụng → hook chặn Write/Edit TOOL; capture_proof.py ghi qua Python I/O nên lọt.

PreToolUse(Write|Edit|MultiEdit): file `proof.json` → exit 2. Fail-open.
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
        path = ((data.get("tool_input", {}) or {}).get("file_path") or "").replace("\\", "/")
    except Exception:
        return 0
    if path.endswith("proof.json"):
        sys.stderr.write(
            "[guard_proof] proof.json là bằng chứng MÁY-sinh — KHÔNG sửa tay. "
            "Chạy `python scripts/capture_proof.py` để cập nhật (make check + health thật). Tick tay không thay được proof.\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
