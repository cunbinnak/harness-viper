# SECURITY — {{PROJECT_NAME}}

> Baseline bảo mật của bộ khung (**framework** — mọi project). Chạm dữ liệu người thật thì không có ngoại lệ "làm nhanh nên bỏ qua".
> Checklist tick ở `PRODUCTION-READY.md Nhóm 2` khi SHIP.

## §1 Secret
- Không secret trong code / commit / log / client bundle. `.env` trong `.gitignore` (mọi cấp, kể cả `deployment/local/.env`).
  `.env.example` chỉ **TÊN** biến + mô tả, không giá trị thật.
- Secret production ở dashboard PaaS, không máy cá nhân. Lỡ commit = **coi như đã lộ** → xoay key mới, đừng chỉ xoá commit.

## §2 Đầu vào
- Mọi dữ liệu ngoài (form / query / header / webhook) validate schema ở **TẦNG SERVER**. Client validate chỉ để UX.
- Query DB qua tham số / ORM, **không nối chuỗi SQL**. Upload file: giới hạn size, kiểm loại thật, không lưu vào thư mục web-accessible.

## §3 Danh tính & phân quyền
- Đăng nhập dùng managed provider — không tự viết lưu mật khẩu.
- Mỗi truy vấn đọc/ghi dữ liệu người dùng kiểm **người đăng nhập CÓ QUYỀN với bản ghi này** (theo `PERSONAS.md §2 ma trận vai`),
  không chỉ "đã đăng nhập". Chặn ở **server**, UI không tính.
- Test tay: đăng nhập A, đổi id trên URL sang bản ghi B → **phải bị chặn**. Session hết hạn được, đăng xuất được.

## §4 Đường ra
- HTTPS bắt buộc, redirect http→https. CORS chỉ mở domain của mình. Không trả stack trace / thông tin nội bộ ra response lỗi.
- Rate limit ít nhất cho: đăng nhập · đăng ký · endpoint ghi dữ liệu · endpoint gửi email/SMS.

## §5 Dữ liệu
- Chỉ thu thập dữ liệu AC trong PRD cần — không "lưu sẵn cho sau này". Dữ liệu nhạy cảm (SĐT/địa chỉ/thanh toán): nói rõ lưu gì, dùng gì.
- Backup có + **đã thử khôi phục MỘT lần** (chưa thử = coi như chưa có). Không dùng dữ liệu production test ở local.

## §6 Phụ thuộc
- Chạy audit package manager trước publish; lỗ hổng nghiêm trọng → vá hoặc đổi thư viện. Không cài thư viện lạ chỉ vì một hàm tiện.

## §7 Ngoại lệ đã chấp nhận
> Mục nào cố tình bỏ qua thì ghi đây kèm điều kiện làm lại. Để trống mà lờ đi là cách sản phẩm chết.

| Mục | Vì sao chấp nhận | Rủi ro | Làm lại khi |
|---|---|---|---|
