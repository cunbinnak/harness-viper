#!/usr/bin/env python3
"""guard_archive — chặn Write/Edit vào `archive/**` (wave đã đóng = hợp đồng BẤT BIẾN). PROTOCOL §3 · §5.

Snapshot `archive/wave-N/` là hồ sơ wave đã ship — sửa nó = mất vết / giả mạo lịch sử.
Đổi tính năng đã giao = FEAT version mới ở `docs/` sống (wave sau), KHÔNG sửa snapshot.

PreToolUse(Write|Edit|MultiEdit): file trong archive/ → exit 2 = deny. Fail-open.
"""
import json
import re
import sys
from pathlib import Path

ROOT_S = str(Path(__file__).resolve().parents[2]).replace("\\", "/")

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def rel(path: str) -> str:
    """Đường dẫn tính từ gốc repo (so không phân biệt hoa thường — Windows `d:` vs `D:`). Ngoài repo → ""."""
    if path.lower().startswith(ROOT_S.lower() + "/"):
        return path[len(ROOT_S) + 1:]
    return "" if re.match(r"^([a-zA-Z]:)?/", path) else path.removeprefix("./")


def main() -> int:
    try:
        data = json.load(sys.stdin)
        path = ((data.get("tool_input", {}) or {}).get("file_path") or "").replace("\\", "/")
    except Exception:
        return 0
    if rel(path).startswith("archive/"):   # chỉ archive/ ở gốc repo — không chặn nhầm services/**/archive/
        sys.stderr.write(
            "[guard_archive] archive/** BẤT BIẾN — wave đã đóng là hợp đồng, KHÔNG sửa (PROTOCOL §3/§5). "
            "Đổi tính năng đã giao = FEAT version mới ở docs/ sống (wave sau), không sửa snapshot.\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
