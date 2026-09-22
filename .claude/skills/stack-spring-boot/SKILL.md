---
name: stack-spring-boot
description: Stack backend Java 21 + Spring Boot 4.x — scaffold · convention · make · config · §review (forbidden patterns cho reviewer/bug-hunter). Load khi target kind=backend stack=spring-boot. Version thật do docs/TECHSTACK.md + ADR chốt; 3.x đã EOL 6/2026 (chỉ dùng khi bảo trì codebase cũ).
---

# stack-spring-boot

> Port từ rules-backend + ref-backend-* cũ. Idiom Java/Spring (cross-stack ở `docs/CONVENTIONS.md`; bảo mật ở `SECURITY.md`).
> Load khi BUILD/VERIFY target có frontmatter `kind: backend, stack: spring-boot`.

## §1 Khi load
BUILD target backend (scaffold/code) · VERIFY (reviewer/bug-hunter đọc **§review**).

## §2 Scaffold
- Vào `services/boundaries/<name>/`. Dùng **Spring Initializr / Gradle** (Groovy DSL) — không chép boilerplate.
- Cấu trúc **Layered** (default): `controller/` · `service/` + `service/impl/` · `repository/` · `entities/` · `dto/{request,response}/` · `mapper/` · `config/` · `exception/`. (Hexagonal chỉ khi có ADR.)
- **Dockerfile multi-stage** (Gradle `bootJar` → JRE) + `application.yml` Postgres + migration (Flyway) NGAY lúc scaffold.
- Artifact local → `deployment/local/` (docker-compose db). `git commit`.

## §3 Convention (Java/Spring — bắt buộc)
- **Entity**: `{Resource}Entity` ở `entities/`; `@Getter @Setter @NoArgsConstructor @AllArgsConstructor` — **KHÔNG `@Data` trên `@Entity`**. Không FK constraint (liên kết qua id column + **tự add index**); toàn vẹn ở service layer.
- **Layering**: Controller (map + validate + gọi **service interface**) → Service impl (`@Service`, business logic + `@Transactional` + publish event) → Repository (chỉ query). **Controller KHÔNG gọi repository.** Inject **interface**, `@RequiredArgsConstructor` + `private final` (không `@Autowired` field).
- **DTO**: Request/Response DTO ở biên; **KHÔNG phơi `@Entity`**. Convert bằng **MapStruct** (mapper interface).
- **Exception**: `BusinessException` + error code **enum** theo domain; `@RestControllerAdvice` map tập trung. `orElseThrow(...)`, không `Optional.get()` trần.
- **Transaction**: `@Transactional` ở service; read-only khi phù hợp. **Không gọi external chậm trong transaction.** Publish event **AFTER_COMMIT** / outbox.
- **Persistence**: JPQL/Specification (filter động → Specification, không `(:x IS NULL OR ...)`); `nativeQuery` last-resort + `:tenantId`. Migration additive (không sửa file đã apply). Tránh N+1, list phải `Pageable`.
- **Idempotency**: consumer/webhook/callback/job dedup theo id (inbox). **Multi-tenant**: mọi query filter `tenant_id` từ auth context.
- **Timestamp**: `Instant` (entity/response/event) · `OffsetDateTime` (request) · `LocalDate` (date-only). **KHÔNG `LocalDateTime`**.
- **Import**: không FQCN inline, không wildcard, không `var`. **Config**: `@ConfigurationProperties`, không hardcode; secret qua env.
- **Test**: JUnit5 + Mockito (unit) · **Testcontainers Postgres** (integration, **KHÔNG H2**) · ≥1 test BOOT context + migration + `ddl-auto: validate` (bắt schema-drift). Coverage ≥ **80%**.

## §4 make (điền thân vào `services/boundaries/<name>/Makefile` — root Makefile dispatch tới)
```
dev     : docker compose -f deployment/local/docker-compose.yml up -d db && ./gradlew bootRun
check   : ./gradlew clean build            # compile + test + (spotless/checkstyle nếu có)
test    : ./gradlew test
migrate : ./gradlew flywayMigrate          # hoặc chạy lúc bootRun
```

## §5 Config
- `application.yml` + profile (`local/dev/prod`); env placeholder `${DB_URL}` (đồng bộ TECHSTACK §3 + docker-compose + .env.example).
- Security OAuth2 Resource Server (JWT); local có thể HS256 `@Profile("local")` thay Keycloak (gotcha đã biết — xem KG).

## §review  (reviewer/bug-hunter soi TỪNG DÒNG — forbidden patterns Java/Spring)
| Cấm | Hậu quả thật | Thay bằng |
|---|---|---|
| `ddl-auto: update/create/create-drop` ngoài test | Hibernate tự đổi schema → mất dữ liệu | `validate` + Flyway |
| Sửa migration đã chạy wave trước | Checksum lệch, app không khởi động | File `V{wave}_{seq}__` mới |
| Trả `@Entity` ra response / nhận entity làm request | Lộ field nội bộ; client set `role`/`tenantId`/`status` | Request/Response DTO + MapStruct |
| Controller gọi repository | Bỏ qua BR / ownership / transaction | Controller → service (interface) → repo |
| `findById(id)` không kèm chủ sở hữu/tenant | User A đổi id URL đọc/sửa được của B | `findByIdAndTenantId` / Specification owner |
| Lấy `userId`/`tenantId`/role từ body/param/header client | Client tự khai là người khác | Security context |
| Nối chuỗi input vào JPQL/native; sort theo cột từ request | SQL injection; dò dữ liệu | Bind param; whitelist cột sort |
| `@Transactional` trên controller | Giữ connection cả lúc serialize | Đặt ở service, hẹp nhất |
| Gọi HTTP/downstream chậm trong transaction | Cạn connection pool, service treo | Ngoài transaction; outbox |
| Publish event/ghi cache trước commit | Consumer nhận event của dữ liệu đã rollback | `@TransactionalEventListener(AFTER_COMMIT)` |
| Nuốt exception / catch rồi trả 200 | Client tưởng thành công; lỗi mất khỏi log | `BusinessException` + `@RestControllerAdvice` |
| `Optional.get()` trần | 500 + stack trace lộ nội bộ | `orElseThrow(...)` + enum code |
| Repository trong vòng lặp; `findAll()` không phân trang | N+1; bảng lớn → timeout | Bulk query; `Pageable` |
| Consumer/webhook/callback/job không idempotent | Retry = trừ tiền / tạo đơn 2 lần | Dedup eventId/idempotency key (inbox) |
| Hardcode secret/URL/timeout (kể cả test, yml) | Secret vào git = đã lộ | Env / `@ConfigurationProperties`. Lỡ commit → **xoay key** |
| Log password/token/OTP/Authorization/PII/full body | Log thành kho dữ liệu nhạy cảm | Mask; log id thay nội dung |
| `@Data` trên `@Entity` | hashCode đổi sau persist; toString kích lazy-load | `@Getter @Setter @NoArgsConstructor @AllArgsConstructor` |
| `new RestTemplate()`/`WebClient.create()` trong business | Không timeout, không truyền header tenant | `@HttpExchange` client |
| H2 trong test | Che lỗi dialect/JSONB/`TIMESTAMPTZ` tới lúc chạy thật | Testcontainers Postgres |

## §done
Build/lint/test pass, coverage ≥80%, không H2; file chỉ trong `services/boundaries/{name}/`; KG cập nhật.
