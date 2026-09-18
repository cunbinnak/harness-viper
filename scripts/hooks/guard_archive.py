#!/usr/bin/env python3
"""guard_archive — chặn Write/Edit vào `archive/**` (wave đã đóng = hợp đồng BẤT BIẾN). PROTOCOL §3 · §5.

Snapshot `archive/wave-N/` là hồ sơ wave đã ship — sửa nó = mất vết / giả mạo lịch sử.
Đổi tính năng đã giao = FEAT version mới ở `docs/` sống (wave sau), KHÔNG sửa snapshot.

PreToolUse(Write|Edit|MultiEdit): file trong archive/ → exit 2 = deny. Fail-open.
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
    if "/archive/" in path or path.startswith("archive/"):
        sys.stderr.write(
            "[guard_archive] archive/** BẤT BIẾN — wave đã đóng là hợp đồng, KHÔNG sửa (PROTOCOL §3/§5). "
            "Đổi tính năng đã giao = FEAT version mới ở docs/ sống (wave sau), không sửa snapshot.\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
