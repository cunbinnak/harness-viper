<!-- gate bỏ qua TEMPLATE.* — copy thành docs/PRODUCTION-READY.md. Tick ở SHIP. Mục *(sau deploy)* tick sau khi deploy — guard_bc miễn chúng trước deploy, gate SHIP (chạy sau deploy) đòi đủ. -->
# PRODUCTION-READY — {{PROJECT_NAME}}

## Nhóm 1 — Secret & env
- [ ] Secret ở dashboard PaaS, không trong code · `.env.example` đủ biến
- [ ] Env đồng bộ `application.yml` ↔ `docker-compose.yml` ↔ `.env.example` (không lệch)

## Nhóm 2 — Bảo mật (theo `SECURITY.md`)
- [ ] Validate ở server · phân quyền ở server (theo ma trận vai) · không lộ entity · HTTPS *(sau deploy)*
- [ ] Secret không có giá trị mặc định ở prod + app fail-fast khi thiếu · profile prod đặt tường minh, không endpoint dev
- [ ] JWT kiểm `iss`/`aud`/`exp`, định danh theo claim bất biến · khoá tài khoản thu hồi token ngay
- [ ] Security header (CSP/HSTS/nosniff/frame) + cookie `HttpOnly; Secure; SameSite` · swagger/api-docs/actuator tắt hoặc sau auth
- [ ] IP client qua proxy tin cậy (rate limit đúng người) · SCA (`dependencyCheckAnalyze` + `npm audit`) không còn CVE high

## Nhóm 3 — Observability
- [ ] Log structured + correlation id · health check trả 200 · metrics *(sau deploy)*

## Nhóm 4 — Vận hành
- [ ] `make deploy` / `make doctor` có thân · đường rollback ở `arch/OVERVIEW.md §5.8` · backup DB *(sau deploy)*
