#!/usr/bin/env python3
"""guard_doc — chặn Write/Edit vào SPEC doc đã khoá scope (ngoài phase DOCUMENT).

Sau khoá scope (BUILD/VERIFY/SHIP/NEXT-WAVE) doc spec ĐÓNG BĂNG: vấn đề dồn sang wave sau
(`docs/ROADMAP.md §backlog` → `/next-wave` → `/document` top-up = re-lock). Không "vừa code vừa vặn
doc" — giữ hợp đồng ổn định cho review/dogfood đánh.

CHO SỬA lúc BUILD (sổ SỐNG, append): DECISIONS.md · ROADMAP.md (§backlog + tick tiến độ) ·
BACKWARD-COMPAT.md · PRODUCTION-READY.md. Ngoài `docs/` (services/ · knowledge-base/ · tracking/ · STATE)
không đụng. Phase DOCUMENT (author + top-up) → cho sửa mọi doc.
Ngoại lệ `amend-arch` (PROTOCOL §3): `docs/arch/*.md` ở BUILD/VERIFY cho qua — hook không xét được ngữ nghĩa
(kẹt luồng? truy về AC? chỉ thêm?) → `trace_docsync` nhắc 6 điều kiện sau khi ghi, reviewer kiểm ở VERIFY.

PreToolUse(Write|Edit|MultiEdit): exit 2 nếu spec doc + phase != DOCUMENT. Fail-open.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROOT_S = str(ROOT).replace("\\", "/")
LIVING = {"DECISIONS.md", "ROADMAP.md", "BACKWARD-COMPAT.md", "PRODUCTION-READY.md"}

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def rel(path: str) -> str:
    """Đường dẫn tính từ gốc repo (so không phân biệt hoa thường — Windows `d:` vs `D:`). Ngoài repo → ""."""
    if path.lower().startswith(ROOT_S.lower() + "/"):
        return path[len(ROOT_S) + 1:]
    return "" if re.match(r"^([a-zA-Z]:)?/", path) else path.removeprefix("./")


def phase() -> str:
    try:
        t = (ROOT / "STATE.md").read_text(encoding="utf-8")
    except OSError:
        return ""
    m = re.search(r"Phase hiện tại\s*:\s*([A-Za-z-]+)", t)
    return m.group(1).upper().replace(" ", "-") if m else ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
        fp = str((data.get("tool_input") or {}).get("file_path", "")).replace("\\", "/")
    except Exception:
        return 0  # fail-open
    fp = rel(fp)
    if not fp.startswith("docs/"):        # chỉ canh docs/ ở gốc repo — không chặn nhầm services/**/docs/
        return 0
    if fp.rsplit("/", 1)[-1] in LIVING:   # sổ sống — luôn cho append
        return 0
    p = phase()
    if p in ("", "DOCUMENT"):             # DOCUMENT author/top-up → cho sửa
        return 0
    if p in ("BUILD", "VERIFY") and fp.startswith("docs/arch/") and fp.endswith(".md"):
        return 0                          # amend-arch (PROTOCOL §3) — trace_docsync nhắc điều kiện
    sys.stderr.write(
        f"[guard_doc] Pha {p}: doc SPEC đã KHOÁ — không sửa lúc BUILD/VERIFY.\n"
        "Thiếu/lệch → `docs/ROADMAP.md §backlog` → wave sau `/document` top-up (re-lock). "
        "Mơ hồ trong AC → `docs/DECISIONS.md` (được sửa).\n"
        "Chỉ `docs/arch/*.md` được bổ sung tại chỗ khi thiếu/sai kỹ thuật làm KẸT luồng của AC đã khoá "
        "(`amend-arch`, 6 điều kiện PROTOCOL §3). AC · mockup · PRD · PERSONAS thì không.\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
