<!-- gate bỏ qua TEMPLATE.* — copy thành docs/feat/FEAT-<slug>.md. Điền hết {{...}}; gate check "còn {{ = chưa xong".
     VAI: frontmatter · §1 · §Ngoài phạm vi · §References = PO (domain-po, Bước 5 nhịp 1) · §2 · §3 = BA (domain-ba D, nhịp 2).
     FEAT KHÔNG chứa chặn ở đâu / contract / tên class-bảng-công nghệ — đó là SA ở docs/arch/{name}.md. -->
---
name: FEAT-{{slug}}
capability: CAP-{{id}}            # truy về docs/CAPABILITIES-MAP.md — MỌI FEAT phải có (gom nhóm theo capability, KHÔNG có Epic)
version: 1                       # bump khi sửa qua /document top-up ở wave sau
status: DRAFT                    # DRAFT → APPROVED (Authority ký ở /document bước cuối)
has_ui: true                     # true → cần mockup docs/ux/ · false → backend-only
---

# FEAT-{{slug}} — {{tên feature}}

<!-- §1 (PO): 1 đoạn góc nhìn NGƯỜI DÙNG — feature xong thì ai làm được gì mà trước chưa. Không mô tả theo module. -->
## §1 Mục tiêu
{{mục tiêu}}

<!-- §2 (BA): mỗi AC = Given/When/Then đo được, actor = cột Ai LÀM của bảng luồng, đánh số AC-1, AC-2… Ca biên viết INLINE dưới mỗi AC.
     Cân nhắc bắt buộc: gửi 2 lần · rỗng · xoá · sai thứ tự · thu hồi quyền · concurrency · idempotency.
     `n/a` hợp lệ (ghi rõ) nhưng bỏ trống thì không. -->
## §2 Acceptance Criteria (BDD — testable)

### AC-1 — {{tên ngắn}}
- **Given** {{tiền đề}}
- **When** {{hành động}}
- **Then** {{kết quả đo được}}
- *Ca biên*: {{gửi 2 lần → lần 2 không tạo bản ghi trùng · rỗng → hiện trạng thái rỗng}}

<!-- §3 (BA): điều KHÔNG BAO GIỜ được xảy ra — nói bằng lời nghiệp vụ, 1 dòng/AC hoặc /rule.
     Business-rule gắn ≥2 feature (chỉ 1 FEAT → là AC) ghi ở ĐÂY (dòng `BR-<slug>`); rule nền/cross-cutting → docs/adr/.
     Chặn Ở ĐÂU (server/DB, UI disable không tính) do SA ghi ở arch/{name}.md §6, cột AC/BR trỏ về dòng này. -->
## §3 Ràng buộc nghiệp vụ
| AC / BR | Phải chặn gì (không được xảy ra) | Nguồn |
|---|---|---|
| AC-1 | {{một bàn chỉ có một đơn đang mở}} | {{bảng luồng dòng 3 · BR-… }} |

<!-- §Ngoài phạm vi (PO). -->
## §Ngoài phạm vi
- {{điều FEAT này KHÔNG làm — để QC biết không test gì}}

<!-- §References (PO): dòng bảng luồng FEAT phủ — dòng có thao tác hệ thống mà không FEAT nào phủ = thiếu FEAT. -->
## §References
- Bảng luồng phủ: {{<nghiệp vụ> dòng 1-4}} · Capability: `CAP-{{id}}` · BR liên quan: {{BR-… / ADR-… nếu có}} · Màn UI: {{SCREEN-MAP mục … nếu has_ui}}
