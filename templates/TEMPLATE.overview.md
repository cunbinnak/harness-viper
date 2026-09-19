<!-- gate bỏ qua TEMPLATE.* — copy thành docs/arch/OVERVIEW.md. Sơ đồ TỔNG; chi tiết per-target ở arch/<name>.md. -->
# ARCHITECTURE OVERVIEW — {{PROJECT_NAME}}

<!-- §1: bản đồ target — mỗi target + kind + ai gọi ai (dependency). -->
## §1 Boundary map
{{sơ đồ / danh sách target + kind + phụ thuộc}}

<!-- §2: tích hợp cross-boundary — cặp gọi nhau qua đâu, contract nào. -->
## §2 Tích hợp cross-boundary
| Từ → Đến | Qua (REST/event) | Contract |
|---|---|---|
| {{customer-web → order-service}} | REST | `order-service.api` |

<!-- §3: hạ tầng dùng chung. -->
## §3 Hạ tầng dùng chung
{{PostgreSQL · Redis · Kafka · …}}

<!-- §4: event-storming ghi vào đây — mỗi candidate domain (CAPABILITIES §2) một khối con `### <domain>`.
     Làm từng domain một; events ≥ vài cái (past-tense, chronological) · commands+actor · aggregates · hot-spots · external. -->
## §4 Event Storming
### {{order}}
- **Events** (past-tense, theo thời gian): {{OrderPlaced}} · {{OrderPaid}} · {{OrderShipped}} · {{OrderCancelled}} · …
- **Commands → event** (actor): {{PlaceOrder}} (customer) → {{OrderPlaced}} · {{CancelOrder}} (customer) → {{OrderCancelled}} · …
- **Aggregates** (+ state proto): {{Order — NEW → PAID → SHIPPED → CLOSED}}
- **Hot-spots** (chưa chắc/tranh cãi): {{ai được huỷ sau khi đã trả tiền?}}
- **External systems**: {{payment-gateway · warehouse}}
