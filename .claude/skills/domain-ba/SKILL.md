---
name: domain-ba
description: Phương pháp Business-Analyst cho /document Bước 3 — viết Persona + ma trận vai×hành động (docs/PERSONAS.md) + Business-rule (FEAT §3 field kỹ thuật hoặc docs/adr). Suy từ tài liệu khám phá, KHÔNG hỏi lại user; mơ hồ → docs/DECISIONS.md.
---

> Phương pháp cho /document (fork gộp DOMAIN/DESIGN/PLAN vào DOCUMENT, 1 lớp doc). Không stage riêng, không translate.

# Business-Analyst Method (Business-rule + Persona)

## Khi dùng
Bước phân tích nghiệp vụ của `/document` — vai **Business Analyst**. Viết **THẲNG** vào 1 lớp doc:
- **Business-rule** = ràng buộc nghiệp vụ → ghi vào **FEAT `docs/feat/*` §3 Field kỹ thuật** (dòng rule + `enforcement_location`) khi rule gắn 1-2 feature; rule nền/cross-cutting → **`docs/adr/`** (ADR).
- **Persona** = chi tiết hóa persona → **`docs/PERSONAS.md`** (+ ma trận vai × hành động).

> Wireframe/UI KHÔNG thuộc method này — đó là UX: `docs/ux/` + `docs/DESIGN-SYSTEM.md`.

## Output
| Đối tượng | Output |
|---|---|
| Business-rule | FEAT `docs/feat/FEAT-*.md` §3 Field kỹ thuật (gắn 1-2 feat — dòng rule + enforcement) · hoặc `docs/adr/ADR-NNN-*.md` (rule nền/cross-cutting) |
| Persona | `docs/PERSONAS.md` §persona + §ma trận vai × hành động |

## Boot sequence (targeted — Bước 3: CAPABILITIES-MAP/FEAT CHƯA tồn tại, đừng tìm)
1. `STATE.md` + `PROTOCOL.md`.
2. `docs/PRD.md` + `docs/INTERVIEW.md` (nguồn khám phá — persona/quyền moi từ đây).
3. Nếu có intake: `intake/*`.
4. *(BR gắn feature: FEAT viết ở Bước 5 — rule nào gắn 1-2 feature thì ghi nháp, điền vào FEAT §3 khi Bước 5 chạy; rule nền → `docs/adr/` ngay.)*

## Cách viết
- **Business-rule**: §Phát biểu (1 câu rõ) + §Lý do (**reference nguồn**: luật/policy/contract/quyết định — KHÔNG "best practice") + §Khi nào áp dụng + §Ngoại lệ + §Hệ quả + **≥2 ví dụ** (1 happy + 1 vi phạm, số liệu — QC seed test) + `severity` CORNERSTONE/NORMAL + **`related_features` ≥1** (rule chỉ 1 FEAT → đáng lẽ là AC, đưa thành AC trong FEAT đó). §**Enforce ở đâu** trỏ nơi CHẶN được (unique index · cột `version` · idempotency key · DB constraint · state machine) — viết chung file với contract (fork 1 lớp, không TODO-engineer để dịch sau).
- **PERSONA**: role/goals/pains/workflow narrative. **Anti-persona BẮT BUỘC**. Cập nhật ma trận vai × hành động (ai được/cấm làm gì) trong `docs/PERSONAS.md §2`.

## Không hỏi user (fork rule)
`/document` đã phỏng vấn Authority hoặc có `intake/`. Thứ tự khi bí: **(1)** tìm trong `PRD`/`PERSONAS`/`CAPABILITIES-MAP`/`INTERVIEW`/`intake` · **(2)** mơ hồ → 1 dòng `docs/DECISIONS.md` (what/why dẫn về artifact/assume/reversible) · **(3)** tắc cứng → `STATE.md §Blocker` · ngoài scope → `docs/ROADMAP.md §backlog`.

## Quy tắc
- ID `BR-<slug>` (nếu tách rule) / persona đặt trong `PERSONAS.md`. Cross-ref bằng ID canonical đầy đủ.
- Enforce viết chung file với contract (fork 1 lớp — KHÔNG `docs/domain/`, KHÔNG bước translate/TODO-engineer).
- Sửa doc đã chốt = **wave sau** (`ROADMAP §backlog` → `/next-wave` → `/document` top-up).

## Done
- Business-rule (≥2 ví dụ + nguồn + Enforce ở đâu) đặt đúng chỗ (FEAT §3 hoặc ADR) + Persona + ma trận vai × hành động trong `PERSONAS.md` + mọi chỗ tự quyết có dòng `DECISIONS.md` → tiếp Bước 4 `capability-mapping` (đọc PERSONAS vừa viết).
