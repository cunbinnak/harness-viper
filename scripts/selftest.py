#!/usr/bin/env python3
"""selftest.py — smoke test bộ khung: scripts chạy đúng · file đủ · JSON hợp lệ. exit 1 nếu fail.

Không thay thế test thật (chạy end-to-end mới đo được chất lượng) — chỉ bắt gãy hiển nhiên:
gate/guard crash, thiếu command/agent, settings.json hỏng.

Usage: python scripts/selftest.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:      # máy mới chưa có PyYAML: vẫn chạy được, chỉ bỏ kiểm cú pháp YAML của frontmatter
    yaml = None

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
    print("[selftest] smoke bộ khung\n")

    # 1. gate.py — DOCUMENT trên state trống phải THIẾU (exit 1)
    check(run("scripts/gate.py", ["DOCUMENT"]) == 1, "gate.py DOCUMENT → exit 1 (báo thiếu, đúng)")
    check(run("scripts/gate.py", ["SAI-PHASE"]) == 2, "gate.py phase lạ → exit 2")

    # 1b. logic regression theo phạm vi ảnh hưởng: đoạn danh sách + cột nguồn R
    sys.path.insert(0, str(ROOT / "scripts"))
    import gate
    sample = ("## Phạm vi ảnh hưởng\n- đổi A → B → TC chọn: TC-1-001\n- Không ảnh hưởng: C — vì D\n\n"
              "| TC | loại | nguồn | AC | tag | mô tả | cách chạy | kết quả | thực tế |\n|---|---|---|---|---|---|---|---|---|\n"
              "| TC-1-001 | functional | R | FEAT-a AC-1 | @regression | x | y | PASS | z |\n")
    check(len(gate.impact_block(sample)) == 2, "gate.impact_block đọc đoạn Phạm vi ảnh hưởng (2 dòng danh sách)")
    check([x["src"] for x in gate.tc_rows(sample)] == ["R"], "gate.tc_rows đọc cột nguồn")
    rr = gate.tc_rows(sample)
    check(gate.r_desc_drift(rr, {"TC-1-001": " x "}) == [], "gate.r_desc_drift: TC cũ chép nguyên văn → không báo")
    check(gate.r_desc_drift(rr, {"TC-1-001": "khác"}) == ["TC-1-001"], "gate.r_desc_drift: TC cũ bị sửa mô tả → báo")

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
    check(run("scripts/hooks/guard_archive.py", [],
              '{"tool_input":{"file_path":"services/web/app/archive/page.tsx","content":"x"}}') == 0,
          "guard_archive code sản phẩm có thư mục archive/ → allow")
    check(run("scripts/hooks/guard_proof.py", [],
              '{"tool_input":{"file_path":"tracking/wave-1/proof.json","content":"x"}}') == 2,
          "guard_proof sửa proof.json → deny (exit 2)")
    check(run("scripts/hooks/guard_makefile.py", [],
              '{"tool_input":{"file_path":"Makefile","content":"x"}}') == 2,
          "guard_makefile ROOT Makefile → deny (exit 2)")
    check(run("scripts/hooks/guard_makefile.py", [],
              '{"tool_input":{"file_path":"services/boundaries/order/Makefile","content":"x"}}') == 0,
          "guard_makefile per-target Makefile → allow")
    check(run("scripts/hooks/guard_doc.py", [],
              '{"tool_input":{"file_path":"docs/DECISIONS.md","content":"x"}}') == 0,
          "guard_doc DECISIONS (sổ sống) → allow")
    check(run("scripts/hooks/reanchor.py", [], "") == 0, "reanchor → exit 0")

    # 2b. hook sinh ra từ lần rà soát + lỗi đã vá (mỗi ca là một lỗi từng có thật)
    import importlib.util

    def load_hook(name: str):
        spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "hooks" / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    ga, gq, gb = load_hook("guard_agent"), load_hook("guard_qa"), load_hook("guard_bc")
    check(ga.verdict({"run_in_background": False}, "VERIFY") is None, "guard_agent: spawn đứng chờ (run_in_background=false) → cho qua")
    check(ga.verdict({}, "VERIFY") is not None, "guard_agent: bỏ trống run_in_background (= chạy nền) → chặn")
    check(ga.verdict({"run_in_background": True}, "DOCUMENT") is not None, "guard_agent: run_in_background=true → chặn")
    check(ga.verdict({"run_in_background": False}, "BUILD") is not None, "guard_agent: BUILD cấm mọi spawn, kể cả đứng chờ")
    check(gq.verdict("test-writer", str(ROOT / "services" / "web" / "x" / "a.test.ts")) is not None, "guard_qa: test-writer ghi vào services/ → chặn")
    check(gq.verdict("test-writer", str(ROOT / "tracking" / "wave-1" / "test-cases.md")) is None, "guard_qa: test-writer ghi test-cases.md → cho qua")
    check(gq.verdict("test-writer", str(ROOT / "tracking" / "wave-1" / "qa" / "run.mjs")) is not None, "guard_qa: script .mjs trong tracking/ → chặn")
    check(gq.verdict("test-writer", str(Path(tempfile.gettempdir()) / "run.mjs")) is None, "guard_qa: file tạm ngoài repo → cho qua")
    check(gq.verdict("reviewer", str(ROOT / "services" / "a.ts")) is None, "guard_qa: chỉ soi test-writer (agent khác đã bị chặn Write/Edit ở frontmatter)")
    real_cmds = ["cd services/x && make deploy", "sh -c 'make deploy'", "FOO=1 make -C services/web/x deploy"]
    text_only = ['git commit -m "docs: ghi make deploy"', "grep -rn 'make deploy' docs", "echo make deploy"]
    check(all(gb.real_invocation(c) for c in real_cmds), "guard_bc: nhận ra lệnh deploy thật (sau &&, trong sh -c, sau biến môi trường)")
    check(not any(gb.real_invocation(c) for c in text_only), "guard_bc: chữ nhắc trong commit message / grep / echo không bị coi là deploy")
    check(run("scripts/hooks/guard_ds.py", [], json.dumps({"tool_input": {"file_path": "docs/ux/mockups/x.html",
          "content": "<td>Mã đơn #1042</td>"}})) == 0, "guard_ds: '#1042' trong chữ hiển thị của mockup → cho qua")
    check(run("scripts/hooks/guard_ds.py", [], json.dumps({"tool_input": {"file_path": "docs/ux/mockups/x.html",
          "content": "<div style=\"color:#f00\">x</div>"}})) == 2, "guard_ds: hex trong style= của mockup → chặn")
    if not (ROOT / "docs" / "PRODUCTION-READY.md").exists():
        check(run("scripts/hooks/guard_bc.py", [], json.dumps({"tool_input": {"command": real_cmds[0]}})) == 2,
              "guard_bc: deploy khi chưa có PRODUCTION-READY → chặn (không fail-open)")
    check(gate._norm_api("IPC transcribe") == "IPC transcribe" and gate._norm_api("GET /api/v1/x/{id}") == "GET /x/{}",
          "gate._norm_api hiểu cả REST lẫn IPC (kind desktop)")
    import next_wave
    check(next_wave.accept_ok("DEC-9999")[0] is False, "next_wave: --accept-red với DEC không có thật → từ chối")
    mk = (ROOT / "Makefile").read_text(encoding="utf-8")
    check("-mindepth 3 -maxdepth 3" in mk, "Makefile: tìm target ở độ sâu 3 (services/<nhóm>/<tên>/Makefile)")

    # 3. settings.json hợp lệ
    try:
        d = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
        matchers = [h["matcher"] for h in d["hooks"]["PreToolUse"]]
        check(set(matchers) >= {"AskUserQuestion", "Bash"}, "settings.json hợp lệ + 3 guard hook")
        used = set(re.findall(r"scripts/hooks/(\w+)\.py", json.dumps(d)))
        have_hooks = {p.stem for p in (ROOT / "scripts" / "hooks").glob("*.py")}
        check(have_hooks <= used, f"settings.json nối đủ {len(have_hooks)} hook"
              + (f" — CHƯA nối: {', '.join(sorted(have_hooks - used))}" if have_hooks - used else ""))
    except Exception as e:
        check(False, f"settings.json: {e}")

    # 4. command · agent · skill đủ
    cmds = {"document", "build", "verify", "ship", "next-wave", "status", "dogfood"}
    have = {p.stem for p in (ROOT / ".claude/commands").glob("*.md")}
    check(cmds <= have, f"7 command đủ ({len(cmds & have)}/7)")

    agents = {"pre-mortem", "reviewer", "bug-hunter", "test-writer",
              "persona-newbie", "persona-edge", "persona-picky",
              "persona-rushed", "persona-breaker", "persona-mobile"}
    hava = {p.stem for p in (ROOT / ".claude/agents").glob("*.md")}
    check(agents <= hava, f"{len(agents)} agent đủ ({len(agents & hava)}/{len(agents)})")
    # frontmatter YAML phải parse được — hỏng là Claude Code lặng lẽ bỏ agent ("not available", MAIN thay
    # general-purpose) / skill / command. Hay dính: `description:` có ": " giữa câu mà không bọc nháy.
    if yaml is None:
        print("  ! thiếu PyYAML — chỉ kiểm có khối --- ở đầu file, không kiểm cú pháp YAML (pip install pyyaml)")
    bad = []
    fm_files = (list((ROOT / ".claude/agents").glob("*.md")) + list((ROOT / ".claude/commands").glob("*.md"))
                + list((ROOT / ".claude/skills").glob("*/SKILL.md")))
    for p in sorted(fm_files):
        m = re.match(r"^---\r?\n(.*?)\r?\n---", p.read_text(encoding="utf-8"), re.S)
        try:
            if not m or not isinstance(yaml.safe_load(m.group(1)) if yaml else {}, dict):
                bad.append(p.parent.name if p.name == "SKILL.md" else p.stem)
        except Exception:      # YAMLError khi có PyYAML
            bad.append(p.parent.name if p.name == "SKILL.md" else p.stem)
    check(not bad, f"frontmatter agent/command/skill parse được YAML ({len(fm_files)} file)"
          + (f" — HỎNG: {', '.join(bad)} (bọc description trong \"…\")" if bad else ""))

    stacks = {"stack-spring-boot", "stack-nextjs", "stack-bff", "stack-flutter", "stack-electron"}
    have_sk = {p.name for p in (ROOT / ".claude/skills").glob("*") if p.is_dir()}
    check(stacks <= have_sk, f"{len(stacks)} stack skill đủ ({len(stacks & have_sk)}/{len(stacks)})")
    check(len(have_sk) >= 20, f"skill library ({len(have_sk)} skill — ref/review/method chắt lọc)")

    # 5. file khung
    for f in ("CLAUDE.md", "PROTOCOL.md", "STATE.md", "Makefile", ".gitignore"):
        check((ROOT / f).exists(), f"{f} tồn tại")

    # 6. templates gom 1 folder (docs/ + knowledge-base/ chỉ file thật)
    tpls = list((ROOT / "templates").glob("TEMPLATE.*.md"))
    check(len(tpls) >= 16, f"templates/ đủ ({len(tpls)} template) + README")
    stray = list((ROOT / "docs").rglob("TEMPLATE.*")) + list((ROOT / "knowledge-base").glob("TEMPLATE.*"))
    check(not stray, f"docs/ + knowledge-base/ không còn TEMPLATE lạc ({len(stray)} sót)")

    # 7. công cụ máy (CẢNH BÁO, không tính FAIL — khung vẫn đúng; thiếu thì BUILD không chạy được make/proof)
    import shutil
    need = {"make": "Windows: `winget install ezwinports.make` · macOS: `xcode-select --install` · Linux: `apt install make`",
            "sh": "Windows: cài Git for Windows, chạy trong Git Bash",
            "docker": "cài Docker Desktop / Docker Engine"}
    for tool, hint in need.items():
        if not shutil.which(tool):
            print(f"  ! thiếu `{tool}` — {hint} (README §Yêu cầu máy)")

    print(f"\n{'PASS — smoke sạch' if ok else 'FAIL — có mục gãy'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
