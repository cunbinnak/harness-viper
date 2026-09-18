# services/ — code sản phẩm (MAIN scaffold + commit)

Trống lúc bootstrap. MAIN scaffold vào đây ở `/build` (Bước 3) theo stack skill. Chia nhóm theo `kind`
(khai ở frontmatter `docs/arch/{name}.md`):

| Nhóm | `kind` | Stack skill |
|---|---|---|
| `boundaries/{name}/` | backend (API + DB) | `stack-spring-boot` · `stack-go` · `stack-fastapi` |
| `web/{name}/` | web frontend | `stack-nextjs` |
| `bff/{name}/` | GraphQL gateway | `stack-bff` |
| `mobile/{name}/` | mobile app | `stack-flutter` |

- Mỗi target có `Makefile` riêng (thân 6 lệnh do stack skill điền); **root `Makefile` dispatch** `make -C services/<nhóm>/<name>`.
- `services/` **được track** (fork monorepo-ish); build artifact (`node_modules`/`target`/…) trong `.gitignore`.
- Hạ tầng dùng chung (db/redis/kafka) ở `deployment/local/docker-compose.yml`.
