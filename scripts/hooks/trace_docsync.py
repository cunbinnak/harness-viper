#!/usr/bin/env python3
"""trace_docsync — PostToolUse: sửa spec doc ở pha DOCUMENT → NHẮC cascade + re-trace (PROTOCOL §8).

Vấn đề: khi Authority đọc lại rồi bảo "thêm thông tin X vào FEAT", agent point-edit đúng FEAT nhưng
QUÊN propagate sang arch data model / §3 API / mockup → doc lệch nhau, lọt tới BUILD. Văn xuôi dặn thì
sau compact trôi. Hook này biến thành TRIGGER: mỗi lần Edit spec doc ở DOCUMENT → nhắc chạy propagation
+ trace 6 chiều. **Hook KHÔNG tự trace** (đó là việc ngữ nghĩa của LLM) — chỉ kích đúng lúc + đúng state.

+ MỘT việc máy làm được: ô `PRE-LOCK AUDIT PASS` đang [x] mà spec doc vừa đổi → audit đó chấm trên
bản CŨ = tick ôi → hook TỰ BỎ TICK trong STATE.md (nhắc thì lơ được, gate đỏ thì không — muốn khoá
scope bắt buộc re-run audit trên bản mới).

CHỈ kích khi: phase == DOCUMENT (kể cả top-up wave sau, khi ô Scope khoá còn tick từ wave trước) + file thuộc
"spec web" liên kết (PRD/PERSONAS/CAPABILITIES/INTERVIEW/feat/arch/ux/DESIGN-SYSTEM). Ngoài đó → im.
+ phase BUILD/VERIFY mà sửa `docs/arch/` (guard_doc cho qua vì `amend-arch`) → nhắc 6 điều kiện PROTOCOL §3, không bỏ tick gì.
Gắn ở PostToolUse `Write|Edit|MultiEdit` (ghi đè cả file — hay gặp ở mockup — cũng phải nhắc). Exit 2 = đưa nhắc lại cho model (tool đã chạy
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
# (DECISIONS/ROADMAP) hay doc framework (CONVENTIONS/SECURITY). INTERVIEW CÓ: bảng luồng + màn nháp +
# business rule của BA là nguồn của AC, API và mockup.
SPEC_HINTS = (
    "docs/feat/", "docs/arch/", "docs/ux/",
    "docs/prd.md", "docs/personas.md", "docs/capabilities-map.md", "docs/design-system.md",
    "docs/interview.md",
)

REMINDER = (
    "[trace_docsync] Vừa sửa spec doc ở pha DOCUMENT: {path}\n"
    "NẾU đây là AMENDMENT (đọc lại → bổ sung/sửa để chốt tài liệu): 1 thay đổi = CASCADE, KHÔNG point-edit.\n"
    "  · field/thông tin mới → FEAT + arch data model + arch §3 API + mockup (+ CAPABILITIES nếu năng lực mới)\n"
    "  · luồng/AC mới       → bảng luồng (Authority ký lại) + màn nháp + FEAT + arch API/events/luồng + mockup màn (+ ROADMAP nếu đổi scope)\n"
    "  · sửa từ MÀN HÌNH, chức năng (thêm cột/lọc/nút/bước) → màn nháp (BA) → AC (BA) → arch §3 API (SA) → mockup + data-api (UX)\n"
    "    — hình thức (chữ/màu/khoảng cách) → chỉ sửa TOKEN ở DESIGN-SYSTEM §2\n"
    "Rồi RE-RUN trace 6 chiều (technical-design §Trọn vẹn) + chiều UI↔AC. Còn tham chiếu treo = CHƯA xong.\n"
    "(Đang authoring lần ĐẦU theo Bước tuần tự → trace đã ở Bước 6; bỏ qua nhắc này.)\n"
)

UNTICKED_NOTE = (
    "[trace_docsync] Ô 'PRE-LOCK AUDIT PASS' (và 'Scope khoá' nếu còn tick) trong STATE.md ĐÃ BỊ BỎ TICK tự động — audit trước đó\n"
    "chấm trên bản doc CŨ, spec vừa đổi thì kết quả đó hết giá trị. Xử xong CASCADE + re-trace thì\n"
    "Tới lời chốt kế của Authority → RE-RUN pre-lock audit (/document Bước 10) rồi mới tick lại. KHÔNG tick chay.\n"
)

AMEND_ARCH = (
    "[trace_docsync] Vừa sửa arch SAU khoá scope: {path} — chỉ hợp lệ nếu là `amend-arch` (PROTOCOL §3), đủ 6 điều kiện:\n"
    "  1. chỉ docs/arch/*.md (AC · mockup · PRD · PERSONAS không đụng)\n"
    "  2. truy về AC/Mã màn đã khoá mà nó phục vụ — không truy được = thiếu hành vi → backlog/Blocker, HOÀN lại sửa\n"
    "  3. chỉ THÊM (cột · field · endpoint · mã lỗi) — không đổi nghĩa/xoá thứ đã có\n"
    "  4. target consumer (`consumes`) cập nhật cùng commit\n"
    "  5. 1 dòng docs/DECISIONS.md loại `amend-arch` (đổi gì · AC nào · vì sao kẹt luồng), cùng commit với code\n"
    "  6. reviewer kiểm ở VERIFY — thiếu điều nào = MAJOR\n"
    "Lệch nhưng KHÔNG kẹt luồng → hoàn lại sửa; code bám arch + DECISIONS `kỹ-thuật` + backlog.\n"
)

PRELOCK_RE = re.compile(r"(-\s*)\[[xX]\](\s*\*\*PRE-LOCK AUDIT PASS)")   # chấp nhận chú thích trong phần in đậm
SCOPE_RE = re.compile(r"(-\s*)\[[xX]\](\s*\*\*Scope khoá)")


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
    # Chỉ xét phase: ngoài DOCUMENT doc đóng băng (guard_doc lo). Ở DOCUMENT thì LUÔN nhắc — kể cả top-up wave sau
    # khi ô Scope khoá còn tick từ wave trước (trước đây hook im lặng đúng lúc hay sửa doc nhất).
    m = re.search(r"Phase hiện tại\s*:\s*([A-Za-z-]+)", state)
    ph = m.group(1).upper().replace(" ", "-") if m else ""
    if ph in ("BUILD", "VERIFY") and "docs/arch/" in low:   # guard_doc đã cho qua → nhắc điều kiện amend-arch
        sys.stderr.write(AMEND_ARCH.format(path=path))
        return 2
    if ph != "DOCUMENT":
        return 0
    sys.stderr.write(REMINDER.format(path=path))
    # PRE-LOCK AUDIT đã tick mà spec vừa đổi → tick ôi → tự bỏ tick (việc cơ học, không phải trace hộ)
    new_state, n = PRELOCK_RE.subn(r"\1[ ]\2", state)
    new_state, n2 = SCOPE_RE.subn(r"\1[ ]\2", new_state)   # khoá cũ cũng hết giá trị khi spec vừa đổi
    n += n2
    if n:
        try:
            (ROOT / "STATE.md").write_text(new_state, encoding="utf-8")
            sys.stderr.write(UNTICKED_NOTE)
        except Exception:
            pass  # fail-open: không ghi được thì thôi, reminder vẫn đã nhắc
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
