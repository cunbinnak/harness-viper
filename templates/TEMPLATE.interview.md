<!-- gate bỏ qua TEMPLATE.* — copy thành docs/INTERVIEW.md.
     Đường INTERVIEW: điền §1, xoá §2.  ·  Đường INTAKE: xoá §1, GIỮ §2. Mục "Luồng nghiệp vụ đã xác nhận" GIỮ ở cả 2 đường (dòng `NGUỒN: INTAKE` ngoài comment —
     marker cho MAIN/top-up vòng sau nhận diện đường vào; máy đọc đường vào ở STATE.md dòng `Đường vào`). -->
<!-- VAI: PO (discovery-hypothesis) — lời kể/bằng chứng/cược · BA (domain-ba A) — §Luồng nghiệp vụ đã xác nhận (bảng luồng + màn nháp + câu hỏi mở). -->
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
| Mã màn | Module | Vai dùng | Hành động phải có trên màn | Dữ liệu hiển thị (mọi vùng, kể cả chỉ xem) |
|---|---|---|---|---|
| {{REC-LIST}} | {{recruitment}} | {{HR}} | {{tạo tin · lọc · mở ứng viên}} | {{danh sách tin (tiêu đề · phòng ban · trạng thái · số ứng viên) · ô lọc phòng ban (danh mục phòng ban) · badge số tin chờ duyệt}} |

Chính sách từng hành động:
<!-- domain-ba A.6 — mỗi dòng bảng luồng có thao tác trên hệ thống = 1 dòng. Research lấy dấu vết + suy luận 4 phép thử
     (lạm dụng · hạ nguồn chốt lúc nào · xung đột · vòng đời) → đề xuất mặc định, Author chọn. Không ô trống; không áp dụng → `n/a — <lý do>`.
     Nguồn: `Author` · `[luật] <link>` · `suy luận → Author chọn` · `suy luận + tham khảo <link> → Author chọn`. -->
| Hành động | Khi nào được làm | Ai | Giới hạn | Trạng thái tiền đề | Trùng / xung đột | Vi phạm thì | Ngoại lệ | Nguồn |
|---|---|---|---|---|---|---|---|---|
| {{Đăng ký làm từ xa}} | {{trước 17h ngày làm việc liền trước · không đăng ký lùi ngày}} | {{nhân viên}} | {{≤ 2 ngày/tuần}} | {{n/a — tạo mới}} | {{ngày đã có phép duyệt · ngày lễ}} | {{chặn, báo lý do}} | {{HR đăng ký hộ, bắt buộc ghi lý do}} | {{suy luận → Author chọn (chấm công chốt cuối ngày; không chặn thì đăng ký lùi để hợp thức hoá ngày vắng)}} |

Câu hỏi còn mở (hệ quả lên màn):
- {{Ai duyệt CV? A: HR → REC-DETAIL chỉ HR có nút duyệt · B: Trưởng phòng → thêm hàng chờ duyệt cho trưởng phòng}}

## Business rules  *(BA — domain-ba mục B; FEAT §3 trỏ về đây)*
**BR-{{slug}}** — {{phát biểu 1 câu}} · severity: {{CORNERSTONE | NORMAL}} · related_features: {{FEAT-…, FEAT-…}} · {{nền nếu cross-cutting}}
- Lý do + nguồn: {{luật / policy / quyết định Authority — kèm link nếu chuẩn ngành}}
- Khi nào áp dụng · ngoại lệ: {{…}}
- Phải chặn gì: {{điều không bao giờ được xảy ra}}
- Ví dụ: {{happy — số liệu}} · {{vi phạm — số liệu}}

## §2 Nguồn intake  *(đường INTAKE)*
NGUỒN: INTAKE
<!-- bảng truy vết: mỗi mục intake đã render vào FEAT/doc nào. -->
| Mục intake | → FEAT / doc |
|---|---|
| {{intake/PRD §capability X}} | {{FEAT-order-create}} |
