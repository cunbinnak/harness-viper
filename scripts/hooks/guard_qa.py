#!/usr/bin/env python3
"""guard_qa — `test-writer` chỉ được GHI `tracking/wave-N/test-cases.md` trong repo (PROTOCOL §7 · luật #9).

PreToolUse(Write|Edit|MultiEdit): hook chạy bên trong subagent nhận thêm `agent_type` (tài liệu hooks: có mặt khi
hook bắn trong một subagent). `agent_type == "test-writer"` mà ghi file TRONG repo khác test-cases.md → exit 2.
File ngoài repo (script chạy TC để ở thư mục tạm) → cho qua; dọn ngay là việc của luật #9.
Không chặn đường Bash (người dùng đã chọn giữ nguyên). Fail-open khi không đọc được input.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT_S = str(Path(__file__).resolve().parents[2]).replace("\\", "/")
ALLOWED = re.compile(r"^tracking/wave-\d+/test-cases\.md$")

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def rel(path: str) -> str:
    """Đường dẫn tính từ gốc repo (so không phân biệt hoa thường — Windows `d:` vs `D:`). Ngoài repo → ""."""
    if path.lower().startswith(ROOT_S.lower() + "/"):
        return path[len(ROOT_S) + 1:]
    return "" if re.match(r"^([a-zA-Z]:)?/", path) else path.removeprefix("./")


def verdict(agent_type: str, file_path: str) -> str | None:
    """Lý do chặn, hoặc None nếu cho qua."""
    if agent_type != "test-writer":
        return None
    r = rel(file_path.replace("\\", "/"))
    if not r or ALLOWED.match(r):
        return None
    return (f"test-writer chỉ được ghi tracking/wave-N/test-cases.md trong repo — `{r}` thì không. "
            "Script chạy TC (Playwright .mjs · k6 · shell) là file tạm: để NGOÀI repo, dùng xong dọn ngay (luật #9). "
            "Không viết code, kể cả test code.")


def main() -> int:
    try:
        data = json.load(sys.stdin)
        agent_type = str(data.get("agent_type") or "")
        path = str((data.get("tool_input") or {}).get("file_path") or "")
    except Exception:
        return 0  # fail-open
    why = verdict(agent_type, path)
    if why:
        sys.stderr.write(f"[guard_qa] {why}\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
