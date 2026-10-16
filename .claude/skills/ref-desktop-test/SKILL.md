---
name: ref-desktop-test
description: "Pattern test cho MAIN viết ở BUILD — desktop Electron (Windows). Renderer theo ref-frontend-test với window.api giả có kiểu từ hợp đồng IPC; IPC handler test như endpoint (tham số sai · đường dẫn ngoài vùng · tiến trình con lỗi); e2e trên bản ĐÃ ĐÓNG GÓI bằng Playwright _electron; chế độ --smoke; đường dẫn có dấu cách + tiếng Việt; coverage 60%. Load khi BUILD target kind=desktop."
---

# Reference: Desktop Test (MAIN viết ở BUILD)

> **Lưới an toàn của người làm** (`make test`) — không thay TC nghiệm thu của `test-writer` (chạy trên app đã cài). Viết CÙNG LÚC code. Quy ước stack: `stack-electron`.

## 1. Viết test cho gì (ưu tiên)
1. **IPC handler** (main) — test như endpoint: tham số đúng → kết quả đúng · sai kiểu / thiếu → lỗi có mã · **đường dẫn ngoài vùng cho phép** (`..\..\Windows\…`) → từ chối · tiến trình con lỗi / quá thời gian → mã lỗi, không treo.
2. **Renderer** — như `ref-frontend-test` (4 trạng thái · form · quyền), nhưng thay MSW bằng **`window.api` giả có kiểu từ `src/shared/ipc.ts`** (giả lệch hợp đồng IPC = test xanh giả).
3. **Đường dẫn khó** — thư mục có dấu cách + tiếng Việt (`Nguyễn Văn A\Video mới\`), tạo trong thư mục tạm của test.
4. **Secret** — lưu key → đọc lại được; file trên đĩa không chứa key dạng chữ thường.
5. **`--smoke`** — thiếu binary đi kèm / `userData` không ghi được → thoát `1`.
Không test: cửa sổ/menu tĩnh · style.

## 2. Mẫu: IPC handler (tách khỏi `ipcMain` để test thuần)
```ts
// tests/main/transcribe.test.ts
import { it, expect } from 'vitest';
import os from 'node:os'; import path from 'node:path'; import fs from 'node:fs';
import { transcribeHandler } from '../../src/main/ipc/transcribe';

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'Nguyễn Văn A '));        // dấu cách + tiếng Việt

it('từ chối đường dẫn ngoài thư mục được phép', async () => {
  await expect(transcribeHandler({ file: 'C:\\Windows\\win.ini' }, { allowedRoot: root }))
    .rejects.toMatchObject({ code: 'PATH_NOT_ALLOWED' });
});

it('chạy được với đường dẫn có dấu cách và tiếng Việt', async () => {
  const f = path.join(root, 'video mới.mp4'); fs.writeFileSync(f, fakeMp4());
  await expect(transcribeHandler({ file: f }, { allowedRoot: root, stt: fakeStt }))
    .resolves.toMatchObject({ segments: expect.any(Array) });
});
```

## 3. Mẫu: e2e trên bản đóng gói — Playwright `_electron`
```ts
// tests/e2e/main-flow.spec.ts — chạy sau `npm run package`
import { _electron as electron, test, expect } from '@playwright/test';
import os from 'node:os'; import path from 'node:path'; import fs from 'node:fs';

test('mở app đã đóng gói, đi luồng chính', async () => {
  const env = { ...process.env }; delete env.ELECTRON_RUN_AS_NODE;               // VS Code đặt sẵn biến này
  const userData = fs.mkdtempSync(path.join(os.tmpdir(), 'app-e2e '));          // không đụng userData thật
  const app = await electron.launch({ executablePath: 'out/<App>-win32-x64/<App>.exe',
                                      args: [`--user-data-dir=${userData}`], env });
  const win = await app.firstWindow();
  await win.getByRole('button', { name: 'Tạo phụ đề' }).click();
  await expect(win.getByText('Đang xử lý')).toBeVisible();
  await app.close();
});
```
- e2e chạy trên **bản đóng gói** (`out/…exe`), không chỉ dev server — lỗi thiếu file khi đóng gói chỉ lộ ở đây.

## 4. Coverage + chạy
Vitest coverage ≥ **60%** (main + renderer). e2e nằm trong `make check` sau bước `package`.

## 5. Cấm
- Test gọi dịch vụ ngoài thật (nhận giọng nói / dịch) — giả tại ranh giới tiến trình con / HTTP client; QC chạy thật ở VERIFY.
- Test ghi vào `userData` thật của máy dev — dùng thư mục tạm.
- Bỏ e2e bản đóng gói vì "dev server chạy được rồi".
