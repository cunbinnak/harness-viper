<!-- gate bỏ qua TEMPLATE.* — copy thành docs/PERSONAS.md. Điền hết {{...}}. -->
<!-- VAI: BA (domain-ba C) — persona + ma trận sinh TỪ bảng luồng. -->
# PERSONAS — {{PROJECT_NAME}}

<!-- §1: mỗi persona = chân dung + năng lực được cấp + luồng chính. Đánh mã P-01, P-02… -->
## §1 Persona

### {{P-01}} — {{tên vai, vd Nhân viên order}}
- **Chân dung**: {{ai · mục tiêu · bối cảnh dùng}}
- **Năng lực được cấp**: {{tạo order · sửa order của mình · …}}
- **Luồng chính**: {{luồng ở INTERVIEW §Luồng nghiệp vụ mà vai này có dòng Ai LÀM}}

<!-- §2: MA TRẬN vai × hành động. Mỗi ô `có`/`cấm` — KHÔNG ô trống (gate DOCUMENT chặn: "PERSONAS §2 ma trận không ô trống").
     Đây là spec phân quyền khi code + nguồn TC âm + danh sách phép thử vai `breaker`. -->
## §2 Ma trận vai × hành động
| Hành động \ Vai | {{P-01}} | {{P-02}} | {{P-03}} |
|---|---|---|---|
| {{tạo order}} | có | cấm | có |
| {{xem order người khác}} | cấm | có | cấm |
| {{huỷ order đã duyệt}} | cấm | cấm | có |

<!-- §3: gán 6 lăng kính dogfood ↔ persona thật. Thứ tự chạy 2 đợt do `/dogfood` quyết, không ghi ở đây. -->
## §3 Gán vai dogfood
| Vai dogfood | Persona đóng |
|---|---|
| edge | {{P-01}} |
| newbie | {{P-02}} |
| picky | {{P-01}} |
| rushed | {{P-03}} |
| breaker | {{P-02}} |
| mobile | {{P-01}} |
