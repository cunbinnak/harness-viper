#!/usr/bin/env python3
"""guard_bc — canh deploy production. PROTOCOL §8.

PreToolUse(Bash): lệnh `make … deploy` (mọi biến thể: `make deploy` · `make -s deploy` · `make -C services/x deploy`):
- Thiếu docs/PRODUCTION-READY.md, hoặc còn mục chưa tick (trừ mục `(sau deploy)` — tick sau khi deploy) → exit 2.
- Wave ≥2: thiếu docs/BACKWARD-COMPAT.md (hoặc thiếu §3), hoặc §3 còn `- [ ]` → exit 2. Thiếu sổ KHÔNG được coi là xanh.
- Còn lại → buộc HỎI Authority (permissionDecision `ask`) — deploy = ra ngoài, không đảo ngược.
`docker compose up` (local) KHÔNG phải deploy → cho qua. Fail-open khi không đọc được input.
Chỉ lệnh GỌI chương trình thật (đầu một đoạn lệnh, kể cả sau env/sudo/time hay trong sh -c) mới bị canh; chữ nằm
trong chuỗi, heredoc hay commit message thì bỏ qua — không hỏi/chặn nhầm công việc bình thường.
"""
import json
import re
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEPLOY = re.compile(r"\bmake\b[^;&|\n]*\bdeploy\b")

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


SHELLS = ("sh", "bash", "zsh", "dash")


def split_commands(cmd: str) -> list[str]:
    """Tách lệnh ghép theo `&&` `||` `;` `|` và xuống dòng — KHÔNG tách bên trong dấu nháy."""
    segs, cur, quote, i = [], [], "", 0
    while i < len(cmd):
        c = cmd[i]
        if quote:
            cur.append(c)
            if c == quote:
                quote = ""
            elif c == "\\" and quote == '"' and i + 1 < len(cmd):
                i += 1
                cur.append(cmd[i])
        elif c in "\"'":
            quote = c
            cur.append(c)
        elif c == "\\" and i + 1 < len(cmd):
            cur.append(c)
            i += 1
            cur.append(cmd[i])
        elif c in ";\n|" or cmd[i:i + 2] == "&&":
            segs.append("".join(cur))
            cur = []
            if cmd[i:i + 2] in ("&&", "||"):
                i += 1
        else:
            cur.append(c)
        i += 1
    segs.append("".join(cur))
    return segs


def real_invocation(cmd: str) -> bool:
    """Lệnh GỌI chương trình make thật với đích cần canh (đầu một đoạn lệnh, kể cả sau env/sudo/time hay trong sh -c).
    Chữ nằm trong chuỗi, heredoc hay commit message KHÔNG tính."""
    for seg in split_commands(cmd):
        try:
            toks = shlex.split(seg, posix=False)
        except ValueError:          # nháy không cân: đây là mảnh chữ, không phải một lệnh hoàn chỉnh
            continue
        while toks and (toks[0] in ("env", "sudo", "time", "command", "nice", "exec") or re.match(r"^\w+=", toks[0])):
            toks = toks[1:]
        if not toks:
            continue
        prog = toks[0].strip("\"'").replace("\\", "/").rsplit("/", 1)[-1]
        if prog in SHELLS and "-c" in toks[1:]:
            idx = toks.index("-c") + 1
            inner = toks[idx].strip("\"'") if idx < len(toks) else ""
            if inner and inner != cmd and real_invocation(inner):
                return True
            continue
        is_make = re.fullmatch(r"g?make(\.exe)?", prog) is not None
        if is_make and "deploy" in [t.strip("\"'") for t in toks[1:]]:
            return True
    return False


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
    if not real_invocation(cmd):
        return 0          # chỉ là chữ nằm trong chuỗi/heredoc/commit message — không phải lệnh deploy thật
    why = []
    if not (ROOT / "docs" / "PRODUCTION-READY.md").exists():
        why.append("chưa có docs/PRODUCTION-READY.md — checklist SHIP chưa lập, không có gì để kiểm trước khi deploy")
    todo = [ln.strip() for ln in read("docs/PRODUCTION-READY.md").splitlines()
            if re.match(r"\s*- \[ \]", ln) and "(sau deploy)" not in ln]
    if todo:
        why.append(f"PRODUCTION-READY còn {len(todo)} mục chưa xanh (trừ mục sau deploy): {todo[0][:80]}")
    wm = re.search(r"Wave\s*:\s*(\d+)", read("STATE.md"))
    sec3 = re.search(r"## §3.*?(?=^##\s|\Z)", read("docs/BACKWARD-COMPAT.md"), flags=re.DOTALL | re.MULTILINE)
    if wm and int(wm.group(1)) >= 2:
        if not (ROOT / "docs" / "BACKWARD-COMPAT.md").exists():
            why.append("chưa có docs/BACKWARD-COMPAT.md — wave ≥2 phải có sổ hợp đồng trước khi deploy")
        elif not sec3:
            why.append("docs/BACKWARD-COMPAT.md thiếu mục §3 (checklist rà tương thích)")
        elif re.search(r"- \[ \]", sec3.group(0)):
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
