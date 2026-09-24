---
name: stack-bff
description: Stack BFF — Apollo Server / NestJS GraphQL gateway (Node/TS) — scaffold · convention · make · §review (forbidden patterns cho reviewer/bug-hunter). Load khi target kind=bff.
---

# stack-bff

> Idiom GraphQL gateway (cross-stack ở `docs/CONVENTIONS.md`; bảo mật ở `SECURITY.md`).
> Load khi BUILD/VERIFY target có frontmatter `kind: bff`.

## §1 Khi load
BUILD target bff (scaffold/code) · VERIFY (reviewer/bug-hunter đọc **§review**).

BFF = GraphQL gateway: aggregate nhiều backend REST (`docs/arch/{backend}.md §3`) thành 1 graph cho FE. KHÔNG chứa business logic — chỉ orchestrate + shape data.

## §2 Scaffold
- Vào `services/bff/<name>/`. kind=bff. Dùng **Apollo Server** (hoặc **NestJS GraphQL**) + TypeScript — code-first schema (không viết SDL tay).
- Cấu trúc: `src/schema/` (type + resolver code-first) · `src/resolvers/{type}.resolver.ts` · `src/loaders/{entity}.loader.ts` · `src/datasources/` (HTTP client per backend) · `src/context/` (auth context factory) · `src/errors/` · `src/config/`.
- **Dockerfile multi-stage** (build TS → node runtime) + config env NGAY lúc scaffold. Introspection tắt ở production, bật depth + complexity limit từ đầu.
- Artifact local → `deployment/local/` (docker-compose). `git commit`.

## §3 Convention (GraphQL/Node — bắt buộc)
- **Schema (SDL/type)**: additive — deprecate field cũ (`@deprecated`), **KHÔNG remove/đổi type breaking**. Relay-style `Connection` cho pagination. **Code-first hoặc codegen** — không viết SDL tay rồi tự đồng bộ.
- **Resolver**: implement theo `docs/arch/{name}.md §3` (integration per backend); gọi backend qua **datasource/HTTP client**, map response → GraphQL type. **KHÔNG chạm thẳng DB/downstream** ngoài datasource. Resolver chỉ orchestrate + shape.
- **DataLoader**: BẮT BUỘC cho mọi field quan hệ có N+1 risk (vd `order.customer`). Batch + cache **per-request** (tạo mới mỗi request, không dùng chung toàn cục).
- **Auth context**: extract JWT ở **context factory một lần** → populate `userId / tenantId / roles[]` vào `GraphQLContext`; resolver đọc từ context, **KHÔNG tự decode JWT lại**, KHÔNG lấy `userId`/`tenantId`/role từ GraphQL args.
- **Error mapping**: HTTP status backend → GraphQL error `extensions.code` (`UNAUTHENTICATED` / `FORBIDDEN` / `BAD_USER_INPUT` / `INTERNAL`). Lỗi nghiệp vụ biết trước → union/result type hoặc code riêng theo `docs/arch/{name}.md §3`, KHÔNG gộp `INTERNAL`.
- **Cache**: Redis key cho sensitive data PHẢI include `userId`/`tenantId` (tránh leak cross-tenant).
- **Query safety**: depth + complexity limit + list phải phân trang (Relay `Connection`); introspection tắt ở production.
- **Config**: env placeholder, không hardcode secret/URL/timeout.
- **Test**: **Vitest** unit (resolver + mapper) + integration mock backend; coverage ≥ **70%**. DataLoader batching verified (no N+1).

## §4 make (điền thân vào `services/bff/<name>/Makefile` — root Makefile dispatch tới)
```
dev     : docker compose -f deployment/local/docker-compose.yml up -d && npm run dev
check   : npm run build && npm run typecheck && npm run lint   # + schema validate
test    : npm test                                             # vitest
```

## §review  (reviewer/bug-hunter soi TỪNG DÒNG — forbidden patterns BFF GraphQL)
| Cấm | Hậu quả thật | Thay bằng |
|---|---|---|
| Nghiệp vụ (tính giá, eligibility) trong resolver | Logic nhân đôi với backend, sớm muộn lệch số | Backend tính, resolver chỉ orchestrate + shape |
| Resolver chạm thẳng DB/downstream không qua datasource | Không tái dùng, không test được | Resolver → datasource/service theo `docs/arch/{name}.md §3` |
| Field quan hệ không có DataLoader | N+1, sập dưới tải nhẹ | DataLoader batch |
| DataLoader/cache dùng chung toàn cục | Rò dữ liệu giữa các người dùng | Tạo mới mỗi request; key cache có `userId`/`tenantId` |
| Lấy `userId`/`tenantId`/role từ GraphQL args | Client tự khai là người khác | Context từ JWT |
| Decode JWT lại trong từng resolver | Lệch cách verify giữa các resolver | Context factory một lần |
| Bật introspection ở production | Công bố toàn bộ bề mặt tấn công | Tắt |
| Không giới hạn depth/complexity; list không phân trang | Một query đủ làm sập | depth + complexity limit; Relay `Connection` |
| Trả nguyên lỗi backend ra client | Lộ stack/thông tin nội bộ | Map `extensions.code` |
| Lỗi nghiệp vụ biết trước (hết hàng, trùng lịch) gộp chung `INTERNAL` | Client không phân biệt lỗi hệ thống với lỗi người dùng sửa được | Union/result type hoặc code nghiệp vụ riêng, theo `docs/arch/{name}.md §3` |
| Remove/rename/đổi type field SDL | App đã phát hành gãy | `@deprecated` rồi mới bỏ |
| Viết SDL tay rồi tự đồng bộ với type | Chắc chắn lệch | Code-first hoặc codegen |
| Nối input vào URL/query downstream | Injection/SSRF đi xuyên gateway | Validate + encode tham số |

## §done
Build pass, typecheck pass, schema validate, DataLoader no-N+1, test ≥70%; file chỉ trong `services/bff/<name>/`; KG cập nhật.
