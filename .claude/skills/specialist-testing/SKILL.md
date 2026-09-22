---
name: specialist-testing
description: Test chuyên sâu — contract (consumer-driven/Pact + backward-compat), regression, isolation, perf (k6 smoke/load/stress/soak), security (OWASP), resilience/chaos, migration. Bổ sung vào registry khi vượt CRUD cơ bản.
---

# Specialist Testing Skill

> Load bởi `test-writer` ở /verify khi test vượt CRUD cơ bản (contract/Pact · k6 perf · OWASP · chaos · migration).

## Hoạt động
Bổ sung TC chuyên sâu = **thêm row** vào `tracking/wave-N/test-cases.md` (điền cột **`loại`** = test_type), mỗi TC trace ≥1 `FEAT-N:AC-M` trong cột `AC` (+ `BR-N` nếu enforce rule, ghi ở `mô tả`). **Dedupe trước**: các wave tích luỹ TC — check trùng (cùng feature + `loại`) → reuse thay vì tạo mới.

> `loại` (test_type) enum + khi-nào-dùng: **SSOT là skill này** (bảng dưới) — điền vào cột `loại` của `test-cases.md`. Skill chi tiết **rigor PER LOẠI**.

## test_type taxonomy — khi nào dùng + scope (SSOT của cột `loại`)
| group | Khi nào (wave strategy) | Scope | Nguồn input single-repo |
|---|---|---|---|
| `functional` | mọi wave (1 AC/1 luồng) | hẹp: 1 feature | `feat/FEAT-*.md` AC |
| `integration` | backend-heavy / full-stack | qua ranh giới target / BE↔FE contract | FEAT + `arch/{name}.md` (§3 API/events) + `adr/` |
| `e2e` | CHỈ full-stack (BE+FE chạy thật) | dài: nhiều màn hình UI→DB | `feat/FEAT-*.md` + `ux/` + FEAT |
| `performance` | backend-heavy / FEAT high-load | metric cụ thể (p95<Xms, RPS≥Y) | `arch/{name}.md` perf targets + ADR scaling + `PRD.md` NFR |
| `security` | mọi wave chạm auth/payment/PII | negative testing là chính | `docs/SECURITY.md` + `adr/` security + FEAT phân quyền |
| `accessibility` | CHỈ full-stack FE (WCAG 2.1 AA) | FE-only, ref WCAG criterion ID | `docs/ux/` + FEAT |

## Dựng tiền đề (Arrange) — seed / fixture / mock / sandbox
> Mọi TC = **Arrange→Act→Assert**. "Thiếu data để test" **KHÔNG phải lý do bỏ TC** — dựng tiền đề là bước Arrange, **việc của test-writer**. Ghi "không test được, dựa unit test" khi chỉ thiếu data = **né việc** (anti-pattern thật đã gặp: TC bù lương tháng này cần bảng lương tháng trước → phải seed tháng trước rồi chạy bù, không phải bỏ).

| Tiền đề cần | Cách dựng (ưu tiên trên xuống) |
|---|---|
| **Data lịch sử** (lương/đơn/giao dịch kỳ trước) | Chạy **luồng tạo thật qua API** cho kỳ trước → đúng invariant. Không có API tạo → insert DB / seed migration với data **hợp lệ nghiệp vụ** |
| **Trạng thái nhiều bước** (đơn đã duyệt+thanh toán+giao) | fixture/factory builder dựng sẵn, hoặc chuỗi API act tuần tự |
| **Thời gian** (hết hạn · cron · chốt kỳ lương · TTL) | clock injection / override env giờ hệ thống / set field ngày trực tiếp — KHÔNG `sleep` chờ thật |
| **External API** có phí / rate-limit / đối tác | stub tại **seam HTTP client** (WireMock/MSW), trả response mẫu theo `arch §API` |
| **Payment gateway** (MoMo/VNPay) | **sandbox + credential test** — test THẬT vs sandbox, KHÔNG mock (mock che mất lỗi ký/callback) |
| **Email / SMS / push** | fake sink (MailHog/Mailpit) hoặc provider sandbox → assert đã gửi + nội dung |
| **Webhook / callback từ ngoài** (IPN, event đối tác) | tự `POST` **payload giả đúng schema** (`arch §Events`) vào endpoint nhận — mô phỏng bên ngoài gọi |
| **Event Kafka** (nhận từ target khác) | EmbeddedKafka / produce event giả đúng schema vào topic |

**Luật mock:**
- Mock tại **ranh giới ngoài cùng** (HTTP/SMTP/gateway/broker client) — **KHÔNG** mock service/repo **nội bộ** (mock nội bộ = test cái mock, che bug tích hợp thật).
- Fake data phải **hợp lệ nghiệp vụ** — đi qua **cùng validation/invariant** như data thật (seed thẳng DB thì tự đảm bảo ràng buộc). Fake bậy (bỏ qua rule) → **test đậu giả**, tệ hơn không test.
- Mock/stub xong **assert được tương tác** (đã gọi đúng endpoint/payload gì) — không chỉ "không nổ".
- Dọn seed/fixture cuối phase (luật #9) — không để rác data giữa các TC (gây phập phù).

## Rigor per loại
- **contract**: verify API/event contract khớp `docs/arch/{name}.md §3 API` / events.
  - Consumer-driven (Pact hoặc tương đương): consumer định nghĩa expectation → provider verification chạy ở CI provider.
  - Provider state setup cho từng interaction; verify path/method/field/enum/error code/response shape + event payload schema.
  - **Backward-compat (additive-only)**: thêm field optional / enum value OK; remove/rename/đổi type/bắt buộc field mới = **breaking → FAIL** (bắt sớm trước khi vỡ consumer).
- **regression**: `TC-R*` chốt lại lỗi đã sửa (link `ref_tc=TC-NNN`) — chống tái phát. Tag `@regression`.
- **isolation**: unit/integration biên domain (mock infra) cho logic phức tạp / invariant.
- **performance** (khi NFR latency): k6, threshold = SLO từ `PRD.md` NFR (p95/p99 + error rate). Phân loại: **smoke** (vài VU, sanity) · **load** (tải kỳ vọng) · **stress** (tìm điểm gãy) · **soak** (chạy dài → phát hiện memory leak).
  ```javascript
  import http from 'k6/http'; import { check } from 'k6';
  export const options = { vus: 10, duration: '1m',
    thresholds: { http_req_duration: ['p(99)<500'] } };   // theo NFR PRD.md
  export default function () {
    const r = http.get(`${__ENV.BASE_URL}/v1/health`);
    check(r, { 'ok': (res) => res.status === 200 });
  }
  ```
- **security** (khi NFR security): theo `docs/SECURITY.md` (OWASP) — injection (SQL/JPQL/native), SSRF, mass-assignment, deserialization; authz bypass + tenant leakage; secret trong response/log; **dependency scan (CVE nghiêm trọng)**; FE: XSS/CSRF/token storage; rate-limit/brute-force. Negative test: User A KHÔNG xem được resource User B → 403.
- **accessibility** (WCAG 2.1 AA, CHỈ full-stack FE): keyboard nav, screen reader, color contrast, focus management; tool axe/Lighthouse; ref WCAG criterion ID (vd 2.1.1, 4.1.2). FE-isolated dễ false positive → defer sang full-stack wave.
- **resilience/chaos** (khi NFR availability): inject downstream fail/timeout → verify timeout + circuit-breaker mở + fallback đúng; partial failure (DB commit nhưng event/cache fail) → reconcile/outbox bù.
- **migration** (khi đổi schema): chạy migration forward trên DB có data + verify **rollout an toàn** (thêm column NULLABLE → backfill → enforce NOT NULL ở migration sau); KHÔNG mất data, KHÔNG khoá bảng lâu.
- **architecture-drift** (tuỳ chọn — KHÔNG có trong khung, tự cài khi cần): đo coupling/cohesion + drift khỏi `arch/{name}.md` bằng **số** (metric). Mặc định `reviewer`/`bug-hunter` soi "logic sai tầng / ranh giới module" **định tính** là đủ. Project multi-boundary phức tạp cần đo bằng số → tự thêm skill wrap tool ngoài, vd [arcade-agent](https://github.com/lemduc/arcade-agent) (đa ngôn ngữ, MCP + CI drift-check). Cân dep nặng (tree-sitter) vs lợi ích trước khi thêm.

## Done
- TC chuyên sâu vào `tracking/wave-N/test-cases.md` (cột `loại` + trace AC ở cột `AC`). Contract/perf/security/resilience/migration chỉ thêm khi contract phức tạp / NFR yêu cầu / có đổi schema. Dedupe-check trước khi tạo (reuse > create).
