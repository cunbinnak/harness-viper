---
description: DOCUMENT — interview|intake → doc set (PRD/PERSONAS/FEAT/ARCHITECTURE/UX) → chia wave → khoá scope
---
# /document — Phase DOCUMENT

> Đây là chỗ **DUY NHẤT được hỏi Authority**. Cuối phase = **KHOÁ SCOPE**, từ đó im lặng (BUILD trở đi tự quyết).
> Gọi lại = chạy tiếp từ chốt đang dở. Gọi **sau `/next-wave`** = *top-up* (bổ sung doc + chia lại kế hoạch),
> đọc `docs/ROADMAP.md §backlog` trước — phần bù chen vào wave kế, KHÔNG sửa doc wave đã ship (`archive/`).

**Việc ĐẦU TIÊN**: sửa `STATE.md` → `Phase hiện tại: DOCUMENT` (nếu đang ở phase khác = back-edge top-up).
`gate.py` + `guard_ask` đọc dòng này — không sửa thì máy tưởng còn phase cũ.

## Bước 0 — Nhận diện đường vào
- `intake/` có tài liệu đã điền thật (không phải template `_*.md` trơ)? → **ĐƯỜNG INTAKE**: ghi marker
  `NGUỒN: INTAKE` (ngoài comment) vào `docs/INTERVIEW.md`.
- Không → **ĐƯỜNG INTERVIEW**.
Ghi kết quả vào `STATE.md` dòng `Đường vào`.

## Bước 1 — Nạp nguyên liệu (rẽ nhánh theo đường vào)
- **INTERVIEW**: phỏng vấn Authority — hỏi tới khi đủ dựng PRD/persona/capability (không trần số câu; đây là
  chỗ được hỏi). Kết tinh vào `docs/INTERVIEW.md`, mỗi mục có dòng `Bằng chứng:`.
- **INTAKE**: đọc `intake/*.md` — **KHÔNG phỏng vấn lại**. Dịch/render sang doc set bên dưới, lập **bảng truy
  vết** `intake → FEAT` trong `docs/INTERVIEW.md`. `intake/TECHSTACK` **thắng** default của stack skill.

## Bước 2 — PRD (`docs/PRD.md`)
Vấn đề (pain) + đối tượng cụ thể + **out-of-scope tường minh** + ≥1 success metric **có số**.

## Bước 3 — PERSONAS (`docs/PERSONAS.md`)
Persona + năng lực được cấp + **ma trận vai × hành động** — mỗi ô `có`/`cấm`, **KHÔNG ô trống**
(đây là spec phân quyền khi code + nguồn TC âm khi test + danh sách phép thử của vai `breaker` ở dogfood).

## Bước 4 — CAPABILITIES-MAP (`docs/CAPABILITIES-MAP.md`)
`capability → outcome → FEAT`. **Mọi FEAT truy về ≥1 capability**; capability TRƯỚC feature. Cột `Wave giao` để trống (điền ở Bước 9).

nhu

## Bước 7 — TECHSTACK (`docs/TECHSTACK.md`)
Chốt stack (khớp skill `stack-<tên>`) + **1 dòng lý do** ở `docs/DECISIONS.md`. INTAKE: giữ đúng lựa chọn của intake.

## Bước 7b — Quy ước chung  *(đã có sẵn — framework default, KHÔNG author lại)*
`docs/CONVENTIONS.md` + `docs/SECURITY.md` là **doc framework cố định**. Chỉ **rà + chỉnh §API error-envelope/header/versioning**
nếu project khác default → sửa thẳng file + ghi `DECISIONS.md`.
- Contract **CỤ THỂ** từng target (endpoints) → `arch/<name>.md §3 API`; FE khai `consumes_contracts` trong FEAT;
  đồng bộ bằng **contract-test** (VERIFY) + **BACKWARD-COMPAT** (SHIP). (Skill `stack-*` lo idiom CODE.)

## Bước 8 — Design system + UX  *(nếu có UI; backend-only → ghi marker `KHÔNG CÓ UI`, bỏ qua bước này)*
Thứ tự bắt buộc: `docs/DESIGN-SYSTEM.md` (token — **khoá TRƯỚC**) → `docs/ux/SCREEN-MAP.md` (mục lục màn ↔
boundary ↔ FEAT) → `docs/ux/mockups/<exp>/*.html` (dựng **từ token đã chốt**, mọi màn khai ở SCREEN-MAP) →
**Authority chốt** mockup. Token là thứ **DUY NHẤT chép nguyên** sang code ở BUILD.

## Bước 9 — Chia wave (`docs/ROADMAP.md`)
Bảng wave: mỗi wave khai **target** (boundary/experience) + **phases chạy** (`BUILD,VERIFY[,SHIP]`) + **AC in-scope**.
**AC-cap**: mỗi wave đủ nhỏ để **một phiên BUILD của MAIN làm nổi** (MAIN-code-hết, không dev-agent). Điền cột
`Wave giao` ở CAPABILITIES-MAP. Để trống `§backlog` (amendment tương lai đổ vào đây).

## Bước 10 — Challenge DOCUMENT (luật #8 — tới khi hiểu ĐÚNG Ý AUTHOR)
Tự ra **≥3 câu hỏi khó nhất**, trả lời **CHỈ bằng tài liệu vừa viết**. Câu nào phải đoán = **một lỗ tài liệu** →
vá (INTERVIEW: **hỏi Authority thêm** · INTAKE: dịch lại + vá lỗ). **Lặp tới khi tài liệu trả lời được HẾT và
phản ánh ĐÚNG ý Author** (không còn chỗ đoán, không còn lệch ý) — **không giới hạn số vòng**. **PASS** mới đi tiếp.
Ghi mỗi vòng vào `STATE.md §Challenge log`.

## Bước cuối — Chốt + khoá scope
1. `python scripts/gate.py` (phase DOCUMENT) phải **xanh**.
2. ≥2 dòng `docs/DECISIONS.md`.
3. **Trình Authority đọc** toàn bộ doc set → OK = duyệt.
4. Tick hết gate DOCUMENT + `Scope khoá` trong `STATE.md`. **Từ đây không hỏi Authority nữa.**
5. Báo: tài liệu xong, chạy `/build <wave-1>` để vào wave đầu.

## Ranh giới
- **Không viết code** ở phase này. Không dựng `services/`.
- INTAKE: **không tự đẻ target** ngoài `intake/ARCHITECTURE`, **không đổi** lựa chọn intake cho hợp default skill.
- Không bỏ qua challenge cho nhanh — cái giá trả ở BUILD/dogfood.
- Không khoá scope khi Authority chưa đọc + chưa tick `Scope khoá`.
