#!/usr/bin/env python3
"""reanchor — sau compact, nhồi lại PROTOCOL §2 (luật nền) + STATE (phase/wave) vào context.

Van an toàn cho MAIN-code-hết: phiên BUILD dài bị compact → mất luật thủ tục → reanchor kéo lại.
SessionStart(matcher=compact): stdout JSON `additionalContext`. exit 0 luôn (hook lỗi không chặn phiên).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    try:
        sys.stdin.read()
        proto = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")
        state = (ROOT / "STATE.md").read_text(encoding="utf-8")
        laws = re.search(r"## §2 — Luật nền(.*?)(?=^---|\Z)", proto, flags=re.DOTALL | re.MULTILINE)
        ph = re.search(r"Phase hiện tại\s*:\s*(.+)", state)
        wv = re.search(r"Wave\s*:\s*(.+)", state)
        ctx = (
            f"[reanchor sau compact] Đang: phase={ph.group(1).strip() if ph else '?'} · "
            f"wave={wv.group(1).strip() if wv else '?'}.\n"
            f"LUẬT NỀN (PROTOCOL §2) — không được quên sau compact:\n"
            f"{laws.group(1).strip() if laws else '(đọc PROTOCOL.md §2)'}\n"
            f"→ Đọc STATE.md (gate đang mở) + PROTOCOL.md để tiếp đúng phase.")
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": ctx}}))
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
