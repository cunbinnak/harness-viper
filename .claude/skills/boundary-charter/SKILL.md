---
name: boundary-charter
description: Phương pháp boundary + charter cho /document — identify boundary từ event-storming → boundary map + charter per boundary (vào docs/arch/OVERVIEW.md + docs/arch/{name}.md), RỒI tổng hợp PRD (scope/NFR/security/metrics). KHÔNG sinh FEAT (domain-po/ba sở hữu).
---

> Phương pháp cho /document (fork gộp discovery vào DOCUMENT). Không phải stage riêng.

# Boundary Charter Skill

## Khi load
Phương pháp **boundary + charter** cho `/document` (Architecture Authority). Vai trò kép:
1. **Identify boundary** từ aggregates/domains ở event-storming → boundary map (`docs/arch/OVERVIEW.md`) + charter per boundary (`docs/arch/{name}.md`).
2. **Tổng hợp PRD** (`docs/PRD.md`) — scope + NFR + security + metrics.

> **KHÔNG sinh FEAT/Epic/BR ở đây**: phương pháp `domain-po`/`domain-ba` (cùng trong `/document`) sở hữu product — viết Epic/Feature/Journey (BDD AC) thẳng vào `docs/feat/` + Business-rule/Persona. Bước này chỉ boundary map + charter + tổng hợp PRD.

Input: `docs/PRD.md` (vision/problem) + `docs/CAPABILITIES-MAP.md` + `docs/PERSONAS.md` + section event-storming trong `docs/arch/OVERVIEW.md`.

## Deliverable
1. **Boundary map trong `docs/arch/OVERVIEW.md`** — **≥1 row non-placeholder** (backend boundary / web experience): boundary + mission + owned data + wave + status.
2. **`docs/arch/{boundary}.md`** cho mỗi boundary (frontmatter `kind/stack/consumes`) — **§Mission có content thật**; owned data (từ aggregates event-storming); capabilities exposed/consumed; NON-NEGOTIABLES.
3. **`docs/PRD.md`** — tổng hợp từ vision/problem (đã có) + capability (scope) + event-storming: scope in/out + **NFR có số** + security/compliance + success metrics + glossary.

## Phương pháp (identify + tổng hợp)
1. **Boundary identification**: group aggregates (event-storming §5) chia sẻ data/lifecycle → 1 boundary. Mỗi boundary owns data duy nhất (no overlap — verify qua boundary map).
2. **Mission**: 1 câu "what & why" từ capability-map.
3. **Owned data / capabilities**: từ aggregates event-storming + capability-map.
4. **NON-NEGOTIABLES**: hỏi Architecture Authority (AskUserQuestion).
5. **Tổng hợp PRD**: gộp vision + capability + event-storming thành scope/NFR-số/security/metrics/glossary trong `docs/PRD.md`. KHÔNG bịa số NFR — hỏi user nếu chưa rõ.

## Quy tắc
- KHÔNG invent capability/boundary ngoài những gì đã khám phá — refer back các bước trước (khai thác ý tưởng / capability / event-storming).
- 1 lượt có thể tạo nhiều boundary charter (identification), nhưng giữ data ownership không overlap.
- KHÔNG tạo `knowledge-base/*` (KG do BUILD/next-wave sinh sau).
- Idempotent re-run.

## Sau boundary-charter
Sau bước này, `/document` tiếp sang author product: `domain-po`/`domain-ba` viết Epic/Feature/Journey + Business-rule/Persona vào `docs/feat/` (suy từ tài liệu khám phá, mơ hồ → `docs/DECISIONS.md`), rồi chia wave (`docs/ROADMAP.md`) → **khoá scope** (1 lần cho dự án) → `/build 1`.

## Quality checklist
- [ ] Boundary map ≥1 row non-placeholder.
- [ ] Mỗi boundary có `docs/arch/{name}.md` §Mission thật + owned data không overlap.
- [ ] `docs/PRD.md` có scope + NFR số + security/compliance + glossary.
- [ ] KHÔNG sinh FEAT/Epic/BR (để domain-po/ba).

## Chốt — user ĐỌC và ĐÁNH GIÁ rồi mới ký

Đây là artifact khép lại phần khám phá, nên nó gánh thêm lượt **rà chéo toàn lớp** mà từng bước riêng lẻ không thấy: vision ↔ capability ↔ persona ↔ ma trận quyền ↔ event-storming ↔ boundary ↔ PRD. Lệch chỗ nào sửa trước, đừng đẩy sang cho user phát hiện hộ.

Rồi **DỪNG LẠI**: trình danh sách file kèm *mỗi file nên soi gì*, nói rõ chỗ đã tự quyết (trỏ `docs/DECISIONS.md`) và chỗ mình không chắc nhất. **KHÔNG tự ký, KHÔNG chạy tiếp.**

User góp ý → sửa → rà lại → trình lại. User **duyệt** → khoá scope (trong `/document`) → complete.

Vì sao rà kỹ ở đây: FEAT + design + wave đều xây trên phần khám phá này. Tìm ra lỗ ở vision/boundary lúc đã dựng tầng trên nghĩa là tháo ngược nhiều tầng.

## Done
- Boundary map + charter + `docs/PRD.md` đầy đủ; user confirm → tiếp author product (domain-po/ba) trong `/document`.
