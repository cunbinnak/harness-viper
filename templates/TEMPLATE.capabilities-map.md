<!-- gate bỏ qua TEMPLATE.* — copy thành docs/CAPABILITIES-MAP.md. -->
# CAPABILITIES-MAP — {{PROJECT_NAME}}

<!-- capability TRƯỚC feature. Mỗi capability → outcome → FEAT. MỌI FEAT phải truy về ≥1 capability ở đây.
     Cột "Wave giao" để trống ở DOCUMENT (PLAN điền lúc chia wave); "Trạng thái" do /next-wave cập nhật. -->
## §1 Capability → FEAT
| Capability | Persona | Outcome (kết quả kinh doanh) | FEAT | Wave giao | Trạng thái |
|---|---|---|---|---|---|
| {{CAP-01}} — {{mô tả ngắn}} | {{P-01}} | {{kết quả đo được}} | {{FEAT-order-create}} | {{—}} | {{chưa giao}} |
| {{CAP-02}} — {{…}} | {{P-02}} | {{…}} | {{FEAT-…}} | {{—}} | {{chưa giao}} |

<!-- §2: gom capability (§1) theo core-entity/data chung thành domain candidate. Tên kebab (payment/auth/order).
     event-storming ĐỌC mục này (mỗi domain 1 section). Tên domain ở đây = tên section event-storming trong arch/OVERVIEW §4. -->
## §2 Candidate domains
| Domain candidate | Capability gom vào (§1) | Core entity / lý do gom | MVP/Phase |
|---|---|---|---|
| {{order}} | {{CAP-01, CAP-02}} | {{Order — cùng vòng đời đơn hàng}} | {{MVP}} |
| {{payment}} | {{CAP-03}} | {{Payment — dữ liệu thanh toán}} | {{Phase 2}} |
