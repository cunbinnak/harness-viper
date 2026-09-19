---
name: review-mobile
description: Checklist review kind=mobile cho reviewer/bug-hunter ở /verify — soi app Flutter theo 6 trục (AC · bảo mật mobile · Forbidden patterns · data layer + offline · UI/cấu trúc/test · lệch thứ đã chốt). Mỗi mục có lệnh tìm và chỗ nhìn.
---

# Review Mobile

> Checklist review kind=mobile — reviewer/bug-hunter load ở /verify khi boundary là kind này. Report: [nặng/vừa/nhẹ]+file:dòng+hỏng-thế-nào+đề-xuất.

Bạn soi code với con mắt độc lập — **bạn không phải người viết nó**, và đó là giá trị của bạn.
Chỉ đọc. Không hỏi user.

## 1. Nạp trước

| Đọc | Để soi |
|---|---|
| `docs/feat/FEAT-*.md` boundary đảm nhận | trục 1 |
| `docs/ux/SCREEN-MAP.md` · `docs/ux/mockups/{name}/*.html` | trục 1, 5 |
| `docs/arch/{backend}.md §3 API` hoặc integration BFF trong `docs/arch/{name}.md` | trục 4 |
| `docs/arch/{name}.md §6.1` ca biên | trục 1 |
| `docs/PERSONAS.md §2` (ma trận vai × hành động) | trục 2 |
| skill `stack-flutter` §review + §Done | trục 3, 5 |
| `docs/DECISIONS.md` · `docs/adr/ADR-*.md` (state, storage, auth) | trục 6 |
| Wave ≥ 2: `docs/BACKWARD-COMPAT.md` §1 · `archive/wave-*/` | trục 6 |

## 2. Phạm vi

Code ở `services/mobile/{name}/`.

- **Vòng 1** — chưa có finding cho boundary này ở `STATE.md §Findings` → soi **cả boundary**.
- **Re-review** — đã review vòng trước → soi `git diff --stat <mốc>..HEAD` rồi `git diff <mốc>..HEAD`, và với **mỗi**
  finding của boundary MAIN báo đã sửa: mở đúng `file:dòng`, lỗi hết thật chưa. Mốc không còn trong git → soi cả boundary.

## 3. Chạy máy trước — đỏ là finding luôn

```bash
flutter analyze                    # 0 error
flutter test --coverage            # coverage/lcov.info — ngưỡng mobile 60%
dart run build_runner build --delete-conflicting-outputs && git diff --exit-code   # chỉ khi đi qua BFF
```
Đỏ → BLOCKER `type=test`. Coverage < 60% → BLOCKER.

## 4. Soi theo trục

`grep` chỉ để **tìm chỗ phải đọc** — mọi dòng dưới đây kết thúc bằng mở file ra đọc.

### Trục 1 — Đúng AC

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Mọi AC có màn/luồng làm đúng | AC → màn trong `SCREEN-MAP.md` → widget + provider + repository | không thấy = BLOCKER · làm nửa = MAJOR |
| Ca biên `arch/{name}.md §6.1` phía app: gửi hai lần · mất mạng giữa chừng · bản cũ. **Disable nút không tính** — ràng buộc thật ở BE, thiếu thì ghi finding cho boundary BE | Đọc mutation + màn | app thiếu = MINOR · BE thiếu = BLOCKER |

### Trục 2 — Bảo mật mobile (6 nhóm)

| Nhóm | Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|---|
| Secret | Không key/secret trong code hoặc asset | lệnh (a) | BLOCKER — lỡ commit thì **xoay key** |
| | Không log token/PII | `grep -rni -e "print(.*token" -e "log(.*token" -e "print(.*password" -e "print(.*otp" lib` | BLOCKER |
| Đầu vào | Tham số deep link/intent validate; WebView không load URL không tin, JS tắt khi không cần | `grep -rn -e uriLinkStream -e getInitialLink -e GoRoute -e WebView -e JavaScriptMode lib` | BLOCKER |
| Danh tính & phân quyền | Token + dữ liệu nhạy cảm trong secure storage (Keychain/Keystore) | `grep -rn SharedPreferences lib` → key nào chứa token/PII | BLOCKER |
| | Deep link tới màn cần quyền có route guard trong app **và** API chặn ở server; mỗi ô `cấm` của ma trận có chỗ chặn | Router `redirect` + endpoint tương ứng | server thiếu = BLOCKER (ghi cho BE) |
| | Đăng xuất xoá token + reset provider — đăng nhập B không thấy dữ liệu A | `grep -rn -e logout -e signOut lib` → `invalidate`/`dispose` | MAJOR |
| | Không persist dữ liệu sinh trắc học | `grep -rni biometric lib` | BLOCKER |
| Đường ra | Chỉ HTTPS; không bật cleartext; pinning cho API nhạy cảm nếu yêu cầu | `grep -rn "http://" lib` · `grep -rn usesCleartextTraffic android` · `grep -rn NSAllowsArbitraryLoads ios` | BLOCKER |
| | Không hiện exception/stack/message server thô lên UI | `grep -rn -e "Text(.*toString()" -e "Text(.*\.message" lib` | MAJOR |
| Dữ liệu | Không lưu dữ liệu nhạy cảm plain trong Hive/sqlite | `grep -rn -e "Hive." -e openDatabase lib` | MAJOR |
| | Obfuscation cho bản release nếu yêu cầu (`--obfuscate --split-debug-info`) | Script build/CI | MINOR |
| Phụ thuộc | Không package discontinued hoặc có lỗ hổng đã biết | `flutter pub outdated` | MAJOR |

```bash
# (a) secret hardcode
grep -rnE "(api[_-]?key|secret|password|token)\s*[:=]\s*[\"'][A-Za-z0-9_-]{12,}" lib assets
```

### Trục 3 — Forbidden patterns

Mở `stack-flutter` §review, đi **TỪNG dòng** bảng. Mỗi dòng tìm được trong code → một finding:
`description` mở bằng `[stack-flutter Forbidden: <cột Cấm>]`, `hậu quả thật` lấy từ cột `Vì sao` (viết cụ
thể cho chỗ này), `suggested fix` từ cột `Thay bằng`. Lệnh tìm cho các dòng chưa có ở trục 2:

```bash
grep -rlE "Dio\(|http\.(get|post|put|delete)\(" lib | grep -iE "widget|screen|page|view"   # widget gọi API
grep -rn -e "offline" -e "queue" -e "retry" lib        # mutation offline: có idempotency key sinh lúc tạo?
grep -rniE "price|total|discount|eligib" lib           # nghiệp vụ trong app
```

### Trục 4 — Data layer và offline

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| REST: client gọi đúng `arch/{backend}.md §3 API`; interceptor gắn auth + map lỗi | Đọc repository/client | sai endpoint = BLOCKER · khác = MAJOR |
| BFF: codegen up-to-date; operation khớp integration BFF trong `docs/arch/{name}.md` | Mục 3 | MAJOR |
| Offline queue: mọi mutation "queue if offline" có idempotency key, retry gửi lại cùng key | Lệnh trục 3 | BLOCKER |
| Không nghiệp vụ trong app — validate/tính ở BE/BFF | Lệnh trục 3 | BLOCKER |
| State: provider scope đúng (Riverpod theo ADR), không global state rò giữa màn | `grep -rn -e "StateProvider" -e "ChangeNotifierProvider" -e "static " lib` | MAJOR |

### Trục 5 — UI, cấu trúc, test

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Mỗi action có loading · error · success; bám `ux-{name}.md` + design system đã chốt (Material 3) | Đọc màn | MAJOR |
| Naming `snake_case.dart` / `PascalCase` class; folder feature-first (`features/` · `shared/` · `core/`) hoặc theo design | `find lib -type d` | MINOR · lệch cấu trúc đã chốt = MAJOR |
| Widget test cho màn/action chính; test không phụ thuộc mạng thật | `ls test` · đọc test đại diện | MAJOR |

### Trục 6 — Lệch thứ đã chốt

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Code làm khác một dòng `docs/DECISIONS.md` mà không có dòng mới đè lên | Mỗi dòng liên quan boundary → tìm chỗ code | MAJOR |
| State lib / storage / auth flow khác ADR | `pubspec.yaml` so với ADR | MAJOR |
| Wave ≥ 2: deep link/màn đã giao vẫn mở được; bản app cũ ngoài kia vẫn gọi được API | Router so với `archive/wave-*/` | BLOCKER |
| Thuật ngữ trên UI lệch FEAT/Glossary | Đọc label | MINOR |

## 5. Report finding

Trả finding về cho phiên chính — MAIN ghi vào `STATE.md §Findings`. Mỗi finding một dòng:

```
[severity] file:dòng — [nguồn] hỏng thế nào → đề xuất
```

- `[nguồn]`: `[FEAT-X AC-2]` · `[Bảo mật: <nhóm>]` · `[stack-flutter Forbidden: <cột Cấm>]` · `[ux <màn>]` · `[DECISIONS <ngày>]`.
- **BLOCKER (nặng)** — AC không chạy · lủng bảo mật · ghi trùng khi offline · phá surface đã giao.
  **MAJOR (vừa)** — nên sửa trước bàn giao. **MINOR/NIT (nhẹ)** — không chặn. **QUESTION** — chưa chắc.
  Ý thích cá nhân không bao giờ là BLOCKER.
- Re-review: mở đúng `file:dòng` MAIN báo đã sửa, xác nhận; còn lỗi → báo lại vì sao chưa hết.

## 6. Bốn luật cho mọi finding

1. **Hậu quả thật** — chuyện gì xảy ra với người dùng thật: mất dữ liệu · lộ dữ liệu · sai kết quả · AC
   không chạy · wave trước gãy. Viết không nổi câu này thì không phải finding.
2. **Trục sạch thì nói sạch** — ghi thẳng "trục N sạch" trong phần trả về; đừng bịa nhận xét cho có.
3. **Mở file ra đọc** — `file:dòng` phải là dòng đã đọc thật; không suy từ tên hàm.
4. **Không chắc → `QUESTION`**, cột `suggested fix` ghi **cách kiểm chứng**.

Không góp ý: đặt tên cho đẹp · tách file cho gọn · trừu tượng hoá "để sau dễ mở rộng" · tối ưu khi chưa có số đo.

## 7. Kết luận

- Sạch chỉ khi: không còn finding BLOCKER/MAJOR của boundary · analyze/test xanh ·
  coverage ≥ 60%.
- Không spawn fix, không tự loop — phiên chính đọc findings, tự sửa, rồi gọi bạn re-review.
