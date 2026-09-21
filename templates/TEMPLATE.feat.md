<!-- gate bỏ qua TEMPLATE.* — copy thành docs/feat/FEAT-<slug>.md. Điền hết {{...}}; gate check "còn {{ = chưa xong". -->
---
name: FEAT-{{slug}}
capability: CAP-{{id}}            # truy về docs/CAPABILITIES-MAP.md — MỌI FEAT phải có (gom nhóm theo capability, KHÔNG có Epic)
version: 1                       # bump khi sửa qua /document top-up ở wave sau
status: DRAFT                    # DRAFT → APPROVED (Authority ký ở /document bước cuối)
has_ui: true                     # true → cần mockup docs/ux/ · false → backend-only
consumes_contracts: []           # consumer (FE/bff): [order-service.api, ...] — nối contract BE↔FE
---

# FEAT-{{slug}} — {{tên feature}}

<!-- §1: 1 đoạn góc nhìn NGƯỜI DÙNG — feature xong thì ai làm được gì mà trước chưa. Không mô tả theo module. -->
## §1 Mục tiêu
{{mục tiêu}}

<!-- §2: mỗi AC = Given/When/Then đo được, đánh số AC-1, AC-2… Ca biên viết INLINE dưới mỗi AC.
     Cân nhắc bắt buộc: gửi 2 lần · rỗng · xoá · sai thứ tự · thu hồi quyền · concurrency · idempotency.
     `n/a` hợp lệ (ghi rõ) nhưng bỏ trống thì không. -->
## §2 Acceptance Criteria (BDD — testable)

### AC-1 — {{tên ngắn}}
- **Given** {{tiền đề}}
- **When** {{hành động}}
- **Then** {{kết quả đo được}}
- *Ca biên*: {{gửi 2 lần → lần 2 không tạo bản ghi trùng · rỗng → hiện trạng thái rỗng}}

<!-- §3: enforcement_location = chặn/kiểm Ở ĐÂU. Phải server/DB, UI disable KHÔNG tính. 1 dòng/AC hoặc /rule.
     Business-rule gắn 1-2 feature (domain-ba viết) ghi ở ĐÂY (dòng `BR-<slug>` + enforcement); rule nền/cross-cutting → docs/adr/. -->
## §3 Field kỹ thuật
| AC / rule | enforcement_location | Ghi chú |
|---|---|---|
| AC-1 | {{server: `OrderService.create` · DB: `unique(order, table_id) where active`}} | |

## §References
- Capability: `CAP-{{id}}` · BR liên quan: {{BR-… / ADR-… nếu có}} · Màn UI: {{SCREEN-MAP mục … nếu has_ui}}
