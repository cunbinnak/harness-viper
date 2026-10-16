---
name: review-backend
description: Checklist review kind=backend cho reviewer/bug-hunter ở /verify — soi code Java/Spring theo 7 trục (AC/BR · bảo mật 6 nhóm + OWASP · Forbidden patterns · giao dịch/hợp đồng/idempotency/persistence · kiến trúc · test · lệch thứ đã chốt). Mỗi mục có lệnh tìm và chỗ nhìn.
---

# Review Backend

> Checklist review kind=backend — reviewer/bug-hunter load ở /verify khi boundary là kind này. Report: [BLOCKER/MAJOR/MINOR]+file:dòng+hỏng-thế-nào+đề-xuất.

Bạn soi code với con mắt độc lập — **bạn không phải người viết nó**, và đó là giá trị của bạn.
Chỉ đọc. Không hỏi user.

## 1. Nạp trước

| Đọc | Để soi |
|---|---|
| `docs/feat/FEAT-*.md` boundary đảm nhận | trục 1 |
| `docs/arch/{name}.md` §4 kiến trúc · §6 ca biên | trục 1, 5 |
| `docs/arch/{name}.md §3 API` · data model · events · integrations trong `docs/arch/{name}.md` | trục 4 |
| `docs/PERSONAS.md §2` (ma trận vai × hành động) | trục 2 |
| skill `stack-spring-boot §review` — **ĐÃ nạp ở Bước 0 (định nghĩa agent), KHÔNG Read lại** | trục 3, 5 |
| `docs/DECISIONS.md` · `docs/adr/ADR-*.md` | trục 7 |
| Wave ≥ 2: `docs/BACKWARD-COMPAT.md` §1 · `archive/wave-*/` | trục 4 |

## 2. Phạm vi

Code ở `services/boundaries/{name}/`.

- **Vòng 1** — chưa có finding cho boundary này ở `STATE.md §Findings` → soi **cả boundary**.
- **Re-review** — đã review vòng trước → soi `git diff --stat <mốc>..HEAD` rồi `git diff <mốc>..HEAD`, và với **mỗi**
  finding của boundary MAIN báo đã sửa: mở đúng `file:dòng`, lỗi hết thật chưa. Mốc không còn trong git → soi cả boundary.

## 3. Chạy máy trước — đỏ là finding luôn

```bash
./gradlew check jacocoTestReport     # check = test + jacocoTestCoverageVerification → coverage < 80% là ĐỎ. Maven chỉ khi ADR chọn: mvn -q verify
# build.gradle thiếu `check.dependsOn jacocoTestCoverageVerification` (ref-backend-config) = BLOCKER: coverage không chặn được gì
# coverage: build/reports/jacoco/test/jacocoTestReport.xml, counter LINE — ngưỡng backend 80%
# mapper: pom/build.gradle có mapstruct mà 0 @Mapper trong source = dep chết + toàn map tay
grep -c mapstruct pom.xml build.gradle 2>/dev/null; grep -rl "@Mapper" src/main/java | wc -l
grep -rnE "\.set[A-Z]\w+\(\w+\.(get|is)[A-Z]" src/main/java --include="*.java" | wc -l   # đếm dòng setX(getX())
grep -rnE 'new \w+(Response|Dto|DTO|Item)\(([^;]*\.(get|is)[A-Z]\w*\(\)){3,}' --include=*.java src/main | grep -v /mapper/   # map tay bằng constructor record
# tìm kiếm/danh sách (Trục 4): lọc trong bộ nhớ · JPQL null-check · GET nhiều tham số lọc
grep -rnE -A3 "findAll\(" --include=*ServiceImpl.java src/main | grep -E "\.filter\(|subList\("
grep -rnE "subList\(|new PageImpl<>\(" --include=*ServiceImpl.java src/main
grep -rnE ":\w+ IS NULL OR" src/main
grep -rn -A12 "@GetMapping" --include=*Controller.java src/main | awk '/@GetMapping/{if(n>=3)print h" ("n" lọc)"; h=$0; n=0} /@RequestParam/ && !/ (page|size|sort)[,)]/{n++} END{if(n>=3)print h" ("n" lọc)"}'
# response/request generic (ref-backend-pattern §6 — Trục 4): khung có chưa · bọc lồng · PageResponse tay · data không kiểu · catch trong controller
for c in ResponseUtil SuccessResponse PageRequestBase SearchSpecification; do grep -rqE "(class|record) $c\b" src/main || echo "THIẾU khung: $c"; done
grep -rnE 'ResponseEntity<\s*(SuccessResponse|ApiResponse|BaseResponse)|ResponseEntity\.(ok|status\([^)]*\)\.body)\(\s*(ResponseUtil|ApiResponse)' --include=*Controller.java src/main
grep -rnE 'new PageResponse<' --include=*.java src/main | grep -v '/common/'
grep -rnE '(SuccessResponse|ApiResponse)<\s*(Map<|Object>|\?>|List<Map<)' --include=*Controller.java src/main
grep -rn 'catch (' --include=*Controller.java src/main
# hằng số (Trục 5): field String cho tập đóng · so literal · tên hằng trùng ≥ 2 class
grep -rnE "private String (role|status|type|\w+Status|\w+Type|\w+Role);" --include=*.java src/main
grep -rnE -e '"[A-Z_]{2,}"\.equals\(' -e 'case "[A-Z_]' --include=*.java src/main
grep -rhoE 'static final\s+\S+\s+\w+\s*=' --include=*.java src/main | sed -E 's/\s*=$//' | awk '{print $NF}' | sort | uniq -d
# bỏ qua test (luật #6) — ra dòng = BLOCKER
grep -nE '\|\| *true|-x +test|skipTests|ignoreFailures' Makefile build.gradle* 2>/dev/null

# ── quy ước Java (stack-spring-boot §3) ──
# FQCN inline (MINOR)
grep -rnE '(^|[^[:alnum:]_."/])(java|javax|jakarta|org|com)\.[a-z0-9_]+(\.[a-z0-9_]+)*\.[A-Z]' --include=*.java src/main | grep -vE ':[0-9]+:\s*(import|package|//|\*|/\*)'
# import wildcard (MINOR)
grep -rnE '^import (static )?[[:alnum:]_.]+\.\*;' --include=*.java src
# var (MINOR)
grep -rnE '(^|[;({ ])\s*(final )?var [a-z]\w* *[=:]' --include=*.java src/main
# @Autowired field · LoggerFactory · sysout · printStackTrace · LocalDateTime · @Value (MINOR)
grep -rnE '@Autowired|LoggerFactory\.getLogger|System\.(out|err)\.print|printStackTrace\(' --include=*.java src/main
grep -rnE '\bLocalDateTime\b|@(org\.springframework\.beans\.factory\.annotation\.)?Value\(' --include=*.java src/main | grep -v ':import '
# constructor viết tay trong bean — dùng @RequiredArgsConstructor (MINOR)
for f in $(grep -rlE '@(Service|Component|RestController|Configuration)' --include=*.java src/main); do c=$(basename $f .java); grep -nE "^\s*(public |protected )?$c\([^)]" $f | sed "s|^|$f:|"; done
# @Transactional ngoài service/ — job/scheduler bọc cả lô trong 1 transaction (MAJOR)
grep -rnE '@Transactional\b' --include=*.java src/main | grep -v '/service/'
# entity / Map ở biên controller (MAJOR)
grep -rnE '\b[A-Z]\w*Entity\b' --include=*Controller.java src/main | grep -vE 'ResponseEntity|HttpEntity|RequestEntity'
grep -rnE '@RequestBody\s+(java\.util\.)?Map<' --include=*Controller.java src/main
# exception chung — GlobalExceptionHandler không map thì thành 500 (MAJOR)
grep -rnE 'throw new (RuntimeException|IllegalArgumentException|IllegalStateException|Exception)\(' --include=*.java src/main
# FK trong migration (MAJOR)
grep -rniE 'foreign key|references ' src/main/resources/db
# tên header truy vết lệch / literal rải rác — phải X-Request-ID qua constant/HeaderConstants, lệch = truy vết đứt giữa service (MAJOR)
grep -rniE '"X-(Correlation|Request|Trace)-I[Dd]"' --include=*.java src/main | grep -v '/constant/'
# MDC: số chỗ đặt + job/listener không đặt MDC — log không truy vết được (MAJOR)
grep -rn 'MDC\.put' --include=*.java src/main | wc -l
for f in $(grep -rlE '@Scheduled|@Async|@KafkaListener|@TransactionalEventListener' --include=*.java src/main); do grep -q MDC $f || echo "noMDC: $f"; done

# ── bảo mật (docs/SECURITY.md) ──
# JwtDecoder tự dựng không kiểm iss/aud (BLOCKER)
grep -rlE "withJwkSetUri|withSecretKey|withPublicKey|withIssuerLocation" src/main | xargs -r grep -LE "setJwtValidator|createDefaultWithIssuer|JwtIssuerValidator|JwtAudienceValidator"
# định danh người dùng theo claim đổi được — phải theo sub/oid (BLOCKER)
grep -rnE 'getClaim(AsString)?\("(email|preferred_username|upn|name)"\)' --include=*.java src/main
# secret có giá trị mặc định ngoài local/test (BLOCKER)
grep -rnE '\$\{[A-Z_]*(SECRET|PASSWORD|KEY|TOKEN)[A-Z_]*:[^}]{4,}\}' src/main/resources | grep -vE 'application-(local|test)\.ya?ml'
# profile mặc định fail-open + controller chỉ-dev (BLOCKER khi có controller dev)
grep -rnE 'active: *\$\{[A-Z_]+:(local|dev|test)\}' src/main/resources
grep -rlE '@Profile\("(local|dev|test)"\)' --include=*Controller.java src/main
# api-docs/swagger ở prod (MAJOR)
grep -A2 -E '^\s*api-docs:' src/main/resources/application-prod.yml 2>/dev/null | grep -q 'enabled: false' || echo "api-docs CHƯA tắt ở prod"
grep -rn '"/v3/api-docs' --include=*.java src/main
# khoá / đổi quyền / đặt mật khẩu → mở xem token cũ có bị thu hồi (MAJOR)
grep -rnE 'set(Active|Enabled|Locked|Role|PasswordHash|Password)\(' --include=*ServiceImpl.java src/main
# IP client sau reverse proxy — rate limit chung 1 bucket hoặc bị giả IP (MAJOR)
grep -rnE 'getRemoteAddr\(\)|X-Forwarded-For' --include=*.java src/main; grep -rn 'forward-headers-strategy' src/main/resources
# upload chỉ tin Content-Type client gửi (MAJOR)
grep -rnE 'getContentType\(\)' --include=*.java src/main | grep -iE 'contains|equals|startsWith|matches'
# body Map tự do — mass assignment (MAJOR)
grep -rnE 'readValue\([^,]+, *Map\.class\)|@RequestBody +Map<' --include=*.java src/main
# log PII/token (token/password = BLOCKER · PII = MAJOR)
grep -rnE 'log\.(info|warn|error|debug|trace)\(.*\b\w*([eE]mail|[pP]hone|nationalId|taxCode|password|token|[aA]uthorization)\w*\b *[,)]' --include=*.java src/main
# page size không trần (MINOR)
grep -rnE 'PageRequest\.of\(\s*page\s*,\s*size' --include=*.java src/main
# mã hoá at-rest: 0 trong khi PRD/arch yêu cầu mã hoá = MAJOR
grep -rnE 'AttributeConverter|@Convert\(|Cipher\.getInstance' --include=*.java src/main | wc -l
# SCA — CVE high = MAJOR; không chạy được (mạng / thiếu plugin) → QUESTION, không im lặng bỏ qua
./gradlew dependencyCheckAnalyze || echo "SCA KHÔNG chạy được → QUESTION"
```
**Khối quy ước Java + hằng số**: mỗi luật ra dòng = **1 finding GỘP** kèm **số đếm + 2–3 ví dụ `file:dòng`** — vi phạm hàng loạt không được bỏ vì "MINOR". **Khối bảo mật**: dòng nào ra kết quả → mở file xác nhận, severity theo comment; không ra dòng ≠ an toàn, Trục 2 vẫn phải đọc.
Build/test đỏ → BLOCKER `type=test`, dẫn tên test + dòng lỗi. Coverage < 80% → BLOCKER.
Lệnh tìm kiếm/danh sách ra dòng → mở từng chỗ, phán theo dòng "API tìm kiếm/danh sách" ở Trục 4 (lọc trong bộ nhớ trên bảng nghiệp vụ = BLOCKER).
Có mapstruct trong build mà **0 `@Mapper`** = finding MINOR ngay (dep chết + convention vỡ); dòng `setX(getX())` nhiều bất thường (>10) → mở từng cụm phân loại 1-1 thuần vs có-lý-do (chi tiết trục 5 dòng MapStruct) — **số đếm ở đây là bằng chứng phải ghi vào báo cáo**, không được bỏ qua vì "MINOR".

## 4. Soi theo trục

`grep` chỉ để **tìm chỗ phải đọc** — mọi dòng dưới đây kết thúc bằng mở file ra đọc. Viết tắt:
`J` = `--include=*.java src/main`.

### Trục 1 — Đúng AC và BR

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Mọi AC có code, gồm nhánh không-happy | Liệt kê AC trong FEAT → `grep -rn "AC-" J` (rules bắt comment `FEAT-N AC-M`); không có comment thì lần từ endpoint trong `arch/{name}.md §3 API` xuống service | không thấy = BLOCKER · làm nửa = MAJOR |
| Mọi BR enforce ở service/domain, chạy **trước** khi ghi | `grep -rn "BR-" J` → mở chỗ check | BLOCKER |
| Ca xấu: không tồn tại · inactive · status đã final · request lặp · không sở hữu · tenant khác | Mở từng method service có ghi dữ liệu | MAJOR |
| Chuyển trạng thái hợp lệ; default đúng; không side effect ngoài ý | `grep -rn "setStatus(" J` → trước đó có kiểm trạng thái nguồn không | MAJOR |
| Ca biên `arch/{name}.md §6` (gửi hai lần · sửa đồng thời · xoá · sai thứ tự · hỏng nửa chừng · bản cũ · rỗng · thu hồi quyền) | Mỗi dòng không `n/a` → ràng buộc DB (`grep -rniE "unique" src/main/resources/db`), `@Version`, hoặc check ở service. Không tìm thấy = chưa xử | BLOCKER |

### Trục 2 — Bảo mật (6 nhóm)

| Nhóm | Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|---|
| Secret | Không secret trong code / yml / test | Lệnh (a) dưới bảng | BLOCKER — `suggested fix` ghi **xoay key**, không chỉ xoá commit |
| | Không log password/token/OTP/Authorization/PII/full body | `grep -rni -e "log\..*password" -e "log\..*token" -e "log\..*otp" -e "log\..*authorization" J` | token/password = BLOCKER · PII = MAJOR |
| Đầu vào | DTO có Bean Validation, controller có `@Valid` | `grep -rn "@RequestBody" J` → dòng nào thiếu `@Valid` | MAJOR |
| | Injection: không nối input vào JPQL/native; cột sort whitelist | `grep -rn -e createQuery -e createNativeQuery -e "nativeQuery = true" -e "Sort.by(" J` → tìm `+` ghép chuỗi, tên cột lấy từ request | BLOCKER |
| | Mass assignment: không bind body vào `@Entity`; mapper request→entity không map `id`/`role`/`tenantId`/`status`/`price` | `grep -rnE "@RequestBody +\w+Entity" J` + đọc `*Mapper` | BLOCKER |
| | Upload: giới hạn size, kiểm loại thật, tên do server sinh, lưu ngoài web root | `grep -rn "MultipartFile" J` · `grep -rn "max-file-size" src/main/resources` | MAJOR · path theo tên client = BLOCKER |
| | Deserialization, XXE, SSRF | `grep -rn -e ObjectInputStream -e activateDefaultTyping -e DocumentBuilderFactory -e SAXParserFactory -e XMLInputFactory -e "URI.create(" -e "new URL(" J` → parser tắt external entity? URL dựng từ input có allowlist? | BLOCKER |
| Danh tính & phân quyền | Không endpoint public ngoài ý | `grep -rn "permitAll" J` → mỗi path phải public theo `arch/{name}.md §3 API` | BLOCKER |
| | Identity từ security context, không từ client | `grep -rn -e userId -e tenantId -e ownerId --include=*Request.java src/main` · `grep -rn -e "@RequestParam.*Id" -e "@PathVariable.*tenantId" -e "@RequestHeader.*tenantId" J` | BLOCKER |
| | Lấy bản ghi theo id kèm chủ sở hữu/tenant | `grep -rn -e "findById(" -e "getById(" -e "getReferenceById(" -e "findOne(" J` → trước khi trả/ghi có so owner/tenant với security context? | BLOCKER |
| | Mỗi ô `cấm` của ma trận vai × hành động có chỗ chặn **ở server** | Từng ô `cấm` liên quan boundary → tìm `@PreAuthorize`/check role ở endpoint hoặc service. Ẩn nút ở FE KHÔNG tính | BLOCKER |
| | Admin/internal endpoint: role rõ; internal dùng cơ chế đã duyệt (mTLS/internal JWT/gateway); token hết hạn, đăng xuất được | `SecurityConfig` + ADR auth | MAJOR |
| | Password BCrypt/Argon2; token/nonce `SecureRandom`; không tự chế crypto | `grep -rn -e MessageDigest -e MD5 -e SHA1 -e "SHA-1" -e "new Random(" J` | BLOCKER |
| Đường ra | Không lộ stack trace/SQL/message nội bộ | `grep -rn -e include-stacktrace -e include-message src/main/resources` · `grep -rn "getMessage()" --include=*Handler*.java src/main` | MAJOR |
| | CORS không `*` khi có credential; CSRF bật nếu cookie session; security headers | `grep -rn -e allowedOrigins -e allowedOriginPatterns -e "@CrossOrigin" -e csrf J` | BLOCKER |
| | Actuator/endpoint nhạy cảm không public | `grep -rn -A3 "exposure" src/main/resources` → `include: "*"` không auth = finding | MAJOR |
| | Rate limit: đăng nhập · đăng ký · quên mật khẩu · gửi OTP/email/SMS | `grep -rni -e login -e signin -e register -e signup -e otp -e forgot --include=*Controller.java src/main` → có rate limiter (theo ADR)? ADR không nói → QUESTION kèm cách kiểm | MAJOR |
| Dữ liệu | Response không thừa field nhạy cảm (hash, cờ nội bộ, dữ liệu người khác) | Mở từng `*Response` so với `arch/{name}.md §3 API` | MAJOR |
| | Chỉ thu dữ liệu AC cần; PII mã hoá at-rest khi arch/PRD NFR yêu cầu; chỉ qua TLS | Cột trong migration so với AC — cột cá nhân không AC nào dùng = finding | MINOR · thiếu mã hoá khi yêu cầu = MAJOR |
| Phụ thuộc | Không lib có CVE nghiêm trọng; không thêm lib vì một hàm | Có plugin thì `./gradlew dependencyCheckAnalyze`; không có → đọc dependency mới trong `git diff <mốc>..HEAD -- build.gradle*` | MAJOR |

```bash
# (a) secret viết trần — giá trị mặc định dạng ${VAR:default} do lệnh secret ở §3 Chạy máy bắt
grep -rnE "(password|secret|api[_-]?key|token)\s*[:=]\s*[\"']?[A-Za-z0-9_/+=-]{8,}" src \
  --include=*.java --include=*.yml --include=*.yaml --include=*.properties | grep -v '\${'
```

### Trục 3 — Forbidden patterns

Mở `stack-spring-boot §review` §Forbidden patterns, đi **TỪNG dòng** bảng. Mỗi dòng tìm được trong code → một
finding: `description` mở bằng `[stack-spring-boot Forbidden: <cột Cấm>]`, `hậu quả thật` lấy từ cột
`Vì sao` (viết cụ thể cho chỗ này), `suggested fix` từ cột `Thay bằng`. Lệnh tìm cho các dòng chưa có ở trục 2:

```bash
grep -rnE "ddl-auto: *(update|create)" src/main/resources          # ddl-auto
git log --diff-filter=M --name-only --format= -- src/main/resources/db  # migration bị sửa: file có từ wave trước = BLOCKER
grep -rln "@Transactional" --include=*Controller.java src/main       # transaction ở controller
grep -rn "Repository" --include=*Controller.java src/main            # controller gọi repository
grep -rnE "catch *\([^)]*\) *\{ *\}" --include=*.java src/main       # catch rỗng
grep -rn -A4 "catch *(" --include=*Controller.java src/main | grep -E "ok\(|HttpStatus\.OK"   # catch rồi trả 200
grep -rn ").get()" --include=*.java src/main                         # Optional.get() trần
grep -rn -e "FetchType.LAZY" -e "@OneToMany" -e "@ManyToOne" --include=*.java src/main   # lazy: mapper có đọc sau khi service trả về?
grep -rn "findAll()" --include=*.java src/main                       # list không phân trang
grep -rln "@Data" --include=*Entity.java src/main                    # @Data trên entity
grep -rn -e "new RestTemplate" -e "WebClient.create" --include=*.java src/main
grep -rni -e h2database -e "jdbc:h2" build.gradle* src               # H2
```

### Trục 4 — Giao dịch, hợp đồng, idempotency, persistence, tích hợp

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| `@Transactional` ở service, phạm vi hẹp; chỉ đọc thì `readOnly = true` | `grep -rn "@Transactional" J` | MAJOR |
| Không gọi HTTP/downstream chậm trong transaction | Mở từng method `@Transactional`, tìm `*Client.` / `restClient` / `.send(` | MAJOR |
| Event/cache/index phụ thuộc DB đi **sau commit** hoặc qua outbox | `grep -rn -e "kafkaTemplate.send" -e "publishEvent(" -e "opsForValue()" J` → nằm trong transaction mà không `AFTER_COMMIT`/outbox | BLOCKER |
| Ghi nhiều bảng cần atomic nằm cùng transaction | Đọc service ghi ≥ 2 bảng | BLOCKER |
| Khớp `arch/{name}.md §3 API`: path · method · field · enum · error code · HTTP status · pagination · sort/filter | So từng `@*Mapping` với spec | breaking không có yêu cầu = BLOCKER |
| Wave ≥ 2: surface trong `docs/BACKWARD-COMPAT.md` §1 chỉ được THÊM, không đổi/xoá | `git diff <mốc wave trước>..HEAD` trên controller · DTO · migration · topic | BLOCKER |
| Request/Response là DTO, không Entity; list có phân trang; GET không đổi state | `grep -rn "Entity" --include=*Controller.java src/main` · đọc `@GetMapping` | BLOCKER · phân trang = MAJOR |
| Webhook · callback · consumer · job · retry · import · sync idempotent — dedup theo eventId/transactionId/idempotency key | `grep -rn -e "@KafkaListener" -e "@RabbitListener" -e "@Scheduled" -e webhook -e callback J` → mỗi chỗ tìm bảng inbox/unique key | luồng tiền/critical = BLOCKER · còn lại MAJOR |
| Event: payload DTO (không `Map`/entity) · topic/retry từ config · có eventId + header `X-Request-ID` (truy vết) · retry + DLQ · không giả định thứ tự · envelope khớp `arch/{name}.md` §events (`ref-backend-kafka`) | Đọc producer/consumer | MAJOR |
| Không N+1 / repository trong vòng lặp / query không giới hạn; projection khi đủ, không eager thừa | `grep -rn -A4 -e "for (" -e ".forEach(" --include=*ServiceImpl.java src/main` → có gọi repository bên trong | MAJOR · không giới hạn trên bảng lớn = BLOCKER |
| Response/request generic theo `ref-backend-pattern §6`: **(a)** thiếu khung ở `common/` (`ResponseUtil`, `SuccessResponse`, `PageRequestBase`, `SearchSpecification`) hoặc tự chế wrapper khác · **(b)** bọc lồng `ResponseEntity<SuccessResponse<..>>` / `ResponseEntity.ok(ResponseUtil.ok(..))` ngoài 3 ca được phép (tải file · 201 kèm `Location` · header đặc biệt) · **(c)** `new PageResponse<>(..)` dựng tay · **(d)** `data` là `Map`/`Object`/`?` · **(e)** try/catch trong controller tự dựng lỗi · **(f)** lỗi trả HTTP status cứng 400 thay vì `ErrorCode.httpStatus()` | Khối "response/request generic" ở §3 Chạy máy → mở từng chỗ; (f) đọc `GlobalExceptionHandler` | (a) MAJOR — ghi 1 finding cho cả boundary · (b)(c)(d)(e)(f) MAJOR, gộp 1 finding/ý kèm số đếm |
| API tìm kiếm/danh sách theo `stack-spring-boot §3 Tìm kiếm`: **(a)** lọc/phân trang trong bộ nhớ (`findAll()` → `.stream().filter`, `subList`, `new PageImpl<>(list)`) thay vì `SearchSpecification.of(req)` (+ `{Resource}Specifications` cho điều kiện đặc thù) + `findAll(spec, req.toPageable(SORTABLE))` · **(b)** lọc động bằng JPQL `(:x IS NULL OR …)` / derived query tổ hợp / if-else theo tổ hợp tiêu chí · **(c)** `@GetMapping` có ≥ 3 `@RequestParam` lọc (không tính page/size/sort) mà không phải `POST …/search`. Tha: `findAll()` bảng danh mục nhỏ (phòng ban, loại phép) để map tên. **Chạy đủ 3 lệnh** — chỉ grep (b) là sót (a) | Khối "tìm kiếm/danh sách" ở §3 Chạy máy (4 lệnh) → mở từng chỗ | (a) trên bảng nghiệp vụ = BLOCKER · (b) MAJOR · (c) MAJOR — arch §3 đã chốt GET thì code đúng contract, finding vào `ROADMAP §backlog` sửa arch wave sau; endpoint đã giao (BC §1) → THÊM `POST …/search`, giữ GET cũ |
| Index cho cột filter/sort/join (không FK nên không tự có index) | So `findBy*`/`WHERE` với `CREATE INDEX` trong migration | MAJOR |
| Migration: file mới, NOT NULL mới có default/rollout an toàn, không FK | `grep -rni -e "foreign key" -e "references " src/main/resources/db` | MAJOR |
| Entity ↔ migration khớp tên/kiểu/nullable (`varchar(n)`↔`CHAR(n)`, `TIMESTAMPTZ`↔`Instant`) | Đọc song song entity và migration | BLOCKER |
| Không hardcode URL/timeout/retry/batch/topic/role/header; đúng chỗ: constant theo domain · yml · secret store · enum · i18n | `grep -rn -e "\"http://" -e "\"https://" -e "Duration.of" J` | MAJOR |
| Downstream: `@HttpExchange` · timeout + retry/fallback · 4xx→`BusinessException`, 5xx/timeout→`EXTERNAL_SERVICE_ERROR` · không return null · truyền Authorization/X-Tenant-ID/X-Request-ID · base URL/credential/flag cấu hình được (`ref-backend-restclient`) | Đọc `*Client` | MAJOR |
| Cache (`ref-backend-redis`): qua service interface, key có convention + TTL, invalidate sau ghi, không cache dữ liệu nhạy cảm, lock có timeout + release | `grep -rn -e RedisTemplate -e "@Cacheable" -e "@CacheEvict" -e RLock J` | MAJOR |
| Job: idempotent, lock khi nhiều instance, batching/phân trang, log tổng kết (start/end/duration/processed/success/failure), cấu hình ra ngoài | `grep -rn "@Scheduled" J` → có `@SchedulerLock`? | MAJOR |

### Trục 5 — Kiến trúc và quy ước

ArchUnit gác layer/package/cycle (`gradle test` chạy nó). Bạn soi thứ nó không bắt được.

> **BƯỚC 5.0 — SOI HÌNH DẠNG CÂY, LÀM TRƯỚC khi đọc code (đọc nội dung code KHÔNG thay được bước này).**
> Đọc file trong package chỉ cho biết code viết gì, KHÔNG cho biết cấu trúc **tổ chức đúng pattern** hay không — phải lùi lại nhìn cây:
> 1. **Pattern đã chốt là gì?** Đọc `docs/arch/{name}.md §4` + `docs/adr/*` → **Layered** hay **Hexagonal**?
> 2. **Dump cây THẬT:** `find src/main/java -type d` (hoặc `tree src/main/java`).
> 3. **Phân loại hình dạng cây:** nó ra **Layered** (`controller/ · service/ + impl/ · repository/ · entities/ · dto/ · mapper/`) · **Hexagonal** (`domain/ · application/ · adapter/in · adapter/out/...`) · hay **phẳng/tự chế** (mọi class 1 package · tên package tự đặt · không thấy tầng)?
> 4. **Cây THẬT phải KHỚP pattern ĐÃ CHỐT.** Chốt Layered mà cây không ra tầng · trộn 2 kiểu · phẳng · package tự đặt = **BLOCKER**. Hình dạng chuẩn từng pattern: `ref-backend-pattern §2/§3`.
>
> Chưa làm 5.0 mà đã kết luận "cấu trúc ổn" = review CHƯA soi cấu trúc, chỉ mới đọc code.

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| `ArchitectureTest.java` tồn tại, rule khớp layout arch §4 | `find src/test -name ArchitectureTest.java` → đọc rule | thiếu/rỗng = BLOCKER |
| **(5.0)** Cây THẬT khớp pattern đã chốt (Layered/Hexagonal, không trộn, không phẳng, không package tự đặt) | `find src/main/java -type d` → **phân loại hình dạng** vs `arch §4`/ADR + `ref-backend-pattern §2/§3` | BLOCKER |
| Class đúng package; `@Entity` ở `entities/` (Hexagonal: `adapter/out/persistence/entities/`), tên `{Resource}Entity` | `grep -rl "@Entity" J` | MAJOR |
| Không package rỗng, không scaffold mẫu | `find src/main -type d -empty` · `find src -name "Example*" -o -name "Demo*" -o -name "Sample*" -o -name "HelloController*"` | thừa = MAJOR · mẫu lẫn code thật = BLOCKER |
| Đúng tầng: controller map + validate + gọi service interface · nghiệp vụ + transaction ở service · query ở repository · convert ở mapper · không nghiệp vụ trong controller/repository/mapper/config/migration | Đọc controller + mapper | MAJOR |
| Bean Validation cho input; nghiệp vụ + chuyển trạng thái validate ở service | Đọc DTO + service | MAJOR |
| Lỗi không lọt 500: exception map qua `GlobalExceptionHandler` → error code typed; input null/rỗng → 400 typed; catch phải log + ném lại/map | Lệnh trục 3 (catch, `.get()`) | BLOCKER |
| `stack-spring-boot §review` §Coding checklist — đi từng dòng: interface/impl, inject interface · `@RequiredArgsConstructor` + `private final` · MapStruct · `Instant` đúng tầng · id/tenant boxed · Specification thay JPQL `(:x IS NULL OR …)`, `nativeQuery` phải kèm comment `// native: <lý do>` (thiếu = MAJOR) · error code từ enum · `@ConfigurationProperties` · không FQCN/wildcard import · theo convention sẵn có, không tự thêm pattern | `grep -rn -e "@Autowired" -e "LoggerFactory.getLogger" -e "ServiceImpl " J` | MAJOR · FQCN = MINOR |
| Hằng số đặt đúng chỗ theo bảng 4 loại ở `stack-spring-boot §3 Hằng số`: **(a)** tập giá trị đóng (role/status/type) khai `String` ở entity/principal/DTO, hoặc so literal thay enum — kể cả khi enum đã có mà không dùng (ghi finding ở **field gốc**, không liệt kê từng chỗ so) · **(b)** cùng một hằng số khai ở ≥ 2 class thay vì `constant/{Domain}Constants` · **(c)** tham số nghiệp vụ (số ngày, trần, giờ ca, ngưỡng, TTL) ghi cứng trong class thay vì yml. Hằng số nội bộ chỉ 1 class dùng (`Pattern`, magic byte, header cột export) = **đúng, KHÔNG ghi finding** | Khối "hằng số" ở §3 Chạy máy → mở từng tên trùng xem có cùng ý nghĩa · (c) đọc `static final` số/thời gian trong `service/`·`scheduler/`·`security/`, đối chiếu `DECISIONS` | (a) (b) MAJOR · (c) MINOR, là con số DECISIONS chốt = MAJOR |
| **MapStruct là DEFAULT** (convention stack) — map tay CHỈ khi MapStruct **không biểu diễn nổi** (logic biến đổi/điều kiện/tính chéo field) + nêu lý do. Căn cứ = **bản chất, không đếm field**: map tay 1-1 thuần = finding→MapStruct; map tay có lý do = tha | Hai số đếm map tay ở §3 Chạy máy (`setX(getX())` + constructor record) → mở hàm xem là **gán 1-1 thuần** (→ finding) hay **có logic/điều kiện** MapStruct khó (→ tha) | MINOR (nêu "map tay 1-1 thuần, MapStruct làm được") |
| Logging (`ref-backend-logging`): `@Slf4j`, JSON structured, MDC traceId/tenantId, mask PII, level đúng, log lỗi đủ ngữ cảnh, async/job có correlation | `grep -rn "MDC" J` | MAJOR |
| Config (`ref-backend-config`): `application.yml` + `application-{dev,sit,prod}.yml`; Dockerfile multi-stage `bootJar` | `ls src/main/resources/application*.yml Dockerfile` | MAJOR |
| Dễ bảo trì: method gọn, không lồng sâu, không nhân đôi logic nghiệp vụ, không dependency vô cớ | Ghi khi nêu được **chi phí bảo trì cụ thể** (người mới vấp thế nào) | MINOR |

### Trục 6 — Test

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Ca đủ: success · validation fail · not found · permission denied · tenant khác · chuyển trạng thái sai · trùng/idempotency · external fail · publish event · rollback · biên | Đối chiếu `src/test` với AC + `arch/{name}.md §6` | MAJOR |
| Unit: given-when-then, tên test mô tả hành vi (đọc tên biết ca gì — không `test1`/`testCreate`), assert hành vi + error code (không assert chi tiết cài đặt), mock đúng ranh giới (không mock class đang test), deterministic (Clock/seed), branch coverage có nghĩa | Đọc 2–3 test đại diện | MAJOR |
| Integration trên Testcontainers Postgres (không H2); contract API status + envelope; tenant isolation | `grep -rl -e PostgreSQLContainer -e "@Testcontainers" src/test` | MAJOR |
| **Schema drift**: ≥ 1 test boot Spring context + chạy migration + `ddl-auto: validate` | `grep -rn "ddl-auto" src/test/resources src/main/resources` + test `@SpringBootTest` dùng container | BLOCKER |
| Đổi logic có test mới; không xoá test có nghĩa; không test rỗng / chỉ `assertDoesNotThrow`; không `@Disabled` thiếu lý do | `grep -rn -e assertDoesNotThrow -e "@Disabled" src/test` · `git diff --stat <mốc>..HEAD -- src/test` | MAJOR |

### Trục 7 — Lệch thứ đã chốt

| Kiểm gì | Tìm ở đâu | Nặng |
|---|---|---|
| Code làm khác một dòng `docs/DECISIONS.md` mà không có dòng mới đè lên | Mỗi dòng liên quan boundary → tìm chỗ code tương ứng | MAJOR |
| **`amend-arch`** (PROTOCOL §3): mỗi thay đổi `docs/arch/*.md` sau khoá scope có dòng `DECISIONS` loại `amend-arch` · truy về AC/Mã màn đã khoá · chỉ THÊM (không đổi nghĩa/xoá) · target consumer cập nhật cùng commit · không kèm sửa FEAT/mockup/PRD | `git log --oneline <mốc>..HEAD -- docs/` (`<mốc>` = commit đầu wave) → `git show` từng commit, đối chiếu `DECISIONS` | thiếu điều kiện = MAJOR · đổi/xoá surface đã giao = BLOCKER |
| Thư viện/kiểu kiến trúc khác ADR | Dependencies trong `build.gradle*` so với ADR tech-stack | MAJOR |
| **Build tool khác ADR** (chốt Gradle → phải `build.gradle`+`gradlew`, KHÔNG `pom.xml`; chốt Maven → ngược lại) | `ls build.gradle* gradlew pom.xml` so với ADR/TECHSTACK — sai công cụ = **MAJOR** (cả CI/Dockerfile/lệnh sai theo) | MAJOR |
| Framework/version khác `TECHSTACK.md` khai (soi tới đúng mức khai — vd khai `3.4` thì code phải `3.4.x`) | `build.gradle*`/`pom.xml` version vs `docs/TECHSTACK.md §1` | MAJOR |
| **Lệch System design đã khai** (`docs/arch/OVERVIEW.md §5`): 5.8 ≥ 2 instance mà `@Scheduled` không lock · 5.8 sau proxy mà rate limit/audit dùng `getRemoteAddr()` không `forward-headers-strategy` · 5.4 bảng lớn mà list nạp cả bảng / không trần size · 5.7 dữ liệu nhạy cảm mà cột không mã hoá / log không che · 5.4 cache khai TTL mà code không có | Đọc §5 → đối chiếu kết quả các khối Chạy máy (job lock · IP · tìm kiếm · bảo mật) — có §5 làm căn cứ thì không ghi QUESTION | bảo mật/dữ liệu = BLOCKER · còn lại MAJOR |
| Thuật ngữ lệch: FEAT/Glossary gọi "lịch hẹn" mà code chỗ `booking` chỗ `schedule` | `grep` tên class/bảng | MINOR |
| TODO/FIXME chặn một AC; code chết để dạng comment | `grep -rn -e TODO -e FIXME -e HACK J` | chặn AC = MAJOR |

## 5. Report finding

Trả finding về cho phiên chính — MAIN ghi vào `STATE.md §Findings`. Mỗi finding một dòng:

```
[severity] file:dòng — [nguồn] hỏng thế nào → đề xuất
```

- `[nguồn]`: `[FEAT-X AC-2]` · `[BR-...]` · `[Bảo mật: <nhóm>]` · `[stack-spring-boot Forbidden: <cột Cấm>]` · `[arch/{name}.md §6 <ca>]` · `[DECISIONS <ngày>]`.
- **BLOCKER (nặng)** — sai nghiệp vụ · lủng bảo mật/tenant · hỏng dữ liệu/transaction · phá hợp đồng không có yêu
  cầu · thiếu idempotency ở luồng tiền · secret · sửa migration đã chạy · query không giới hạn.
  **MAJOR (vừa)** — nên sửa trước bàn giao. **MINOR/NIT (nhẹ)** — không chặn. **QUESTION** — chưa chắc.
  Ý thích cá nhân không bao giờ là BLOCKER.
- Re-review: mở đúng `file:dòng` MAIN báo đã sửa, xác nhận; còn lỗi → báo lại vì sao chưa hết.
- Ít thời gian thì theo thứ tự: AC/BR → bảo mật & tenant → giao dịch/dữ liệu → hợp đồng → idempotency →
  hiệu năng query → config/secret → test → dễ đọc.

## 6. Bốn luật cho mọi finding

1. **Hậu quả thật (trục A) HOẶC chi phí bảo trì cụ thể (trục B)** — trục A: mất/lộ dữ liệu · sai kết quả · AC
   không chạy · wave trước gãy. Trục B: người mới đọc/sửa vấp thế nào (vd "20 field map tay, thêm field dễ sót").
   Viết không nổi **một trong hai** thì không phải finding.
2. **Trục sạch thì nói sạch** — ghi thẳng "trục N sạch" trong phần trả về; đừng bịa nhận xét cho có.
3. **Mở file ra đọc** — `file:dòng` phải là dòng đã đọc thật; không suy từ tên hàm.
4. **Không chắc → `QUESTION`**, cột `suggested fix` ghi **cách kiểm chứng** (vd "gọi API bằng token A với
   id bản ghi của B, xem có trả 200 không").

Góp ý **bảo trì/nhất quán được** (trục B) — khi nêu **chi phí cụ thể** hoặc **trích chuẩn** (cây thư mục · `CONVENTIONS` · Glossary). **Vẫn cấm khẩu vị thuần**: thích tên khác không lý do · trừu tượng "để sau dễ mở rộng" · tối ưu chưa đo · coverage%. Style tùy-ca (map 2–3 field tay) → **mặc định tha** (`var` KHÔNG thuộc diện này — `stack-spring-boot §3` cấm, khối quy ước Java ở §3 Chạy máy), chỉ nêu khi che mất ý.

## 7. Kết luận

- Sạch chỉ khi: không còn finding BLOCKER/MAJOR của boundary · build/test xanh · coverage ≥ 80%.
- Không spawn fix, không tự loop — phiên chính đọc findings, tự sửa, rồi gọi bạn re-review.
