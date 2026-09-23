#!/usr/bin/env python3
"""trace_docsync — PostToolUse: sửa spec doc ở pha DOCUMENT → NHẮC cascade + re-trace (PROTOCOL §8).

Vấn đề: khi Authority đọc lại rồi bảo "thêm thông tin X vào FEAT", agent point-edit đúng FEAT nhưng
QUÊN propagate sang arch data model / §3 API / mockup → doc lệch nhau, lọt tới BUILD. Văn xuôi dặn thì
sau compact trôi. Hook này biến thành TRIGGER: mỗi lần Edit spec doc ở DOCUMENT → nhắc chạy propagation
+ trace 5 chiều. **Hook KHÔNG tự trace** (đó là việc ngữ nghĩa của LLM) — chỉ kích đúng lúc + đúng state.

+ MỘT việc máy làm được: ô `PRE-LOCK AUDIT PASS` đang [x] mà spec doc vừa đổi → audit đó chấm trên
bản CŨ = tick ôi → hook TỰ BỎ TICK trong STATE.md (nhắc thì lơ được, gate đỏ thì không — muốn khoá
scope bắt buộc re-run audit trên bản mới).

CHỈ kích khi: phase == DOCUMENT (scope chưa khoá) + file thuộc "spec web" liên kết (PRD/PERSONAS/
CAPABILITIES/feat/arch/ux/DESIGN-SYSTEM). Ngoài đó → im. Exit 2 = đưa nhắc lại cho model (tool đã chạy
xong, KHÔNG undo). Fail-open (lỗi / không đọc được STATE → exit 0).
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

# "spec web" — các doc liên kết nhau qua đồ thị phụ thuộc (sửa 1 → cascade). KHÔNG gồm sổ sống
# (DECISIONS/ROADMAP) hay doc framework (CONVENTIONS/SECURITY) hay nguồn (INTERVIEW).
SPEC_HINTS = (
    "docs/feat/", "docs/arch/", "docs/ux/",
    "docs/prd.md", "docs/personas.md", "docs/capabilities-map.md", "docs/design-system.md",
)

REMINDER = (
    "[trace_docsync] Vừa sửa spec doc ở pha DOCUMENT: {path}\n"
    "NẾU đây là AMENDMENT (đọc lại → bổ sung/sửa để chốt tài liệu): 1 thay đổi = CASCADE, KHÔNG point-edit.\n"
    "  · field/thông tin mới → FEAT + arch data model + arch §3 API + mockup (+ CAPABILITIES nếu năng lực mới)\n"
    "  · luồng/AC mới       → FEAT + arch API/events/luồng + mockup màn (+ ROADMAP nếu đổi scope)\n"
    "Rồi RE-RUN trace 5 chiều (technical-design §Trọn vẹn) + chiều UI↔AC. Còn tham chiếu treo = CHƯA xong.\n"
    "(Đang authoring lần ĐẦU theo Bước tuần tự → trace đã ở Bước 6; bỏ qua nhắc này.)\n"
)

UNTICKED_NOTE = (
    "[trace_docsync] Ô 'PRE-LOCK AUDIT PASS' trong STATE.md ĐÃ BỊ BỎ TICK tự động — audit trước đó\n"
    "chấm trên bản doc CŨ, spec vừa đổi thì kết quả đó hết giá trị. Xử xong CASCADE + re-trace thì\n"
    "RE-RUN pre-lock audit (spawn pre-mortem + trace 5 chiều) rồi mới tick lại. KHÔNG tick chay.\n"
)

PRELOCK_RE = re.compile(r"(-\s*)\[[xX]\](\s*\*\*PRE-LOCK AUDIT PASS\*\*)")


def main() -> int:
    try:
        data = json.load(sys.stdin)
        path = (data.get("tool_input", {}) or {}).get("file_path") or ""
        low = path.replace("\\", "/").lower()
    except Exception:
        return 0
    if not any(h in low for h in SPEC_HINTS):
        return 0
    try:
        state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    except Exception:
        return 0
    # scope đã khoá → doc đóng băng (guard_doc lo), không nhắc nữa
    if re.search(r"- \[[xX]\]\s*\*\*Scope khoá\*\*", state):
        return 0
    m = re.search(r"Phase hiện tại\s*:\s*([A-Za-z-]+)", state)
    if not m or m.group(1).upper().replace(" ", "-") != "DOCUMENT":
        return 0
    sys.stderr.write(REMINDER.format(path=path))
    # PRE-LOCK AUDIT đã tick mà spec vừa đổi → tick ôi → tự bỏ tick (việc cơ học, không phải trace hộ)
    new_state, n = PRELOCK_RE.subn(r"\1[ ]\2", state)
    if n:
        try:
            (ROOT / "STATE.md").write_text(new_state, encoding="utf-8")
            sys.stderr.write(UNTICKED_NOTE)
        except Exception:
            pass  # fail-open: không ghi được thì thôi, reminder vẫn đã nhắc
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
