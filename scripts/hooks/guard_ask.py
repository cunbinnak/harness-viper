#!/usr/bin/env python3
"""guard_ask — chặn AskUserQuestion sau khi khoá scope (PROTOCOL §2 luật #2 · §8).

Cho phép hỏi Authority ở: DOCUMENT (author + top-up) · NEXT-WAVE (go/pivot/kill).
Block ở: BUILD / VERIFY / SHIP — mơ hồ thì tự quyết (DECISIONS.md), tắc thì STATE §Blocker.
Hành động ra-ngoài/không-đảo-ngược vẫn hỏi được bằng LỜI trong chat (không qua tool này) → lớp permission `ask` lo.

PreToolUse(AskUserQuestion): exit 2 + stderr = deny · exit 0 = allow. Fail-open.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOW = {"DOCUMENT", "NEXT-WAVE"}

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def phase() -> str:
    try:
        text = (ROOT / "STATE.md").read_text(encoding="utf-8")
    except OSError:
        return ""
    m = re.search(r"Phase hiện tại\s*:\s*(.+)", text)
    return m.group(1).strip().upper().replace(" ", "-") if m else ""


def main() -> int:
    try:
        sys.stdin.read()
        p = phase()
    except Exception:
        return 0
    if p and p not in ALLOW:
        sys.stderr.write(
            f"[guard_ask] Phase {p}: KHÔNG hỏi Authority (đã khoá scope — PROTOCOL §2 luật #2).\n"
            f"Mơ hồ → tự quyết + docs/DECISIONS.md. Tắc cứng → STATE.md §Blocker. "
            f"Chỉ hành động ra-ngoài/không-đảo-ngược mới hỏi (bằng lời, không qua tool này).\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
