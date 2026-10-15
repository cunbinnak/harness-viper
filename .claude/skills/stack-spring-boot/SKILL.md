---
name: stack-spring-boot
description: Stack backend Java 21 + Spring Boot 4.x — scaffold · convention · make · config · §review (forbidden patterns cho reviewer/bug-hunter). Load khi target kind=backend stack=spring-boot. Version thật do docs/TECHSTACK.md + ADR chốt; 3.x đã EOL 6/2026 (chỉ dùng khi bảo trì codebase cũ).
---

# stack-spring-boot

> Idiom Java/Spring (cross-stack ở `docs/CONVENTIONS.md`; bảo mật ở `SECURITY.md`).
> Load khi BUILD/VERIFY target có frontmatter `kind: backend, stack: spring-boot`.

## §1 Khi load
BUILD target backend (scaffold/code) · VERIFY (reviewer/bug-hunter đọc **§review**).

## §2 Scaffold
- Vào `services/boundaries/<name>/`. Dùng **Spring Initializr / Gradle** (Groovy DSL) — không chép boilerplate.
- **Gradle KHÔNG cần cài trên máy** — Initializr zip kèm sẵn `gradlew` wrapper, wrapper tự tải Gradle về. **"Máy không có gradle" KHÔNG phải lý do đổi build tool.** Build tool nằm trong ADR/TECHSTACK đã chốt — muốn đổi = đổi thứ đã chốt → `STATE §Blocker` hoặc `ROADMAP §backlog` (wave sau top-up ADR), **KHÔNG xử bằng 1 dòng DECISIONS rồi đổi luôn**.
- Cấu trúc **Layered** (default): `controller/` · `service/` + `service/impl/` · `repository/` · `entities/` · `dto/{request,response}/` · `mapper/` · `config/` · `exception/` · `enums/` · `constant/` (tạo khi có hằng số dùng chung — xem §3 Hằng số). (Hexagonal chỉ khi có ADR.)
- **Dockerfile multi-stage** (Gradle `bootJar` → JRE) + `application.yml` Postgres + migration (Flyway) NGAY lúc scaffold.
- Artifact local → `deployment/local/` (docker-compose db). `git commit`.

## §3 Convention (Java/Spring — bắt buộc)
- **Entity**: `{Resource}Entity` ở `entities/`; `@Getter @Setter @NoArgsConstructor @AllArgsConstructor` — **KHÔNG `@Data` trên `@Entity`**. Không FK constraint (liên kết qua id column + **tự add index**); toàn vẹn ở service layer.
- **Layering**: Controller (map + validate + gọi **service interface**) → Service impl (`@Service`, business logic + `@Transactional` + publish event) → Repository (chỉ query). **Controller KHÔNG gọi repository.** Inject **interface**, `@RequiredArgsConstructor` + `private final` (không `@Autowired` field).
- **DTO**: Request/Response DTO ở biên; **KHÔNG phơi `@Entity`**. Convert bằng **MapStruct** (mapper interface) — **HYBRID, KHÔNG hand-map cả cụm**: field trùng tên/kiểu → mapper tự map; field KHÔNG-1-1 khai `@Mapping` (generated → `ignore` rồi set tay ở service · hằng số → `constant` · điều kiện/theo quyền → `expression`/param · đa nguồn → `source="b.x"` + tham số thứ 2). Set tay CHỈ field có lý do đó; dãy `setX(src.getX())` thuần = sai (dùng mapper). Chi tiết + ví dụ: `ref-backend-pattern §Mapper`.
- **Response/Request generic** (`ref-backend-pattern §6`, dựng 1 lần ở `common/` lúc scaffold): controller trả **một lớp** `SuccessResponse<T>` qua `ResponseUtil.ok(..)` — KHÔNG `ResponseEntity<SuccessResponse<..>>` lồng; `ResponseEntity` chỉ khi tải file / 201 kèm `Location` / header đặc biệt (201 thường → `@ResponseStatus(CREATED)`). Service trả DTO hoặc `Page<DTO>` — `ResponseUtil.ok(page)` tự thành `PageResponse`, KHÔNG dựng `PageResponse` tay. `data` là DTO có kiểu, KHÔNG `Map`/`Object`/`?`. Lỗi: `ErrorResponse` (`code` = mã nghiệp vụ, HTTP status theo `ErrorCode.httpStatus()`), chỉ sinh ở `GlobalExceptionHandler` — KHÔNG try/catch trong controller để tự dựng lỗi; BE trả mã, không quản message i18n.
- **Exception**: `BusinessException` + error code **enum** theo domain; `@RestControllerAdvice` map tập trung. `orElseThrow(...)`, không `Optional.get()` trần.
- **Hằng số**: "hằng số" = giá trị cố định viết thẳng trong code (chuỗi · số · thời lượng · giờ trong ngày, viết trần hoặc khai `static final`), không đổi khi chạy. Phân loại rồi đặt đúng chỗ:

  | Loại | Nhận biết | Đặt ở |
  |---|---|---|
  | **Tập giá trị đóng** | role · status · type · action · source — tập hữu hạn biết trước | **enum** ở `enums/`; field entity/principal/DTO khai **kiểu enum** (`@Enumerated(EnumType.STRING)`), KHÔNG `String`. So `== UserRole.HR`, KHÔNG `"HR".equals(...)` / `case "HR"` |
  | **Hằng số dùng chung** | ≥ 2 class dùng, HOẶC là khoá mà hai bên phải khớp: tên header · MDC key · prefix key cache/storage · entity type audit · link điều hướng | `constant/{Domain}Constants.java` (`final` + private ctor). Một giá trị — một nơi khai |
  | **Tham số nghiệp vụ/vận hành** | con số Authority/DECISIONS chốt, có thể đổi mà logic không đổi: số ngày lưu · trần OT · giờ ca · ngưỡng rate limit · dung lượng file tối đa · TTL | `application.yml` + `@ConfigurationProperties` (default trong yml, KHÔNG trong class) |
  | **Hằng số nội bộ** | chỉ 1 class dùng, là chi tiết cài đặt: regex `Pattern` · magic byte · header cột file export · formatter | để `private static final` ngay trong class đó — **đúng, không chuyển** |

  Không thuộc diện này: error code (enum `*ErrorCode` — dòng Exception) · secret (env).
- **Transaction**: `@Transactional` ở service; read-only khi phù hợp. **Không gọi external chậm trong transaction.** Publish event **AFTER_COMMIT** / outbox.
- **Persistence**: JPQL/Specification (filter động → Specification, không `(:x IS NULL OR ...)`). **`nativeQuery` CHỈ khi JPQL/Specification không diễn đạt được** (window function · CTE · full-text search) — bắt buộc comment `// native: <lý do>` + bind param + `:tenantId`; thiếu lý do = dùng sai. Migration additive (không sửa file đã apply). Tránh N+1, list phải `Pageable`.
- **Tìm kiếm/danh sách có lọc**: method theo `arch §3` (≥ 3 tiêu chí hoặc lọc mảng/khoảng → `POST /{resources}/search` + `{Resource}SearchRequest`; ít hơn → `GET` + `@ModelAttribute`). Lọc động **LUÔN bằng Specification** qua khung generic `ref-backend-pattern §6`: `{Resource}SearchRequest extends PageRequestBase`, field gắn annotation toán tử (`@Equal` `@Like` `@In` `@Bw`…) → `SearchSpecification.of(req)`; điều kiện annotation không biểu diễn được (phạm vi quyền, subquery) → hàm trong `{Resource}Specifications` ghép `.and(..)`; repository `JpaSpecificationExecutor` → `findAll(spec, req.toPageable(SORTABLE))` — lọc, phân trang, sort (whitelist, size ≤ 100) đều ở DB. **CẤM**: `findAll()` rồi `.stream().filter(..)` · tự cắt trang `subList` / `new PageImpl<>(list)` · JPQL `(:x IS NULL OR ..)` · derived query tổ hợp `findByAAndBAndC` · if/else chọn method repository theo tổ hợp tiêu chí. Ngoại lệ: `findAll()` bảng danh mục nhỏ (phòng ban, loại phép) để map tên.
- **Idempotency**: consumer/webhook/callback/job dedup theo id (inbox). **Multi-tenant**: mọi query filter `tenant_id` từ auth context.
- **Timestamp**: `Instant` (entity/response/event) · `OffsetDateTime` (request) · `LocalDate` (date-only). **KHÔNG `LocalDateTime`**.
- **Import**: không FQCN inline, không wildcard, không `var`. **Config**: `@ConfigurationProperties`, không hardcode; secret qua env.
- **Test**: JUnit5 + Mockito (unit) · **Testcontainers Postgres** (integration, **KHÔNG H2**) · ≥1 test BOOT context + migration + `ddl-auto: validate` (bắt schema-drift) · thời gian qua `Clock` tiêm được (không `now()` trần). Coverage ≥ **80%**. Mẫu + cấu trúc: **`ref-backend-test`**.

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
| `nativeQuery` không có comment `// native: <lý do>` | JPQL/Spec làm được mà đi cửa sau — mất type-safety, schema-drift không bắt lúc compile | JPQL/Specification; native kèm comment lý do (window/CTE/full-text) |
| Response lồng `ResponseEntity<SuccessResponse<..>>` · `ResponseEntity.ok(ResponseUtil.ok(..))` · wrapper tự chế theo màn | Mỗi màn một kiểu bọc — FE parse lệch, đổi khung phải sửa trăm chỗ | Trả thẳng `SuccessResponse<T>` qua `ResponseUtil.ok(..)` (§6) |
| `new PageResponse<>(..)` dựng tay · `Map`/`Object`/`?` làm `data` | Lệch shape phân trang; contract không có kiểu, FE đoán field | Service trả `Page<DTO>` → `ResponseUtil.ok(page)`; DTO có kiểu |
| Sort theo tên field client gửi không whitelist · size không trần | Dò cột / sort cột không index · kéo cả bảng một trang | `PageRequestBase.toPageable(SORTABLE)` · `@Max(100)` |
| Lọc/phân trang trong bộ nhớ: `findAll()` → `.stream().filter` · `subList` · `new PageImpl<>(list)` | Nạp cả bảng mỗi request — chậm dần theo dữ liệu, có thể OOM | `{Resource}Specifications` + `findAll(spec, pageable)` |
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
