<!-- gate bỏ qua TEMPLATE.* — copy thành docs/PERSONAS.md. Điền hết {{...}}. -->
# PERSONAS — {{PROJECT_NAME}}

<!-- §1: mỗi persona = chân dung + năng lực được cấp + luồng chính. Đánh mã P-01, P-02… -->
## §1 Persona

### {{P-01}} — {{tên vai, vd Nhân viên order}}
- **Chân dung**: {{ai · mục tiêu · bối cảnh dùng}}
- **Năng lực được cấp**: {{tạo order · sửa order của mình · …}}
- **Luồng chính**: {{FEAT/journey liên quan}}

<!-- §2: MA TRẬN vai × hành động. Mỗi ô `có`/`cấm` — KHÔNG ô trống (gate table_cells chặn).
     Đây là spec phân quyền khi code + nguồn TC âm + danh sách phép thử vai `breaker`. -->
## §2 Ma trận vai × hành động
| Hành động \ Vai | {{P-01}} | {{P-02}} | {{P-03}} |
|---|---|---|---|
| {{tạo order}} | có | cấm | có |
| {{xem order người khác}} | cấm | có | cấm |
| {{huỷ order đã duyệt}} | cấm | cấm | có |

<!-- §3: gán 6 lăng kính dogfood ↔ persona thật + đợt (1 = DB sạch, 2 = DB có data). -->
## §3 Gán vai dogfood
| Vai dogfood | Persona đóng | Đợt |
|---|---|---|
| edge | {{P-01}} | 1 |
| newbie | {{P-02}} | 1 |
| picky | {{P-01}} | 1 |
| rushed | {{P-03}} | 2 |
| breaker | {{P-02}} | 2 |
| mobile | {{P-01}} | 2 |
