<!-- gate bỏ qua TEMPLATE.* — copy thành docs/INTERVIEW.md.
     Đường INTERVIEW: điền §1, xoá §2.  ·  Đường INTAKE: xoá §1, GIỮ §2. Mục "Luồng nghiệp vụ đã xác nhận" GIỮ ở cả 2 đường (dòng `NGUỒN: INTAKE` ngoài comment —
     marker cho MAIN/top-up vòng sau nhận diện đường vào; máy đọc đường vào ở STATE.md dòng `Đường vào`). -->
# INTERVIEW — {{PROJECT_NAME}}

## §1 Bằng chứng phỏng vấn  *(đường INTERVIEW)*
<!-- Nhật ký theo đợt: mỗi lần /document (đầu = Wave 1; sau /next-wave = top-up) THÊM một khối ### Wave N mới,
     KHÔNG sửa/xoá khối wave cũ. Mỗi dòng gắn FEAT nó phục vụ (nếu có) để truy vết Bằng chứng → FEAT. -->

### Wave 1 — phỏng vấn nền
- {{câu hỏi Authority}} → **Bằng chứng**: {{trả lời}}  · _(FEAT: {{FEAT-… hoặc — nếu là nền chung}})_

<!-- Khối dưới chỉ thêm khi top-up wave sau (xoá comment này khi dùng):
### Wave 2 — top-up
- {{câu hỏi bổ sung cho FEAT mới của wave 2}} → **Bằng chứng**: {{trả lời}}  · _(FEAT: {{FEAT-…}})_
-->

## Luồng nghiệp vụ đã xác nhận  *(cả 2 đường vào — domain-ba mục A; Authority đọc từng dòng rồi ký)*
<!-- Ai LÀM = người thao tác trong hệ thống → actor của AC + ô `có` ma trận PERSONAS §2.
     Ai NHỜ/duyệt = người nêu nhu cầu hoặc phê duyệt — KHÔNG phải actor, trừ khi có thao tác riêng (dòng riêng).
     Bằng chứng = `§1 dòng N` · `[C] <link>` (chuẩn ngành) · `intake/<file>`. Không có → `CHƯA HỎI` = câu hỏi kế tiếp. -->
**Luồng: {{Tuyển dụng}}** — chốt bởi Authority: {{ngày ISO}}
| # | Ai LÀM | Làm gì | Ai NHỜ / duyệt | Đầu vào → đầu ra | Bằng chứng |
|---|---|---|---|---|---|
| 1 | {{HR}} | {{Đăng tin tuyển dụng}} | {{Bộ phận (nhờ, qua chat)}} | {{nhu cầu → tin đăng}} | {{§1 dòng 34}} |
| 2 | {{?}} | {{Duyệt CV đạt sàng lọc}} | {{?}} | {{hồ sơ → trạng thái}} | {{CHƯA HỎI}} |

Màn nháp:
| Mã màn | Module | Vai dùng | Hành động phải có trên màn |
|---|---|---|---|
| {{REC-LIST}} | {{recruitment}} | {{HR}} | {{tạo tin · lọc · mở ứng viên}} |

Câu hỏi còn mở (hệ quả lên màn):
- {{Ai duyệt CV? A: HR → REC-DETAIL chỉ HR có nút duyệt · B: Trưởng phòng → thêm hàng chờ duyệt cho trưởng phòng}}

## §2 Nguồn intake  *(đường INTAKE)*
NGUỒN: INTAKE
<!-- bảng truy vết: mỗi mục intake đã render vào FEAT/doc nào. -->
| Mục intake | → FEAT / doc |
|---|---|
| {{intake/PRD §capability X}} | {{FEAT-order-create}} |
