#!/usr/bin/env python3
"""selftest.py — smoke test bộ khung: scripts chạy đúng · file đủ · JSON hợp lệ. exit 1 nếu fail.

Không thay thế test thật (chạy end-to-end mới đo được chất lượng) — chỉ bắt gãy hiển nhiên:
gate/guard crash, thiếu command/agent, settings.json hỏng.

Usage: python scripts/selftest.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PY = sys.executable
ok = True


def check(cond: bool, msg: str) -> None:
    global ok
    print(f"  {'✓' if cond else '✗'} {msg}")
    ok = ok and cond


def run(rel: str, args: list[str], stdin: str = "") -> int:
    return subprocess.run([PY, str(ROOT / rel), *args], input=stdin,
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          cwd=ROOT).returncode


def main() -> int:
    print("[selftest] smoke bộ khung viper-adlc\n")

    # 1. gate.py — DOCUMENT trên state trống phải THIẾU (exit 1)
    check(run("scripts/gate.py", ["DOCUMENT"]) == 1, "gate.py DOCUMENT → exit 1 (báo thiếu, đúng)")
    check(run("scripts/gate.py", ["SAI-PHASE"]) == 2, "gate.py phase lạ → exit 2")

    # 2. guards
    check(run("scripts/hooks/guard_ask.py", [], "") == 0, "guard_ask (DOCUMENT, scope chưa khoá) → allow")
    check(run("scripts/hooks/guard_ds.py", [],
              '{"tool_input":{"file_path":"docs/ux/mockups/x.html","content":"a{color:#f00}"}}') == 2,
          "guard_ds hex thô mockup → deny (exit 2)")
    check(run("scripts/hooks/guard_ds.py", [],
              '{"tool_input":{"file_path":"services/web/x.css","content":"a{color:#f00}"}}') == 0,
          "guard_ds file thường → allow")
    check(run("scripts/hooks/guard_bc.py", [], '{"tool_input":{"command":"ls"}}') == 0,
          "guard_bc lệnh thường → allow")
    check(run("scripts/hooks/guard_archive.py", [],
              '{"tool_input":{"file_path":"archive/wave-1/x.md","content":"x"}}') == 2,
          "guard_archive sửa archive/ → deny (exit 2)")
    check(run("scripts/hooks/guard_proof.py", [],
              '{"tool_input":{"file_path":"tracking/wave-1/proof.json","content":"x"}}') == 2,
          "guard_proof sửa proof.json → deny (exit 2)")
    check(run("scripts/hooks/reanchor.py", [], "") == 0, "reanchor → exit 0")

    # 3. settings.json hợp lệ
    try:
        d = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
        matchers = [h["matcher"] for h in d["hooks"]["PreToolUse"]]
        check(set(matchers) >= {"AskUserQuestion", "Bash"}, "settings.json hợp lệ + 3 guard hook")
    except Exception as e:
        check(False, f"settings.json: {e}")

    # 4. command · agent · skill đủ
    cmds = {"document", "build", "verify", "ship", "next-wave", "status", "dogfood"}
    have = {p.stem for p in (ROOT / ".claude/commands").glob("*.md")}
    check(cmds <= have, f"7 command đủ ({len(cmds & have)}/7)")

    agents = {"reviewer", "bug-hunter", "test-writer",
              "persona-newbie", "persona-edge", "persona-picky",
              "persona-rushed", "persona-breaker", "persona-mobile"}
    hava = {p.stem for p in (ROOT / ".claude/agents").glob("*.md")}
    check(agents <= hava, f"9 agent đủ ({len(agents & hava)}/9)")

    stacks = {"stack-spring-boot", "stack-nextjs", "stack-bff", "stack-flutter"}
    have_sk = {p.name for p in (ROOT / ".claude/skills").glob("*") if p.is_dir()}
    check(stacks <= have_sk, f"4 stack skill đủ ({len(stacks & have_sk)}/4)")
    check(len(have_sk) >= 20, f"skill library ({len(have_sk)} skill — ref/review/method chắt lọc)")

    # 5. file khung
    for f in ("CLAUDE.md", "PROTOCOL.md", "STATE.md", "Makefile", ".gitignore"):
        check((ROOT / f).exists(), f"{f} tồn tại")

    # 6. templates gom 1 folder (docs/ + knowledge-base/ chỉ file thật)
    tpls = list((ROOT / "templates").glob("TEMPLATE.*.md"))
    check(len(tpls) >= 16, f"templates/ đủ ({len(tpls)} template) + README")
    stray = list((ROOT / "docs").rglob("TEMPLATE.*")) + list((ROOT / "knowledge-base").glob("TEMPLATE.*"))
    check(not stray, f"docs/ + knowledge-base/ không còn TEMPLATE lạc ({len(stray)} sót)")

    print(f"\n{'PASS — smoke sạch' if ok else 'FAIL — có mục gãy'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
