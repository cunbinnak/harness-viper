---
name: review-desktop
description: Checklist review kind=desktop cho reviewer/bug-hunter ở /verify — soi app Electron (Windows) theo 6 trục (AC · bảo mật desktop · Forbidden patterns · IPC + dữ liệu cục bộ · UI/cấu trúc/test · lệch thứ đã chốt). Mỗi mục có lệnh tìm và chỗ nhìn.
---

# Review Desktop

> Checklist review kind=desktop — reviewer/bug-hunter load ở /verify khi target là kind này. Report: [BLOCKER/MAJOR/MINOR]+file:dòng+hỏng-thế-nào+đề-xuất.

Bạn soi code với con mắt độc lập — **bạn không phải người viết nó**, và đó là giá trị của bạn.
Chỉ đọc. Không hỏi user.

## 1. Nạp trước

| Đọc | Để soi |
|---|---|
| `docs/feat/FEAT-*.md` target đảm nhận | trục 1 |
| `docs/ux/SCREEN-MAP.md` · `docs/ux/mockups/{name}/*.html` | trục 1, 5 |
| `docs/arch/{name}.md §3` (hợp đồng IPC) · §1 (dữ liệu cục bộ) · §6 ca biên | trục 1, 4 |
| `docs/PERSONAS.md §2` (ma trận vai × hành động) | trục 2 |
| skill `stack-electron` §review + §done — **ĐÃ nạp ở Bước 0 (định nghĩa agent), KHÔNG Read lại** | trục 3, 5 |
| `docs/DECISIONS.md` · `docs/adr/ADR-*.md` (đóng gói, cập nhật, lưu trữ) | trục 6 |
| Wave ≥ 2: `docs/BACKWARD-COMPAT.md` §1 · `archive/wave-*/` | trục 6 |

## 2. Phạm vi

Code ở `services/desktop/{name}/`.

- **Vòng 1** — chưa có finding cho target này ở `STATE.md §Findings` → soi **cả target**.
- **Re-review** — đã review vòng trước → soi `git diff --stat <mốc>..HEAD` rồi `git diff <mốc>..HEAD`, và với **mỗi**
  finding MAIN báo đã sửa: mở đúng `file:dòng`, lỗi hết thật chưa. Mốc không còn trong git → soi cả target.

## 3. Chạy máy trước — đỏ là finding luôn

```bash
npm run typecheck && npm run lint
npm run test -- --coverage           # ngưỡng desktop 60%
npm run package && make doctor       # bản đóng gói chạy --smoke, exit 0
```
Đỏ → BLOCKER `type=test`. Coverage < 60% → BLOCKER.

## 4. Soi theo trục

`grep` chỉ để **tìm chỗ phải đọc** — mọi dòng dưới đây kết thúc bằng mở file ra đọc.

### Trục 1 — Đúng AC

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Mọi AC có màn/luồng làm đúng | AC → màn trong `SCREEN-MAP.md` → component renderer → kênh IPC → handler main | không thấy = BLOCKER · làm nửa = MAJOR |
| Ca biên `arch/{name}.md §6` phía app: bấm hai lần · tắt app giữa lúc xử lý · file hỏng/rỗng · mất mạng khi gọi dịch vụ ngoài | Đọc handler + màn | MAJOR · mất dữ liệu = BLOCKER |

### Trục 2 — Bảo mật desktop

| Nhóm | Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|---|
| Cô lập renderer | `contextIsolation` · `nodeIntegration` · `sandbox` · `webSecurity` giữ mặc định an toàn | `grep -rn -e nodeIntegration -e contextIsolation -e "sandbox:" -e webSecurity src` | BLOCKER |
| | Preload chỉ lộ hàm hẹp | `grep -rn exposeInMainWorld src` → đọc từng hàm | BLOCKER |
| Đầu vào IPC | Mỗi handler kiểm kiểu + đường dẫn trong vùng cho phép | `grep -rn -e "ipcMain.handle" -e "ipcMain.on" src` → mỗi handler tìm chỗ kiểm | BLOCKER |
| | Tiến trình con nhận mảng đối số, không ghép chuỗi shell | `grep -rnE "exec\(|execSync\(|shell: *true" src` | BLOCKER |
| Đường ra | Link ngoài chỉ `https:` đã kiểm; chặn điều hướng lạ + cửa sổ mới | `grep -rn -e openExternal -e will-navigate -e setWindowOpenHandler src` | BLOCKER |
| Secret | API key mã hoá bằng `safeStorage`; không nằm trong code, log, renderer | `grep -rniE "api[_-]?key|token|secret" src` → đọc chỗ lưu | BLOCKER |
| | Không key hardcode | `grep -rnE "(api[_-]?key|secret|token)\s*[:=]\s*[\"'][A-Za-z0-9_-]{12,}" src` | BLOCKER — lỡ commit thì **xoay key** |
| Bản phát hành | Fuse tắt `RunAsNode` + `EnableNodeCliInspectArguments`; không mở cổng gỡ lỗi ngoài dogfood | `grep -rn FuseV1Options forge.config.*` · `grep -rn remote-debugging src` | MAJOR |
| Log | File log không chứa key/PII | Đọc chỗ ghi log | MAJOR |
| Phụ thuộc | Không gói có lỗ hổng đã biết | `npm audit --omit=dev` | MAJOR |

### Trục 3 — Forbidden patterns

Mở `stack-electron` §review, đi **TỪNG dòng** bảng. Mỗi dòng tìm được trong code → một finding:
`description` mở bằng `[stack-electron Forbidden: <cột Cấm>]`, `hậu quả thật` lấy từ cột `Hậu quả thật` (viết cụ
thể cho chỗ này), `suggested fix` từ cột `Thay bằng`. Lệnh tìm cho các dòng chưa có ở trục 2:

```bash
grep -rnE "getPath\(['\"](exe|appPath)|process\.cwd\(\)|C:\\\\" src     # ghi cạnh file cài / đường dẫn cứng
grep -rnE "readFileSync|writeFileSync|execSync" src/main                 # việc chặn main process
grep -rniE "price|total|discount|eligib" src/renderer                    # nghiệp vụ trong renderer
```

### Trục 4 — IPC và dữ liệu cục bộ

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Kênh IPC khớp hợp đồng `arch/{name}.md §3` (tên · tham số · kết quả · mã lỗi); kiểu dùng chung một nơi | `src/shared/ipc.ts` vs `arch §3` | sai kênh = BLOCKER · lệch kiểu = MAJOR |
| Dữ liệu người dùng chỉ ở `userData`; cập nhật bản mới không xoá | Đọc chỗ ghi file / DB | BLOCKER |
| Ghi file dở dang không làm hỏng dữ liệu (ghi tạm rồi đổi tên) khi tắt app giữa chừng | Đọc chỗ ghi | MAJOR |
| Việc nặng có tiến độ + huỷ được, không treo cửa sổ | Đọc tiến trình con / `utilityProcess` | MAJOR |

### Trục 5 — UI, cấu trúc, test

> **BƯỚC 5.0 — SOI HÌNH DẠNG CÂY TRƯỚC.** (1) cấu trúc chốt ở `arch §4`/ADR · (2) `find src -type d` dump cây THẬT · (3) phân loại: tách main · preload · renderer · shared chưa? · (4) lệch = **MAJOR** (renderer và main trộn một chỗ = BLOCKER).

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Mỗi action có loading · error · success; bám `SCREEN-MAP` + mockup + design system đã chốt; `data-screen`/`data-ds` đủ | Đọc màn | MAJOR |
| Có test IPC handler + e2e trên bản đóng gói (`ref-desktop-test`) | `ls tests` · đọc test đại diện | MAJOR |

### Trục 6 — Lệch thứ đã chốt

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Code làm khác một dòng `docs/DECISIONS.md` mà không có dòng mới đè lên | Mỗi dòng liên quan target → tìm chỗ code | MAJOR |
| **`amend-arch`** (PROTOCOL §3): mỗi thay đổi `docs/arch/*.md` sau khoá scope có dòng `DECISIONS` loại `amend-arch` · truy về AC/Mã màn đã khoá · chỉ THÊM · không kèm sửa FEAT/mockup/PRD | `git log --oneline <mốc>..HEAD -- docs/` → `git show` từng commit, đối chiếu `DECISIONS` | thiếu điều kiện = MAJOR · đổi/xoá surface đã giao = BLOCKER |
| Electron version / cách đóng gói / cập nhật khác `TECHSTACK.md` + ADR | `package.json` · `forge.config.*` vs `docs/TECHSTACK.md` | MAJOR |
| Wave ≥ 2: dữ liệu bản cũ đọc được ở bản mới; kênh IPC đã giao không đổi nghĩa | So với `archive/wave-*/` | BLOCKER |

## 5. Report finding

Trả finding về cho phiên chính — MAIN ghi vào `STATE.md §Findings`. Mỗi finding một dòng:

```
[severity] file:dòng — [nguồn] hỏng thế nào → đề xuất
```

- `[nguồn]`: `[FEAT-X AC-2]` · `[Bảo mật: <nhóm>]` · `[stack-electron Forbidden: <cột Cấm>]` · `[ux <màn>]` · `[DECISIONS <ngày>]`.
- **BLOCKER** — AC không chạy · lủng bảo mật · mất dữ liệu người dùng · phá surface đã giao.
  **MAJOR** — nên sửa trước bàn giao. **MINOR** — không chặn. **QUESTION** — chưa chắc.
  Ý thích cá nhân không bao giờ là BLOCKER.
- Re-review: mở đúng `file:dòng` MAIN báo đã sửa, xác nhận; còn lỗi → báo lại vì sao chưa hết.

## 6. Bốn luật cho mọi finding

1. **Hậu quả thật** — chuyện gì xảy ra với người dùng thật: mất dữ liệu · lộ key · máy bị điều khiển · AC
   không chạy · wave trước gãy. Viết không nổi câu này thì không phải finding.
2. **Trục sạch thì nói sạch** — ghi thẳng "trục N sạch" trong phần trả về; đừng bịa nhận xét cho có.
3. **Mở file ra đọc** — `file:dòng` phải là dòng đã đọc thật; không suy từ tên hàm.
4. **Không chắc → `QUESTION`**, cột `suggested fix` ghi **cách kiểm chứng**.

## 7. Kết luận

- Sạch chỉ khi: không còn finding BLOCKER/MAJOR của target · typecheck/lint/test xanh · coverage ≥ 60% · `make doctor` exit 0.
- Không spawn fix, không tự loop — phiên chính đọc findings, tự sửa, rồi gọi bạn re-review.
