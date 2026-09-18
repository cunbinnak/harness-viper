# CONVENTIONS — {{PROJECT_NAME}}

> Quy ước CHUNG **cross-stack** (backend · web · bff · mobile) — tổng hợp từ rules-backend/web/bff/mobile.
> Idiom stack cụ thể (Lombok/JPA/MapStruct · React Query/Zod…) ở `.claude/skills/stack-<tên> §review`.
> Bảo mật baseline ở `SECURITY.md`. **§3 error-envelope/header là DEFAULT** — project khác thì sửa file này + ghi `DECISIONS.md`.

## §1 Phân tầng & tách bạch
- Luồng đi qua tầng rõ: giao diện/controller → **nghiệp vụ/service** → dữ liệu. Business logic ở tầng nghiệp vụ, KHÔNG ở controller / component / mapper / entity.
- **KHÔNG business logic ở FE** (tính giá/điểm/điều kiện → backend; hai nơi tính là lệch). Role-gate FE chỉ để UX, backend enforce.
- Data access gom một chỗ: BE qua repository (**chỉ một tầng** chạm DB) · FE qua tầng `api/` (không `fetch`/`axios` rải rác trong component).
- Ranh giới module theo `arch/<target>.md §4`. Logic sai tầng là lỗi, không phải phong cách.

## §2 Đặt tên & hằng số
- Theo ngôn ngữ nghiệp vụ, đúng thuật ngữ PRD (PRD gọi "lịch hẹn" → `appointment`, không chỗ `booking` chỗ `schedule`).
- KHÔNG magic string/number: route · key · role · status · error-code · topic → **constants/enum**, không rải rác.
- Tiếng Anh cho identifier · tiếng Việt cho hiển thị + comment.

## §3 Contract & API (BE↔FE)
- **KHÔNG invent** field / endpoint / op / error-code ngoài `arch §3 API` — thiếu contract → **blocker**, không tự đoán.
- Type/DTO bám spec. BE: **DTO ở biên, KHÔNG phơi entity nội bộ**. FE: type từ spec/codegen, không định nghĩa tay.
- Pagination/filter/sort theo contract **server** (không tự filter client nếu server đã định nghĩa).
- Đổi surface đã giao = **additive** (`BACKWARD-COMPAT.md`).
- **Error envelope** (default): `{ "error": { "code", "message", "details" } }` · **status** 2xx/4xx/5xx · **header** `X-Tenant-ID`/`X-Correlation-ID` · **versioning** `/v1`.

## §4 Xử lý lỗi
- KHÔNG nuốt lỗi (`catch` rỗng, catch rồi trả 200). Lỗi người dùng: tiếng Việt, nói **làm gì tiếp**, KHÔNG stack trace / lỗi thô. Lỗi hệ thống: log đủ ngữ cảnh (ai · làm gì · dữ liệu nào).
- Map lỗi **TẬP TRUNG** (BE: global handler · FE: error-code → message theo `ux`). FE: lỗi field hiện **gần field**, toast không thay field error.

## §5 Trạng thái & hành động
- Mọi màn fetch data xử đủ **loading · empty · error · success**. KHÔNG action "im lặng" (click phải có phản hồi: spinner/toast/inline/navigation).
- **Idempotency**: consumer / webhook / callback / job (BE) dedup theo id · FE **chống double-submit** (disable khi pending).
- **Confirm** hành động phá huỷ (xoá / huỷ / reset) nếu có nguy cơ mất dữ liệu.

## §6 Comment (agent-first)
- Giải thích **VÌ SAO**, không WHAT (tên đã nói). Làm khác lẽ thường → ref: `// BR-… / ADR-… / FEAT-… AC-… / xem DECISIONS.md <ngày>`.
- KHÔNG authorship/date (git nhớ) · không để code chết dạng comment.

## §7 Git & phụ thuộc
- Commit nhỏ, message tiếng Việt thể chủ động. **Code lệch doc → sửa doc CÙNG commit** (luật #4).
- Thêm thư viện = quyết định → `DECISIONS.md` nếu động kiến trúc / khó gỡ. Ưu tiên thứ có sẵn trong framework.

## §8 Test
- Test theo **HÀNH VI** (không theo hiện thực). Bug fix → **regression test**. Coverage ngưỡng theo kind (BE ~80% · web ~60%) — chi tiết ở stack skill.

## §9 Backend (mọi stack backend — Java/Go/Python…)
> Nguyên tắc backend-universal (không phụ thuộc ngôn ngữ). Idiom cụ thể (Lombok/JPA/@Transactional…) ở `stack-<tên>`.
- **Truy vấn dữ liệu người dùng kèm điều kiện chủ sở hữu/tenant** — không `findById` trần (chi tiết `SECURITY.md §3`).
- **Migration additive**: KHÔNG sửa migration đã apply; cột `NOT NULL` mới đi 2 bước (nullable → backfill → enforce). Add **index** cho field hay join/filter/sort.
- **Không N+1 / query không giới hạn**: không gọi repository trong vòng lặp; list API phải **paginate**.
- **Không gọi external chậm TRONG DB transaction** (cạn connection pool). Publish event **SAU commit** (after-commit / outbox), không trước.
- **Phân loại hardcoded value**: kỹ thuật ổn định → constant · theo môi trường → config/env · secret → vault/env · trạng thái nghiệp vụ → enum · message user → i18n. **KHÔNG hardcode secret** kể cả trong test.
- **Idempotency**: consumer / webhook / callback / job dedup theo id (xem §5).
- **Không phơi entity** ra API (request/response = DTO); không tin id/role/tenant từ client (lấy từ auth context).
