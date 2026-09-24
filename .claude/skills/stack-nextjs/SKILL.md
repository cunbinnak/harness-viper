---
name: stack-nextjs
description: Stack web frontend React 19 + Vite/Next — scaffold · convention · make · §review (forbidden patterns cho reviewer/bug-hunter). Load khi target kind=web stack=nextjs/react.
---

# stack-nextjs

> Idiom React/TS (cross-stack ở `docs/CONVENTIONS.md`; bảo mật ở `SECURITY.md`).
> Load khi BUILD/VERIFY target có frontmatter `kind: web`.

## §1 Khi load
BUILD target web (scaffold/code) · VERIFY (reviewer/bug-hunter đọc **§review**; picky đọc để đối chiếu mockup).

## §2 Scaffold
- Vào `services/web/<name>/`. Dùng CLI chính chủ (Vite/Next create). TypeScript `strict: true`.
- Layout: `pages`/`components`/`hooks`/`api`/`stores`/`router`.
- **Design token**: nếu ADR chọn ui-kit (khuyến nghị **Ant Design 5**) → map `docs/DESIGN-SYSTEM.md §2` vào theme (`ConfigProvider`), dùng component library thật. Nếu **Tailwind** → map token vào `theme.extend.colors/spacing/borderRadius` trong `tailwind.config` — **CẤM dùng palette mặc định** (`blue-600`...): primary trên màn phải là token §2, không phải màu Tailwind gốc. Nếu plain-CSS → copy token vào `:root`, dùng `var(--...)`. Map **trước màn đầu tiên** — theme config là việc của scaffold, không phải "để sau".

## §3 Convention (React/TS — bắt buộc)
- **Data layer**: API client tách `api/` theo target; **KHÔNG `fetch`/`axios` rải rác trong component**. Type từ `arch/<backend> §3 API` (hoặc codegen). Server-state qua **React Query/SWR** (query key tập trung); không tự chế cache.
- **KHÔNG business logic ở FE** (giá/điểm/điều kiện → backend). Role-gate FE **chỉ UX**, backend enforce.
- **Component nhỏ**: UI render + emit event; container/page fetch + orchestrate. Không mutate props/state (immutable).
- **UX states**: mỗi màn fetch đủ **loading · empty · error · success**; KHÔNG action im lặng; **confirm** destructive; lỗi field hiện **gần field** (toast không thay).
- **Form**: schema validation (Zod/Yup); FE validate chỉ UX; chống double-submit (disable khi pending).
- **Auth**: token theo auth design (**KHÔNG localStorage** — httpOnly/in-memory); logout `queryClient.clear()`.
- **a11y**: semantic HTML (`button`/`a`/`label`/`input`); icon button có `aria-label`; màu không là tín hiệu duy nhất. axe 0 critical.
- **Styling**: token/theme cho màu/spacing/typography — **không hardcode hex/px** (guard_ds chặn ở mockup). Component đủ `:hover`/`:focus-visible`/`disabled`.
- **Test**: Vitest + RTL + **MSW** (mock network boundary); assert theo hành vi (role/label/text). Coverage ≥ **60%**.

## §4 make (điền thân vào `services/web/<name>/Makefile` — root Makefile dispatch tới)
```
dev     : npm run dev                 # trỏ backend thật
check   : npm run typecheck && npm run lint && npm run build
test    : npm run test
```

## §review  (reviewer/bug-hunter soi TỪNG DÒNG — forbidden patterns React/TS)
| Cấm | Hậu quả thật | Thay bằng |
|---|---|---|
| Component UI gọi `fetch`/`axios` trực tiếp | Đổi API sửa hai chục chỗ; không mock được | `api/` → `hooks/` → component |
| `any` / `@ts-ignore` để qua typecheck | Mất tác dụng TS đúng chỗ API đổi hình | Type từ spec/codegen; `unknown` + zod parse |
| Coi validate client / ẩn nút theo role là chốt chặn | `curl` thẳng API là qua | BE enforce; FE chỉ UX |
| Tính giá/điểm/điều kiện nghiệp vụ ở FE | Hai nơi tính lệch số; sửa JS đổi kết quả | Lấy kết quả từ BE |
| Hiện lỗi thô (stack/SQL/`error.message` server) ra UI | Lộ nội bộ; user không biết làm gì | Map error code → thông báo theo `ux` |
| Token trong `localStorage`/`sessionStorage` | 1 lỗ XSS là mất phiên | httpOnly cookie / in-memory |
| `dangerouslySetInnerHTML` dữ liệu chưa sanitize | XSS | Render text; buộc HTML thì sanitize |
| Secret trong `VITE_*`/`NEXT_PUBLIC_*` | Nằm nguyên trong bundle ai cũng tải | Giữ ở server |
| Redirect theo `?next=`/`?redirect=` không kiểm | Open redirect lừa đăng nhập | Chỉ nhận path nội bộ |
| Chỉ render nhánh success | API lỗi = màn trắng; user bấm lại, gửi 2 lần | Đủ loading · empty · error · success |
| Submit không chống bấm 2 lần | Tạo bản ghi trùng | Disable khi pending + idempotency key |
| `className` không có stylesheet; hardcode hex/px | UI không định dạng, lệch token | Token `:root`/theme ui-kit |
| Định nghĩa lại type API bằng tay | Lệch contract sau vài ngày | Type từ spec/codegen |
| `useEffect` fetch dependency array sai | Gọi API vô hạn, dội tải BE | Server-state lib |
| Đăng xuất không xoá cache server-state | Người sau thấy dữ liệu người trước | `queryClient.clear()` khi logout |

## §done
typecheck/build/lint/test pass, coverage ≥60%, a11y clean; đủ loading/empty/error/success; không `console.log`/`any`; API type khớp contract; không business logic quan trọng ở FE; file chỉ trong `services/web/{name}/`.
