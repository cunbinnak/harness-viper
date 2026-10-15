#!/usr/bin/env python3
"""guard_bc — canh deploy production. PROTOCOL §8.

PreToolUse(Bash): lệnh `make … deploy` (mọi biến thể: `make deploy` · `make -s deploy` · `make -C services/x deploy`):
- PRODUCTION-READY còn mục chưa tick (trừ mục `(sau deploy)` — tick sau khi deploy) → exit 2.
- Wave ≥2 + BACKWARD-COMPAT §3 còn `- [ ]` → exit 2.
- Còn lại → buộc HỎI Authority (permissionDecision `ask`) — deploy = ra ngoài, không đảo ngược.
`docker compose up` (local) KHÔNG phải deploy → cho qua. Fail-open khi không đọc được input.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEPLOY = re.compile(r"\bmake\b[^;&|\n]*\bdeploy\b")

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def read(rel: str) -> str:
    try:
        return (ROOT / rel).read_text(encoding="utf-8")
    except OSError:
        return ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
        cmd = (data.get("tool_input", {}) or {}).get("command", "")
    except Exception:
        return 0
    if not DEPLOY.search(cmd):
        return 0
    why = []
    todo = [ln.strip() for ln in read("docs/PRODUCTION-READY.md").splitlines()
            if re.match(r"\s*- \[ \]", ln) and "(sau deploy)" not in ln]
    if todo:
        why.append(f"PRODUCTION-READY còn {len(todo)} mục chưa xanh (trừ mục sau deploy): {todo[0][:80]}")
    wm = re.search(r"Wave\s*:\s*(\d+)", read("STATE.md"))
    sec3 = re.search(r"## §3.*?(?=^##\s|\Z)", read("docs/BACKWARD-COMPAT.md"), flags=re.DOTALL | re.MULTILINE)
    if wm and int(wm.group(1)) >= 2 and sec3 and re.search(r"- \[ \]", sec3.group(0)):
        why.append("BACKWARD-COMPAT §3 chưa xanh — đổi/xoá surface đang dùng phải additive hoặc khai `Legacy được phép phá`")
    if why:
        sys.stderr.write("[guard_bc] KHÔNG deploy (PROTOCOL §8):\n" + "".join(f"  · {w}\n" for w in why))
        return 2
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "ask",
        "permissionDecisionReason": "[guard_bc] Deploy production = ra ngoài, không đảo ngược — Authority xác nhận."}},
        ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
