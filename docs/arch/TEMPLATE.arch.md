<!-- gate bỏ qua TEMPLATE.* — copy thành docs/arch/<name>.md (1 file/target). Điền frontmatter + các §. -->
---
name: {{name}}                   # vd order-service, customer-web
kind: backend                    # backend | web | bff | mobile → quyết stack · scaffold · chạy thật · review
stack: spring-boot               # khớp skill stack-<tên>
consumes: []                     # target này GỌI API của ai: [menu-service.api] — nối contract
provides_api: true               # có phơi API cho consumer? → §3 là HỢP ĐỒNG (BACKWARD-COMPAT so với đây)
---

# arch: {{name}} ({{kind}})

<!-- §1: mô hình dữ liệu — entity/bảng chính + quan hệ. CHỈ của target này. -->
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

<!-- §4: ranh giới module — cái gì KHÔNG được gọi qua đường nào (chống logic sai tầng). -->
## §4 Ranh giới module
{{vd: controller không gọi thẳng repository — phải qua service}}

<!-- §5: event phát/nhận (nếu có), hoặc n/a. -->
## §5 Events
{{phát: OrderCreated · nhận: PaymentConfirmed}}
