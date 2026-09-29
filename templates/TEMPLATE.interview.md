<!-- gate bỏ qua TEMPLATE.* — copy thành docs/INTERVIEW.md.
     Đường INTERVIEW: điền §1, xoá §2.  ·  Đường INTAKE: xoá §1, GIỮ §2 (dòng `NGUỒN: INTAKE` ngoài comment —
     marker cho MAIN/top-up vòng sau nhận diện đường vào; máy đọc đường vào ở STATE.md dòng `Đường vào`). -->
# INTERVIEW — {{PROJECT_NAME}}

## §1 Bằng chứng phỏng vấn  *(đường INTERVIEW)*
<!-- Nhật ký theo đợt: mỗi lần /document (đầu = Wave 1; sau /next-wave = top-up) THÊM một khối ### Wave N mới,
     KHÔNG sửa/xoá khối wave cũ. Mỗi dòng gắn FEAT nó phục vụ (nếu có) để truy vết Bằng chứng → FEAT. -->

### Wave 1 — phỏng vấn nền
- {{câu hỏi Authority}} → **Bằng chứng**: {{trả lời}}  · _(FEAT: {{FEAT-… hoặc — nếu là nền chung}})_

### Luồng nghiệp vụ đã xác nhận  *(Bước 1b — 1 bảng/nghiệp vụ; Authority đọc từng dòng rồi ký)*
<!-- Ai LÀM = người thao tác trong hệ thống → actor của AC + ô `có` trong ma trận PERSONAS §2.
     Ai NHỜ/duyệt = người nêu nhu cầu hoặc phê duyệt — KHÔNG phải actor, trừ khi họ có thao tác riêng (dòng riêng).
     Bằng chứng = số dòng §1. Không có → ghi `CHƯA HỎI` → đó là câu hỏi kế tiếp, không được đoán. -->
**Luồng: {{Tuyển dụng}}** — chốt bởi Authority: {{ngày ISO}}
| # | Ai LÀM | Làm gì | Ai NHỜ / duyệt | Đầu vào → đầu ra | Bằng chứng |
|---|---|---|---|---|---|
| 1 | {{HR}} | {{Đăng tin tuyển dụng}} | {{Bộ phận (nhờ, qua chat)}} | {{nhu cầu → tin đăng}} | {{§1 dòng 34}} |
| 2 | {{?}} | {{Duyệt CV đạt sàng lọc}} | {{?}} | {{hồ sơ → trạng thái}} | {{CHƯA HỎI}} |

<!-- Khối dưới chỉ thêm khi top-up wave sau (xoá comment này khi dùng):
### Wave 2 — top-up
- {{câu hỏi bổ sung cho FEAT mới của wave 2}} → **Bằng chứng**: {{trả lời}}  · _(FEAT: {{FEAT-…}})_
-->

## §2 Nguồn intake  *(đường INTAKE)*
NGUỒN: INTAKE
<!-- bảng truy vết: mỗi mục intake đã render vào FEAT/doc nào. -->
| Mục intake | → FEAT / doc |
|---|---|
| {{intake/PRD §capability X}} | {{FEAT-order-create}} |
