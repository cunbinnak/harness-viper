# templates/ — mẫu tài liệu (gom 1 folder)

> Mọi `TEMPLATE.*` gom về đây → `docs/` + `knowledge-base/` chỉ chứa file THẬT (đang sống).
> **Cách dùng**: copy template → path đích bên dưới · xoá comment `<!-- -->` (guidance) · điền hết `{{...}}`.
> `gate.py` **không quét** folder này (ngoài phạm vi chấm; template giữ `{{...}}` là hợp lệ).

| Template | Copy sang | Khi (DOCUMENT) |
|---|---|---|
| `TEMPLATE.interview.md` | `docs/INTERVIEW.md` | Bước 1 |
| `TEMPLATE.prd.md` | `docs/PRD.md` | Bước 2 |
| `TEMPLATE.personas.md` | `docs/PERSONAS.md` | Bước 3 |
| `TEMPLATE.capabilities-map.md` | `docs/CAPABILITIES-MAP.md` | Bước 4 |
| `TEMPLATE.feat.md` | `docs/feat/FEAT-<slug>.md` | Bước 5 (mỗi FEAT) |
| `TEMPLATE.overview.md` | `docs/arch/OVERVIEW.md` | Bước 6 |
| `TEMPLATE.arch.md` | `docs/arch/<name>.md` | Bước 6 (mỗi target) |
| `TEMPLATE.adr.md` | `docs/adr/ADR-NNNN-<slug>.md` | Bước 6 (mỗi ADR) |
| `TEMPLATE.techstack.md` | `docs/TECHSTACK.md` | Bước 7 |
| `TEMPLATE.design-system.md` | `docs/DESIGN-SYSTEM.md` | Bước 8 (có UI) |
| `TEMPLATE.screen-map.md` | `docs/ux/SCREEN-MAP.md` | Bước 8 |
| `TEMPLATE.roadmap.md` | `docs/ROADMAP.md` | Bước 9 |
| `TEMPLATE.decisions.md` | `docs/DECISIONS.md` | xuyên suốt |
| `TEMPLATE.backward-compat.md` | `docs/BACKWARD-COMPAT.md` | SHIP (wave ≥2) |
| `TEMPLATE.production-ready.md` | `docs/PRODUCTION-READY.md` | SHIP |
| `TEMPLATE.kg.md` | `knowledge-base/<name>.md` | plan skeleton → BUILD/VERIFY điền |
