---
name: ref-backend-pattern
description: Cấu trúc backend boundary — DEFAULT Layered (classic Spring 3-tier); Hexagonal (Ports & Adapters) chỉ opt-in qua ADR khi domain phức tạp. JPA @Entity ở package entities/ tên {Resource}Entity. Layout artifact, layer responsibilities, interface/impl, response & error shape, forbidden patterns.
---

> Situational ref cho stack-spring-boot — load khi BUILD backend boundary (layout cấu trúc).
# Reference: Backend Structure (Layered | Hexagonal)

> **Purpose:** Layout chuẩn 1 backend boundary để BUILD/verify scaffold đồng nhất.
> **Load khi:** BUILD backend target — scaffold cấu trúc boundary (stack-spring-boot §situational trỏ tới).
> **Quan hệ:** `stack-spring-boot` là convention bắt buộc và trỏ sang file này cho cấu trúc; file này KHÔNG lặp lại rule, chỉ mô tả nơi đặt từng artifact (thuật ngữ khớp `stack-spring-boot §Layering`).
> **Tách bạch:** cấu trúc = file này · config chi tiết (application.yml, security, kafka…) = `ref-backend-config`.
> **Tuning:** mô hình + layer/package của boundary **đã chốt ở `docs/arch/{name}.md`** (theo ADR backend-architecture). File này KHÔNG quyết lại — chỉ cung cấp layout chuẩn cho mô hình mà arch doc đã chốt. Cây thư mục dưới là khung tối thiểu — package tùy chọn (`event/`, `scheduler/`, `util/`…) chỉ thêm khi boundary cần.
> **Cache/Redis:** có ref skill riêng (pattern interface + impl adapter), KHÔNG mô tả ở file này.

## 1. Chọn mô hình — **DEFAULT = Layered**

> **Mặc định LUÔN dùng Layered.** Chỉ dùng Hexagonal khi ADR backend-architecture giải trình rõ domain đủ phức tạp (nhiều inbound/outbound, cần tách domain khỏi framework). Không chắc → Layered.

| Mô hình | Khi dùng | Luồng |
|---|---|---|
| **Layered** (classic Spring) — **DEFAULT** | CRUD, domain ít/vừa phức tạp (đa số boundary) | `controller → service → repository` |
| **Hexagonal** (Ports & Adapters) — opt-in qua ADR | Nghiệp vụ phức tạp rõ rệt, cần tách domain khỏi framework | `adapter.in → application (use case) → domain`; outbound qua port, `adapter.out` impl |

Một boundary = một target, root `services/boundaries/{name}/`.

## 2. Layout — Layered (classic Spring 3-tier)

```
services/boundaries/{name}/src/main/java/.../{name}/
├── controller/
│   └── {Resource}Controller.java           # map request/response, validation annotation, gọi service
├── service/
│   ├── {Resource}Service.java              # interface use case
│   └── impl/{Resource}ServiceImpl.java     # @Service, @Transactional, business logic, @RequiredArgsConstructor injection
├── repository/
│   └── {Resource}Repository.java           # Spring Data JPA interface (JPQL/Specification, no nativeQuery)
├── entities/                               # JPA @Entity (KHÔNG để 'model')
│   └── {Resource}Entity.java               # @Entity: tên {Resource}Entity, no @Data, no FK (liên kết qua id column)
├── dto/
│   ├── request/{Resource}Request.java      # request DTO + Bean Validation
│   └── response/{Resource}Response.java    # response DTO (KHÔNG expose entity)
├── mapper/{Resource}Mapper.java            # convert DTO ↔ entity (không gọi service/repository/client)
├── event/                                  # Kafka — thêm khi boundary phát/nhận event
│   ├── producer/{Resource}EventPublisher.java  # publish after-commit (@TransactionalEventListener AFTER_COMMIT)
│   ├── consumer/{Topic}Consumer.java           # @KafkaListener — idempotent (dedup theo event/message id)
│   └── payload/{Resource}Event.java            # event schema/DTO (không raw Map); topic name lấy từ config
├── enums/                                  # business enum
│   ├── {Resource}Status.java               # enum trạng thái nghiệp vụ
│   └── {Resource}ErrorCode.java            # enum mã lỗi per-domain
├── constant/                               # constants class theo domain (final + private ctor)
│   ├── {Domain}Constants.java
│   └── HeaderConstants.java · LogConstants.java   # tên header (X-Request-ID…) · khoá MDC (traceId…) — ref-backend-logging §3
├── common/                                 # khung generic dựng 1 lần lúc scaffold (§6) — KHÔNG chế wrapper riêng theo màn
│   ├── response/                           # ResponseBase · SuccessResponse<T> · ErrorResponse · PageResponse<T> · ResponseUtil · ResponseStatusType
│   ├── request/                            # PageRequestBase (page · size ≤100 · sort whitelist · order) · SortOrder
│   └── search/                             # annotation toán tử (@Equal @Like @In @Bw…) · Range<T> · SearchSpecification
├── exception/
│   ├── ErrorCode.java                      # interface (code, message, httpStatus) — enum per-domain implements
│   ├── CommonErrorCode.java                # mã chung mọi target: VALIDATION_ERROR · INVALID_SORT · FORBIDDEN · INTERNAL_ERROR
│   ├── BusinessException.java              # base business exception (nhận ErrorCode [+ additionalData])
│   └── GlobalExceptionHandler.java         # @RestControllerAdvice: map exception → ErrorResponse (§6)
├── config/                                 # CHỈ @Configuration bean + @ConfigurationProperties
│   ├── {Domain}Properties.java             # @ConfigurationProperties (config nhóm)
│   └── {Web,Security,…}Config.java         # @Configuration bean (chi tiết → ref-backend-config)
├── scheduler/                              # job định kỳ (@Scheduled) — thêm khi boundary cần (data lớn: paginate/batch)
└── util/                                   # helper thuần (formatter, validator, date) — thêm khi dự án cần

resources/db/migration/                     # migration versioned, no FK
src/test/java/.../{name}/                   # unit/ (service mock repo) · integration/ (controller + DB thật) · architecture/ArchitectureTest.java (§7.5)
```

## 3. Layout — Hexagonal (Ports & Adapters)

```
services/boundaries/{name}/src/main/java/.../{name}/
├── domain/
│   ├── model/                  # Domain model: aggregate, entity, value object (pure, no framework)
│   ├── enums/                  # business enum + {Resource}ErrorCode (mã lỗi)
│   ├── service/                # Domain service thuần (nếu có)
│   └── exception/              # ErrorCode (interface) + BusinessException  (GlobalExceptionHandler ở adapter/in/web)
├── application/
│   ├── port/
│   │   ├── in/                 # Inbound port = use case interface (vd CreateOrderUseCase)
│   │   └── out/                # Outbound port = repository/gateway interface (vd LoadOrderPort, SaveOrderPort)
│   └── service/                # Use case impl (application service), @Transactional, impl inbound port
├── adapter/
│   ├── in/
│   │   ├── web/                 # Inbound adapter (REST): Controller + dto/{request,response} + mapper + GlobalExceptionHandler
│   │   ├── messaging/           # Inbound adapter (Kafka consumer): {Topic}Consumer — idempotent
│   │   └── scheduler/           # Inbound adapter (job định kỳ @Scheduled) — thêm khi cần
│   └── out/
│       ├── persistence/         # Outbound adapter: repository + entities/{Resource}Entity.java (JPA @Entity), impl outbound port
│       ├── client/              # Outbound adapter: external HTTP client, impl outbound port
│       └── messaging/           # Outbound adapter (Kafka producer): {Resource}EventPublisher — publish after-commit
├── constant/                   # constants class theo domain
├── common/                     # khung generic §6: response/ · request/ · search/ (dùng ở adapter/in/web + adapter/out/persistence)
├── config/                     # @ConfigurationProperties + @Configuration bean + DI wiring
└── util/                       # helper thuần — thêm khi dự án cần

resources/db/migration/         # migration versioned, no FK
src/test/java/.../{name}/       # unit/ · integration/ · architecture/ArchitectureTest.java (§7.5)
```

## 4. Trách nhiệm từng thành phần

**Layered:**

| Thành phần | Trách nhiệm |
|---|---|
| `controller/` | Map request/response, validation annotation, gọi service. KHÔNG business logic. |
| `service/` (+`impl/`) | Business logic, transaction boundary, business validation, orchestration, quyết định publish event. |
| `repository/` | Persistence/query (Spring Data, JPQL/Specification). |
| `entities/` | JPA `@Entity` class tên `{Resource}Entity` (no @Data, no FK). KHÔNG để 'model'. |
| `dto/request` · `dto/response` | Schema vào/ra ở biên API. |
| `mapper/` | Convert DTO ↔ entity. KHÔNG gọi service/repository/client. |
| `event/` | Kafka: producer (publish after-commit) + consumer (idempotent) + payload DTO. Topic name từ config. |
| `enums/` | Business enum (status/type) + `{Resource}ErrorCode` (implements `ErrorCode`). |
| `constant/` | Constants class theo domain (`final`, private constructor). |
| `common/` | Khung generic §6: response bọc 1 lớp · `PageRequestBase` · `SearchSpecification`. Dựng 1 lần, mọi màn dùng lại. |
| `exception/` | `ErrorCode` interface + `CommonErrorCode` + `BusinessException` + `GlobalExceptionHandler` (khung §6). |
| `config/` | `@ConfigurationProperties` + `@Configuration` bean. |
| `util/` | Helper thuần, không state, không phụ thuộc layer khác. |
| `scheduler/` | Job định kỳ (`@Scheduled`) — thêm khi cần; data lớn phải paginate/batch. |

**Hexagonal:**

| Thành phần | Trách nhiệm |
|---|---|
| `domain/` | Model + enum + business rule + exception, thuần — KHÔNG phụ thuộc framework/adapter. |
| `application/port/in` · `port/out` | Hợp đồng (interface) vào/ra của use case. |
| `application/service` | Use case impl: orchestrate domain qua outbound port, transaction boundary. |
| `adapter/in/web` · `in/messaging` | Inbound adapter: REST controller (+ dto + mapper + GlobalExceptionHandler) / Kafka consumer (idempotent). |
| `adapter/out/persistence` · `out/client` · `out/messaging` | Outbound adapter: impl outbound port (DB / HTTP / Kafka producer). |

## 5. Interface + impl
- **Service / use case**: interface + impl tách riêng; caller phụ thuộc interface.
  - Layered: `service/{Resource}Service` + `service/impl/{Resource}ServiceImpl`.
  - Hexagonal: inbound port `application/port/in/{X}UseCase` impl ở `application/service/{X}Service`.
- **Repository**:
  - Layered: Spring Data interface `{Resource}Repository extends JpaRepository<…>` — auto-impl (custom query phức tạp → `{Resource}RepositoryCustom` + impl đi kèm).
  - Hexagonal: outbound port `application/port/out/{X}Port` impl bởi adapter `adapter/out/persistence/{X}PersistenceAdapter` (DIP).
- **Injection**: `@RequiredArgsConstructor` + `private final` — **Lombok sinh constructor, KHÔNG tự viết constructor tay**, KHÔNG `@Autowired` trên field/setter.

```java
// service/{Resource}Service.java + service/impl/{Resource}ServiceImpl.java  (Layered)
public interface OrderService { OrderResponse create(OrderRequest req); }

@Service
@RequiredArgsConstructor                     // Lombok sinh constructor từ field `final` — KHÔNG viết constructor tay
class OrderServiceImpl implements OrderService {
    private final OrderRepository repository;
    private final OrderMapper mapper;
    // KHÔNG khai constructor tay, KHÔNG @Autowired field/setter
}

// repository/OrderRepository.java  (Spring Data — auto-impl, JPQL khi cần)
public interface OrderRepository extends JpaRepository<Order, Long> {
    Optional<Order> findByCode(String code);
}
```

### Mapper (MapStruct)
- Mapper là **interface** + `@Mapper` — MapStruct generate impl, KHÔNG viết impl tay.
- Config chuẩn: `componentModel = "spring"` (inject qua constructor) · `nullValuePropertyMappingStrategy = IGNORE` cho update (partial — không ghi đè null) · `unmappedTargetPolicy = IGNORE` (không fail khi field chưa map) · custom type converter gom `MapperComponent` (`@Named`), reuse mọi mapper qua `uses =`.

```java
@Mapper(componentModel = "spring",
        uses = MapperComponent.class,
        nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE,  // update partial
        unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface OrderMapper {
    OrderResponse toResponse(OrderEntity entity);
    OrderEntity toEntity(CreateOrderRequest request);
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updateEntity(UpdateOrderRequest request, @MappingTarget OrderEntity entity);
}

// Custom type conversion (Instant↔String, enum↔code…) reuse mọi mapper qua uses=
@Component
public class MapperComponent {
    @Named("instant2StringTz") public String i2s(Instant v) { return v != null ? v.toString() : null; }
    @Named("stringTz2Instant") public Instant s2i(String v) { return v != null ? Instant.parse(v) : null; }
}
```

**HYBRID — field KHÔNG map 1-1** (lỗi hay gặp: vài field đặc biệt → hand-map CẢ CỤM. SAI: mapper vẫn lo phần trùng, chỉ field dưới mới khai/set tay):

| Loại field | Cách khai (không hand-map cả cụm) |
|---|---|
| **Generated** (id · `employeeNumber` sinh runtime) | `@Mapping(target=..., ignore=true)` → **set tay ở service** sau khi gọi mapper |
| **Hằng số** (`status = PENDING_ACTIVATION`) | `@Mapping(target="status", constant="PENDING_ACTIVATION")` |
| **Điều kiện / theo quyền** (`baseSalary` che theo role — DEC) | thêm **param** + `@Mapping(target="baseSalary", expression="java(canView ? e.getBaseSalary() : null)")` |
| **Đa nguồn** (`departmentName` từ `Department`) | **tham số thứ 2** + `@Mapping(target="departmentName", source="dept.name")` |

```java
@Mapping(target = "id", ignore = true)
@Mapping(target = "employeeNumber", ignore = true)              // generated → set tay ở service
@Mapping(target = "status", constant = "PENDING_ACTIVATION")    // hằng số
EmployeeEntity toEntity(CreateEmployeeRequest request);

@Mapping(target = "departmentName", source = "dept.name")       // đa nguồn (tham số thứ 2)
@Mapping(target = "baseSalary",
         expression = "java(canViewSalary ? emp.getBaseSalary() : null)")  // điều kiện/quyền
EmployeeDetailResponse toDetailResponse(EmployeeEntity emp, DepartmentEntity dept, boolean canViewSalary);
```
```java
// service — chỉ field generated set tay:
EmployeeEntity emp = employeeMapper.toEntity(request);
emp.setEmployeeNumber(generateEmployeeNumber());
```
> Reviewer: hand-map field **trùng 1-1** mà mapper làm được = finding → chuyển mapper; set tay/expression field **có lý do** (4 loại trên) = tha. Che field null theo quyền → `@JsonInclude(NON_NULL)` đặt **trên field đó**, KHÔNG cả class (kẻo nuốt field null-có-nghĩa như `probationEndDate`).

## 6. Request/Response generic + tìm kiếm generic (khung chung)

Khung tự viết **trong dự án**, theo SDK nội bộ `cec-core` (response) + `cec-jpa` (tìm kiếm) — không kéo SDK làm dependency. MAIN dựng **một lần** lúc scaffold ở `common/` (+ `exception/`); mọi controller/service dùng lại, KHÔNG tự chế wrapper riêng theo màn. Contract cụ thể (mã lỗi, endpoint) chốt ở `docs/arch/{name}.md §3 API`.

1. **Success** — `SuccessResponse<T>`: `code` = `"SUCCESS"` · `message` · `timestamp` · `data`. Tạo **chỉ** qua `ResponseUtil.ok(..)`.
2. **Error** — `ErrorResponse`: `code` = mã nghiệp vụ (`ErrorCode.code()`) · `message` · `timestamp` · `additionalData` (field lỗi validate…, KHÔNG stacktrace/SQL). Tạo **chỉ** trong `GlobalExceptionHandler` qua `ResponseUtil.err(..)`. BE trả **mã** — FE tự hiển thị theo mã, BE không quản message i18n.
3. **HTTP status đúng trường hợp** theo `ErrorCode.httpStatus()` (400/401/403/404/409/422/500) — không ép mọi lỗi về 400.
4. **Một lớp bọc**: controller trả `SuccessResponse<T>`. KHÔNG `ResponseEntity<SuccessResponse<..>>` / `ResponseEntity.ok(ResponseUtil.ok(..))`. `ResponseEntity` CHỈ khi: tải file · 201 kèm `Location` · header đặc biệt. 201 không cần header → `@ResponseStatus(HttpStatus.CREATED)`. Handler lỗi được dùng `ResponseEntity` (status theo `ErrorCode`).
5. **Phân trang**: service trả `Page<XResponse>` → `ResponseUtil.ok(page)` → `SuccessResponse<PageResponse<XResponse>>`. KHÔNG `new PageResponse<>(..)` tay, KHÔNG tự cắt trang.
6. `data` là DTO có kiểu — KHÔNG `Map<String,Object>` / `Object` / `?`. Lỗi đi bằng `throw new BusinessException(XErrorCode.Y)` — KHÔNG try/catch trong controller để tự dựng lỗi.
7. **Tìm kiếm**: `{Resource}SearchRequest extends PageRequestBase`, field gắn annotation toán tử (`@Equal` `@NotEqual` `@Like` `@In` `@Ge` `@Le` `@Bw` `@IsNull`) → `SearchSpecification.of(req)`. Điều kiện annotation không biểu diễn được (phạm vi quyền, subquery, join) → hàm trong `{Resource}Specifications`, ghép `.and(..)`. Sort CHỈ theo whitelist; size ≤ 100.

```json
// success
{ "code": "SUCCESS", "message": "Success", "timestamp": "2026-10-14T08:00:00Z", "data": { "id": 42, "code": "ORD-001" } }
// page
{ "code": "SUCCESS", "message": "Success", "timestamp": "...",
  "data": { "content": [ ... ], "number": 0, "size": 20, "numberOfElements": 20, "totalElements": 137, "totalPages": 7,
            "first": true, "last": false, "hasNext": true, "hasPrevious": false, "hasContent": true } }
// error — HTTP 404
{ "code": "ORDER_NOT_FOUND", "message": "Order không tồn tại", "timestamp": "...", "additionalData": null }
// error — HTTP 400 validate
{ "code": "VALIDATION_ERROR", "message": "Dữ liệu không hợp lệ", "timestamp": "...",
  "additionalData": [ { "field": "quantity", "code": "Min" } ] }
```

### Khung code (copy theo — Layered: `common/` + `exception/`)

```java
// ── common/response ──────────────────────────────────────────────
public enum ResponseStatusType {
    SUCCESS("SUCCESS", "Success");
    private final String code; private final String message;
    ResponseStatusType(String code, String message) { this.code = code; this.message = message; }
    public String code() { return code; } public String message() { return message; }
}

@Getter @Setter
public abstract class ResponseBase {
    private String code;          // "SUCCESS" | mã lỗi nghiệp vụ
    private String message;
    private Instant timestamp;
}

@Getter @NoArgsConstructor @AllArgsConstructor(access = AccessLevel.PACKAGE)
public class SuccessResponse<T> extends ResponseBase {
    private T data;
}

@Getter @NoArgsConstructor @AllArgsConstructor(access = AccessLevel.PACKAGE)
public class ErrorResponse extends ResponseBase {
    private Object additionalData;
}

@Getter @NoArgsConstructor
public class PageResponse<T> {
    private List<T> content;
    private boolean hasContent, first, last, hasNext, hasPrevious;
    private int number, size, numberOfElements, totalPages;
    private long totalElements;

    static <T> PageResponse<T> of(Page<T> p) {
        PageResponse<T> r = new PageResponse<>();
        r.content = p.getContent(); r.hasContent = p.hasContent(); r.first = p.isFirst(); r.last = p.isLast();
        r.hasNext = p.hasNext(); r.hasPrevious = p.hasPrevious(); r.number = p.getNumber(); r.size = p.getSize();
        r.numberOfElements = p.getNumberOfElements(); r.totalPages = p.getTotalPages(); r.totalElements = p.getTotalElements();
        return r;
    }
}

public final class ResponseUtil {
    private ResponseUtil() {}
    public static <T> SuccessResponse<T> ok(T data) {
        return stamp(new SuccessResponse<>(data), ResponseStatusType.SUCCESS.code(), ResponseStatusType.SUCCESS.message());
    }
    public static SuccessResponse<Void> ok() {             // KHÔNG gọi ok(null): null khớp cả ok(Page) → NPE
        return stamp(new SuccessResponse<Void>(null), ResponseStatusType.SUCCESS.code(), ResponseStatusType.SUCCESS.message());
    }
    public static <T> SuccessResponse<PageResponse<T>> ok(Page<T> page) { return ok(PageResponse.of(page)); }
    public static ErrorResponse err(ErrorCode ec) { return err(ec, null); }
    public static ErrorResponse err(ErrorCode ec, Object additionalData) {
        return stamp(new ErrorResponse(additionalData), ec.code(), ec.message());
    }
    private static <R extends ResponseBase> R stamp(R r, String code, String message) {
        r.setCode(code); r.setMessage(message); r.setTimestamp(Instant.now());
        return r;
    }
}

// ── exception ────────────────────────────────────────────────────
public interface ErrorCode { String code(); String message(); HttpStatus httpStatus(); }

public enum CommonErrorCode implements ErrorCode {          // mã chung — giống nhau mọi target
    VALIDATION_ERROR("VALIDATION_ERROR", "Dữ liệu không hợp lệ", HttpStatus.BAD_REQUEST),
    INVALID_SORT("INVALID_SORT", "Trường sắp xếp không hợp lệ", HttpStatus.BAD_REQUEST),
    FORBIDDEN("FORBIDDEN", "Không có quyền", HttpStatus.FORBIDDEN),
    INTERNAL_ERROR("INTERNAL_ERROR", "Lỗi hệ thống", HttpStatus.INTERNAL_SERVER_ERROR);
    private final String code; private final String message; private final HttpStatus status;
    CommonErrorCode(String c, String m, HttpStatus s) { this.code = c; this.message = m; this.status = s; }
    public String code() { return code; } public String message() { return message; } public HttpStatus httpStatus() { return status; }
}
// enums/OrderErrorCode.java — mỗi domain một enum implements ErrorCode, cùng khuôn: NOT_FOUND("ORDER_NOT_FOUND", "Order không tồn tại", HttpStatus.NOT_FOUND)

public class BusinessException extends RuntimeException {
    private final transient ErrorCode errorCode;
    private final transient Object additionalData;
    public BusinessException(ErrorCode ec) { this(ec, null); }
    public BusinessException(ErrorCode ec, Object additionalData) { super(ec.message()); this.errorCode = ec; this.additionalData = additionalData; }
    public ErrorCode errorCode() { return errorCode; }
    public Object additionalData() { return additionalData; }
}

public record FieldViolation(String field, String code) {}

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {                       // nơi DUY NHẤT map exception → ErrorResponse
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handle(BusinessException e) {
        return ResponseEntity.status(e.errorCode().httpStatus()).body(ResponseUtil.err(e.errorCode(), e.additionalData()));
    }
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException e) {
        List<FieldViolation> fields = e.getBindingResult().getFieldErrors().stream()
                .map(f -> new FieldViolation(f.getField(), f.getCode())).toList();
        return ResponseEntity.badRequest().body(ResponseUtil.err(CommonErrorCode.VALIDATION_ERROR, fields));
    }
    @ExceptionHandler(Exception.class)                         // fallback — log đủ stacktrace, KHÔNG trả chi tiết ra client
    public ResponseEntity<ErrorResponse> handleUnknown(Exception e) {
        log.error("Unhandled exception", e);
        return ResponseEntity.internalServerError().body(ResponseUtil.err(CommonErrorCode.INTERNAL_ERROR));
    }
}

// ── common/request ───────────────────────────────────────────────
public enum SortOrder { ASC, DESC }

@Getter @Setter
public class PageRequestBase {
    @Min(0) private int page = 0;
    @Min(1) @Max(100) private int size = 20;                   // trần 100 — SECURITY §4
    private String sort;                                       // tên thuộc tính entity — PHẢI thuộc whitelist
    private SortOrder order = SortOrder.ASC;

    public Pageable toPageable(Set<String> sortable) {
        if (sort == null || sort.isBlank()) return PageRequest.of(page, size);
        if (!sortable.contains(sort)) throw new BusinessException(CommonErrorCode.INVALID_SORT);
        return PageRequest.of(page, size, Sort.by(order == SortOrder.DESC ? Sort.Direction.DESC : Sort.Direction.ASC, sort));
    }
}

// ── common/search — annotation toán tử (theo cec-jpa); field() = tên thuộc tính ENTITY ──
@Target(ElementType.FIELD) @Retention(RetentionPolicy.RUNTIME) public @interface Equal    { String field(); }
@Target(ElementType.FIELD) @Retention(RetentionPolicy.RUNTIME) public @interface NotEqual { String field(); }
@Target(ElementType.FIELD) @Retention(RetentionPolicy.RUNTIME) public @interface Like     { String field(); }   // chứa, không phân biệt hoa thường
@Target(ElementType.FIELD) @Retention(RetentionPolicy.RUNTIME) public @interface In       { String field(); }   // field kiểu Collection
@Target(ElementType.FIELD) @Retention(RetentionPolicy.RUNTIME) public @interface Ge       { String field(); }
@Target(ElementType.FIELD) @Retention(RetentionPolicy.RUNTIME) public @interface Le       { String field(); }
@Target(ElementType.FIELD) @Retention(RetentionPolicy.RUNTIME) public @interface IsNull   { String field(); }   // Boolean: true = IS NULL, false = IS NOT NULL
@Target(ElementType.FIELD) @Retention(RetentionPolicy.RUNTIME) public @interface Bw       { String field(); String from() default "from"; String to() default "to"; }

@Getter @Setter
public class Range<T extends Comparable<? super T>> { private T from; private T to; }   // dùng cho @Bw (Instant, LocalDate, BigDecimal…)

public final class SearchSpecification {
    private SearchSpecification() {}

    /** Dựng Specification từ các field có annotation toán tử; giá trị null / chuỗi rỗng / collection rỗng = bỏ qua. */
    public static <T> Specification<T> of(Object request) {
        Specification<T> spec = (root, query, cb) -> cb.conjunction();
        for (Field f : request.getClass().getDeclaredFields()) {
            Object v = read(f, request);
            if (v == null || (v instanceof String s && s.isBlank()) || (v instanceof Collection<?> c && c.isEmpty())) continue;
            Specification<T> part = toSpec(f, v);
            if (part != null) spec = spec.and(part);
        }
        return spec;
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static <T> Specification<T> toSpec(Field f, Object v) {
        if (f.isAnnotationPresent(Equal.class))    return (r, q, cb) -> cb.equal(r.get(f.getAnnotation(Equal.class).field()), v);
        if (f.isAnnotationPresent(NotEqual.class)) return (r, q, cb) -> cb.notEqual(r.get(f.getAnnotation(NotEqual.class).field()), v);
        if (f.isAnnotationPresent(Like.class))     return (r, q, cb) -> cb.like(cb.upper(r.<String>get(f.getAnnotation(Like.class).field())),
                                                           "%" + escapeLike(v.toString().trim().toUpperCase()) + "%", '\\');
        if (f.isAnnotationPresent(In.class))       return (r, q, cb) -> r.get(f.getAnnotation(In.class).field()).in((Collection<?>) v);
        if (f.isAnnotationPresent(Ge.class))       return (r, q, cb) -> cb.greaterThanOrEqualTo(r.<Comparable>get(f.getAnnotation(Ge.class).field()), (Comparable) v);
        if (f.isAnnotationPresent(Le.class))       return (r, q, cb) -> cb.lessThanOrEqualTo(r.<Comparable>get(f.getAnnotation(Le.class).field()), (Comparable) v);
        if (f.isAnnotationPresent(IsNull.class))   return (r, q, cb) -> Boolean.TRUE.equals(v)
                                                           ? cb.isNull(r.get(f.getAnnotation(IsNull.class).field()))
                                                           : cb.isNotNull(r.get(f.getAnnotation(IsNull.class).field()));
        if (f.isAnnotationPresent(Bw.class))       return between(f.getAnnotation(Bw.class), v);
        return null;
    }

    // Thiếu một đầu → chỉ >= hoặc <= (cb.between với null sẽ lỗi — lỗi có ở bản SDK)
    @SuppressWarnings({"unchecked", "rawtypes"})
    private static <T> Specification<T> between(Bw a, Object range) {
        BeanWrapper w = new BeanWrapperImpl(range);
        Comparable from = (Comparable) w.getPropertyValue(a.from());
        Comparable to = (Comparable) w.getPropertyValue(a.to());
        return (r, q, cb) -> {
            Path<Comparable> p = r.get(a.field());
            if (from != null && to != null) return cb.between(p, from, to);
            if (from != null) return cb.greaterThanOrEqualTo(p, from);
            if (to != null) return cb.lessThanOrEqualTo(p, to);
            return cb.conjunction();
        };
    }

    private static String escapeLike(String s) { return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_"); }

    private static Object read(Field f, Object target) {
        try { f.setAccessible(true); return f.get(target); }
        catch (IllegalAccessException e) { throw new IllegalStateException("Không đọc được field " + f.getName(), e); }
    }
}
```

### Dùng — controller · service · request

```java
// dto/request/OrderSearchRequest.java
@Getter @Setter
public class OrderSearchRequest extends PageRequestBase {
    @Equal(field = "status")         private OrderStatus status;
    @In(field = "outletId")          private List<UUID> outletIds;
    @Like(field = "code")            private String keyword;
    @Bw(field = "createdAt")         private Range<Instant> createdAt;
}

// service/impl/OrderServiceImpl.java
private static final Set<String> SORTABLE = Set.of("createdAt", "code");   // whitelist sort — hằng số nội bộ
public Page<OrderResponse> search(OrderSearchRequest req, UserPrincipal actor) {
    Specification<OrderEntity> spec = SearchSpecification.<OrderEntity>of(req)
            .and(OrderSpecifications.visibleTo(actor));                    // phạm vi quyền — annotation không biểu diễn được
    return orderRepository.findAll(spec, req.toPageable(SORTABLE)).map(orderMapper::toResponse);
}

// controller/OrderController.java — một lớp bọc, không ResponseEntity
@PostMapping("/search")
public SuccessResponse<PageResponse<OrderResponse>> search(@Valid @RequestBody OrderSearchRequest req,
                                                           @AuthenticationPrincipal UserPrincipal actor) {
    return ResponseUtil.ok(orderService.search(req, actor));
}
@GetMapping("/{id}")
public SuccessResponse<OrderResponse> get(@PathVariable UUID id) { return ResponseUtil.ok(orderService.get(id)); }
@PostMapping @ResponseStatus(HttpStatus.CREATED)
public SuccessResponse<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) { return ResponseUtil.ok(orderService.create(req)); }
@DeleteMapping("/{id}")
public SuccessResponse<Void> delete(@PathVariable UUID id) { orderService.delete(id); return ResponseUtil.ok(); }
@GetMapping("/{id}/export")                                              // ResponseEntity hợp lệ: tải file cần header
public ResponseEntity<byte[]> export(@PathVariable UUID id) { /* Content-Disposition + body */ }
```

> List ≤ 2 tiêu chí đi `GET` (technical-design): bind cùng `OrderSearchRequest` bằng `@Valid @ModelAttribute` — vẫn dùng `SearchSpecification`, không viết riêng.
> Không lấy từ SDK: `@SQLInjectionSafe` (lọc theo danh sách đen — phòng thủ thật là bind param + `escapeLike`), `BaseMapper<D,E>` (khung tách Request/Response DTO, MapStruct theo từng mapper), message i18n ở BE.

## 7. Forbidden patterns
- Business logic trong `controller/` (Layered) hoặc `adapter/in` (Hexagonal) — chỉ map + delegate.
- `controller/` gọi `repository/` trực tiếp — phải qua `service/`.
- Business logic trong `repository/` hoặc `mapper/`.
- `mapper/` gọi service/repository/external client.
- Hexagonal: `domain/` hoặc `application/` import `adapter/` — chỉ giao tiếp qua port.
- Expose entity ra API hoặc dùng entity làm request body.
- Import code từ `services/boundaries/{other}/` — cross-boundary chỉ qua HTTP/event theo `docs/arch/OVERVIEW.md §2`.

## 7.5. ArchUnit — enforce §7 bằng TEST (bắt buộc)

> Luật §7 phải được ép bằng **test chạy được** (deterministic), KHÔNG chỉ để review đọc — reviewer đọc N file có thể sót, ArchUnit thì không. Là JUnit test → gradle/Stop hook tự chạy; vi phạm = build ĐỎ ngay ở BUILD. **Scaffold BẮT BUỘC gồm `src/test/java/**/architecture/ArchitectureTest.java`** (≥1 file import `com.tngtech.archunit`). Dependency: xem `ref-backend-config` (`archunit-junit5`). Chọn biến thể theo mô hình chốt ở `docs/arch/{name}.md`.

**Layered:**
```java
@AnalyzeClasses(packages = "com.{org}.{boundary}", importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {
  @ArchTest static final ArchRule layered = layeredArchitecture().consideringAllDependencies()
      .layer("Controller").definedBy("..controller..")
      .layer("Service").definedBy("..service..")
      .layer("Repository").definedBy("..repository..")
      .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
      .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
      .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service");
  // controller KHÔNG gọi repository trực tiếp (§7)
  @ArchTest static final ArchRule ctrl_no_repo = noClasses().that().resideInAPackage("..controller..")
      .should().dependOnClassesThat().resideInAPackage("..repository..");
  // @Entity ở entities/ + tên *Entity
  @ArchTest static final ArchRule entity_pkg = classes().that().areAnnotatedWith(jakarta.persistence.Entity.class)
      .should().resideInAPackage("..entities..").andShould().haveSimpleNameEndingWith("Entity");
  // không cycle giữa slice
  @ArchTest static final ArchRule no_cycles = slices().matching("com.{org}.{boundary}.(*)..").should().beFreeOfCycles();
}
```

**Hexagonal (thêm/thay):** `domain`/`application` KHÔNG phụ thuộc `adapter` hay Spring —
```java
  @ArchTest static final ArchRule domain_pure = noClasses().that().resideInAPackage("..domain..")
      .should().dependOnClassesThat().resideInAnyPackage("..adapter..", "org.springframework..");
  @ArchTest static final ArchRule hexagonal = onionArchitecture()
      .domainModels("..domain..").applicationServices("..application..")
      .adapter("web", "..adapter.in.web..").adapter("persistence", "..adapter.out.persistence..");
```

> Rule phải khớp CHÍNH XÁC layout §2/§3 + stack-spring-boot (kẻo false-positive). Thêm rule khi boundary có pattern riêng (event handler, scheduler). ArchUnit chỉ cover **intra-boundary**; cross-boundary FK/import giữ ở review + contract-graph.

## 8. Done
- Cấu trúc khớp mô hình chốt trong ADR backend-architecture + `docs/arch/{name}.md`.
- API khớp `docs/arch/{name}.md §3 API`; schema khớp `docs/arch/{name}.md §1`.
- Build chạy được (`./gradlew` — default; `./mvnw` nếu ADR chọn Maven).
