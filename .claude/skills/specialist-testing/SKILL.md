---
name: specialist-testing
description: "Phương pháp QA cho test-writer — ba nguồn ra test case (AC · bảng chính sách · thăm dò ngoài tài liệu) + kỹ thuật thiết kế (phân vùng tương đương · giá trị biên · bảng quyết định · chuyển trạng thái) + chuẩn kiểm (điều kiện được ghi PASS) + dữ liệu đối kháng + regression theo phạm vi ảnh hưởng + dựng tiền đề (seed/fixture/mock/sandbox) + rigor chuyên sâu theo loại (contract · perf k6 · security OWASP · resilience · migration). test-writer LUÔN nạp."
---

# Specialist Testing Skill

> `test-writer` **LUÔN nạp** ở /verify: §Ba nguồn → §Kỹ thuật → §Chuẩn kiểm → §Dữ liệu đối kháng → §Thăm dò → §Regression theo phạm vi ảnh hưởng là phương pháp mọi wave ≥ 2. §Đợt kiểm chuyên sâu: wave có `SHIP`. §Rigor per loại dùng khi vượt CRUD (contract · perf · security · tenant isolation · resilience · migration).

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

Kết quả: hệ chặn hợp lý → `PASS` (ghi hành vi làm mốc) · hệ **cho phép điều phép thử chỉ ra là có hại** → `CHƯA CÓ QUY ĐỊNH` — nghĩa là *tài liệu (AC + bảng chính sách) không quy định ca này, hệ đang cho phép một việc có thể gây hại* — **KHÔNG phải FAIL** (code đúng tài liệu; thêm quy định hay không là quyết định của Authority): `thực tế / bằng chứng` ghi hành vi + phép thử + hệ quả (vd `201 lúc 18:05 · hạ nguồn: chấm công đã chốt → công ngày đó sai`). MAIN đưa vào báo cáo cuối VERIFY + `ROADMAP §backlog`.
Giới hạn **~5 thăm dò / hành động**, ưu tiên hành động chạm tiền · công · quyền.

## Regression theo phạm vi ảnh hưởng
**Mục đích**: bắt lỗi *nở ra ở chỗ đã PASS* — wave này đổi thứ X làm vỡ thứ Y đã giao. Bộ regression KHÔNG phải kho TC cộng dồn mãi rồi chạy lại nguyên mỗi wave: mỗi wave **chọn lại**, chỉ chạy lại TC cũ nằm trong vùng mà wave này làm ảnh hưởng tới. Phần lớn TC cũ nằm ở chỗ wave này không chạm tới — chạy lại chúng làm thời gian VERIFY tăng theo số wave mà hiếm khi bắt thêm lỗi.

**Nhãn**: `@regression` = "TC CŨ này được chọn chạy lại ở wave hiện tại" — chỉ gắn khi chép TC cũ sang `test-cases.md` của wave hiện tại. KHÔNG gắn cho TC mới viết ở wave hiện tại (lúc đó chưa biết wave sau sẽ đổi gì; wave sau tự chọn lại). Ngoại lệ duy nhất là `@smoke`: gắn lúc thiết kế cho **1 TC đi trọn mỗi luồng chính** (bảng luồng đã ký); `@smoke` luôn chạy lại mỗi wave và mỗi lượt sửa, không cần phân tích.

**Wave ≥ 2 — làm TRƯỚC khi viết TC mới (bước 3a).** QC đánh giá bằng **ngôn ngữ nghiệp vụ trên tài liệu**, KHÔNG đọc code: phạm vi ảnh hưởng suy từ FEAT / AC, luồng, vai, dữ liệu và bề mặt giao tiếp ghi ở `arch`. Người viết code không phải nguồn khai phạm vi (không tự khoanh phạm vi kiểm bài mình).
1. **Đọc thay đổi của wave**:
   - `docs/ROADMAP.md §1` hàng wave này: cột `AC in-scope` (AC cũ nào được top-up "bản 2"), `Phụ thuộc wave trước`, `Legacy được phép phá`; `§2` điều chỉnh khi mở.
   - **Tài liệu đổi từ lúc đóng wave trước**: mốc là commit đóng wave trước (`git log -1 --format=%H -- archive/wave-<N-1>`); xem `git diff <mốc>..HEAD -- docs/` (chỉ tài liệu, không phải code): FEAT / AC mới hoặc đổi, bảng luồng và bảng chính sách (`INTERVIEW`), vai và hành động (`PERSONAS §2`), bề mặt đã giao bị chạm (`BACKWARD-COMPAT §1`), `arch` (endpoint, event, bảng, mã lỗi, trạng thái thêm hoặc đổi) và các dòng `amend-arch` ở `DECISIONS`.
   - `knowledge-base/<target>.md` §Gotchas / §Failure-modes: cặp phụ thuộc ngầm đã từng gây lỗi.
   - Chức năng dùng chung theo nghiệp vụ (đăng nhập, phân quyền, gửi thông báo, lưu và tải file, lịch ngày lễ…): `arch/OVERVIEW.md` (§2 tích hợp · §3 hạ tầng dùng chung) và `arch/<target>.md §4`.
   - Mục `Chức năng cũ bị chạm` trong báo cáo của `reviewer` (Bước 2; MAIN chuyển nguyên văn trong prompt): nguồn độc lập về phụ thuộc ngầm trong code, đã dịch sang nghiệp vụ — mỗi dòng phải có dòng ảnh hưởng tương ứng ở đoạn `Phạm vi ảnh hưởng`.
2. **Suy ra TC cũ bị ảnh hưởng** — mỗi thay đổi tìm TC cũ theo bảy quan hệ dưới, trong `archive/wave-*/tracking/wave-*/test-cases.md` (mã TC có ở nhiều wave → lấy bản của wave MỚI NHẤT):

   | Wave này thay đổi | Chọn TC cũ nào | Tìm bằng |
   |---|---|---|
   | AC của FEAT đã giao (top-up) | TC cũ của AC đó và các AC cùng FEAT | cột `AC` |
   | Surface đã giao: thêm / đổi field, endpoint, mã lỗi, trạng thái, event | TC cũ gọi surface đó | endpoint ở cột `cách chạy`, `BACKWARD-COMPAT §1` |
   | Bảng / dữ liệu dùng chung (migration, thêm cột, thêm trạng thái) | TC cũ ghi, đọc hoặc đi qua trạng thái đó | tên bảng / trạng thái ở `mô tả` |
   | Gọi hoặc bị gọi bởi chức năng cũ (`Phụ thuộc wave trước`, `consumes`) | TC contract và TC luồng của bên cung cấp / bên dùng | cột `AC`, loại `contract` |
   | Quyền: hành động hoặc vai mới, đổi điều kiện (phạm vi, trạng thái) | TC phân quyền của hành động / vai đó | tên hành động, vai ở `mô tả` |
   | Luồng cũ thêm bước, hoặc nối sang luồng mới | TC đi qua điểm nối | bảng luồng `INTERVIEW` |
   | Chức năng dùng chung mà wave này làm đổi hoặc dùng thêm: đăng nhập / phiên, phân quyền chung, thông báo, lưu file, lịch / múi giờ, khung lỗi | mọi TC dùng chức năng đó | `arch/OVERVIEW.md §2-§3`, `knowledge-base` |

   Không chắc có ảnh hưởng hay không → **chọn**: chạy thừa vài TC rẻ hơn bỏ lọt lỗi nở. Thay đổi chạm chức năng dùng chung (dòng cuối) → chọn rộng, không chỉ `@smoke`.
3. **Ghi phạm vi** ở đầu `test-cases.md`, trước bảng, đoạn `## Phạm vi ảnh hưởng` (danh sách, KHÔNG phải bảng; khung ở `templates/TEMPLATE.test-cases.md`): mỗi dòng `thay đổi của wave → cái cũ bị ảnh hưởng → TC chọn: <mã>…`; thêm dòng `Luôn chạy: @smoke mọi luồng chính (<n> TC)` và `Không ảnh hưởng: <FEAT / vùng cũ> — <vì sao>`.
4. **Chép TC cũ được chọn** (cộng `@smoke` mọi luồng) vào bảng: giữ mã gốc · `nguồn` = `R` · `tag` có `@regression` · `kết quả` = `CHƯA CHẠY`. TC cũ hết hợp lệ vì AC đổi qua top-up → vẫn chép dòng, `kết quả` = `ĐÃ THAY` + `thực tế / bằng chứng` = `AC đổi ở <FEAT vN> → thay bằng <TC mới>`; TC mới phải PASS — không tự xoá dòng cũ (`bug-hunter` rà đề kiểm TC thay thế có thật).
5. Rồi mới **thiết kế TC mới** (AC · CS · TD). TC cho chỗ nối giữa chức năng mới và cũ (dữ liệu, quyền, luồng đi qua cả hai) thiết kế như TC thường.

**Chạy**: TC nguồn `R` và `@smoke` TRƯỚC TC mới. FAIL ở TC `R` = chỗ đã giao bị phá → **BLOCKER**.

**Fix-loop** (cùng phương pháp, quy mô nhỏ): vùng ảnh hưởng của lượt sửa suy từ **các finding vừa sửa** (MAIN chuyển nguyên danh sách mã finding; nội dung finding do reviewer / bug-hunter / persona báo, không phải MAIN khai): lấy AC, Mã màn, hành động, dữ liệu mà finding nêu → chọn TC (cũ và mới) thuộc vùng đó theo bảy quan hệ trên, chạy cùng FAIL + BLOCKED + `@smoke`. Không chạy lại cả bộ.

**Lỗi nở ngoài vùng đã chọn** (dogfood, persona hoặc lượt sau lộ lỗi ở chỗ không được chọn) = phân tích sót một phụ thuộc: viết 1 TC tái hiện (`mô tả` ghi mã finding) và MAIN ghi cặp phụ thuộc đó vào `knowledge-base/<target>.md` §Gotchas — wave sau bước 1 đọc lại.

## Đợt kiểm chuyên sâu — không chạy đủ mọi wave
Wave thường: perf · security · tenant isolation · resilience **chỉ** cho AC/NFR mà wave đó chạm (vd AC có ngưỡng thời gian phản hồi → đo đúng endpoint đó).
**Đợt kiểm sâu BẮT BUỘC** ở wave có `SHIP` trong cột `phases` của ROADMAP §1 (trước khi lên production — thường là wave cuối): chạy **toàn bộ** hệ đã giao, không chỉ AC wave đó:
- **performance**: k6 smoke + load theo NFR PRD §3 / OVERVIEW §5.1 trên các luồng chính.
- **security**: đủ nhóm OWASP ở §Rigor + SCA (`docs/SECURITY.md §6`) + mỗi endpoint public không token → 401.
- **tenant isolation** (sản phẩm nhiều tenant): §Rigor `tenant isolation` cho MỌI endpoint đọc/ghi.
- **resilience**: mỗi hệ ngoài ở OVERVIEW §5.6 chết/chậm → hệ phản ứng đúng như đã khai.
TC đợt sâu ghi chung `test-cases.md` (cột `loại` tương ứng). Ca chặn thật (lỗ bảo mật / rò tenant đã vá) có TC tái hiện — wave sau chọn lại nếu nằm trong vùng ảnh hưởng.

## test_type taxonomy — khi nào dùng + scope (SSOT của cột `loại`)
| group | Khi nào (wave strategy) | Scope | Nguồn input single-repo |
|---|---|---|---|
| `functional` | mọi wave (1 AC/1 luồng) | hẹp: 1 feature | `feat/FEAT-*.md` AC |
| `integration` | backend-heavy / full-stack | qua ranh giới target / BE↔FE contract | FEAT + `arch/{name}.md` (§3 API/events) + `adr/` |
| `e2e` | CHỈ full-stack (BE+FE chạy thật) | dài: nhiều màn hình UI→DB | `feat/FEAT-*.md` + `ux/` + FEAT |
| `performance` | backend-heavy / FEAT high-load | metric cụ thể (p95<Xms, RPS≥Y) | `arch/{name}.md` perf targets + ADR scaling + `PRD.md` NFR |
| `security` | mọi wave chạm auth/payment/PII | negative testing là chính | `docs/SECURITY.md` + `adr/` security + FEAT phân quyền |
| `install` | CHỈ target desktop | cài · chạy lần đầu · cập nhật · gỡ trên máy giả lập sạch | `arch/{name}.md` (desktop) + `PRODUCTION-READY` nhóm 5 — §Desktop |
| `accessibility` | CHỈ full-stack FE (WCAG 2.1 AA) | FE-only, ref WCAG criterion ID | `docs/ux/` + FEAT |

Ngoài 7 dòng trên, `loại` còn dùng: `contract` · `resilience` · `migration` · `isolation` (rigor ở §Rigor per loại; tenant isolation ghi `security`). `@smoke` / `@regression` là **tag**, không phải loại.

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
| **Event Kafka** (nhận từ target khác) | produce event giả đúng schema vào topic của hệ đang chạy (công cụ dòng lệnh của broker); không viết code test |

**Luật mock:**
- Mock tại **ranh giới ngoài cùng** (HTTP/SMTP/gateway/broker client) — **KHÔNG** mock service/repo **nội bộ** (mock nội bộ = test cái mock, che bug tích hợp thật).
- Fake data phải **hợp lệ nghiệp vụ** — đi qua **cùng validation/invariant** như data thật (seed thẳng DB thì tự đảm bảo ràng buộc). Fake bậy (bỏ qua rule) → **test đậu giả**, tệ hơn không test.
- Mock/stub xong **assert được tương tác** (đã gọi đúng endpoint/payload gì) — không chỉ "không nổ".
- Dọn seed/fixture cuối phase (luật #9) — không để rác data giữa các TC (gây phập phù).

## Rigor per loại
- **contract**: verify API/event contract khớp `docs/arch/{name}.md §3 API` / events.
  - Consumer-driven (Pact hoặc tương đương): consumer định nghĩa expectation → chạy kiểm tra phía provider trên hệ thật (VERIFY chạy local, không có CI).
  - Provider state setup cho từng interaction; verify path/method/field/enum/error code/response shape + event payload schema.
  - **Backward-compat (additive-only)**: thêm field optional / enum value OK; remove/rename/đổi type/bắt buộc field mới = **breaking → FAIL** (bắt sớm trước khi vỡ consumer).
- **regression**: xem §Regression theo phạm vi ảnh hưởng (tag `@regression`, không phải loại).
- **isolation**: unit/integration biên domain (mock infra) cho logic phức tạp / invariant.
- **tenant isolation** (`loại` = `security`; sản phẩm nhiều tenant/chi nhánh/công ty): dựng **2 bộ dữ liệu A và B** khác tenant, cùng cấu trúc. Với MỖI endpoint, đăng nhập A rồi:
  - **đọc**: gọi id bản ghi của B → bị chặn (thống nhất **403 hay 404** theo `arch §3` — không lẫn lộn mỗi endpoint một kiểu) · danh sách/tìm kiếm/xuất file/badge đếm của A **không lẫn** dữ liệu B;
  - **ghi**: sửa/xoá/duyệt bản ghi của B → bị chặn, đọc lại bản ghi B không đổi · tạo mới mà body/header tự khai `tenantId` của B → bị bỏ qua hoặc chặn, bản ghi thuộc A;
  - **cache**: A đọc trước, B đọc sau cùng khoá (cùng trang/cùng bộ lọc) → B KHÔNG nhận dữ liệu A từ cache;
  - **job/thông báo**: job chạy theo tenant không gửi/ghi chéo (email của A không tới người dùng B).
  Bất kỳ ca rò nào = **BLOCKER**.
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
- **accessibility** (WCAG 2.1 AA, CHỈ full-stack FE): keyboard nav, screen reader, color contrast, focus management; tool axe/Lighthouse; ref WCAG criterion ID (vd 2.1.1, 4.1.2). Chạy trên web đã nối backend thật. Không hoãn sang wave sau: AC a11y in-scope phải có TC PASS.
- **resilience/chaos** (khi NFR availability): inject downstream fail/timeout → verify timeout + circuit-breaker mở + fallback đúng; partial failure (DB commit nhưng event/cache fail) → reconcile/outbox bù.
- **migration** (khi đổi schema): chạy migration forward trên DB có data + verify **rollout an toàn** (thêm column NULLABLE → backfill → enforce NOT NULL ở migration sau); KHÔNG mất data, KHÔNG khoá bảng lâu.
- **architecture-drift** (tuỳ chọn — KHÔNG có trong khung, tự cài khi cần): đo coupling/cohesion + drift khỏi `arch/{name}.md` bằng **số** (metric). Mặc định `reviewer`/`bug-hunter` soi "logic sai tầng / ranh giới module" **định tính** là đủ. Project multi-boundary phức tạp cần đo bằng số → tự thêm skill wrap tool ngoài, vd [arcade-agent](https://github.com/lemduc/arcade-agent) (đa ngôn ngữ, MCP + CI drift-check). Cân dep nặng (tree-sitter) vs lợi ích trước khi thêm.

## Desktop — TC trên app đã đóng gói + TC cài đặt (target `kind: desktop`)
- **TC chức năng** chạy như web nhưng trên **app ĐÃ ĐÓNG GÓI** MAIN đang mở với `--remote-debugging-port=9222`: script tạm (ngoài repo, luật #9) nối `chromium.connectOverCDP('http://127.0.0.1:9222')`. Cột `cách chạy` ghi đủ bước để tái hiện.
- **TC cài đặt** (`loại` = `install`) chạy trên **máy giả lập sạch** — đóng vai máy người dùng mới, KHÔNG phải máy dev (máy dev có sẵn Node/runtime/dữ liệu cũ nên che lỗi). Windows Sandbox (Windows 10/11 Pro trở lên: file `.wsb` tạm ngoài repo, `LogonCommand` cài im lặng + chạy `--smoke` + ghi kết quả ra thư mục map) · không có Sandbox → máy ảo. Lần đầu dùng trong dự án: chạy thử một vòng, báo cách chạy được trong report → MAIN ghi `knowledge-base/{name}.md`.

| TC | Kiểm |
|---|---|
| Cài lần đầu | Máy không có Node / ffmpeg / runtime → cài xong, mở được, `--smoke` exit 0 |
| Không quyền admin | Tài khoản thường cài + chạy được (cài theo user) |
| Đường dẫn khó | Tài khoản / thư mục có dấu cách + tiếng Việt |
| Lần chạy đầu | Chưa có key / cấu hình → app dẫn người dùng, không văng lỗi |
| Cập nhật | Cài bản cũ → lên bản mới → dữ liệu + key còn nguyên |
| Gỡ | Gỡ xong không còn file cài / shortcut; dữ liệu `userData` xử đúng `DECISIONS` (giữ hay xoá) |
| Cảnh báo hệ điều hành | Bản chưa ký → SmartScreen hiện đúng như rủi ro đã chấp nhận ở `PRODUCTION-READY`; không bị diệt virus chặn |

- **Không có máy giả lập sạch** → KHÔNG viết nhóm `install` (không ghi PASS/BLOCKED giả); báo trong report "chưa kiểm cài đặt trên máy sạch" → MAIN ghi rủi ro chấp nhận ở `DECISIONS` + `PRODUCTION-READY` nhóm 5.

## Mobile (target `kind: mobile`) — chưa tự động
Khung chưa có công cụ lái emulator. TC gọi API của backend chạy như thường. TC UI của mobile do MAIN chạy tay trên emulator, ghi kết quả ngay tại dòng và gắn tag `@thủ-công` (`verify.md` Bước 3c). Không ghi PASS cho dòng chưa ai chạy.

## Done
- `tracking/wave-N/test-cases.md` đúng khung template: TC từ đủ 3 nguồn (AC · CS · TD) · kỹ thuật đã áp (ngưỡng có giá trị biên · trạng thái có cạnh cấm + 1 TC vòng đời) · mọi PASS đạt chuẩn kiểm · (wave ≥ 2) đoạn `Phạm vi ảnh hưởng` đủ + TC cũ được chọn đã chạy lại. Contract/perf/security/resilience/migration chỉ thêm khi contract phức tạp / NFR yêu cầu / có đổi schema.
