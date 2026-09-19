<!-- gate bỏ qua TEMPLATE.* — copy thành docs/PRODUCTION-READY.md. Tick ở SHIP. Mục (sau deploy) tick ở P2. -->
# PRODUCTION-READY — {{PROJECT_NAME}}

## Nhóm 1 — Secret & env
- [ ] Secret ở dashboard PaaS, không trong code · `.env.example` đủ biến
- [ ] Env đồng bộ `application.yml` ↔ `docker-compose.yml` ↔ `.env.example` (không lệch)

## Nhóm 2 — Bảo mật (theo `SECURITY.md`)
- [ ] Validate ở server · phân quyền ở server (theo ma trận vai) · không lộ entity · HTTPS *(sau deploy)*

## Nhóm 3 — Observability
- [ ] Log structured + correlation id · health check trả 200 · metrics *(sau deploy)*

## Nhóm 4 — Vận hành
- [ ] `make deploy` / `make doctor` có thân · đường rollback ở deploy doc · backup DB *(sau deploy)*
