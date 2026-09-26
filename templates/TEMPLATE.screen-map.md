<!-- gate bỏ qua TEMPLATE.* — copy thành docs/ux/SCREEN-MAP.md. Mục lục màn ↔ module ↔ mockup ↔ FEAT:AC. -->
# SCREEN-MAP — {{PROJECT_NAME}}

<!-- MỖI MODULE NGHIỆP VỤ = 1 FILE mockup `docs/ux/mockups/<target>/<module>.html`, chứa ĐỦ màn của module + mọi tương tác
     (tab · modal · form · khuôn rỗng/lỗi/tải) dưới dạng section có `id`. MỖI ROW = 1 màn HOẶC 1 màn con (tab/modal/form).
     - Mã màn     : MỘT mã nối tất cả = `id` section trong mockup = `data-screen` trong mockup = `data-screen` trên trang FE.
                    Màn con: `<MÃ-CHA>--<tên>` (vd EMP-DETAIL--modal-deactivate).
     - URL mẫu    : URL MỞ ĐƯỢC NGAY, id lấy từ dữ liệu mẫu PRD §7 (= seed) — KHÔNG để `:id`.
     - Mockup     : CHỈ 2 dạng — `<module>.html#<Mã màn>` · hoặc `(Wave N)` khi màn thuộc wave sau (chưa vẽ).
     - Mở từ      : thao tác để tới màn này (từ màn nào, bấm gì) — picky làm y hệt ở mockup lẫn app.
     - Wave       : wave giao màn — gate + picky lọc màn in-scope theo cột này.
     Gate: row in-scope mà file không tồn tại HOẶC không có section `id` đúng Mã màn = đỏ (khai mà không vẽ). -->
| Mã màn | Module | Tên màn | Target | URL mẫu | Mockup | Mở từ | Wave | FEAT:AC | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| {{EMP-LIST}} | {{employee}} | {{Danh sách nhân viên}} | {{hrms-web}} | {{/employees}} | {{employee.html#EMP-LIST}} | {{menu Nhân sự}} | {{1}} | {{FEAT-001 AC-1,2}} | {{empty→CTA Thêm · lọc phòng ban}} |
| {{EMP-DETAIL--modal-deactivate}} | {{employee}} | {{Xác nhận nghỉ việc}} | {{hrms-web}} | {{/employees/NV0001}} | {{employee.html#EMP-DETAIL--modal-deactivate}} | {{EMP-DETAIL → bấm "Nghỉ việc"}} | {{1}} | {{FEAT-001 AC-5}} | {{confirm + lý do bắt buộc}} |
