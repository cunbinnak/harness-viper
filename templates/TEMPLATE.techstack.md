<!-- gate bỏ qua TEMPLATE.* — copy thành docs/TECHSTACK.md. `stack` phải khớp frontmatter arch/<target>.md. -->
# TECHSTACK — {{PROJECT_NAME}}

## §1 Stack per target
| Target (kind) | Stack | Skill |
|---|---|---|
| {{order-service (backend)}} | {{Java 21 + Spring Boot 4.1}} | `stack-spring-boot` |
| {{customer-web (web)}} | {{React 19 + Vite}} | `stack-nextjs` |

## §2 Hạ tầng
{{PostgreSQL · Redis · Kafka}}

<!-- §3: biến môi trường — đồng bộ với application.yml + docker-compose + .env.example (PRODUCTION-READY Nhóm 1). -->
## §3 Biến môi trường
| Biến | Target | Mô tả |
|---|---|---|
| {{DB_URL}} | {{order-service}} | {{connection string}} |
