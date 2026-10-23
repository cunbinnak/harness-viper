---
name: stack-electron
description: Stack desktop Windows — Electron + React/TS (Electron Forge) — scaffold · convention · make · §review (forbidden patterns cho reviewer/bug-hunter). Load khi target kind=desktop.
---

# stack-electron

> Idiom Electron (cross-stack ở `docs/CONVENTIONS.md`; bảo mật ở `SECURITY.md`). Renderer là React → quy ước UI theo `stack-nextjs` §3 (data layer · UX states · a11y · `data-screen`/`data-ds` · token).
> Load khi BUILD/VERIFY target có frontmatter `kind: desktop`. Bản đầu: **Windows** (macOS/Linux mở rộng sau — ghi ADR khi thêm).

## §1 Khi load
BUILD target desktop (scaffold/code) · VERIFY (reviewer/bug-hunter đọc **§review**; dogfood mở app đã đóng gói qua cổng gỡ lỗi — skill `browse` §7).

## §2 Scaffold
- Vào `services/desktop/<name>/`. CLI chính chủ: `npm init electron-app@latest <name> -- --template=vite-typescript` (Electron Forge), rồi thêm React + script `typecheck`/`test`. Version Electron theo `docs/TECHSTACK.md`.
- Ba phần tách bạch: **main** (`src/main/` — cửa sổ, IPC handler, việc đụng hệ điều hành) · **preload** (`src/preload/` — `contextBridge` lộ API hẹp) · **renderer** (`src/renderer/` — React, layout theo `ref-frontend-pattern`) · kiểu IPC dùng chung ở `src/shared/ipc.ts`.
- Đóng gói + phát hành theo ADR: mặc định Forge maker **Squirrel.Windows** (cài theo user vào `%LocalAppData%`, **không cần admin**). Cần bộ cài NSIS hoặc cập nhật qua máy chủ riêng → `electron-builder` + `electron-updater`, ghi ADR.
- **Chế độ kiểm nhanh `--smoke`** (bắt buộc — `make doctor` + `capture_proof` dùng): bản đóng gói chạy với `--smoke` → mở cửa sổ chính ẩn, kiểm phụ thuộc thiết yếu (thư mục `userData` ghi được · DB cục bộ mở được · binary đi kèm có mặt) → in kết quả, thoát `0` (khoẻ) hoặc `1`.
- Token: map `docs/DESIGN-SYSTEM.md §2` như `stack-nextjs` §2. Shell cửa sổ dịch từ `docs/ux/mockups/<target>/_shell.html`.

## §3 Convention (Electron — bắt buộc)
- **Ranh giới tiến trình**: renderer KHÔNG `require` module Node; mọi việc đụng hệ điều hành (file · tiến trình con · gọi API có key) đi qua **IPC** `ipcRenderer.invoke` ↔ `ipcMain.handle`. **Hợp đồng IPC** (tên kênh · tham số · kết quả · mã lỗi) nằm ở `docs/arch/{name}.md §3` — vai trò như API của web.
- **Preload lộ hàm, không lộ module**: `contextBridge.exposeInMainWorld('api', { transcribe: (p) => ipcRenderer.invoke('transcribe', p) })` — KHÔNG expose `ipcRenderer`/`fs` nguyên con.
- **Kiểm tham số IPC ở main** như kiểm request ở server: kiểu · đường dẫn nằm trong vùng được phép · kích thước. Coi renderer là không tin được.
- **Mặc định an toàn giữ nguyên**: `contextIsolation: true` · `nodeIntegration: false` · `sandbox: true` · `webSecurity: true` · CSP trong HTML renderer · chặn điều hướng lạ (`will-navigate`) và cửa sổ mới (`setWindowOpenHandler` → deny; mở link ngoài bằng `shell.openExternal` chỉ với URL `https:` đã kiểm).
- **Đường dẫn**: dữ liệu người dùng chỉ ở `app.getPath('userData')` — KHÔNG ghi cạnh file cài. Đường dẫn có dấu cách/tiếng Việt (`C:\Users\Nguyen Thanh Cong\…`) phải chạy: `path.join`, tiến trình con nhận **mảng đối số** (không ghép chuỗi lệnh shell).
- **Secret** (API key người dùng nhập): `safeStorage.encryptString` (Windows: DPAPI theo tài khoản) rồi mới ghi đĩa; không log key; không đưa key sang renderer khi không cần.
- **Việc nặng** (nhận giọng nói, xử lý video): tiến trình con / `utilityProcess`, không chạy trên main (cửa sổ treo "Not Responding"); có tiến độ + huỷ được.
- **Log lỗi**: ghi file trong `userData/logs` (xoay vòng, che key/PII) — nguồn chẩn đoán trên máy người dùng sau phát hành.
- **Bản phát hành**: fuse tắt `RunAsNode` + `EnableNodeCliInspectArguments` (Forge `FusesPlugin`); cổng gỡ lỗi chỉ mở khi MAIN chạy dogfood trên máy dev.
- **Môi trường dev**: VS Code (và mọi tiến trình con của nó) đặt sẵn `ELECTRON_RUN_AS_NODE=1` → Electron chạy như Node thường, không mở cửa sổ. Mọi lệnh chạy app phải bỏ biến này (`env -u ELECTRON_RUN_AS_NODE …`).
- **Test**: renderer theo `ref-frontend-test`; IPC + main + e2e bản đóng gói theo **`ref-desktop-test`**. Coverage ≥ **60%**.

## §4 make (điền thân vào `services/desktop/<name>/Makefile` — root Makefile dispatch tới)
```
dev     : env -u ELECTRON_RUN_AS_NODE npm start                       # electron-forge start (renderer hot reload)
check   : npm run typecheck && npm run lint && npm run package && npm run test
test    : npm run test
migrate : true      # DB cục bộ (nếu có) migrate lúc app khởi động — ghi ở arch §1
deploy  : npm run publish                                             # phát hành bản mới — guard_bc buộc hỏi Authority
doctor  : env -u ELECTRON_RUN_AS_NODE "out/<App>-win32-x64/<App>.exe" --smoke   # bản đóng gói, exit 0 = khoẻ
```

## §review  (reviewer/bug-hunter soi TỪNG DÒNG — forbidden patterns Electron)
| Cấm | Hậu quả thật | Thay bằng |
|---|---|---|
| `nodeIntegration: true` / `contextIsolation: false` / `sandbox: false` | Một lỗ XSS trong renderer = chạy lệnh tuỳ ý trên máy người dùng | Giữ mặc định an toàn; việc cần Node đi qua IPC |
| Preload expose `ipcRenderer` / `fs` / `child_process` nguyên con | Renderer gọi được mọi kênh, đọc/ghi mọi file | Expose từng hàm hẹp qua `contextBridge` |
| `ipcMain.handle` không kiểm tham số / đường dẫn | Renderer bị chiếm đọc được file bất kỳ (`..\..\`) | Kiểm kiểu + đường dẫn nằm trong vùng cho phép |
| `shell.openExternal(url)` với URL chưa kiểm | Mở `file:` / giao thức lạ → chạy chương trình | Chỉ `https:` đã kiểm |
| Ghép chuỗi lệnh shell gọi tiến trình con (`exec(\`ffmpeg -i ${p}\`)`) | Đường dẫn có dấu cách vỡ; tên file độc thành lệnh | `execFile` / `spawn` với mảng đối số |
| API key lưu chữ thường (file · `localStorage` · store không mã hoá) | Ai đọc được ổ đĩa là lấy key | `safeStorage` |
| Ghi dữ liệu vào thư mục cài / đường dẫn cứng `C:\…` | Cài theo user không có quyền ghi; cập nhật xoá mất dữ liệu | `app.getPath('userData')` |
| Việc nặng chạy trên main process | Cửa sổ treo, người dùng tắt ngang làm hỏng dữ liệu | Tiến trình con / `utilityProcess` + tiến độ |
| Bản phát hành để fuse `RunAsNode` bật / mở cổng gỡ lỗi | Phần mềm khác trên máy điều khiển được app | Fuse tắt; cổng gỡ lỗi chỉ ở dogfood |
| Log chứa key / nội dung người dùng | Lộ khi người dùng gửi file log | Che key/PII trước khi ghi |
| `dialog.showMessageBox` / `showErrorBox` cho xác nhận hoặc cảnh báo thường | Hộp của hệ điều hành: công cụ tự động (CDP) không điều khiển được → đứng im; a11y kém | Hộp trong renderer (modal của ui-kit); `dialog.showOpenDialog` chọn file phải có đường thay thế: kéo-thả hoặc ô nhập đường dẫn |

## §done
typecheck/lint/package/test pass, coverage ≥60%; `make doctor` (bản đóng gói `--smoke`) exit 0; mặc định an toàn giữ nguyên; IPC khớp `arch §3`; không business logic quan trọng ở renderer; file chỉ trong `services/desktop/{name}/`.
