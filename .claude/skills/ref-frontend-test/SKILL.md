---
name: ref-frontend-test
description: Pattern test cho MAIN viết ở BUILD — web React/TS. Vitest + React Testing Library + user-event + MSW v2; query theo vai trò/nhãn; đủ trạng thái tải/rỗng/lỗi/thành công; form + validate; hook với renderHook; MOCK PHẢI KHỚP CONTRACT (handler có kiểu từ arch §3, chống mock lệch hệ thật); coverage 60%. Load khi BUILD target kind=web.
---

# Reference: Frontend Test (MAIN viết ở BUILD)

> **Lưới an toàn của người làm** (`make test`) — không thay TC nghiệm thu của `test-writer` (chạy trên app thật). Viết CÙNG LÚC code. Script: `ref-frontend-config` (`test`, `test:coverage`). Cấu trúc: `ref-frontend-pattern` (`tests/{unit,integration}` hoặc `*.test.tsx` cạnh component — chọn 1 kiểu, ghi ADR/KG).

## 1. Viết test cho gì (ưu tiên)
1. **Màn có dữ liệu**: đủ 4 trạng thái **đang tải · rỗng · lỗi · có dữ liệu** (+ vô hiệu theo quyền).
2. **Form**: validate (bắt buộc · định dạng · biên), **khoá nút khi đang gửi** (chống gửi 2 lần), lỗi server theo mã → hiện **gần field**.
3. **Hiển thị theo quyền**: vai không có quyền không thấy nút (chỉ là UX — server vẫn phải chặn, QC kiểm phần đó).
4. Hook / util có logic: format tiền `1.234.567 ₫`, ngày `dd/MM/yyyy`, giờ VN.
Không test: component chỉ render tĩnh · style · snapshot lớn.

## 2. Truy vấn theo cách người dùng thấy
`getByRole('button', { name: 'Gửi đăng ký' })` · `getByLabelText('Ngày làm từ xa')` · `findByText(...)` cho nội dung bất đồng bộ. `data-testid` chỉ khi không có vai trò/nhãn phù hợp. Thao tác bằng `userEvent` (`await user.click(...)`), không `fireEvent`.

## 3. Mock API — MSW v2, và mock PHẢI KHỚP contract
```ts
// tests/msw/handlers.ts — dữ liệu mock có KIỂU từ types/ (sinh/khai theo arch §3) → contract đổi = test lỗi biên dịch
import { http, HttpResponse } from 'msw';
import type { RemoteRequest, ErrorResponse } from '@/types/remote';
export const remoteOk = http.post('/v1/remote', async () =>
  HttpResponse.json({ code: 'SUCCESS', message: '', timestamp: '', data: { id: 12, status: 'PENDING', date: '2026-10-16' } satisfies RemoteRequest }, { status: 201 }));
export const remoteDeadline = http.post('/v1/remote', () =>
  HttpResponse.json({ code: 'REMOTE_DEADLINE_PASSED', message: '', timestamp: '', additionalData: [] } satisfies ErrorResponse, { status: 422 }));
```
```ts
// test: server.use(remoteDeadline) cho từng ca
const server = setupServer(remoteOk); beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers()); afterAll(() => server.close());
```
- **Chống mock lệch hệ thật**: dữ liệu mock `satisfies` type contract · path/method/mã lỗi lấy đúng `arch §3` (copy từ contract, không tự đặt) · `onUnhandledRequest: 'error'` (gọi API lạ = test đỏ). Walking skeleton (`/build` Bước 4) đã gọi **API thật** — mock chỉ để test nhanh các nhánh.
- Envelope bóc ở `api-client` (`ref-frontend-pattern §2`) — test hook/component nhận dữ liệu đã bóc, không tự parse `data.data`.

## 4. Mẫu: trạng thái + form
```tsx
it('hiện lỗi hạn chót gần field khi server từ chối', async () => {
  server.use(remoteDeadline);
  const user = userEvent.setup();
  renderWithProviders(<RemoteRequestForm />);                 // QueryClient mới mỗi test, retry: false
  await user.type(screen.getByLabelText('Ngày làm từ xa'), '16/10/2026');
  await user.click(screen.getByRole('button', { name: 'Gửi đăng ký' }));
  expect(await screen.findByText(/đã quá hạn đăng ký/i)).toBeInTheDocument();
});
it('khoá nút khi đang gửi', async () => { /* click 2 lần nhanh → chỉ 1 request (đếm bằng handler) */ });
```
- `renderWithProviders`: `QueryClient({ defaultOptions: { queries: { retry: false } } })` mới cho mỗi test (không rò cache giữa test), kèm router/i18n/theme.
- Hook: `renderHook(() => useRemoteRequests(), { wrapper })` + `await waitFor(...)`.
- Giờ: `vi.useFakeTimers(); vi.setSystemTime(new Date('2026-10-15T10:00:01Z'))` cho logic hiển thị theo giờ (giờ VN UTC+7).

## 5. Coverage + chạy
`vitest run --coverage --coverage.include='src/**/*.{ts,tsx}'` (thiếu include = số ảo) — ≥ 60%. Coverage là sàn, không phải mục tiêu.

## 6. Cấm
Query theo className · snapshot lớn thay assert · mock `fetch`/`axios` tay thay MSW · handler trả dữ liệu không kiểu / path tự đặt · `setTimeout` chờ thật · test phụ thuộc thứ tự · QueryClient dùng chung giữa test.
