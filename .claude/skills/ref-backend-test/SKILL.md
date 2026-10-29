---
name: ref-backend-test
description: Pattern test cho MAIN viết ở BUILD — backend Java/Spring (unit · integration · kiến trúc · schema drift). JUnit5 + Mockito + AssertJ, Testcontainers Postgres/Kafka (KHÔNG H2), WireMock cho hệ ngoài, đồng hồ tiêm được (Clock) để test hạn chót, factory dữ liệu, đặt tên theo hành vi, JaCoCo 80%. Load khi BUILD target kind=backend.
---

# Reference: Backend Test (MAIN viết ở BUILD)

> Đây là **lưới an toàn của người làm** — chạy bằng `make test`, không thay được TC nghiệm thu của `test-writer` (`test-writer.md` — ba tầng bằng chứng). Viết CÙNG LÚC code (`/build` Bước 5), không dồn cuối.
> Config dependency + JaCoCo: `ref-backend-config §9`. ArchUnit: `ref-backend-pattern §7.5`. Forbidden: `stack-spring-boot §review`.

## 1. Tầng test + đặt ở đâu
| Tầng | Thư mục (`src/test/java/.../{name}/`) | Chạy gì | Không làm |
|---|---|---|---|
| **unit** | `unit/` | 1 service/mapper/validator, phụ thuộc mock bằng Mockito — **không Spring context** (`@ExtendWith(MockitoExtension.class)`) | không DB, không `@SpringBootTest` |
| **integration** | `integration/` | controller → service → repository → **Postgres thật (Testcontainers)**; MockMvc hoặc gọi HTTP | không H2, không mock repository nội bộ |
| **architecture** | `architecture/ArchitectureTest.java` | ArchUnit — layer/package/cycle | — |
| **schema drift** | `integration/` | ≥1 test boot context + chạy migration + `ddl-auto: validate` | — |

Ưu tiên viết (thứ vỡ thì đau nhất): luật nghiệp vụ ở service (BR · bảng chính sách — hạn chót, hạn mức, trùng) → chuyển trạng thái → phân quyền + chủ sở hữu/tenant → validate → mapper có logic.

## 2. Đặt tên + cấu trúc
- Tên nói **hành vi và điều kiện**: `chan_dang_ky_sau_han_chot_17h()` / `rejectsRegistrationAfterDeadline()` — không `test1`, `testCreate`.
- Thân theo **Given / When / Then** (comment 3 khối). Một test = một hành vi.
- Assert **kết quả nghiệp vụ + mã lỗi** (`assertThatThrownBy(...).isInstanceOf(BusinessException.class).extracting("code").isEqualTo(RemoteErrorCode.DEADLINE_PASSED)`), không assert chi tiết cài đặt (thứ tự gọi nội bộ, field private).

## 3. Thời gian — đồng hồ tiêm được (bắt buộc khi có hạn chót / kỳ / hết hạn)
Code KHÔNG gọi `LocalDate.now()` / `Instant.now()` trần — inject `Clock`:
```java
@Configuration
class ClockConfig {
  @Bean Clock clock(@Value("${app.clock.fixed:}") String fixed) {        // fixed chỉ đặt ở profile local
    ZoneId vn = ZoneId.of("Asia/Ho_Chi_Minh");
    return fixed.isBlank() ? Clock.system(vn) : Clock.fixed(OffsetDateTime.parse(fixed).toInstant(), vn);
  }
}
```
- Unit test: `Clock.fixed(Instant.parse("2026-10-15T10:00:01Z"), ZoneId.of("Asia/Ho_Chi_Minh"))` (= 17:00:01 giờ VN) → test đủ 3 điểm biên.
- **QC test được hạn chót trên hệ thật**: `application-local.yml` đọc `app.clock.fixed: ${APP_CLOCK_FIXED:}` → `test-writer` đặt env `APP_CLOCK_FIXED=2026-10-15T17:00:01+07:00`, restart container, chạy TC. Property này **chỉ khai ở profile local** — profile prod không có (không endpoint đổi giờ, SECURITY §4). Compose phải chuyển biến này vào container: khai `APP_CLOCK_FIXED: ${APP_CLOCK_FIXED:-}` ở `environment` của service (mẫu ở `infra-local-dev`). Không khai thì QC đặt biến nào container cũng không nhận. QC thường không restart hệ chính mà chạy **bản sao** bằng `scripts/qa_iso.py` (`--mode frozen` đặt đúng biến này; `--mode run` gắn libfaketime để job định kỳ tự chạy) — script chép environment của container backend, chỉ đổi DB và đồng hồ, nên backend phải đọc DB qua biến chứa `jdbc:postgresql://…/<db>` và image phải có `sh`.

## 4. Unit — mẫu
```java
@ExtendWith(MockitoExtension.class)
class RemoteRequestServiceTest {
  @Mock RemoteRequestRepository repo;
  @Mock LeaveQueryPort leaves;                                   // xung đột với phép đã duyệt
  Clock at(String vnTime) { return Clock.fixed(OffsetDateTime.parse(vnTime).toInstant(), ZoneId.of("Asia/Ho_Chi_Minh")); }

  @Test void chan_dang_ky_sau_han_chot() {
    var svc = new RemoteRequestServiceImpl(repo, leaves, at("2026-10-15T17:00:01+07:00"));
    assertThatThrownBy(() -> svc.register(EMP_A, LocalDate.parse("2026-10-16")))
        .isInstanceOf(BusinessException.class).extracting("code").isEqualTo(RemoteErrorCode.DEADLINE_PASSED);
    verify(repo, never()).save(any());                            // bị chặn → không ghi
  }
}
```
Mapper MapStruct: dùng mapper thật `Mappers.getMapper(X.class)` (hoặc `@Spy`), không mock mapper.

## 5. Integration — Testcontainers (KHÔNG H2)
```java
@SpringBootTest(webEnvironment = RANDOM_PORT) @AutoConfigureMockMvc @Testcontainers
abstract class IntegrationTestBase {
  @Container @ServiceConnection
  static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16-alpine");   // package/generic theo version Testcontainers trong build
}
```
- Kafka: `@Container @ServiceConnection KafkaContainer` — consumer test chờ bằng Awaitility (`await().atMost(5, SECONDS)`), KHÔNG `Thread.sleep`.
- Hệ ngoài (HTTP đối tác, email API): **WireMock** tại base-url cấu hình (`ref-backend-restclient`) — assert đã gọi đúng path/body (`verify(postRequestedFor(...))`).
- Dọn dữ liệu: mỗi test tự tạo dữ liệu qua **factory** (`TestData.employee().inDept("IT").build()`), dọn bằng `@Transactional` rollback (MockMvc cùng thread) hoặc truncate trong `@AfterEach` — test **độc lập thứ tự**.
- Mỗi API ghi: kiểm **status + envelope** (`CONVENTIONS §3`) **và đọc lại DB** (repository) — chuẩn kiểm như QC.
- Phân quyền: test với 2 user (A/B, khác phòng/tenant) — B gọi id của A → 403/404 đúng `arch §3`.

## 6. Schema drift + kiến trúc
- `src/test/resources/application-test.yml`: `spring.jpa.hibernate.ddl-auto: validate` + Flyway bật → test boot context bắt entity ↔ migration lệch.
- `ArchitectureTest` theo `ref-backend-pattern §7.5`.

## 7. Coverage + chạy
`./gradlew test jacocoTestReport` · `check.dependsOn jacocoTestCoverageVerification` (≥ 80% — `ref-backend-config §9`). Coverage là sàn, không phải mục tiêu: test chỉ để tăng % (getter, assert rỗng, `assertDoesNotThrow` suông) = cấm.

## 8. Cấm
H2 · `@SpringBootTest` cho unit · mock repository/service nội bộ trong integration · `Thread.sleep` · `LocalDate.now()` trong code nghiệp vụ · test phụ thuộc thứ tự · `@Disabled` không lý do · sửa test cho xanh khi code sai.
