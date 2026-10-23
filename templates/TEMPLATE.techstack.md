<!-- gate bỏ qua TEMPLATE.* — copy thành docs/TECHSTACK.md. `stack` phải khớp frontmatter arch/<target>.md. -->
<!-- VAI: SA đề xuất (Bước 7) · Authority chốt. -->
# TECHSTACK — {{PROJECT_NAME}}

## §1 Stack per target
| Target (kind) | Stack | Skill |
|---|---|---|
| {{order-service (backend)}} | {{Java 21 + Spring Boot 4.1}} | `stack-spring-boot` |
| {{customer-web (web)}} | {{React 19 + Vite}} | `stack-nextjs` |

## §2 Hạ tầng
{{PostgreSQL · Redis · Kafka}}

<!-- §3: biến môi trường — ghi lúc DOCUMENT. Từ BUILD, nguồn thật là application.yml + docker-compose + .env.example (PRODUCTION-READY Nhóm 1); file này đã đóng băng nên không cập nhật theo. -->
## §3 Biến môi trường
| Biến | Target | Mô tả |
|---|---|---|
| {{DB_URL}} | {{order-service}} | {{connection string}} |
