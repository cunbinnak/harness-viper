# SECURITY — {{PROJECT_NAME}}

> Baseline bảo mật của bộ khung (**framework** — mọi project). Chạm dữ liệu người thật thì không có ngoại lệ "làm nhanh nên bỏ qua".
> Checklist tick ở `PRODUCTION-READY.md Nhóm 2` khi SHIP.

## §1 Secret
- Không secret trong code / commit / log / client bundle. `.env` trong `.gitignore` (mọi cấp, kể cả `deployment/local/.env`).
  `.env.example` chỉ **TÊN** biến + mô tả, không giá trị thật.
- Secret production ở dashboard PaaS, không máy cá nhân. Lỡ commit = **coi như đã lộ** → xoay key mới, đừng chỉ xoá commit.
- Secret **không có giá trị mặc định** trong config base/prod (`${JWT_SECRET}`, KHÔNG `${JWT_SECRET:dev-...}`); app **fail-fast** khi thiếu hoặc còn giá trị dev. Default chỉ ở profile `local`/`test`.

## §2 Đầu vào
- Mọi dữ liệu ngoài (form / query / header / webhook) validate schema ở **TẦNG SERVER**. Client validate chỉ để UX.
- Query DB qua tham số / ORM, **không nối chuỗi SQL**. Upload file: giới hạn size, kiểm loại thật, không lưu vào thư mục web-accessible.

## §3 Danh tính & phân quyền
- Đăng nhập dùng managed provider — không tự viết lưu mật khẩu.
- Mỗi truy vấn đọc/ghi dữ liệu người dùng kiểm **người đăng nhập CÓ QUYỀN với bản ghi này** (theo `PERSONAS.md §2 ma trận vai`),
  không chỉ "đã đăng nhập". Chặn ở **server**, UI không tính.
- Test tay: đăng nhập A, đổi id trên URL sang bản ghi B → **phải bị chặn**. Session hết hạn được, đăng xuất được.
- **JWT/OIDC**: kiểm chữ ký + `exp` + `iss` + `aud` (IdP đa tenant như Azure AD: thêm `tid`); thuật toán cố định. Định danh người dùng theo claim **bất biến** (`sub`/`oid`), KHÔNG theo `email`/`preferred_username`.
- **Thu hồi ngay** khi khoá tài khoản / đổi quyền / đặt lại mật khẩu: token cũ hết hiệu lực (blacklist bền qua restart, `tokenVersion`, hoặc kiểm trạng thái tài khoản mỗi request). Lockout đăng nhập theo **tài khoản**, không chỉ theo IP.

## §4 Đường ra
- HTTPS bắt buộc, redirect http→https. CORS chỉ mở domain của mình. Không trả stack trace / thông tin nội bộ ra response lỗi.
- Rate limit ít nhất cho: đăng nhập · đăng ký · endpoint ghi dữ liệu · endpoint gửi email/SMS.
- **Profile mặc định không fail-open**: `spring.profiles.active` không có default `local`/`dev`; endpoint chỉ-dev (`@Profile("local")`, ký token hộ) không được có trong build prod. Swagger/`/v3/api-docs`/actuator **tắt hoặc sau auth** ở prod.
- **Security header**: CSP · HSTS · `X-Content-Type-Options: nosniff` · `frame-ancestors`/`X-Frame-Options` · `Referrer-Policy` (nginx `add_header` hoặc `next.config` `headers()`). Cookie phiên: `HttpOnly` + `Secure` + `SameSite`.
- **Đứng sau reverse proxy**: lấy IP client qua proxy tin cậy (`server.forward-headers-strategy` + nginx `X-Forwarded-For`), không `getRemoteAddr()` trần (mọi user chung một bucket rate limit) và không tin `X-Forwarded-For` client tự gửi. List có **trần page size** (vd ≤ 100).

## §5 Dữ liệu
- Chỉ thu thập dữ liệu AC trong PRD cần — không "lưu sẵn cho sau này". Dữ liệu nhạy cảm (SĐT/địa chỉ/thanh toán): nói rõ lưu gì, dùng gì.
- Backup có + **đã thử khôi phục MỘT lần** (chưa thử = coi như chưa có). Không dùng dữ liệu production test ở local.

## §6 Phụ thuộc
- Chạy audit package manager trước publish; lỗ hổng nghiêm trọng → vá hoặc đổi thư viện. Không cài thư viện lạ chỉ vì một hàm tiện.
- **SCA bắt buộc ở VERIFY**: `./gradlew dependencyCheckAnalyze` (hoặc osv-scanner) + `npm audit --omit=dev --audit-level=high`. Không chạy được (mạng, thiếu plugin) → ghi MINOR kèm "cần kiểm chứng", không im lặng bỏ qua.

## §7 Ngoại lệ đã chấp nhận
> Mục nào cố tình bỏ qua thì ghi đây kèm điều kiện làm lại. Để trống mà lờ đi là cách sản phẩm chết.
> Ngoại lệ **CHỈ hợp lệ khi có dòng ở bảng này**. KG / DECISIONS / comment ghi "chấp nhận" KHÔNG thay được — reviewer không tha theo chúng.

| Mục | Vì sao chấp nhận | Rủi ro | Làm lại khi |
|---|---|---|---|
