---
name: boundary-charter
description: Phương pháp boundary + charter cho /document Bước 6 — identify boundary từ event-storming (OVERVIEW §4) → boundary map (OVERVIEW §1) + KHỞI TẠO charter docs/arch/{name}.md §Mission; technical-design điền chi tiết sau. Target = boundary (cùng tên file). KHÔNG sinh FEAT/BR, KHÔNG đụng PRD.
---

> Phương pháp cho /document Bước 6 (fork gộp discovery vào DOCUMENT). Không phải stage riêng.
> **Thứ tự trong Bước 6**: `event-storming` (OVERVIEW §4) → **`boundary-charter` (bước này)** → `technical-design` (chi tiết per-target).

# Boundary Charter Skill

## Khi load
Phương pháp **boundary + charter** cho `/document` Bước 6. Một việc duy nhất:
**Identify boundary** từ aggregates/domains ở event-storming → boundary map (`docs/arch/OVERVIEW.md §1`) + **KHỞI TẠO** charter per boundary (`docs/arch/{name}.md §0 Mission`; `technical-design` điền chi tiết §1-§6 sau).

> **Target = boundary** trong khung này: backend boundary nằm `services/boundaries/{name}` ↔ cùng tên file `docs/arch/{name}.md`. KHÔNG có file boundary riêng.
> **KHÔNG sinh FEAT/BR** (`domain-po`/`domain-ba` sở hữu — đã viết ở Bước 3/5). **KHÔNG đụng PRD** (viết trọn ở Bước 2); nếu lúc chia boundary **lộ thêm** NFR/out-of-scope → bổ sung `docs/PRD.md §3/§4` (vẫn trong DOCUMENT, chưa khoá scope — hợp lệ) + 1 dòng `DECISIONS.md`.

Input: `docs/PRD.md` + `docs/CAPABILITIES-MAP.md` + `docs/PERSONAS.md` + `docs/feat/FEAT-*` (đã viết ở Bước 5) + event-storming ở `docs/arch/OVERVIEW.md §4`.

## Deliverable
1. **Boundary map trong `docs/arch/OVERVIEW.md §1`** — **≥1 row non-placeholder** (backend boundary / web target): target + mission + owned data + wave + status.
2. **KHỞI TẠO `docs/arch/{name}.md`** cho mỗi target (frontmatter `kind/stack/consumes` — theo `templates/TEMPLATE.arch.md`) — **§0 Mission có content thật**: mission 1 câu + owned data (từ aggregates event-storming) + capabilities exposed/consumed + NON-NEGOTIABLES. *(Chi tiết §1-§6: `technical-design` điền tiếp — không giẫm.)*

## Phương pháp
1. **Boundary identification**: group aggregates (`docs/arch/OVERVIEW.md §4` Event Storming) chia sẻ data/lifecycle → 1 boundary. Mỗi boundary owns data duy nhất (no overlap — verify qua boundary map).
2. **Mission**: 1 câu "what & why" từ capability-map.
3. **Owned data / capabilities**: từ aggregates event-storming + capability-map.
4. **NON-NEGOTIABLES**: hỏi Architecture Authority (AskUserQuestion — đang ở DOCUMENT, được hỏi).

## Quy tắc
- KHÔNG invent capability/boundary ngoài những gì đã khám phá — refer back các bước trước (khai thác ý tưởng / capability / event-storming).
- 1 lượt có thể tạo nhiều boundary charter (identification), nhưng giữ data ownership không overlap.
- KHÔNG tạo `knowledge-base/*` (KG do BUILD/next-wave sinh sau).
- Idempotent re-run.

## Sau boundary-charter
`/document` Bước 6 tiếp sang `technical-design`: điền chi tiết `docs/arch/{name}.md` (§1 data · §2 luồng · §3 API · §4 kiến trúc/ranh giới · §5 events · §6 ca biên) per target → Bước 7 TECHSTACK → … → Bước 10 challenge → khoá scope.

## Quality checklist
- [ ] Boundary map ≥1 row non-placeholder (OVERVIEW §1).
- [ ] Mỗi boundary có `docs/arch/{name}.md` §Mission thật + owned data không overlap.
- [ ] KHÔNG sinh FEAT/BR (domain-po/ba sở hữu) · KHÔNG viết lại PRD (chỉ bổ sung §3/§4 nếu lộ thêm, kèm DECISIONS).

## Rà chéo trước khi rời bước

Đây là chỗ khép lại phần chia hệ, nên gánh lượt **rà chéo toàn lớp** mà từng bước riêng lẻ không thấy: vision ↔ capability ↔ persona ↔ ma trận quyền ↔ event-storming ↔ boundary. Lệch chỗ nào sửa trước, đừng đẩy sang cho Authority phát hiện hộ.

Chỗ đã tự quyết → trỏ `docs/DECISIONS.md`; chỗ không chắc nhất → nêu rõ khi trình Authority ở **Bước cuối `/document`** (Authority đọc toàn bộ doc set rồi mới ký khoá scope — không ký lẻ ở đây).

Vì sao rà kỹ ở đây: design + wave đều xây trên phần chia hệ này. Tìm ra lỗ ở boundary lúc đã dựng tầng trên nghĩa là tháo ngược nhiều tầng.

## Done
- Boundary map (OVERVIEW §1) + charter khởi tạo (`arch/{name}.md` §Mission/owned-data) đầy đủ, không overlap → tiếp `technical-design` trong Bước 6.
