---
name: ref-frontend-pattern
description: Cấu trúc thư mục + tổ chức component frontend boundary. Data layer REST-default, BFF optional.
---

# Reference: Frontend Structure

> Situational ref cho stack-nextjs. Load khi BUILD web target.
> **Purpose:** Layout chuẩn 1 web target. Dùng để build UI theo cấu trúc nào.
> **Tách bạch:** cấu trúc = file này · config (package.json, build) = `ref-frontend-config` · convention bắt buộc + naming = `stack-nextjs`.
> **Tuning:** theo framework (React/Vue/Next/Svelte) + bundler.

## 1. Layout chuẩn (React/Vite ví dụ)

```
services/web/{name}/
├── src/
│   ├── pages/            # Route page ~ map 1-1 Mã màn trong docs/ux/SCREEN-MAP.md
│   ├── components/
│   │   ├── ui/           # Atomic (Button, Input, Modal) — no business logic
│   │   ├── layout/       # Header, Sidebar, PageWrapper
│   │   └── domain/       # Domain widget (OrderCard, CustomerList)
│   ├── hooks/            # Data fetching, state, side effect (useXxx)
│   ├── api/              # API client layer  ← xem §2
│   ├── stores/           # Cross-component state (Zustand/Redux/Pinia)
│   ├── router/           # index + guards (auth/role guard)
│   ├── types/            # TS interface — khớp DTO (REST) hoặc generated (GraphQL); union type cho tập giá trị đóng
│   ├── constants/        # Hằng số dùng chung: routes · queryKeys · storageKeys (tạo khi có — xem stack §3 Hằng số)
│   ├── utils/            # Pure helper (formatter, validator)
│   └── styles/           # Theme token, global style
├── tests/{unit,integration,e2e}
└── package.json
```

## 1b. Biến thể Next.js App Router (khi ADR chọn Next)

```
services/web/{name}/src/
├── app/                          # ROUTE = thư mục; mỗi màn ~ 1 Mã màn trong docs/ux/SCREEN-MAP.md
│   ├── layout.tsx · providers.tsx · error.tsx · not-found.tsx
│   ├── (auth)/login/page.tsx     # route group theo vùng — không ăn vào URL
│   ├── (app)/                    # vùng đã đăng nhập: layout.tsx chứa app shell (khớp _shell.html)
│   │   └── {resource}/
│   │       ├── page.tsx          # Server Component: lấy data lần đầu, KHÔNG business logic
│   │       ├── loading.tsx       # BẮT BUỘC cho route có data (trạng thái tải)
│   │       ├── error.tsx         # lỗi theo route (khuôn lỗi)
│   │       ├── {Resource}Client.tsx   # 'use client' — tương tác, gọi hooks/
│   │       └── actions.ts        # 'use server' — Server Action: CHỈ gọi api/, không business logic, trả kết quả có kiểu
│   └── api/                      # Route Handler — chỉ cho BFF mỏng/auth callback; KHÔNG thay backend
├── components/{ui,layout,domain}/  # như §1 — KHÔNG import api/ hay app/**/actions trực tiếp
├── hooks/                        # React Query hooks (client) — query key từ constants/
├── api/                          # api-client + {resource}-service (§2) — dùng chung server & client
├── constants/ · types/ · lib/ · styles/
```
- Server Component đọc qua `api/` (chạy server, token từ cookie httpOnly); Client Component đọc qua `hooks/` → `api/`. Không `fetch` rải rác.
- Thư mục `components/ui` · `components/domain` · `hooks` rỗng = scaffold mồ côi → xoá hoặc dùng.
- Review soi cây theo biến thể này khi `app/` tồn tại (review-web 6.0).

## 2. Data layer — REST default | BFF optional
- **REST (default)**: `api/api-client.ts` (Axios/fetch wrapper + auth interceptor) + `api/{resource}-service.ts` gọi contract `docs/arch/{backend}.md §3 API`. `types/` viết tay khớp DTO.
  - **Bóc envelope MỘT chỗ** ở `api-client` (shape `CONVENTIONS §3`): thành công trả `data` (list → `PageResponse<T>`: `content` · `number` · `size` · `totalElements` · `totalPages`…); lỗi ném `ApiError { code, status, additionalData }`. Hook/component KHÔNG đọc `.data.data`, KHÔNG tự parse envelope; hiển thị lỗi theo `code` (map `code` → câu tiếng Việt ở FE, field lỗi từ `additionalData[].field`).
- **BFF/GraphQL (optional, khi design có bff)**: `api/` chứa generated hooks/ops từ codegen; `types/` là generated. Cấu hình codegen ở `ref-frontend-config`.

## 3. Trách nhiệm từng folder
| Folder | Trách nhiệm | Phụ thuộc |
|---|---|---|
| `pages/` | Route entry, compose components | components, hooks, api |
| `components/ui/` | Atomic, no business logic | styles |
| `components/domain/` | Domain widget | hooks, types |
| `hooks/` | Data fetch, state, side effect | api, stores |
| `api/` | API call layer (REST client / GraphQL ops) | types |
| `stores/` | Cross-component state | api |
| `router/` | Navigation map + guard | hooks, stores |

## 4. Forbidden patterns
- `components/` gọi API trực tiếp — phải qua `hooks/` → `api/`.
- `pages/` chứa business logic phức tạp — chuyển vào `hooks/`.
- `api/` chứa UI logic — chỉ data call.
- Business logic (price/eligibility) tính ở FE — chỉ render kết quả từ backend/BFF.
- Prop drilling 3+ level — dùng store/context.

## 5. Done
- Cấu trúc khớp `docs/ux/SCREEN-MAP.md` (page ~ screen) + data layer đúng design (REST/BFF).
- Build/typecheck pass trước `/verify`.
