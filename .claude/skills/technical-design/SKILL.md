---
name: technical-design
description: Phương pháp Architecture cho /document — boundary decomposition + kind/stack, ADR (docs/adr), HLD/API/data-model/events per target vào docs/arch/{name}.md + docs/arch/OVERVIEW.md, integrations, docker-compose skeleton. UX/UI là bước riêng (kind web/mobile).
---

> Phương pháp cho /document (fork gộp DOMAIN/DESIGN/PLAN vào DOCUMENT, 1 lớp doc). Không stage riêng, không translate.

# Architecture Method (bước ARCHITECTURE của /document)

## Khi dùng
Bước ARCHITECTURE của `/document` — vai **solution architect**. Sau khi FEAT (`docs/feat/`) + nền dự án (`docs/PRD.md`/`PERSONAS.md`/`CAPABILITIES-MAP.md`) đủ.
Input: `docs/PRD.md` + `docs/feat/*` (AC + business-rule + field kỹ thuật) + `docs/CAPABILITIES-MAP.md`.

> Đây là **DESIGN docs**, không scaffold code. Scaffold code (`services/{name}/`) xảy ra ở `/build`, KHÔNG ở đây.

## Deliverable
1. **ADR** `docs/adr/ADR-NNN-*.md` — theo chủ đề (tech-stack, backend-architecture [Layered/Hexagonal], auth, **api-error-convention [envelope + generic codes chung]**, **ui-kit [có FE target → chốt component library trưởng thành; React → Ant Design 5, mockup mô phỏng visual language của nó, dev dùng thật, token map qua theme]**, event/messaging…). Theo `docs/TEMPLATE.decisions.md`/ADR: context · decision · **Alternatives considered ≥2 (lý do reject)** · consequences.
2. **Boundary decomposition** — chốt các **target**: mỗi target + **kind** (`backend`/`bff`/`web`/`mobile`) + **stack** (set tại đây, vd Java 21 + Spring Boot 3.4). Ghi nhận **tech situational per-target** (phát/nhận event, dùng cache/lock, external đặc thù) — input cho bước chia wave gắn `ref_skills`.
3. **`docs/arch/OVERVIEW.md`** — bức tranh tổng: danh sách target + kind/stack + quan hệ (ai gọi ai, depends_on), luồng E2E chính, cross-cutting chung.
4. **Per target** — `docs/arch/{name}.md` (frontmatter `kind`/`stack`/`consumes`), gộp mọi mặt của target đó vào MỘT file:
   - **§HLD** — design goals + responsibilities/non-responsibilities · data ownership (no FK) · C4 (context/container/component) + **CHỐT kiến trúc target (Layered/Hexagonal) + layer/package** · integration summary · key flows (happy + critical error) · auth & permission · consistency & transaction *(nếu multi-write/event)* · failure & resilience *(nếu outbound)* · deployment & scaling · observability · NFR. Layout file/folder → `ref-{kind}-pattern`.
   - **§API (contract)** — REST/OpenAPI 3.1 / GraphQL + **Domain error code catalog** (→ `{Domain}ErrorEnum`; map mỗi business-rule / invalid-state transition → 1 code). Common error envelope + generic codes (400/401/403/404/409/429/500) **GIỐNG NHAU mọi target** (chuẩn chung); per-endpoint Errors chỉ **ref** code trong catalog. `kind=bff` aggregation ≥2 backend → thêm §BFF-aggregation (DataLoader/N+1, timeout cascade, graceful degrade, circuit breaker, caching, resolver).
   - **§Data-model** (backend) — ownership · entities + **mục đích từng bảng** · schema (**no FK** — liên kết qua id, app-layer) · state machine (entity có status) · migration approach.
   - **§Events** (nếu phát/nhận) — event (topic, payload schema, consumers, idempotency key).
   - **§Ranh giới liên target** — được gọi qua đường nào, **KHÔNG được** làm gì, vì sao (quyết định riêng của hệ này — không khai thì lúc code đi đường tiện nhất).
5. **Integrations** — cross-target (sync HTTP / async event) + external, ghi trong `docs/arch/OVERVIEW.md §Integrations` hoặc `docs/arch/{name}.md §consumes` — **≥ 1**.
6. **`deployment/docker-compose.yml`** skeleton local dev (service + DB/cache/broker cho target trong scope).

> UX/UI cho FE target (kind web/mobile): **bước riêng của `/document`** (skill `ux-design`) chạy sau khi §API sẵn — sinh `docs/ux/` + mockups + `docs/DESIGN-SYSTEM.md`. Architect chỉ đảm bảo FE target có §HLD + BE contract đủ cho UX consume.

## Enterprise cross-cutting concerns (PHẢI address)
Mỗi concern ghi rõ ở ADR / §HLD / §API (không để hở):
- **Auth**: JWT/OAuth2 flow + điểm tích hợp RBAC/PBAC.
- **Observability**: structured log schema + metrics endpoint + trace propagation header.
- **Resilience**: circuit breaker / retry / timeout hierarchy cho external call.
- **Caching**: chiến lược L1/L2 + TTL + invalidation.
- **Rate limiting**: per-tenant / per-user.
- **Idempotency**: idempotency key cho mutation/callback endpoint.
- **Pagination**: cursor-based cho list lớn (không offset).
- **Versioning**: API version (URL `/v1/` hoặc header).
- **Health checks**: `/health/live`, `/health/ready`.

## Phương pháp
1. **Research** — domain phức tạp + có WebSearch: pattern từ production system (CQRS / Saga / Outbox / Event-Sourcing), API convention, data consistency ở scale, service decomposition. KHÔNG bịa nguồn.
2. Đọc FEAT → chốt danh sách target + kind + quan hệ (depends_on, ai gọi ai) → `docs/arch/OVERVIEW.md`.
3. ADR nền trước (stack, kiến trúc backend, auth, event) → design sau tuân ADR.
4. Per target: §HLD → §API (contract + error) → §Data-model (backend) → §Events → §Ranh giới, tất cả trong `docs/arch/{name}.md`. (FE target: §HLD ở đây; UX = bước riêng sau khi §API sẵn.)
5. Integrations: cross-target + external.
6. docker-compose skeleton.

## Ca biên — phần dễ bỏ nhất, và đắt nhất khi bỏ (giá trị — giữ nguyên)
§HLD của target nên có **bảng TRA** `Tình huống → Xử lý`: lúc code cần trả lời "tình huống X xử ra sao?" mà không phải đoán và không phải hỏi. Rule trong văn xuôi phải suy diễn — có khoảng trống hiểu sai; rule trong bảng thì tra là ra.

**Checklist 8 dòng** (E1-E8) — tình huống hệ có trạng thái nào cũng gặp mà AC hạnh phúc không nói: gửi hai lần · sửa đồng thời · xoá · gọi sai thứ tự · hỏng nửa chừng · đọc bản cũ · rỗng · quyền thu hồi giữa chừng. Danh sách đã có, việc của bạn là **trả lời hết**.
- **`n/a — <lý do>` là câu trả lời hợp lệ.** Checklist ép rà, không ép làm hết.
- **Ô trống thì KHÔNG.** Trống = chưa ai quyết → lúc code mỗi target một kiểu.
- **Cột `Enforce ở đâu` phải trỏ thứ CHẶN ĐƯỢC**: unique index · cột `version` + `WHERE version = ?` · idempotency key · DB constraint · state machine. "Validate ở service" là chưa quyết gì.
- Ca biên riêng target (E9+) thêm vào bảng; đừng nhồi vào 8 dòng chung.

## Quality checklist
- [ ] ADR có decision + **alternatives ≥2** + consequences; nhất quán với `docs/CONVENTIONS.md` (layering, contract-first, no-business-logic-in-FE); deviation phải có ADR override.
- [ ] Mỗi target chốt kind + stack; `docs/arch/{name}.md` có §HLD (goals/responsibilities, data ownership, C4, flows happy+error, auth, deployment; consistency/failure khi áp dụng) + §API.
- [ ] §API có **Domain error catalog** (→ `{Domain}ErrorEnum`, map mọi business-rule/invalid-state → code); common envelope + generic codes **giống nhau mọi target**; per-endpoint chỉ ref code; đủ error responses; pagination cursor; versioning.
- [ ] Backend target có §Data-model (mỗi bảng có mục đích; no FK — liên kết qua id; state machine cho entity có status). (UX cho FE target: bước `ux-design` của `/document`.)
- [ ] Target phát/nhận event có §Events.
- [ ] Ref FEAT/persona/business-rule bằng id canonical ĐẦY ĐỦ (`FEAT-{prefix}-NNN`…), KHÔNG rút gọn — tránh ID drift.
- [ ] `consumes` frontmatter + §Ranh giới khớp topology (ai gọi ai) — đối chiếu được với `docs/arch/OVERVIEW.md` và ROADMAP depends_on.
- [ ] ≥ 1 integration thật (cross-target / external).
- [ ] Enterprise concerns đều addressed: auth · observability · resilience · caching · rate limit · idempotency · health check.
- [ ] `deployment/docker-compose.yml` skeleton có service cho target trong scope.
- [ ] (Nếu research) ≥ 1 nguồn thật, ghi link.

## Done
- ADR (`docs/adr/`) + `docs/arch/OVERVIEW.md` + per-target `docs/arch/{name}.md` (§HLD/§API/§Data-model/§Events/§Ranh giới) + integrations (≥1) + docker-compose skeleton + enterprise concerns addressed. Tiếp: bước chia wave (ROADMAP) + UX (nếu có FE target).
