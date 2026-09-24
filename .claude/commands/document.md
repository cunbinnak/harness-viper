---
description: DOCUMENT — interview|intake → doc set (PRD/PERSONAS/FEAT/ARCHITECTURE/UX) → chia wave → khoá scope
---
# /document — Phase DOCUMENT

> Đây là chỗ **DUY NHẤT được hỏi Authority**. Cuối phase = **KHOÁ SCOPE**, từ đó im lặng (BUILD trở đi tự quyết).
> Gọi lại = chạy tiếp từ chốt đang dở. Gọi **sau `/next-wave`** = *top-up* (bổ sung doc + chia lại kế hoạch),
> đọc `docs/ROADMAP.md §backlog` trước — phần bù chen vào wave kế, KHÔNG sửa doc wave đã ship (`archive/`).

**Việc ĐẦU TIÊN**: sửa `STATE.md` → `Phase hiện tại: DOCUMENT` (nếu đang ở phase khác = back-edge top-up).
`gate.py` + `guard_ask` đọc dòng này — không sửa thì máy tưởng còn phase cũ.

> **Lấy template**: mọi doc dựng từ mẫu ở **`templates/`** (bảng template ↔ path đích: `templates/README.md`).
> Mỗi Bước dưới: copy template tương ứng → path đích → **xoá comment `<!-- -->` guidance** → điền hết `{{...}}`.
> `docs/` + `knowledge-base/` chỉ chứa file THẬT (gate không quét `templates/`).

> **SỬA/BỔ SUNG doc = CASCADE qua đồ thị phụ thuộc, KHÔNG point-edit.** Khi Authority đọc lại phát hiện thiếu (vd "quản lý thêm thông tin X") → **không chỉ sửa doc được nhắc tên**, phải lần hết doc liên đới:
> - Thêm **field/thông tin** → `feat/FEAT-*` (AC + field kỹ thuật) · `arch/{name}.md` (**data model** + **§3 API** request/response) · `ux/mockup` (ô nhập/hiển thị) (+ `CAPABILITIES-MAP` nếu năng lực mới).
> - Thêm **luồng/AC** → FEAT · `arch` (API + events + luồng) · `ux` (màn) (+ `ROADMAP` nếu đổi scope).
> Sau MỖI amendment: **re-run trace 5 chiều** (`technical-design §Trọn vẹn`) + chiều **UI↔AC**. Còn **tham chiếu treo** — phần tử ở doc này mà doc liên đới KHÔNG có phần tương ứng cấp cho nó (vd: field trong AC nhưng **data model thiếu cột** · AC cần API nhưng **arch §3 thiếu endpoint** · màn mockup nhưng **không FEAT/AC nào đứng sau**) — = **chưa xong**. Authority chỉ nói cái họ THẤY thiếu — **agent tự truy các doc liên đới**, không để họ dò lỗ hộ. *(Hook `trace_docsync` nhắc mỗi lần Edit spec doc ở DOCUMENT.)*

## Bước 0 — Nhận diện đường vào
- `intake/` có tài liệu đã điền thật (không phải template `_*.md` trơ)? → **ĐƯỜNG INTAKE**: ghi marker
  `NGUỒN: INTAKE` (ngoài comment) vào `docs/INTERVIEW.md`.
- Không → **ĐƯỜNG INTERVIEW**.
Ghi kết quả vào `STATE.md` dòng `Đường vào`.

## Bước 1 — Nạp nguyên liệu (rẽ nhánh theo đường vào)
- **INTERVIEW**: → **Nạp `Skill("discovery-hypothesis")` trước, đọc xong mới hỏi** (4 luật đào sâu + probe nghiệp vụ hóc búa + cược đo được). Phỏng vấn Authority tới khi đủ dựng PRD/persona/capability (không trần số câu; đây là chỗ được hỏi). Kết tinh vào `docs/INTERVIEW.md` **theo đợt**: DOCUMENT đầu ghi khối `### Wave 1`; top-up sau
  `/next-wave` **thêm khối `### Wave N`** (không sửa khối cũ), mỗi mục có dòng `Bằng chứng:` + gắn FEAT nó phục vụ.
  > **Cách hỏi** (DOCUMENT = chỗ DUY NHẤT `AskUserQuestion` được phép — guard_ask cho qua):
  > · **Khám phá** (pain/persona/ca biên/rỗng-lỗi) → **hội thoại MỞ bằng lời**, KHÔNG dùng `AskUserQuestion` (option mớm lời → Authority bấm cái nghe hợp lý thay vì kể thật).
  > · **Quyết định** (stack/auth/thu tiền/deploy) → `AskUserQuestion` với **option cụ thể + đánh đổi** ("Clerk 20' có phí vs Auth.js 1-2h free").
- **INTAKE**: đọc `intake/*.md` — **KHÔNG phỏng vấn lại**. Dịch/render sang doc set bên dưới, lập **bảng truy
  vết** `intake → FEAT` trong `docs/INTERVIEW.md`. `intake/TECHSTACK` **thắng** default của stack skill.

## Bước 2 — PRD (`docs/PRD.md`)
Vấn đề (pain) + đối tượng cụ thể + **out-of-scope tường minh** + ≥1 success metric **có số**.

## Bước 3 — PERSONAS (`docs/PERSONAS.md`)  → **Nạp `Skill("domain-ba")` trước**
Persona + năng lực được cấp + **ma trận vai × hành động** — mỗi ô `có`/`cấm`, **KHÔNG ô trống**
(đây là spec phân quyền khi code + nguồn TC âm khi test + danh sách phép thử của vai `breaker` ở dogfood).

## Bước 4 — CAPABILITIES-MAP (`docs/CAPABILITIES-MAP.md`)  → **Nạp `Skill("capability-mapping")` trước**
`capability → outcome → FEAT`. **Mọi FEAT truy về ≥1 capability**; capability TRƯỚC feature. Cột `Wave giao` để trống (điền ở Bước 9).

## Bước 5 — FEAT (`docs/feat/FEAT-*.md`)  → **Nạp `Skill("domain-po")` trước · viết xong → nạp `Skill("business-analysis")` để rà**
Mỗi capability → ≥1 FEAT. Mỗi FEAT: **AC dạng BDD** (Given/When/Then) **gồm ca biên** (rỗng/đầy/lỗi/quyền) + **field kỹ thuật** (`enforcement` rule · `consumes_contracts` = target nào cấp API/event). Mỗi FEAT truy về ≥1 capability + ≥1 persona.

## Bước 6 — Architecture (`docs/arch/`)  → **Nạp 3 skill THEO THỨ TỰ: `Skill("event-storming")` → `Skill("boundary-charter")` → `Skill("technical-design")`** (nạp từng cái đúng lúc dùng)**
- Thứ tự + phân đất: `event-storming` ghi **OVERVIEW §4** (events/aggregates/hot-spots per domain) → `boundary-charter` đọc §4, ghi **OVERVIEW §1** (bản đồ target) + **khởi tạo** `arch/{name}.md` §Mission (target = boundary, cùng tên file) → `technical-design` điền **chi tiết** `arch/{name}.md`.
- **Rời bước 6 CHỈ KHI trace 5 chiều PASS** (`technical-design §Trọn vẹn`): AC↔API 2 chiều · endpoint đủ ruột · consumes↔provider khớp · luồng E2E không đứt — **tự rà, KHÔNG để Authority phát hiện lỗ hộ**.
- `docs/arch/OVERVIEW.md`: topology — có target nào, ai gọi ai, ranh giới hệ.
- `docs/arch/<name>.md` **per target**: frontmatter **`kind`** (backend/web/bff/mobile) + **`stack`** + **`consumes`** → **data model** + **§3 API** (endpoint/method/field/error) + **§Events** (nếu phát/nhận) + **§Ranh giới** (logic ở tầng nào). Contract CỤ THỂ nằm ở đây; FEAT chỉ khai `consumes_contracts`.

## Bước 7 — TECHSTACK (`docs/TECHSTACK.md`)
Chốt stack (khớp skill `stack-<tên>`) + **1 dòng lý do** ở `docs/DECISIONS.md`. INTAKE: giữ đúng lựa chọn của intake.
> **VERSION mỗi stack: Read dòng `description` của skill `stack-<tên>` tương ứng lấy default + note EOL — CẤM điền version từ trí nhớ.** Knowledge cutoff của model CŨ hơn thực tại: "version mình nhớ là mới nhất" thường đã lỗi thời/EOL. Authority không chỉ định version → dùng default của skill + 1 dòng `DECISIONS.md`; Authority chỉ định khác default → theo Authority, ghi ADR.
> **Quét FEAT xem feature nào NGẦM đòi tech/infra chưa chốt** (Author hay tả tính năng mà quên "chạy bằng gì"): **upload**→lưu trữ (S3/blob/disk) · **thông báo**→email/SMS/push provider · **tìm kiếm nâng cao**→search engine? · **xuất file**→PDF/Excel + sync/async · **thanh toán**→cổng · **lịch/định kỳ**→job runner · **realtime**→WS/SSE. Mỗi cái chạm → chốt trong TECHSTACK/`adr/`. (Sót thì `pre-mortem` bắt ở pre-lock audit, nhưng chốt sớm ở đây đỡ hơn.)

## Bước 7b — Quy ước chung  *(đã có sẵn — framework default, KHÔNG author lại)*
`docs/CONVENTIONS.md` + `docs/SECURITY.md` là **doc framework cố định**. Chỉ **rà + chỉnh §API error-envelope/header/versioning**
nếu project khác default → sửa thẳng file + ghi `DECISIONS.md`.
- Contract **CỤ THỂ** từng target (endpoints) → `arch/<name>.md §3 API`; FE khai `consumes_contracts` trong FEAT;
  đồng bộ bằng **contract-test** (VERIFY) + **BACKWARD-COMPAT** (SHIP). (Skill `stack-*` lo idiom CODE.)

## Bước 8 — Design system + UX  → **Nạp `Skill("ux-design")` trước** (nếu có UI; backend-only → ghi marker `KHÔNG CÓ UI`, bỏ qua bước này)
Thứ tự bắt buộc: `docs/DESIGN-SYSTEM.md` (token — **khoá TRƯỚC**, cả dự án) → `docs/ux/SCREEN-MAP.md` (mục lục
**mọi màn** ↔ target ↔ FEAT ↔ wave, cả dự án) → `docs/ux/mockups/<target>/*.html` **chỉ dựng màn in-scope
wave đang mở** (ở DOCUMENT = wave 1; màn wave sau để trống, `/document` top-up khi `/next-wave` mở wave đó —
vẽ tới đâu duyệt tới đó, không phí công mockup wave xa dễ đổi) → **rà nhất quán cross-màn** (app shell — sidebar/nav/logo/user-menu — phải giống hệt mọi mockup; lệch = sửa khớp `_shell.html` canonical, xem `ux-design §Nhất quán cross-màn`) → **Authority chốt mockup của wave đó**.
Token là thứ **DUY NHẤT chép nguyên** sang code ở BUILD.

## Bước 9 — Chia wave (`docs/ROADMAP.md`)
Bảng wave: mỗi wave khai **target** (kind: backend/web/bff/mobile) + **phases chạy** (`BUILD,VERIFY[,SHIP]`) + **AC in-scope**.
**FEAT-cap** = `feat_cap_per_wave` (frontmatter `docs/ROADMAP.md`, **mặc định ~3-4 FEAT/wave ≈ 15-20 AC**) — ngưỡng để **một phiên BUILD của MAIN làm nổi** (MAIN-code-hết, không dev-agent). KHUYẾN KHÍCH, **tròn luồng thắng con số**: tách mà đứt luồng → giữ tròn + ghi `rationale`; 1 FEAT quá to (nhiều AC) → tách nhỏ. **SỐ WAVE = số dòng §1** (phái sinh từ scope ÷ cap + phụ thuộc — không đặt tay). → **Nạp `Skill("implementation-plan")` để chia**. Điền cột
`Wave giao` ở CAPABILITIES-MAP. Để trống `§backlog` (amendment tương lai đổ vào đây).

## Bước 10 — Challenge DOCUMENT (luật #8 — tới khi hiểu ĐÚNG Ý AUTHOR)  → **Nạp `Skill("business-analysis")` để rà chéo**
Tự ra **≥3 câu hỏi khó nhất**, trả lời **CHỈ bằng tài liệu vừa viết**. Câu nào phải đoán = **một lỗ tài liệu** →
vá (INTERVIEW: **hỏi Authority thêm** · INTAKE: dịch lại + vá lỗ) — vá theo **luật CASCADE** (đầu file): mỗi vá lan hết doc liên đới, không point-edit. **Lặp tới khi tài liệu trả lời được HẾT và
phản ánh ĐÚNG ý Author** (không còn chỗ đoán, không còn lệch ý) — **không giới hạn số vòng**. **PASS** mới đi tiếp.
Ghi mỗi vòng vào `STATE.md §Challenge log`.

**PRE-LOCK AUDIT (bắt buộc — ĐIỂM KÍCH HOẠT: Author nói "chốt scope"/"chốt tài liệu" ở Bước cuối. LUÔN chạy tại lời chốt, KỂ CẢ ô `PRE-LOCK AUDIT PASS` đang tick — tick là dấu ghi nhận, KHÔNG phải vé skip: bịt tick chay + sửa doc ngoài tool mà hook không thấy. Chạy sớm hơn lời chốt chỉ phí: doc còn đổi theo nhận xét thì audit trên bản trung gian là audit vứt đi) — 2 phần:**

**(1) Khớp nhau — consistency** (đọc TRỌN doc set, báo mọi **tham chiếu treo**):
- **AC↔API 2 chiều** · **data model nuôi đủ field mọi AC cần** · **consumes↔provider khớp** · **luồng E2E không đứt** (`technical-design §Trọn vẹn`).
- **UI↔AC 2 chiều**: mỗi phần tử tương tác trong mockup (search/filter/sort/nút/phân trang) có 1 AC · mỗi AC có UI có phần tử mockup. Phần tử mockup **không AC = quyết NGAY** (thêm AC vì UI đã/ sẽ duyệt · hoặc bỏ khỏi mockup) — **KHÔNG silent-defer wave sau**.

**(2) Không thiếu — completeness** (con mắt ĐỘC LẬP, bù điểm mù Author + MAIN-tự-vấn):
- **Spawn `pre-mortem`** (sub-agent độc lập MAIN) → quét mỗi FEAT/luồng qua **taxonomy ca biên** (`domain-po`) + 3 câu xuyên-luồng → trả **nghi vấn case Author MISS**.
- MAIN nhận nghi vấn → mỗi cái **quyết**: thêm AC (CASCADE) · hỏi Authority (còn DOCUMENT nên được hỏi) · ghi giả định `DECISIONS.md`. **KHÔNG bỏ lửng.**

> Cả 2 phần là việc **NGỮ NGHĨA** — làm bằng đọc/đối chiếu + agent độc lập, **KHÔNG** phải hook. Hook `trace_docsync` chỉ TRIGGER nhắc; audit này mới KIỂM. Còn tham chiếu treo HOẶC nghi vấn pre-mortem chưa xử = **chưa được khoá scope**.
>
> **Tick ô `PRE-LOCK AUDIT PASS` (STATE §Gate DOCUMENT) CHỈ khi xong CẢ 2 phần** — xong mỗi (1) chưa được tick. Tick rồi mà còn sửa spec doc (Authority nhận xét thêm) → `trace_docsync` TỰ BỎ TICK: xử CASCADE xong, tới lời chốt kế phải **re-run audit trên bản mới** rồi mới tick lại.
>
> **Re-run có trọng tâm** (đỡ phí — tick rụng như nhau, khác độ SÂU lượt audit lại): sửa chữ nghĩa/trình bày không đổi AC/field/luồng → re-trace quanh vùng đổi là đủ, khỏi re-spawn. Đổi AC/luồng/field/màn → re-trace + spawn `pre-mortem` quét lại FEAT/luồng bị ảnh hưởng (+3 câu xuyên-luồng nếu luồng đổi).

## Bước cuối — Chốt + khoá scope
1. **Trình Authority đọc** toàn bộ doc set → nhận xét → sửa (CASCADE, `trace_docsync` nhắc + rụng tick nếu có) → lặp tới khi Authority nói **"chốt scope" / "chốt tài liệu"**.
2. **Lời chốt = ỦY QUYỀN, không phải bằng chứng** — nó KÍCH HOẠT lượt kiểm cuối, không nhảy cóc qua được:
   · `python scripts/gate.py` (phase DOCUMENT) phải **xanh**.
   · **CHẠY PRE-LOCK AUDIT NGAY LÚC NÀY — LUÔN LUÔN, kể cả ô đang tick** (tick không phải vé skip — có thể là tick chay đời trước, hoặc doc bị sửa ngoài tool mà hook không thấy). Trên ĐÚNG bản sẽ khoá (khối Bước 10: trace 5 chiều + UI↔AC + spawn `pre-mortem`). Độ sâu: lời chốt ĐẦU → đủ CẢ 2 phần; lời chốt lặp (đã audit đủ ở lời chốt trước, chỉ sửa theo nhận xét) → re-run có trọng tâm (khối Bước 10). Nghi vấn xử hết (thêm AC / hỏi Authority — vẫn DOCUMENT nên còn được hỏi / DECISIONS) → mới tick. KHÔNG tick chay.
3. ≥2 dòng `docs/DECISIONS.md`.
4. Rà TỪNG ô gate DOCUMENT — ô nào chưa tick thì **làm cho đạt rồi mới tick** (KHÔNG tick gộp cho đủ bộ) → cuối cùng tick `Scope khoá` trong `STATE.md`. **Từ đây không hỏi Authority nữa.**
5. Báo: tài liệu xong — **đã chia thành N wave** (đọc `docs/ROADMAP.md §1`, liệt kê `w1: <target/FEAT> · w2: … · wN: …`), chạy `/build 1` để vào wave đầu.

## Ranh giới
- **Không viết code** ở phase này. Không dựng `services/`.
- INTAKE: **không tự đẻ target** ngoài `intake/ARCHITECTURE`, **không đổi** lựa chọn intake cho hợp default skill.
- Không bỏ qua challenge cho nhanh — cái giá trả ở BUILD/dogfood.
- Không khoá scope khi Authority chưa đọc + chưa tick `Scope khoá`.
