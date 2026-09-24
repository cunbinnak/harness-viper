---
name: stack-flutter
description: Stack mobile Flutter/Dart — scaffold · convention · make · §review (forbidden patterns cho reviewer/bug-hunter). Load khi target kind=mobile.
---

# stack-flutter

> Idiom Flutter/Dart (cross-stack ở `docs/CONVENTIONS.md`; bảo mật ở `SECURITY.md`).
> Load khi BUILD/VERIFY target có frontmatter `kind: mobile`.

## §1 Khi load
BUILD target mobile (scaffold/code) · VERIFY (reviewer/bug-hunter đọc **§review**).

## §2 Scaffold
- Vào `services/mobile/<name>/`. kind=mobile. Dùng **`flutter create`** — không chép boilerplate.
- Cấu trúc **feature-first**: `lib/features/` · `lib/shared/` · `lib/core/` (hoặc theo design đã chốt). Data layer + provider tách khỏi widget NGAY.
- **Data layer** theo `docs/arch/{name}.md`:
  - **Default — REST trực tiếp backend**: client (Dio/http) gọi contract `docs/arch/{backend}.md`; interceptor gắn auth + map error.
  - **Optional — qua BFF/GraphQL**: CHỈ khi design có boundary `bff`. `flutter pub run build_runner build` refresh trước khi code; wire ops theo `docs/arch/{name}.md §3`; KHÔNG invent op name.
- Config env / flavor (dev/prod); secret KHÔNG vào code/asset. `git commit`.

## §3 Convention (Flutter/Dart — bắt buộc)
- **Widget**: implement theo `docs/ux/` (mockup) + `docs/arch/{name}.md`, Material 3 (hoặc design system đã chốt). **NO business logic trong app** — validate ở backend (hoặc BFF).
- **Data layer**: **Repository + provider**; widget KHÔNG gọi API trực tiếp. Wire actions map đúng endpoint/op integration design; handle loading / error / success.
- **State**: Riverpod 2 (hoặc state mgmt đã chốt); scope provider per child; **invalidate khi logout** (không giữ dữ liệu user sống qua đăng xuất).
- **Auth**: theo auth flow đã chốt (deep-link / token refresh). Token/dữ liệu nhạy cảm → **secure storage** (Keychain/Keystore), KHÔNG `SharedPreferences`.
- **Deep link / intent**: validate tham số; **route guard** trong app + server chặn API (không chỉ giấu nút). WebView: whitelist host/path, tắt JS khi không cần.
- **Offline queue**: mutation "queue if offline" cần **idempotency key** sinh lúc tạo mutation, gửi lại cùng key mỗi lần retry.
- **Error**: map error code → thông báo theo `docs/ux/`; KHÔNG hiện `exception.toString()`/stack/message server lên UI.
- **Secret**: API key/secret KHÔNG trong code/asset (giải nén APK/IPA là thấy) — server giữ; key public thì giới hạn theo package/bundle id. KHÔNG lưu dữ liệu sinh trắc học.
- **Network**: HTTPS; không cleartext traffic; pinning cho API nhạy cảm nếu yêu cầu.
- **Log**: logger có mask, tắt log ở release; KHÔNG `print`/`debugPrint` token/PII.
- **Naming**: file `snake_case.dart` · class/widget `PascalCase` · test `{module}_test.dart`.
- **Test**: `flutter_test` widget; coverage ≥ **60%**.

## §4 make (điền thân vào `services/mobile/<name>/Makefile` — root Makefile dispatch tới)
```
dev     : flutter run                       # "chạy thật" = emulator/thiết bị (KHÔNG docker)
check   : flutter analyze && flutter test
test    : flutter test
build   : flutter build apk --debug
```

## §review  (reviewer/bug-hunter soi TỪNG DÒNG — forbidden patterns Flutter/mobile)
| Cấm | Hậu quả thật | Thay bằng |
|---|---|---|
| Token/dữ liệu nhạy cảm trong `SharedPreferences` | Máy root hoặc bản backup đọc được | Secure storage (Keychain/Keystore) |
| API key/secret trong code hoặc asset | Giải nén APK/IPA là thấy | Server giữ secret; key public thì giới hạn theo package/bundle id |
| Widget gọi API trực tiếp | Đổi API là sửa khắp nơi; không test được | Repository + provider |
| Mutation offline retry không có idempotency key | Mạng chập chờn là ghi hai lần | Key sinh lúc tạo mutation, gửi lại cùng key mỗi lần retry |
| Hiện `exception.toString()`/stack/message server lên UI | Lộ nội bộ; người dùng không biết làm gì | Map error code → thông báo theo `docs/ux/` |
| Deep link mở thẳng màn cần quyền, chỉ dựa vào giấu nút | Vai bị cấm vẫn vào được bằng link | Route guard trong app + server chặn API |
| Tham số deep link/intent không validate; WebView load URL từ ngoài, bật JS thừa | Mở màn với dữ liệu giả; XSS trong WebView | Whitelist host/path; tắt JS khi không cần |
| Log token/PII bằng `print`/`debugPrint` | Logcat/console đọc được | Logger có mask; tắt log ở release |
| Gọi HTTP thường, bật cleartext traffic | Nghe lén trên wifi công cộng | HTTPS; pinning cho API nhạy cảm nếu yêu cầu |
| Tính nghiệp vụ trong app | Bản app cũ ngoài kia tính theo luật cũ | Backend trả kết quả |
| Provider giữ dữ liệu user sống qua đăng xuất | Đăng nhập B vẫn thấy dữ liệu A | Scope provider; invalidate khi logout |
| Lưu dữ liệu sinh trắc học | Không thu hồi được khi lộ | Dùng API sinh trắc của OS, không lưu |

## §done
Build apk debug pass, `flutter analyze` pass, test ≥60%; no hardcoded key / biometric persisted; file chỉ trong `services/mobile/<name>/`; KG cập nhật.
