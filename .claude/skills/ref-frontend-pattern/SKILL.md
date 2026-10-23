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

## 1b. Next.js

Web là SPA tĩnh: build ra `dist/` rồi nginx phục vụ (PROTOCOL §4). Nếu ADR chọn Next thì chỉ dùng chế độ xuất tĩnh (`output: 'export'`) và giữ cây thư mục ở §1. Không dùng `app/` với Server Component, Server Action hay Route Handler: nginx không chạy được chúng (xem `stack-nextjs` §2).

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
