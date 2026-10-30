#!/usr/bin/env python3
"""guard_qa — hai chiều của luật "QA độc lập" (PROTOCOL §7 · luật #9):

1. `test-writer` chỉ được GHI `tracking/wave-N/test-cases.md` trong repo.
2. `test-cases.md` CHỈ `test-writer` ghi — trạng thái TC do một người xác nhận. MAIN / agent khác ghi vào → exit 2.
   Ngoại lệ duy nhất: dòng TC gắn `@thủ-công` (TC UI mobile MAIN chạy tay — verify.md 3c) — mọi dòng TC trong
   phần ghi mới đều phải mang tag đó.

PreToolUse(Write|Edit|MultiEdit): hook chạy bên trong subagent nhận thêm `agent_type` (tài liệu hooks: có mặt khi
hook bắn trong một subagent); phiên chính không có `agent_type`. File ngoài repo (script chạy TC ở thư mục tạm) →
cho qua; dọn ngay là việc của luật #9. Không chặn đường Bash (người dùng đã chọn giữ nguyên). Fail-open khi không
đọc được input.
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


def new_text(tool_input: dict) -> str:
    """Phần nội dung sắp ghi: Write → content · Edit → new_string · MultiEdit → mọi new_string."""
    parts = [tool_input.get("content") or "", tool_input.get("new_string") or ""]
    parts += [e.get("new_string") or "" for e in (tool_input.get("edits") or []) if isinstance(e, dict)]
    return "\n".join(parts)


def verdict(agent_type: str, file_path: str, tool_input: dict | None = None) -> str | None:
    """Lý do chặn, hoặc None nếu cho qua."""
    r = rel(file_path.replace("\\", "/"))
    if agent_type != "test-writer":
        if not (r and ALLOWED.match(r)):
            return None
        rows = [ln for ln in new_text(tool_input or {}).splitlines() if ln.lstrip().startswith("| TC-")]
        if rows and all("@thủ-công" in ln for ln in rows):
            return None   # ngoại lệ: TC UI mobile MAIN chạy tay
        return (f"`{r}` chỉ test-writer được ghi — trạng thái TC do QA độc lập xác nhận (verify.md Bước 5). "
                "Cần chạy lại TC → spawn test-writer chế độ CHẠY LẠI. Ngoại lệ duy nhất: dòng `@thủ-công` (mobile).")
    if not r or ALLOWED.match(r):
        return None
    return (f"test-writer chỉ được ghi tracking/wave-N/test-cases.md trong repo — `{r}` thì không. "
            "Script chạy TC (Playwright .mjs · k6 · shell) là file tạm: để NGOÀI repo, dùng xong dọn ngay (luật #9). "
            "Không viết code, kể cả test code.")


def main() -> int:
    try:
        data = json.load(sys.stdin)
        agent_type = str(data.get("agent_type") or "")
        tool_input = data.get("tool_input") or {}
        path = str(tool_input.get("file_path") or "")
    except Exception:
        return 0  # fail-open
    why = verdict(agent_type, path, tool_input)
    if why:
        sys.stderr.write(f"[guard_qa] {why}\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
