#!/usr/bin/env python3
"""guard_agent — chặn spawn agent sai luật (PROTOCOL §8).

PreToolUse(Agent): hai luật lõi trước đây chỉ là lời dặn.
  1. BUILD: MAIN tự viết hết code và test, KHÔNG giao cho agent nào (CLAUDE.md · build.md).
  2. Mọi pha: spawn phải đứng chờ kết quả. Công cụ Agent mặc định chạy NỀN; muốn đứng chờ phải truyền
     `run_in_background: false`. Không truyền = chạy nền = MAIN đi tiếp khi agent chưa xong
     (phá "thu đủ finding rồi mới sửa", verify.md).
Exit 2 = chặn, stderr đưa lại cho model. Fail-open khi không đọc được input hoặc STATE.md.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def verdict(tool_input: dict, phase: str) -> str | None:
    """Lý do chặn, hoặc None nếu cho qua."""
    if phase == "BUILD":
        return ("Đang ở pha BUILD: MAIN tự viết hết code và test, không giao cho agent nào "
                "(agent chỉ xuất hiện ở /verify để kiểm). Cần tra cứu thì đọc trực tiếp bằng Read/Grep.")
    if tool_input.get("run_in_background") is not False:
        return ("Spawn agent phải đứng chờ kết quả: truyền `run_in_background: false`. "
                "Công cụ Agent mặc định chạy nền, MAIN sẽ đi tiếp khi agent chưa xong.")
    return None


def phase_of_state() -> str:
    try:
        text = (ROOT / "STATE.md").read_text(encoding="utf-8")
    except OSError:
        return ""
    m = re.search(r"Phase hiện tại\s*:\s*([A-Za-z-]+)", text)
    return m.group(1).upper().replace(" ", "-") if m else ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
        tool_input = data.get("tool_input") or {}
    except Exception:
        return 0  # fail-open
    why = verdict(tool_input, phase_of_state())
    if why:
        sys.stderr.write(f"[guard_agent] {why}\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
