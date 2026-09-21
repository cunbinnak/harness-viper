<!-- gate bỏ qua TEMPLATE.* — copy thành docs/arch/<name>.md (1 file/target). Điền frontmatter + các §. -->
---
name: {{name}}                   # vd order-service, customer-web
kind: backend                    # backend | web | bff | mobile → quyết stack · scaffold · chạy thật · review
stack: spring-boot               # khớp skill stack-<tên>
consumes: []                     # target này GỌI API của ai: [menu-service.api] — nối contract
provides_api: true               # có phơi API cho consumer? → §3 là HỢP ĐỒNG (BACKWARD-COMPAT so với đây)
---

# arch: {{name}} ({{kind}})

<!-- §0: boundary-charter KHỞI TẠO (Bước 6 — trước technical-design): mission 1 câu + owned data (từ aggregates event-storming, không overlap target khác) + capabilities exposed/consumed + NON-NEGOTIABLES. -->
## §0 Mission
{{mission 1 câu · owned data · capabilities exposed/consumed · NON-NEGOTIABLES}}

<!-- §1: mô hình dữ liệu — entity/bảng chính + quan hệ (liên kết qua id, KHÔNG FK cross-boundary). CHỈ của target này. -->
## §1 Data model
{{entity + quan hệ}}

<!-- §2: luồng lõi — các bước xử lý chính (request → ghi/đọc → response). -->
## §2 Luồng lõi
{{luồng}}

<!-- §3: API = CONTRACT consumer đọc. Theo docs/CONVENTIONS.md §API (error envelope · status · header X-Tenant-ID · versioning). -->
## §3 API (contract)
| Method + Path | Request | Response | Ghi chú |
|---|---|---|---|
| `POST /orders` | {{body}} | {{201 + order}} | |

<!-- §4: CHỐT kiến trúc target (Layered HAY Hexagonal — không trộn) + ranh giới module — cái gì KHÔNG được gọi qua đường nào (chống logic sai tầng) + auth/permission enforce ở tầng nào. -->
## §4 Ranh giới module
- Kiến trúc: {{Layered | Hexagonal}} (layout: `ref-{{kind}}-pattern`)
- {{vd: controller không gọi thẳng repository — phải qua service}}
- Auth/permission: {{enforce ở đâu}}

<!-- §5: event phát/nhận (nếu có), hoặc n/a. -->
## §5 Events
{{phát: OrderCreated · nhận: PaymentConfirmed}}

<!-- §6: bảng TRA ca biên — 8 dòng E1-E8 bắt buộc RÀ HẾT (`n/a — <lý do>` hợp lệ, Ô TRỐNG thì không).
     Cột Enforce trỏ thứ CHẶN ĐƯỢC: unique index · cột version + WHERE version=? · idempotency key · DB constraint · state machine. "Validate ở service" = chưa quyết gì. Ca biên riêng target → thêm E9+. -->
## §6 Ca biên (bảng TRA: Tình huống → Xử lý)
| # | Tình huống | Xử lý | Enforce ở đâu |
|---|---|---|---|
| E1 | Gửi hai lần | {{…}} | {{unique index / idempotency key}} |
| E2 | Sửa đồng thời | {{…}} | {{cột version + WHERE version=?}} |
| E3 | Xoá (đang được dùng) | {{…}} | {{…}} |
| E4 | Gọi sai thứ tự | {{…}} | {{state machine}} |
| E5 | Hỏng nửa chừng | {{…}} | {{transaction / outbox}} |
| E6 | Đọc bản cũ | {{…}} | {{…}} |
| E7 | Rỗng | {{…}} | {{…}} |
| E8 | Quyền thu hồi giữa chừng | {{…}} | {{…}} |
