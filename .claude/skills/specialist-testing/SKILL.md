---
name: specialist-testing
description: "Phương pháp QA cho test-writer — ba nguồn ra test case (AC · bảng chính sách · thăm dò ngoài tài liệu) + kỹ thuật thiết kế (phân vùng tương đương · giá trị biên · bảng quyết định · chuyển trạng thái) + chuẩn kiểm (điều kiện được ghi PASS) + dữ liệu đối kháng + regression cộng dồn + dựng tiền đề (seed/fixture/mock/sandbox) + rigor chuyên sâu theo loại (contract · perf k6 · security OWASP · resilience · migration). test-writer LUÔN nạp."
---

# Specialist Testing Skill

> `test-writer` **LUÔN nạp** ở /verify: §Ba nguồn → §Kỹ thuật → §Chuẩn kiểm → §Dữ liệu đối kháng → §Thăm dò → §Regression là phương pháp mọi wave. §Đợt kiểm chuyên sâu: wave có `SHIP`. §Rigor per loại dùng khi vượt CRUD (contract · perf · security · tenant isolation · resilience · migration).

## Hoạt động
Mỗi TC = **1 dòng** trong `tracking/wave-N/test-cases.md` — khung + nghĩa từng cột ở `templates/TEMPLATE.test-cases.md` (gate đọc theo tên cột). Dòng TC **chính là** báo cáo bug khi FAIL: `cách chạy` = bước tái hiện · `mô tả` = kỳ vọng · `thực tế / bằng chứng` = điều quan sát được — không viết báo cáo riêng.

## Ba nguồn ra test case
Tài liệu im lặng chỗ nào thì test im lặng chỗ đó — nên KHÔNG chỉ dẫn xuất từ AC:
| Nguồn (cột `nguồn`) | Đọc ở | Ra TC gì |
|---|---|---|
| **AC** | `docs/feat/FEAT-*` (AC + ca biên inline + §3 Ràng buộc) · `arch/{name}.md §6` (E1-E8) · `PERSONAS §2` (ô `cấm`) | hành vi đã hứa · ca biên đã quyết · mỗi ô `cấm` = 1 TC âm · mỗi ô `có` = 3 chiều (§Kỹ thuật) |
| **CS** — bảng chính sách | `docs/INTERVIEW.md` → "Chính sách từng hành động" (`domain-ba` A.6) | mỗi ô có giá trị → ≥1 TC bị chặn + ≥1 TC được cho qua · giới hạn số/thời gian → **giá trị biên** · ngoại lệ → TC vai ngoại lệ được làm + vai thường bị chặn · trùng/xung đột → TC tạo xung đột thật |
| **TD** — thăm dò | §Thăm dò dưới (4 phép thử trên hệ thật) | chỗ tài liệu im lặng → `CHƯA CÓ QUY ĐỊNH` |

## Kỹ thuật thiết kế — áp cho mỗi AC / mỗi ô chính sách
| Kỹ thuật | Dùng khi | Cách làm | Ví dụ (đăng ký làm từ xa) |
|---|---|---|---|
| **Phân vùng tương đương** | đầu vào có nhóm giá trị được xử lý giống nhau | chia nhóm hợp lệ / không hợp lệ, mỗi nhóm 1 TC. Nhiều tham số: 1 TC mọi tham số hợp lệ + mỗi nhóm không hợp lệ 1 TC (**chỉ sai 1 tham số mỗi lần** — sai 2 cùng lúc thì không biết cái nào bị chặn) | ngày đăng ký: ngày làm việc sắp tới (hợp lệ) · quá khứ · ngày lễ · cuối tuần |
| **Giá trị biên** | có ngưỡng: số · thời gian · độ dài · số lượng | **3 điểm quanh mỗi biên**: dưới · đúng · trên | hạn chót 17:00 → 16:59:59 · 17:00:00 · 17:00:01 · hạn mức 2 ngày/tuần → ngày thứ 2 · thứ 3 |
| **Bảng quyết định** | kết quả phụ thuộc ≥ 2 điều kiện kết hợp | liệt kê điều kiện × kết quả, gộp các cột cùng kết quả, mỗi cột còn lại 1 TC | (trước hạn chót?) × (trùng phép đã duyệt?) × (người gửi là HR?) → chặn / cho qua / cho qua kèm lý do |
| **Chuyển trạng thái** | entity có trạng thái | mỗi cạnh hợp lệ 1 TC · mỗi **cạnh CẤM** (hành động không được phép ở trạng thái đó) 1 TC → phải bị chặn, trạng thái không đổi · **≥1 TC vòng đời nhiều bước** chạy trọn chuỗi | CHỜ DUYỆT → ĐÃ DUYỆT → HUỶ · cấm: duyệt đơn đã huỷ · huỷ sau khi chấm công đã chốt |
| **Phân quyền 3 chiều** | hành động có ô `có` trong ma trận vai | ma trận 2 chiều (vai × hành động) chưa đủ — lỗ thật nằm ở **phạm vi** và **trạng thái** bản ghi. Mỗi ô `có` → 3 TC: đúng vai + **đúng phạm vi** (cho qua) · đúng vai + **sai phạm vi** (của người/nhóm/tenant khác → chặn) · đúng vai + **sai trạng thái** (bản ghi ở trạng thái không cho phép → chặn). Mỗi ô `cấm` vẫn 1 TC âm như cũ | quản lý duyệt đơn: của nhân viên mình (cho) · của phòng khác (chặn) · đơn đã huỷ (chặn) |

**Biên hay quên**: chuỗi rỗng / 1 ký tự / đúng max / max+1 · danh sách 0 / 1 / vừa tràn 1 trang · ngày 29-02 · ngày 31 của tháng 30 ngày · cuối năm · nửa đêm · tiền 0 / âm / làm tròn · file 0 byte / đúng trần / vượt trần.
Không ép số lượng TC — nhưng **có ngưỡng thì BẮT BUỘC giá trị biên**, **có trạng thái thì BẮT BUỘC cạnh cấm + 1 TC vòng đời**.

## Chuẩn kiểm — điều kiện để một TC được ghi PASS
1. Kiểm **kết quả chính**, không chỉ "chạy xong" — `200` / toast "thành công" một mình KHÔNG đủ.
2. Kiểm **MỌI giá trị nghiệp vụ** mà `mô tả` nêu (số tiền · ngày · trạng thái · người) — sót 1 giá trị là chỗ lỗi lọt.
3. Thao tác **GHI → đọc lại dữ liệu đã lưu** (GET lại · màn danh sách · DB). Không đọc lại = chưa PASS.
4. Ca **bị chặn** → kiểm mã lỗi + thông báo **VÀ không sinh tác dụng phụ** (không bản ghi · không event · không email).
5. Dữ liệu theo người / tenant → kiểm thêm phía **người khác không thấy**.
6. Trước khi ghi PASS tự hỏi: *"code sai kiểu X (lệch 1 · sai người · sai tenant · quên đổi trạng thái) thì TC này có đỏ không?"* — không → thêm điểm kiểm.

Cột `thực tế / bằng chứng` ghi gọn điều quan sát được ở bước 3–5 (vd `201 · GET → CHỜ DUYỆT · có trong hàng chờ QL`).

## Dữ liệu đối kháng — trộn vào TC validate + ca biên
Tiếng Việt có dấu · tên rất dài · emoji · khoảng trắng đầu/cuối · chỉ dấu cách · số 0 / âm / cực lớn / thập phân · ngày 29-02 · mốc nửa đêm · giờ máy chủ (UTC) lệch giờ Việt Nam (UTC+7) · mã trùng khác hoa/thường. Dữ liệu chính lấy từ PRD §7 (giá trị thật ngoài đời) — không "test1", "abc".

## Thăm dò ngoài tài liệu — chỗ tài liệu im lặng
**Lên SẴN dòng `TD` lúc viết đề** (để được rà cùng đề), **chạy SAU** các TC AC + CS. Với **mỗi hành động** trong bảng luồng, thử **trên hệ thật** đúng chỗ bảng chính sách KHÔNG nói tới, theo 4 phép thử (cùng bộ với `domain-ba` A.6) — lúc chạy lộ thêm ca đáng thử → thêm dòng:
1. **Lạm dụng** — làm lùi ngày · làm thay người khác · làm nhiều lần.
2. **Hạ nguồn** — làm sau mốc chốt của nghiệp vụ dùng dữ liệu này (cuối ngày · cuối kỳ).
3. **Xung đột** — tạo trùng với nghiệp vụ khác cùng người / thời gian / tài nguyên.
4. **Vòng đời** — sửa / huỷ sau khi đã duyệt hoặc đã bị dùng.

Kết quả: hệ chặn hợp lý → `PASS` (ghi hành vi làm mốc) · hệ **cho phép điều phép thử chỉ ra là có hại** → `CHƯA CÓ QUY ĐỊNH` — nghĩa là *tài liệu (AC + bảng chính sách) không quy định ca này, hệ đang cho phép một việc có thể gây hại* — **KHÔNG phải FAIL** (code đúng tài liệu; thêm quy định hay không là quyết định của Author): `thực tế / bằng chứng` ghi hành vi + phép thử + hệ quả (vd `201 lúc 18:05 · hạ nguồn: chấm công đã chốt → công ngày đó sai`). MAIN đưa vào báo cáo cuối VERIFY + `ROADMAP §backlog`.
Giới hạn **~5 thăm dò / hành động**, ưu tiên hành động chạm tiền · công · quyền.

## Regression cộng dồn
**Gắn `@regression` khi thiết kế**: TC smoke mỗi luồng · TC chạm tiền / số dư / chấm công · TC ô `cấm` · **TC bắt được bug đã sửa** (thêm ở chế độ chạy lại khi xác nhận fix — bug từ review/dogfood cũng viết 1 TC tái hiện).
**Wave ≥ 2**: lúc **viết đề**, chép MỌI TC `@regression` trong `archive/wave-*/tracking/wave-*/test-cases.md` sang `test-cases.md` wave hiện tại (giữ mã gốc · `nguồn` = `R`); lúc **chạy**, chạy chúng TRƯỚC TC wave mới, ghi kết quả. FAIL = surface đã giao bị phá → **BLOCKER**. TC cũ hết hợp lệ vì AC đã đổi qua top-up → vẫn chép dòng, `kết quả` = `ĐÃ THAY` + `thực tế / bằng chứng` = `AC đổi ở <FEAT vN> → thay bằng <TC mới>`; TC mới gắn `@regression` và phải PASS — không tự xoá dòng cũ (`bug-hunter` rà đề test kiểm TC thay thế có thật).

## Đợt kiểm chuyên sâu — không chạy đủ mọi wave
Wave thường: perf · security · tenant isolation · resilience **chỉ** cho AC/NFR mà wave đó chạm (vd AC có ngưỡng thời gian phản hồi → đo đúng endpoint đó).
**Đợt kiểm sâu BẮT BUỘC** ở wave có `SHIP` trong cột `phases` của ROADMAP §1 (trước khi lên production — thường là wave cuối): chạy **toàn bộ** hệ đã giao, không chỉ AC wave đó:
- **performance**: k6 smoke + load theo NFR PRD §3 / OVERVIEW §5.1 trên các luồng chính.
- **security**: đủ nhóm OWASP ở §Rigor + SCA (`docs/SECURITY.md §6`) + mỗi endpoint public không token → 401.
- **tenant isolation** (sản phẩm nhiều tenant): §Rigor `tenant isolation` cho MỌI endpoint đọc/ghi.
- **resilience**: mỗi hệ ngoài ở OVERVIEW §5.6 chết/chậm → hệ phản ứng đúng như đã khai.
TC đợt sâu ghi chung `test-cases.md` (cột `loại` tương ứng), gắn `@regression` cho ca chặn thật (lỗ bảo mật/rò tenant đã vá).

## test_type taxonomy — khi nào dùng + scope (SSOT của cột `loại`)
| group | Khi nào (wave strategy) | Scope | Nguồn input single-repo |
|---|---|---|---|
| `functional` | mọi wave (1 AC/1 luồng) | hẹp: 1 feature | `feat/FEAT-*.md` AC |
| `integration` | backend-heavy / full-stack | qua ranh giới target / BE↔FE contract | FEAT + `arch/{name}.md` (§3 API/events) + `adr/` |
| `e2e` | CHỈ full-stack (BE+FE chạy thật) | dài: nhiều màn hình UI→DB | `feat/FEAT-*.md` + `ux/` + FEAT |
| `performance` | backend-heavy / FEAT high-load | metric cụ thể (p95<Xms, RPS≥Y) | `arch/{name}.md` perf targets + ADR scaling + `PRD.md` NFR |
| `security` | mọi wave chạm auth/payment/PII | negative testing là chính | `docs/SECURITY.md` + `adr/` security + FEAT phân quyền |
| `accessibility` | CHỈ full-stack FE (WCAG 2.1 AA) | FE-only, ref WCAG criterion ID | `docs/ux/` + FEAT |

Ngoài 6 dòng trên, `loại` còn dùng: `contract` · `resilience` · `migration` · `isolation` (rigor ở §Rigor per loại; tenant isolation ghi `security`). `@smoke` / `@regression` là **tag**, không phải loại.

## Dựng tiền đề (Arrange) — seed / fixture / mock / sandbox
> Mọi TC = **Arrange→Act→Assert**. "Thiếu data để test" **KHÔNG phải lý do bỏ TC** — dựng tiền đề là bước Arrange, **việc của test-writer**. Ghi "không test được, dựa unit test" khi chỉ thiếu data = **né việc** (anti-pattern thật đã gặp: TC bù lương tháng này cần bảng lương tháng trước → phải seed tháng trước rồi chạy bù, không phải bỏ).

| Tiền đề cần | Cách dựng (ưu tiên trên xuống) |
|---|---|
| **Data lịch sử** (lương/đơn/giao dịch kỳ trước) | Chạy **luồng tạo thật qua API** cho kỳ trước → đúng invariant. Không có API tạo → insert DB / seed migration với data **hợp lệ nghiệp vụ** |
| **Trạng thái nhiều bước** (đơn đã duyệt+thanh toán+giao) | fixture/factory builder dựng sẵn, hoặc chuỗi API act tuần tự |
| **Thời gian** (hết hạn · cron · chốt kỳ lương · TTL · hạn chót) | hệ thật: đặt env `APP_CLOCK_FIXED=<ISO +07:00>` rồi restart container (đồng hồ tiêm được, chỉ có ở profile local — `ref-backend-test §3`) · set field ngày trực tiếp — KHÔNG `sleep` chờ thật |
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
- **regression**: xem §Regression cộng dồn (tag `@regression`, không phải loại).
- **isolation**: unit/integration biên domain (mock infra) cho logic phức tạp / invariant.
- **tenant isolation** (`loại` = `security`; sản phẩm nhiều tenant/chi nhánh/công ty): dựng **2 bộ dữ liệu A và B** khác tenant, cùng cấu trúc. Với MỖI endpoint, đăng nhập A rồi:
  - **đọc**: gọi id bản ghi của B → bị chặn (thống nhất **403 hay 404** theo `arch §3` — không lẫn lộn mỗi endpoint một kiểu) · danh sách/tìm kiếm/xuất file/badge đếm của A **không lẫn** dữ liệu B;
  - **ghi**: sửa/xoá/duyệt bản ghi của B → bị chặn, đọc lại bản ghi B không đổi · tạo mới mà body/header tự khai `tenantId` của B → bị bỏ qua hoặc chặn, bản ghi thuộc A;
  - **cache**: A đọc trước, B đọc sau cùng khoá (cùng trang/cùng bộ lọc) → B KHÔNG nhận dữ liệu A từ cache;
  - **job/thông báo**: job chạy theo tenant không gửi/ghi chéo (email của A không tới người dùng B).
  Bất kỳ ca rò nào = **BLOCKER**, gắn `@regression`.
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
- `tracking/wave-N/test-cases.md` đúng khung template: TC từ đủ 3 nguồn (AC · CS · TD) · kỹ thuật đã áp (ngưỡng có giá trị biên · trạng thái có cạnh cấm + 1 TC vòng đời) · mọi PASS đạt chuẩn kiểm · (wave ≥ 2) regression đã chạy lại. Contract/perf/security/resilience/migration chỉ thêm khi contract phức tạp / NFR yêu cầu / có đổi schema.
