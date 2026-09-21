---
name: domain-po
description: Phương pháp Product-Owner cho /document Bước 5 — viết FEAT (BDD AC + ca biên + field kỹ thuật) THẲNG vào docs/feat/. Suy từ tài liệu khám phá, KHÔNG hỏi lại user; mơ hồ → docs/DECISIONS.md.
---

> Phương pháp cho /document (fork gộp DOMAIN/DESIGN/PLAN vào DOCUMENT, 1 lớp doc). Không stage riêng, không translate.

# Product-Owner Method (viết FEAT)

## Khi dùng
Bước 5 (viết FEAT) của `/document` — vai **Product Owner**. Chia sản phẩm nhỏ theo capability, viết **THẲNG** vào **`docs/feat/`** theo `templates/TEMPLATE.feat.md` — AC BDD + field kỹ thuật chung một file. Fork 1 lớp doc: **KHÔNG** viết business VN rồi dịch, **KHÔNG** stage business riêng. **KHÔNG Epic/Journey** (khái niệm harness cũ — gom nhóm đã có frontmatter `capability`; hành trình UI đã có `docs/ux/SCREEN-MAP.md`).

## Output
| Đối tượng | Output |
|---|---|
| Feature (duy nhất) | `docs/feat/FEAT-<slug>.md` — AC BDD + ca biên + §3 field kỹ thuật (enforcement, consumes_contracts) — theo `templates/TEMPLATE.feat.md` |

Neo về nền dự án: `docs/PRD.md`, `docs/PERSONAS.md`, `docs/CAPABILITIES-MAP.md`.

## Boot sequence (targeted — đừng đọc sweeping)
1. `STATE.md` + `PROTOCOL.md`.
2. Nền dự án: `docs/PRD.md` · `docs/PERSONAS.md` (kèm ma trận vai × hành động) · `docs/CAPABILITIES-MAP.md`.
3. Nếu có intake: `intake/*` (marker `NGUỒN: INTAKE` trong `docs/INTERVIEW.md`).
4. FEAT liên quan đã có trong `docs/feat/` (tránh trùng ID).

## Cách viết
- **FEATURE**: frontmatter `capability: CAP-<id>` (truy về CAPABILITIES-MAP — mọi FEAT phải có) + `has_ui` + `outcome_persona` + `demo_signature` (1 câu chứng minh khi xong). **≥4 AC BDD (Cho/Khi/Thì)** phủ happy + validation + error + a11y. **§3 field kỹ thuật**: `enforcement_location` (server/DB — UI disable KHÔNG tính) + `consumes_contracts` trỏ `docs/arch/{name}.md` contract thật. Business-rule gắn feature → ghi ở §3 (enforcement) hoặc ref `docs/adr/` (rule nền — domain-ba viết). §Ngoài phạm vi.

## Cách viết AC BDD tốt (giá trị — giữ nguyên)
- **Cho/Khi/Thì (Given/When/Then)** — mỗi AC 1 hành vi kiểm được, có kết quả quan sát được (không "hệ thống hoạt động đúng").
- Phủ **4 loại tối thiểu**: happy path · validation (input sai) · error/failure · a11y (bàn phím/screen-reader/tương phản khi là UI).
- Ca biên: gửi hai lần · sửa đồng thời · rỗng · quyền thu hồi giữa chừng — nếu FEAT chạm trạng thái thì AC/ca biên phải nói tới, đừng để hở cho lúc code đoán.
- Field kỹ thuật ĐI CÙNG AC trong cùng file (fork 1 lớp): AC business + `consumes_contracts`/ranh giới ngồi chung — không tách business rồi dịch.

## Không hỏi user (fork rule)
`/document` đã phỏng vấn Authority (interview) hoặc đã có `intake/`. Bắt trả lời lại = hỏi hai lần cùng câu.
Thứ tự khi bí: **(1)** tìm trong `PRD`/`PERSONAS`/`CAPABILITIES-MAP`/`INTERVIEW`/`intake` · **(2)** vẫn mơ hồ → ghi 1 dòng `docs/DECISIONS.md` (what/why dẫn về artifact/mục/assume/reversible) rồi đi tiếp · **(3)** tắc cứng thật → `STATE.md §Blocker`, chuyển việc khác, báo gộp cuối lượt · ngoài scope → `docs/ROADMAP.md §backlog`.

## Quy tắc
- ID `FEAT-<slug>`. Cross-ref bằng ID canonical đầy đủ (không rút gọn).
- Field kỹ thuật viết chung file FEAT (fork 1 lớp — KHÔNG có `docs/domain/`, KHÔNG có bước translate).
- Sửa FEAT đã chốt (đã khoá scope) = **wave sau**: `ROADMAP §backlog` → `/next-wave` → `/document` top-up.

## Done
- FEAT đúng cấu trúc + ≥4 AC BDD (happy/validation/error/a11y) + §3 field kỹ thuật + mọi chỗ tự quyết có dòng `DECISIONS.md` → rà bằng lens `business-analysis` (AC testable? BR logical? scope rõ?) → tiếp Bước 6 (`event-storming` → `boundary-charter` → `technical-design`).
