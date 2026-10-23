---
name: ref-backend-logging
description: Pattern logging backend — config (JSON structured + level theo profile), SLF4J usage, MDC correlation (traceId/tenantId), masking dữ liệu nhạy cảm, exception logging tập trung. Load khi BUILD backend target cần chuẩn hóa log.
---

> Situational ref cho stack-spring-boot — load khi boundary cần chuẩn hóa logging.
# Reference: Backend Logging

> **Load khi:** BUILD backend target setup/chuẩn hóa logging (`build.md` Bước 3 nêu khi nào nạp).
> **Quan hệ:** convention bắt buộc → `stack-spring-boot` (§Logging & security); observability/tracing nâng cao → `ref-backend-config`.
> **Nguyên tắc:** structured log (JSON) ở môi trường thật; correlation qua MDC (`traceId`); KHÔNG log dữ liệu nhạy cảm; log exception 1 chỗ với context.

## 1. Config — appender theo profile + level

`logback-spring.xml`:
```xml
<configuration>
  <!-- local: console người đọc -->
  <springProfile name="local">
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
      <encoder><pattern>%d{HH:mm:ss} %-5level [%X{traceId}] %logger{36} - %msg%n</pattern></encoder>
    </appender>
    <root level="INFO"><appender-ref ref="CONSOLE"/></root>
  </springProfile>

  <!-- dev/sit/prod: JSON structured (logstash encoder) -->
  <springProfile name="dev,sit,prod">
    <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
      <encoder class="net.logstash.logback.encoder.LogstashEncoder">
        <includeMdcKeyName>traceId</includeMdcKeyName>
        <includeMdcKeyName>tenantId</includeMdcKeyName>
        <includeMdcKeyName>userId</includeMdcKeyName>
      </encoder>
    </appender>
    <root level="INFO"><appender-ref ref="JSON"/></root>
  </springProfile>
</configuration>
```

`application.yml` — level theo package (không hardcode trong code):
```yaml
logging:
  level:
    root: INFO
    com.example.order: DEBUG
    org.springframework.web: WARN
    org.hibernate.SQL: ${SQL_LOG_LEVEL:WARN}
```

## 2. Logger usage (SLF4J qua `@Slf4j`)

```java
@Slf4j                       // Lombok tạo field `log` — KHÔNG tự khai LoggerFactory.getLogger(...)
@Service
class OrderServiceImpl implements OrderService {
    void create(...) {
        log.info("order created id={} tenant={}", orderId, tenantId);   // parameterized, KHÔNG concat chuỗi
        log.debug("order payload size={}", lines.size());               // chi tiết dev -> DEBUG
    }
}
```
- **Logger BẮT BUỘC qua `@Slf4j`** (Lombok) — KHÔNG `private static final Logger log = LoggerFactory.getLogger(...)` thủ công (đồng bộ `stack-spring-boot`: DI dùng `@RequiredArgsConstructor`, logger dùng `@Slf4j`).
- **Levels:** `ERROR` (cần can thiệp) · `WARN` (bất thường có thể chịu được) · `INFO` (mốc nghiệp vụ) · `DEBUG` (chi tiết dev).
- Dùng placeholder `{}`, KHÔNG `"... " + var` (tránh tạo chuỗi khi level tắt).
- KHÔNG `System.out.println` / `printStackTrace()`.

## 3. MDC correlation (traceId / tenantId / userId)

Một mã truy vết đi xuyên mọi service: header **`X-Request-ID`** (theo SDK `cec-core`) ↔ khoá MDC **`traceId`**. Nhận ở cửa vào, gửi kèm mọi lời gọi ra (HTTP — `ref-backend-restclient §6`; Kafka — `ref-backend-kafka §3/§4`), mang sang thread khác (`@Async`). Tên header/khoá MDC khai **một nơi** ở `constant/` — KHÔNG viết literal rải rác (lệch tên = truy vết đứt giữa hai service).

```java
// constant/HeaderConstants.java · constant/LogConstants.java — một giá trị, một nơi khai
public final class HeaderConstants {
    private HeaderConstants() {}
    public static final String REQUEST_ID = "X-Request-ID";
    public static final String TENANT_ID = "X-Tenant-ID";
}
public final class LogConstants {
    private LogConstants() {}
    public static final String TRACE_ID = "traceId";
    public static final String TENANT_ID = "tenantId";
    public static final String USER_ID = "userId";
}

// config/CorrelationIdFilter.java — gắn traceId mỗi request, clear sau khi xong
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
class CorrelationIdFilter extends OncePerRequestFilter {
    private static final Pattern VALID_ID = Pattern.compile("[A-Za-z0-9-]{8,64}");   // id client gửi sai dạng → sinh mới (chặn log injection)

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        String incoming = req.getHeader(HeaderConstants.REQUEST_ID);
        String traceId = incoming != null && VALID_ID.matcher(incoming).matches() ? incoming : UUID.randomUUID().toString();
        MDC.put(LogConstants.TRACE_ID, traceId);
        res.setHeader(HeaderConstants.REQUEST_ID, traceId);
        try {
            chain.doFilter(req, res);
        } finally {
            MDC.clear();   // BẮT BUỘC clear — tránh leak context sang request/thread khác (thread pool)
        }
    }
}

// config/AsyncConfig.java — @Async mang MDC sang thread khác (Boot tự gắn TaskDecorator bean vào executor mặc định)
@Configuration
@EnableAsync
class AsyncConfig {
    @Bean
    TaskDecorator mdcTaskDecorator() {
        return task -> {
            Map<String, String> ctx = MDC.getCopyOfContextMap();
            return () -> {
                if (ctx != null) MDC.setContextMap(ctx);
                try { task.run(); } finally { MDC.clear(); }
            };
        };
    }
}
```
- Sau khi resolve security context: `MDC.put(LogConstants.TENANT_ID, ..)`, `MDC.put(LogConstants.USER_ID, ..)`.
- `@KafkaListener`: `traceId` lấy từ header `X-Request-ID` của record qua `RecordInterceptor` (`ref-backend-kafka §4`). `@Scheduled`: mỗi lượt chạy sinh `traceId` mới, clear ở `finally`.
- KHÔNG đưa IP client / thông tin request khác vào context khi chưa có yêu cầu (audit…) — giữ filter gọn.

## 4. Masking dữ liệu nhạy cảm

```java
log.info("login user={} ip={}", userId, ip);     // OK
// log.info("auth token={}", token);             // CẤM: token/password/secret/OTP/Authorization/PII
log.info("notify email={}", Masks.email(email)); // mask khi buộc phải log: a***@x.com
```
- KHÔNG log: password, token, refresh/access token, secret, OTP, Authorization header, PII (số CMND, thẻ…).
- Cần log định danh → mask (email/phone/card) qua util chung.

## 5. Exception logging (tập trung, không lặp)
- Log exception **1 lần ở boundary** (`GlobalExceptionHandler`) với context (`traceId` đã ở MDC) — KHÔNG `log + rethrow` ở mỗi tầng.
- Lỗi nghiệp vụ kỳ vọng (`BusinessException`) → `WARN`/`INFO` (không cần stacktrace dài).
- Lỗi hệ thống ngoài dự kiến → `ERROR` + stacktrace (exception là tham số CUỐI, không nhét vào `{}`).

```java
@Slf4j                       // KHÔNG LoggerFactory.getLogger(...) thủ công
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    ResponseEntity<ErrorResponse> handleBusiness(BusinessException e) {
        log.warn("business error code={}", e.errorCode().code());            // không stacktrace
        return ResponseEntity.status(e.errorCode().httpStatus()).body(/* ErrorResponse */ null);
    }

    @ExceptionHandler(Exception.class)
    ResponseEntity<ErrorResponse> handleUnexpected(Exception e) {
        log.error("unexpected error", e);                                    // exception cuối -> stacktrace
        return ResponseEntity.status(500).body(/* ErrorResponse code=INTERNAL_ERROR */ null);
    }
}
```

## Anti-patterns (review flag)
- `System.out.println` / `e.printStackTrace()` thay cho logger.
- Concat chuỗi (`"id=" + id`) thay vì placeholder `{}`.
- Log password/token/secret/OTP/PII (kể cả trong DEBUG).
- `log.error` + rethrow ở nhiều tầng → log trùng 1 lỗi nhiều lần.
- Quên `MDC.clear()` → traceId/tenant leak sang request khác (thread pool).
- Đặt level cứng trong code thay vì `application.yml`.

## Done
- Structured JSON ở môi trường thật; mọi log có `traceId` (MDC); không lộ dữ liệu nhạy cảm; exception log tập trung ở boundary; level theo config.
