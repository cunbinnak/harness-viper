---
name: technical-design
description: Phương pháp Architecture cho /document Bước 6 (sau event-storming + boundary-charter) — chốt kind/stack, ADR (docs/adr), điền chi tiết arch/{name}.md theo TEMPLATE.arch (§1 data · §2 luồng · §3 API · §4 kiến trúc/ranh giới · §5 events · §6 ca biên TRA), integrations, docker-compose skeleton. UX/UI là bước riêng (kind web/mobile).
---

> Phương pháp cho /document (fork gộp DOMAIN/DESIGN/PLAN vào DOCUMENT, 1 lớp doc). Không stage riêng, không translate.

# Architecture Method (bước ARCHITECTURE của /document)

## Khi dùng
Bước 6 ARCHITECTURE của `/document` — vai **solution architect**, chạy **CUỐI Bước 6** (sau `event-storming` ghi OVERVIEW §4 + `boundary-charter` ghi OVERVIEW §1 và khởi tạo `arch/{name}.md §0 Mission`).
Input: `docs/PRD.md` + `docs/feat/*` (AC + business-rule + field kỹ thuật) + `docs/CAPABILITIES-MAP.md` + `docs/arch/OVERVIEW.md` (§1 boundary map + §4 event-storming — 2 bước trước để lại).

> Đây là **DESIGN docs**, không scaffold code. Scaffold code (`services/{name}/`) xảy ra ở `/build`, KHÔNG ở đây.

## Deliverable
1. **ADR** `docs/adr/ADR-NNN-*.md` — theo chủ đề (tech-stack, backend-architecture [Layered/Hexagonal], auth, **api-error-convention [envelope + generic codes chung]**, **ui-kit [có FE target → chốt component library trưởng thành; React → Ant Design 5, mockup mô phỏng visual language của nó, dev dùng thật, token map qua theme]**, event/messaging…). Theo `templates/TEMPLATE.decisions.md`/ADR: context · decision · **Alternatives considered ≥2 (lý do reject)** · consequences.
2. **Boundary decomposition** — chốt các **target**: mỗi target + **kind** (`backend`/`bff`/`web`/`mobile`) + **stack** (set tại đây, vd Java 21 + Spring Boot 3.4). Ghi nhận **tech situational per-target** (phát/nhận event, dùng cache/lock, external đặc thù) — input cho bước chia wave gắn `ref_skills`.
3. **`docs/arch/OVERVIEW.md`** — bức tranh tổng: danh sách target + kind/stack + quan hệ (ai gọi ai, depends_on), luồng E2E chính, cross-cutting chung.
4. **Per target** — `docs/arch/{name}.md` (frontmatter `kind`/`stack`/`consumes` — theo `templates/TEMPLATE.arch.md`), điền chi tiết vào file `boundary-charter` đã khởi tạo (§0 Mission có rồi — KHÔNG viết lại):
   - **§2 Luồng lõi** — key flows (happy + critical error) · consistency & transaction *(nếu multi-write/event)* · failure & resilience *(nếu outbound)*.
   - **§4 Kiến trúc + ranh giới** — **CHỐT kiến trúc target (Layered/Hexagonal) + layer/package** (layout → `ref-{kind}-pattern`) · auth & permission enforce ở tầng nào.
   - **§API (contract)** — REST/OpenAPI 3.1 / GraphQL + **Domain error code catalog** (→ `{Domain}ErrorEnum`; map mỗi business-rule / invalid-state transition → 1 code). Common error envelope + generic codes (400/401/403/404/409/429/500) **GIỐNG NHAU mọi target** (chuẩn chung); per-endpoint Errors chỉ **ref** code trong catalog. `kind=bff` aggregation ≥2 backend → thêm §BFF-aggregation (DataLoader/N+1, timeout cascade, graceful degrade, circuit breaker, caching, resolver).
   - **§1 Data-model** (backend) — ownership · entities + **mục đích từng bảng** · schema (**no FK** — liên kết qua id, app-layer) · state machine (entity có status) · migration approach.
   - **§5 Events** (nếu phát/nhận) — event (topic, payload schema, consumers, idempotency key).
   - **§4 Ranh giới liên target** (cùng §4) — được gọi qua đường nào, **KHÔNG được** làm gì, vì sao (quyết định riêng của hệ này — không khai thì lúc code đi đường tiện nhất).
   - **§6 Ca biên (bảng TRA)** — xem mục dưới.
5. **Integrations** — cross-target (sync HTTP / async event) + external, ghi trong `docs/arch/OVERVIEW.md §Integrations` hoặc `docs/arch/{name}.md §consumes` — **≥ 1**.
6. **`deployment/local/docker-compose.yml`** skeleton local dev (service + DB/cache/broker cho target trong scope).

> UX/UI cho FE target (kind web/mobile): **bước riêng của `/document`** (skill `ux-design`) chạy sau khi §API sẵn — sinh `docs/ux/` + mockups + `docs/DESIGN-SYSTEM.md`. Architect chỉ đảm bảo FE target có `arch/{name}.md` (§2 luồng + §4 ranh giới) + BE contract đủ cho UX consume.

## Enterprise cross-cutting concerns (PHẢI address)
Mỗi concern ghi rõ ở ADR / `arch/{name}.md` (§2/§4) / §API (không để hở):
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
1. **Research — MẶC ĐỊNH LÀM TRƯỚC** (target/domain chưa biết đi thế nào → research trước, đừng thiết kế từ giấy trắng thứ đã có lời giải chuẩn): pattern từ production system (CQRS / Saga / Outbox / Event-Sourcing), API convention ngành, data consistency ở scale, service decomposition. Domain quá quen mới bỏ qua (ghi lý do). KHÔNG bịa nguồn.
2. Đọc FEAT → chốt danh sách target + kind + quan hệ (depends_on, ai gọi ai) → `docs/arch/OVERVIEW.md`.
3. ADR nền trước (stack, kiến trúc backend, auth, event) → design sau tuân ADR.
4. Per target (theo thứ tự § của `TEMPLATE.arch.md`): §1 Data-model (backend) → §2 Luồng lõi → §3 API (contract + error) → §4 Kiến trúc/ranh giới → §5 Events → §6 Ca biên (TRA), tất cả trong `docs/arch/{name}.md` (§0 Mission: boundary-charter đã khởi tạo). (FE target: §2/§4 ở đây; UX = bước riêng sau khi §API sẵn.)
5. Integrations: cross-target + external.
6. docker-compose skeleton.

## TRỌN VẸN API + luồng — tự rà, KHÔNG để Authority nhắc (cái ăn tiền của bước này)
Thiết kế xong PHẢI **tự trace 5 chiều** trước khi trình — Authority phát hiện lỗ hộ = bước này thất bại:
1. **AC → API/luồng**: MỌI AC của FEAT in-scope trace được tới endpoint (§3) hoặc bước trong luồng (§2) xử nó. AC không có chỗ xử = lỗ thiết kế, vá ngay.
2. **API → AC**: chiều ngược — endpoint không phục vụ AC nào = thừa (YAGNI, cắt) hoặc AC bị sót chưa viết.
3. **Endpoint đủ ruột**: mỗi dòng §3 đủ method/path + request/response + error codes (ref catalog) + status + authz (vai nào gọi được — đối chiếu ma trận PERSONAS §2) + pagination nếu list. Ô nào trống = contract chưa xong, consumer sẽ đoán.
4. **Consumer ↔ provider**: mọi `consumes_contracts` trong FEAT/frontmatter FE → có endpoint THẬT ở arch BE §3 (tên khớp). Mọi màn `SCREEN-MAP` (has_ui) → API nó gọi tồn tại. Trỏ hụt = FE lúc code sẽ bịa endpoint.
5. **Luồng E2E không đứt**: luồng chính (OVERVIEW) đi xuyên target — mỗi bước chuyển target có contract (REST/event) nêu tên; kèm nhánh lỗi ở điểm gãy (downstream chết thì bước đó trả gì).

+ **Chừa chỗ cho tương lai đã biết** (capability Phase 2/N ở CAPABILITIES-MAP): data model + API không chặn đường mở rộng đã khai (status enum mở được · naming không khoá vào MVP · quan hệ chừa chỗ) — nhưng **chừa chỗ ≠ xây trước** (YAGNI: KHÔNG code/endpoint/bảng cho Phase 2 khi chưa tới wave nó).

## Ca biên — phần dễ bỏ nhất, và đắt nhất khi bỏ (giá trị — giữ nguyên)
**`arch/{name}.md §6`** là **bảng TRA** `Tình huống → Xử lý` (khung 8 dòng có sẵn trong `TEMPLATE.arch.md`): lúc code cần trả lời "tình huống X xử ra sao?" mà không phải đoán và không phải hỏi. Rule trong văn xuôi phải suy diễn — có khoảng trống hiểu sai; rule trong bảng thì tra là ra.

**Checklist 8 dòng** (E1-E8) — tình huống hệ có trạng thái nào cũng gặp mà AC hạnh phúc không nói: gửi hai lần · sửa đồng thời · xoá · gọi sai thứ tự · hỏng nửa chừng · đọc bản cũ · rỗng · quyền thu hồi giữa chừng. Danh sách đã có, việc của bạn là **trả lời hết**.
- **`n/a — <lý do>` là câu trả lời hợp lệ.** Checklist ép rà, không ép làm hết.
- **Ô trống thì KHÔNG.** Trống = chưa ai quyết → lúc code mỗi target một kiểu.
- **Cột `Enforce ở đâu` phải trỏ thứ CHẶN ĐƯỢC**: unique index · cột `version` + `WHERE version = ?` · idempotency key · DB constraint · state machine. "Validate ở service" là chưa quyết gì.
- Ca biên riêng target (E9+) thêm vào bảng; đừng nhồi vào 8 dòng chung.

## Quality checklist
- [ ] ADR có decision + **alternatives ≥2** + consequences; nhất quán với `docs/CONVENTIONS.md` (layering, contract-first, no-business-logic-in-FE); deviation phải có ADR override.
- [ ] Mỗi target chốt kind + stack; `docs/arch/{name}.md` đủ §0-§6 theo `TEMPLATE.arch.md`: §0 Mission (boundary-charter) · §1 data · §2 luồng (happy+error, consistency/failure khi áp dụng) · §3 API · §4 kiến trúc chốt + ranh giới + auth · §5 events · §6 ca biên TRA.
- [ ] §API có **Domain error catalog** (→ `{Domain}ErrorEnum`, map mọi business-rule/invalid-state → code); common envelope + generic codes **giống nhau mọi target**; per-endpoint chỉ ref code; đủ error responses; pagination cursor; versioning.
- [ ] Backend target có §Data-model (mỗi bảng có mục đích; no FK — liên kết qua id; state machine cho entity có status). (UX cho FE target: bước `ux-design` của `/document`.)
- [ ] Target phát/nhận event có §Events.
- [ ] Ref FEAT/persona/business-rule bằng id canonical ĐẦY ĐỦ (`FEAT-<slug>` · `PERSONA-…`…), KHÔNG rút gọn — tránh ID drift.
- [ ] `consumes` frontmatter + §Ranh giới khớp topology (ai gọi ai) — đối chiếu được với `docs/arch/OVERVIEW.md` và ROADMAP depends_on.
- [ ] ≥ 1 integration thật (cross-target / external).
- [ ] **Trace 5 chiều PASS** (mục Trọn vẹn): AC↔API 2 chiều · endpoint đủ ruột (authz theo ma trận) · consumes↔provider khớp · luồng E2E không đứt — tự rà xong mới trình, KHÔNG để Authority phát hiện lỗ.
- [ ] Enterprise concerns đều addressed: auth · observability · resilience · caching · rate limit · idempotency · health check.
- [ ] `deployment/local/docker-compose.yml` skeleton có service cho target trong scope.
- [ ] (Nếu research) ≥ 1 nguồn thật, ghi link.

## Done
- ADR (`docs/adr/`) + `docs/arch/OVERVIEW.md` + per-target `docs/arch/{name}.md` (§0-§6 theo `TEMPLATE.arch.md`) + integrations (≥1) + docker-compose skeleton + enterprise concerns addressed. Tiếp: bước chia wave (ROADMAP) + UX (nếu có FE target).
