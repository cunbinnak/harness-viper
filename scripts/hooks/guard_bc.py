#!/usr/bin/env python3
"""guard_bc — chặn deploy khi BACKWARD-COMPAT §3 chưa xanh (wave ≥2). PROTOCOL §8.

PreToolUse(Bash): đọc command. `make deploy` + wave ≥2 + §3 còn `- [ ]` → exit 2.
`docker compose up` (local) KHÔNG phải deploy → cho qua. Fail-open.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    try:
        data = json.load(sys.stdin)
        cmd = (data.get("tool_input", {}) or {}).get("command", "")
    except Exception:
        return 0
    if "make deploy" not in cmd:
        return 0
    state = ""
    try:
        state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    except OSError:
        return 0
    wm = re.search(r"Wave\s*:\s*(\d+)", state)
    if not wm or int(wm.group(1)) < 2:
        return 0  # wave 1 chưa có legacy để phá
    bc = ROOT / "docs" / "BACKWARD-COMPAT.md"
    if not bc.exists():
        return 0
    sec3 = re.search(r"## §3.*?(?=^##\s|\Z)", bc.read_text(encoding="utf-8"),
                     flags=re.DOTALL | re.MULTILINE)
    if sec3 and re.search(r"- \[ \]", sec3.group(0)):
        sys.stderr.write(
            "[guard_bc] BACKWARD-COMPAT §3 chưa xanh — KHÔNG deploy (PROTOCOL §8). "
            "Rà tương thích ngược §3 trước; đổi/xoá surface đang dùng phải additive hoặc khai `Legacy được phép phá`.\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
