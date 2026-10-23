---
name: technical-design
description: Vai SA — Architecture cho /document Bước 6 (sau event-storming + boundary-charter + system-design, phản ánh OVERVIEW §5) — chốt kind, ĐỀ XUẤT stack (chốt ở Bước 7 bằng hỏi Authority), ADR kiến trúc (docs/adr), điền chi tiết arch/{name}.md theo TEMPLATE.arch (§1 data · §2 luồng · §3 API · §4 kiến trúc/ranh giới · §5 events · §6 ca biên TRA), integrations, docker-compose skeleton. UX/UI là bước riêng (kind web/mobile/desktop).
---

# Architecture Method (bước ARCHITECTURE của /document)

> **Vai: SA** · **Viết**: ADR · `OVERVIEW §2-§3` · `docs/arch/{name}.md` §1 data model · §2 luồng xử lý · §3 API · §4 ranh giới · §5 events · §6 ca biên + chặn ở đâu · `consumes` · docker-compose khung
> **KHÔNG viết**: FEAT / AC (BA) · NFR (PO) · `OVERVIEW §5` (`system-design`) · chốt stack (Bước 7, Authority chốt)

## Khi dùng
Bước 6 ARCHITECTURE của `/document` — vai **solution architect**, chạy **CUỐI Bước 6** (sau `event-storming` ghi OVERVIEW §4 + `boundary-charter` ghi OVERVIEW §1 và khởi tạo `arch/{name}.md §0 Mission` + `system-design` ghi OVERVIEW §5).
Input: `docs/PRD.md` + `docs/feat/*` (AC + §3 Ràng buộc nghiệp vụ) + `docs/CAPABILITIES-MAP.md` + `docs/arch/OVERVIEW.md` (§1 boundary map + §4 event-storming + **§5 system design** — 3 bước trước để lại). Contract PHẢI phản ánh §5 theo bảng ở mục **§Đọc OVERVIEW §5** dưới đây. §5 chưa có (chưa chạy `Skill("system-design")`) → DỪNG, chạy nó trước — không tự đoán quy mô.

> Đây là **DESIGN docs**, không scaffold code. Scaffold code (`services/{name}/`) xảy ra ở `/build`, KHÔNG ở đây. Ngoại lệ: **khung** `deployment/local/docker-compose.yml` (Deliverable 6) — dựng sẵn service + hạ tầng; `/build` (`infra-local-dev`) làm nốt chi tiết.

## Deliverable
1. **ADR** `docs/adr/ADR-NNN-*.md` — theo chủ đề (backend-architecture [Layered/Hexagonal], **api-error-convention [envelope + generic codes chung]**, event/messaging…). **Stack · ui-kit · auth · lưu file · cache KHÔNG tự chốt ở đây** — ghi đề xuất + phương án, chốt bằng lượt hỏi Authority ở `/document` Bước 7 rồi mới viết ADR tương ứng. Theo `templates/TEMPLATE.adr.md`: context · decision · **Alternatives considered ≥2 (lý do reject)** · consequences.
2. **Boundary decomposition** — chốt các **target**: mỗi target + **kind** (`backend`/`bff`/`web`/`mobile`/`desktop` — desktop: app cài trên Windows · §3 ghi **hợp đồng IPC** (kênh · tham số · kết quả · mã lỗi) thay REST nội bộ — mỗi kênh một dòng dạng `IPC <tên-kênh>` để gate đối chiếu với `data-api` trên mockup · §1 dữ liệu cục bộ · §4 quyền hệ điều hành: thư mục được đọc/ghi · tiến trình con · dịch vụ ngoài gọi kèm key) + **stack đề xuất** (chốt ở Bước 7; version lấy từ description skill `stack-<tên>`, không từ trí nhớ). Ghi nhận **tech situational per-target** (phát/nhận event, dùng cache/lock, external đặc thù) — input cho bước chia wave gắn `ref_skills`.
3. **`docs/arch/OVERVIEW.md`** — §2 tích hợp cross-boundary + **luồng E2E chính** · §3 hạ tầng dùng chung (danh sách — căn cứ ở §5). §1 (target · kind · depends_on) do `boundary-charter` chốt — đọc, không viết lại.
4. **Per target** — `docs/arch/{name}.md` (frontmatter `kind`/`stack`/`consumes` — theo `templates/TEMPLATE.arch.md`), điền chi tiết vào file `boundary-charter` đã khởi tạo (§0 Mission có rồi — KHÔNG viết lại):
   - **§2 Luồng xử lý (kỹ thuật)** — mỗi bước thao tác trên hệ thống của luồng nghiệp vụ (`INTERVIEW §Luồng nghiệp vụ đã xác nhận`) mở ra ≥1 luồng xử lý: request → ghi/đọc → response (happy + critical error), ghi `Phục vụ: <luồng> bước N`; bước nghiệp vụ không có luồng xử lý = thiếu thiết kế, luồng xử lý không phục vụ bước nào = thừa · consistency & transaction *(nếu multi-write/event)* · failure & resilience *(nếu outbound)*.
   - **§4 Kiến trúc + ranh giới** — **CHỐT kiến trúc target (Layered/Hexagonal) + layer/package** (layout → `ref-{kind}-pattern`) · auth & permission enforce ở tầng nào.
   - **§API (contract)** — REST/OpenAPI 3.1 / GraphQL + **Domain error code catalog** (→ `{Domain}ErrorEnum`; map mỗi business-rule / invalid-state transition → 1 code). Common envelope (shape `SuccessResponse`/`ErrorResponse`/`PageResponse` — `ref-backend-pattern §6`) + generic codes (400/401/403/404/409/429/500) **GIỐNG NHAU mọi target** (chuẩn chung); per-endpoint Errors chỉ **ref** code trong catalog. `kind=bff` aggregation ≥2 backend → thêm §BFF-aggregation (DataLoader/N+1, timeout cascade, graceful degrade, circuit breaker, caching, resolver).
   - **§1 Data-model** (backend) — ownership · entities + **mục đích từng bảng** · schema (**no FK** — liên kết qua id, app-layer) · state machine (entity có status) · migration approach.
   - **§5 Events** (nếu phát/nhận) — event (topic, payload schema, consumers, idempotency key).
   - **§4 Ranh giới liên target** (cùng §4) — được gọi qua đường nào, **KHÔNG được** làm gì, vì sao (quyết định riêng của hệ này — không khai thì lúc code đi đường tiện nhất).
   - **§6 Ca biên (bảng TRA)** — xem mục dưới. **Mọi dòng FEAT §3 Ràng buộc nghiệp vụ in-scope** (BA viết *chặn gì*) → ≥1 dòng §6 có cột AC/BR trỏ về nó + `Enforce ở đâu` (SA quyết *chặn ở đâu*). Dòng FEAT §3 không có dòng §6 = ràng buộc chưa ai chặn.
5. **Integrations** — cross-target (sync HTTP / async event) + external, ghi trong `docs/arch/OVERVIEW.md §2` + frontmatter `consumes` của target gọi — **≥ 1**.
6. **`deployment/local/docker-compose.yml`** skeleton local dev (service + DB/cache/broker cho target trong scope).

> UX/UI cho FE target (kind web/mobile/desktop): **bước riêng của `/document`** (skill `ux-design`) chạy sau khi §API sẵn — sinh `docs/ux/` + mockups + `docs/DESIGN-SYSTEM.md`. Architect chỉ đảm bảo FE target có `arch/{name}.md` (§2 luồng + §4 ranh giới) + BE contract đủ cho UX consume.

## Enterprise cross-cutting concerns (PHẢI address)
Mỗi concern ghi rõ ở ADR / `arch/{name}.md` (§2/§4) / §API (không để hở):
- **Auth**: JWT/OAuth2 flow + điểm tích hợp RBAC/PBAC — theo mô hình xác thực ở OVERVIEW §5.7 (kiểm `iss`/`aud`, thu hồi token).
- **Observability**: log JSON + header truy vết **`X-Request-ID`** (`ref-backend-logging §3`) + metrics endpoint + cảnh báo theo SLO §5.1.
- **Resilience**: circuit breaker / retry / timeout cho external call — theo §5.6.
- **Caching**: chỉ chỗ §5.4 khai — key + TTL + invalidation.
- **Rate limiting**: per-user / per-tenant; IP client qua proxy tin cậy khi §5.8 khai đứng sau proxy.
- **Idempotency**: idempotency key cho mutation/callback endpoint.
- **Pagination**: **offset** (`PageResponse` — `ref-backend-pattern §6`) mặc định, `size ≤ 100`; cursor chỉ cho luồng đặc thù §5.4 khai (feed, log rất lớn) + ADR.
- **Versioning**: API version (URL `/v1/` hoặc header).
- **Health checks**: `/health/live`, `/health/ready`.

## Đọc OVERVIEW §5 — system design → contract
Đọc `docs/arch/OVERVIEW.md §5` (do `system-design` ghi) TRƯỚC khi viết `arch/{name}.md`. Mỗi điều §5 khai phải hiện xuống contract đúng chỗ:

| §5 khai | `technical-design` ghi xuống |
|---|---|
| bảng lớn (5.4) | list/search phân trang ở DB, `size ≤ 100`, không `findAll` cả bảng — `arch §3` |
| cache (5.4) | key · TTL · invalidation — `arch §4` |
| nhất quán sau (5.5) | outbox/saga/bù — `arch §2` · `§5 Events` · `§6` E5 |
| dữ liệu nhạy cảm (5.7) | cột mã hoá / che log — `arch §1` data model |
| ≥ 2 instance (5.8) | job có lock, session stateless — `arch §4` |
| sau proxy (5.8) | lấy IP qua proxy tin cậy (`forward-headers-strategy`) — `arch §4` |

§5 ghi `n/a` cho mục nào → không thêm thành phần đó (không cache, không queue… khi không có số đòi). Lệch bảng này = lỗ thiết kế, cùng mức với trace 6 chiều.

## Phương pháp
1. **Research — MẶC ĐỊNH LÀM TRƯỚC** (target/domain chưa biết đi thế nào → research trước, đừng thiết kế từ giấy trắng thứ đã có lời giải chuẩn): pattern từ production system (CQRS / Saga / Outbox / Event-Sourcing), API convention ngành, data consistency ở scale, service decomposition. Domain quá quen mới bỏ qua (ghi lý do). KHÔNG bịa nguồn.
2. Đọc FEAT + màn nháp + OVERVIEW §1 (target · kind · depends_on đã chốt) + §5 → ghi `OVERVIEW` §2 (tích hợp + luồng E2E) · §3 (hạ tầng) + frontmatter `stack`/`consumes` mỗi `arch/{name}.md`.
3. ADR nền trước (kiến trúc backend Layered/Hexagonal · event/messaging · api-error-convention) → design sau tuân ADR. Stack · auth · ui-kit · lưu file · cache: chỉ đề xuất ở đây, ADR ghi sau khi Authority chốt ở Bước 7.
4. Per target (theo thứ tự § của `TEMPLATE.arch.md`): §1 Data-model (backend) → §2 Luồng xử lý → §3 API (contract + error) → §4 Kiến trúc/ranh giới → §5 Events → §6 Ca biên (TRA), tất cả trong `docs/arch/{name}.md` (§0 Mission: boundary-charter đã khởi tạo). (FE target: §2/§4 ở đây; UX = bước riêng sau khi §API sẵn.)
5. Integrations: cross-target + external.
6. docker-compose skeleton.

## TRỌN VẸN API + luồng — tự rà, KHÔNG để Authority nhắc (cái ăn tiền của bước này)
Thiết kế xong PHẢI **tự trace 6 chiều** trước khi trình — Authority phát hiện lỗ hộ = bước này thất bại:
1. **AC + màn nháp → API/luồng**: MỌI AC của FEAT in-scope trace được tới endpoint (§3) hoặc bước trong luồng (§2) xử nó. **Màn nháp của BA** (`INTERVIEW §Luồng nghiệp vụ đã xác nhận`): MỖI hành động + MỖI vùng ở cột Dữ liệu hiển thị có endpoint nuôi nó — kể cả thứ AC không nói thẳng (danh mục nguồn của ô chọn · badge đếm · tab lịch sử · lọc/phân trang · xem/tải file). Thiết kế API **từ màn nháp**, không đợi mockup. Thiếu = lỗ thiết kế, vá ngay.
2. **API → AC**: chiều ngược — endpoint không phục vụ AC nào = thừa (YAGNI, cắt) hoặc AC bị sót chưa viết.
3. **Endpoint đủ ruột**: mỗi dòng §3 đủ method/path + request/response + error codes (ref catalog) + status + authz (vai nào gọi được — đối chiếu ma trận PERSONAS §2) + pagination nếu list. Ô nào trống = contract chưa xong, consumer sẽ đoán.
   - **API tìm kiếm/danh sách**: **≥ 3 tiêu chí lọc**, hoặc có lọc mảng/khoảng (`statuses[]`, `fromDate–toDate`) → `POST /{resources}/search`, body `{Resource}SearchRequest` (tiêu chí + `page`/`size`/`sort`), trả trang — chỉ đọc, không đổi state. Ít hơn (≤ 2 lọc bằng-giá-trị) → `GET /{resources}?…&page&size&sort`. Ghi rõ method ở §3 — BUILD làm theo contract, chọn sai ở đây là sửa wave sau.
4. **Consumer ↔ provider**: SA khai `consumes` ở frontmatter `arch` của MỌI target consumer (web/bff/mobile/desktop — FEAT không khai) → mỗi mục có endpoint THẬT ở arch BE §3 (tên khớp). Trỏ hụt = FE lúc code sẽ bịa endpoint. (Vế màn nháp ↔ API đã rà ở chiều 1; vế **mockup ↔ API** (`data-api` + gate `mockup_api_gaps`) rà ở Bước 8 và PRE-LOCK — lưới chặn cuối.)
5. **Luồng E2E không đứt**: luồng chính (OVERVIEW) đi xuyên target — mỗi bước chuyển target có contract (REST/event) nêu tên; kèm nhánh lỗi ở điểm gãy (downstream chết thì bước đó trả gì).
6. **Lifecycle & seam (soi cái VẮNG MẶT — 5 chiều trên chỉ soi cái đã viết)**: mọi **cạnh chuyển trạng thái** của entity chính (state machine §1, kể cả cạnh ngoài-hạnh-phúc) có AC/luồng chủ hoặc `n/a` tường minh · mọi **seam FEAT→FEAT** có CƠ CHẾ truyền được viết (output đến tay actor bên kia bằng gì) · đối chiếu **6 họ luồng phổ quát** (`pre-mortem` Cách săn 3) + **danh sách luồng chuẩn ngành** (PRD §6) — mỗi dòng map hoặc out-of-scope, không bỏ trắng.

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
- [ ] Mọi điều OVERVIEW §5 khai đã hiện xuống contract theo bảng §Đọc OVERVIEW §5 (bảng lớn → phân trang DB · cache · outbox · mã hoá cột · lock job · IP qua proxy).
- [ ] Mỗi target chốt kind + stack; `docs/arch/{name}.md` đủ §0-§6 theo `TEMPLATE.arch.md`: §0 Mission (boundary-charter) · §1 data · §2 luồng (happy+error, consistency/failure khi áp dụng) · §3 API · §4 kiến trúc chốt + ranh giới + auth · §5 events · §6 ca biên TRA.
- [ ] §API có **Domain error catalog** (→ `{Domain}ErrorEnum`, map mọi business-rule/invalid-state → code); common envelope + generic codes **giống nhau mọi target**; per-endpoint chỉ ref code; đủ error responses; pagination offset (`PageResponse`, size ≤ 100 — cursor chỉ khi §5 + ADR); versioning.
- [ ] Backend target có §Data-model (mỗi bảng có mục đích; no FK — liên kết qua id; state machine cho entity có status). (UX cho FE target: bước `ux-design` của `/document`.)
- [ ] Target phát/nhận event có §Events.
- [ ] Ref FEAT/persona/business-rule bằng id canonical ĐẦY ĐỦ (`FEAT-<slug>` · `PERSONA-…`…), KHÔNG rút gọn — tránh ID drift.
- [ ] `consumes` frontmatter + §Ranh giới khớp topology (ai gọi ai) — đối chiếu được với `docs/arch/OVERVIEW.md` và ROADMAP depends_on.
- [ ] ≥ 1 integration thật (cross-target / external).
- [ ] **Trace 6 chiều PASS** (mục Trọn vẹn — cả chiều 6 lifecycle & seam) — tự rà xong mới trình, KHÔNG để Authority phát hiện lỗ.
- [ ] Enterprise concerns đều addressed: auth · observability · resilience · caching · rate limit · idempotency · health check.
- [ ] `deployment/local/docker-compose.yml` skeleton có service cho target trong scope.
- [ ] (Nếu research) ≥ 1 nguồn thật, ghi link.

## Done
- ADR (`docs/adr/`) + `docs/arch/OVERVIEW.md` + per-target `docs/arch/{name}.md` (§0-§6 theo `TEMPLATE.arch.md`) + integrations (≥1) + docker-compose skeleton + enterprise concerns addressed. Tiếp: bước chia wave (ROADMAP) + UX (nếu có FE target).
