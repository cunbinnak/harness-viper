<!-- gate bỏ qua TEMPLATE.* — copy thành docs/arch/OVERVIEW.md. Sơ đồ TỔNG; chi tiết per-target ở arch/<name>.md. -->
# ARCHITECTURE OVERVIEW — {{PROJECT_NAME}}

<!-- VAI: cả file = SA. §1 boundary-charter · §2-§3 technical-design · §4 event-storming · §5 system-design. -->

<!-- §1: bản đồ target — boundary-charter điền (mỗi target = 1 boundary, owned data không overlap). -->
## §1 Boundary map
| Target | kind | Mission (1 câu) | Owned data | Gọi ai (depends_on) |
|---|---|---|---|---|
| {{order-service}} | {{backend}} | {{nhận + quản lý vòng đời đơn}} | {{Order, OrderItem}} | {{menu-service}} |

<!-- §2 (technical-design): tích hợp cross-boundary — cặp gọi nhau qua đâu, contract nào + dòng "Luồng E2E chính" ở cuối. -->
## §2 Tích hợp cross-boundary
| Từ → Đến | Qua (REST/event) | Contract |
|---|---|---|
| {{customer-web → order-service}} | REST | `order-service.api` |

<!-- §3: hạ tầng dùng chung — DANH SÁCH; căn cứ chọn (số liệu, đánh đổi) ở §5. -->
## §3 Hạ tầng dùng chung
{{PostgreSQL · Redis · Kafka · …}}

<!-- §4: event-storming ghi vào đây — mỗi domain SA đã chốt (gợi ý ở CAPABILITIES §2) một khối con `### <domain>`.
     Làm từng domain một; events ≥ vài cái (past-tense, chronological) · commands+actor · aggregates · hot-spots · external. -->
## §4 Event Storming
### {{order}}
- **Events** (past-tense, theo thời gian): {{OrderPlaced}} · {{OrderPaid}} · {{OrderShipped}} · {{OrderCancelled}} · …
- **Commands → event** (actor): {{PlaceOrder}} (customer) → {{OrderPlaced}} · {{CancelOrder}} (customer) → {{OrderCancelled}} · …
- **Aggregates** (+ state proto): {{Order — NEW → PAID → SHIPPED → CLOSED}}
- **Hot-spots** (chưa chắc/tranh cãi): {{ai được huỷ sau khi đã trả tiền?}}
- **External systems**: {{payment-gateway · warehouse}}

<!-- §5: system-design ghi vào đây — TỈ LỆ THUẬN quy mô (5.2 quyết độ sâu). Đủ 5.1–5.9; không áp dụng → `n/a — <lý do>`, không bỏ trắng.
     Luôn bắt buộc kể cả dự án nhỏ: số instance · đứng sau proxy · môi trường · phân loại dữ liệu · bảng lớn. Gate DOCUMENT kiểm đủ mục + 5.7/5.8 có dòng. -->
## §5 System design

### 5.1 NFR → quyết định
| NFR (trích PRD §3) | Kịch bản đo được | Quyết định thiết kế kéo theo |
|---|---|---|
| {{p95 < 500ms}} | {{500 người chấm công lúc 8h00–8h10}} | {{ghi chấm công 1 bảng, không đồng bộ chéo service trong request}} |

### 5.2 Ước lượng tải
{{300 nhân viên × 2 lượt chấm công/ngày, dồn 80% vào 10 phút → ~0,8 req/s ghi cao điểm · đọc/ghi ≈ 5:1 · attendance ~220k dòng/năm}} → **Mức: {{Nhỏ}}**

### 5.3 Sơ đồ thành phần
```mermaid
flowchart LR
  user[{{Trình duyệt}}] --> proxy[{{nginx}}] --> api[{{hrms-backend}}] --> db[({{PostgreSQL}})]
```

### 5.4 Lưu trữ & mở rộng
| Nhóm dữ liệu / bảng | Owner | Mẫu truy cập | Kho | Sau 3 năm | Cache | Index / partition | Lưu giữ |
|---|---|---|---|---|---|---|---|
| {{attendance_record}} | {{hrms-backend}} | {{theo nhân viên + tháng}} | {{PostgreSQL}} | {{~660k dòng — LỚN}} | {{n/a — tải thấp}} | {{(employee_id, work_date)}} | {{5 năm}} |

### 5.5 Nhất quán theo luồng
| Luồng (bước bảng luồng) | Nhất quán ngay? | Cơ chế |
|---|---|---|
| {{Duyệt đơn phép → trừ số dư}} | {{có}} | {{1 transaction}} |

### 5.6 Chế độ lỗi & điểm chết đơn lẻ
| Thành phần | Chết / chậm thì | Người dùng thấy | Xử | Phục hồi |
|---|---|---|---|---|
| {{PostgreSQL}} | {{mọi ghi lỗi}} | {{thông báo thử lại}} | {{timeout 3s, không retry ghi}} | {{backup hằng ngày · RPO 24h}} |

### 5.7 Bảo mật riêng dự án
| Dữ liệu | Mức | Ai được xem | Bảo vệ |
|---|---|---|---|
| {{số CCCD · lương}} | {{PII · tài chính}} | {{HR · C&B · chính chủ}} | {{mã hoá cột · che log}} |

Mối đe dọa chính: {{token của tenant IdP khác → kiểm iss/aud/tid · khoá tài khoản mà token cũ còn sống → thu hồi}}
Xác thực: {{Azure AD OIDC · map người dùng theo oid}}

### 5.8 Triển khai & vận hành
| Target | Instance prod | Đứng sau | Stateless | Job / lock |
|---|---|---|---|---|
| {{hrms-backend}} | {{2}} | {{nginx}} | {{có}} | {{@Scheduled + ShedLock}} |

Môi trường: {{dev · sit · prod}} · Observability: {{log JSON + X-Request-ID · metric · cảnh báo theo 5.1}} · Backup: {{…}} · Rollback: {{cách quay về bản trước — /ship thử 1 lần}}

### 5.9 Quyết định lớn → ADR
- {{ADR-003 không dùng Kafka — 5.2 chỉ ~1 req/s ghi, Spring event + outbox đủ; xem lại khi > 50 req/s}}
