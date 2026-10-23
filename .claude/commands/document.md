---
description: DOCUMENT — interview|intake → doc set (PRD/PERSONAS/FEAT/ARCHITECTURE/UX) → chia wave → khoá scope
---
# /document — Phase DOCUMENT

> Đây là chỗ **DUY NHẤT được hỏi Authority**. Cuối phase = **KHOÁ SCOPE**, từ đó im lặng (BUILD trở đi tự quyết).
> Gọi lại = chạy tiếp từ chốt đang dở. Gọi **sau `/next-wave`** = *top-up* (bổ sung doc + chia lại kế hoạch),
> đọc `docs/ROADMAP.md §backlog` trước — phần bù chen vào wave kế, KHÔNG sửa doc wave đã ship (`archive/`).
> Top-up xử xong item backlog nào (thêm AC · dựng mockup · sửa mockup) → cột **Xử** ghi `đã top-up → <FEAT-x AC-y | màn.html>` — gate BUILD (`pending_topup`) đọc dấu này, thiếu = coi như chưa top-up.

**Việc ĐẦU TIÊN**: sửa `STATE.md` → `Phase hiện tại: DOCUMENT` (nếu đang ở phase khác = back-edge top-up).
**Top-up wave sau**: bỏ tick luôn `Scope khoá` + `PRE-LOCK AUDIT PASS` ở §Gate DOCUMENT — scope mở lại cho phần bù; còn tick thì `guard_ask` chặn hỏi Authority. Lời chốt cuối top-up tick lại (Bước cuối).
`gate.py` + `guard_ask` + `trace_docsync` đọc các dòng này — không sửa thì máy tưởng còn phase cũ.

> **Lấy template**: mọi doc dựng từ mẫu ở **`templates/`** (bảng template ↔ path đích: `templates/README.md`).
> Mỗi Bước dưới: copy template tương ứng → path đích → **xoá comment `<!-- -->` guidance** → điền hết `{{...}}`.
> `docs/` + `knowledge-base/` chỉ chứa file THẬT (gate không quét `templates/`).

> **SỬA/BỔ SUNG doc = CASCADE qua đồ thị phụ thuộc, KHÔNG point-edit.** Khi Authority đọc lại phát hiện thiếu (vd "quản lý thêm thông tin X") → **không chỉ sửa doc được nhắc tên**, phải lần hết doc liên đới:
> - Thêm **field/thông tin** → `feat/FEAT-*` (AC + ràng buộc nghiệp vụ) · `arch/{name}.md` (**data model** + **§3 API** request/response) · `ux/mockup` (ô nhập/hiển thị) (+ `CAPABILITIES-MAP` nếu năng lực mới).
> - Thêm **luồng/AC** → bảng luồng (Authority **ký lại**) + màn nháp · FEAT · `arch` (API + events + luồng) · `ux` (màn) (+ `ROADMAP` nếu đổi scope).
> - Sửa **từ màn hình** (Authority xem mockup): **chức năng** (thêm cột/lọc/nút/màn con, đổi bước) → đi **đúng thứ tự vai**: màn nháp (BA; đổi luồng thì sửa bảng luồng + ký lại) → AC/ràng buộc (BA) → `arch §3` API + data model (SA) → mockup + `data-api` (UX) — KHÔNG sửa mockup trước rồi thôi. **Hình thức** (chữ/màu/khoảng cách) → chỉ sửa token `DESIGN-SYSTEM §2`. Ghi vào `SCREEN-MAP §Chốt`.
> Sau MỖI amendment: **re-run trace 6 chiều** (`technical-design §Trọn vẹn`) + chiều **UI↔AC**. Còn **tham chiếu treo** — phần tử ở doc này mà doc liên đới KHÔNG có phần tương ứng cấp cho nó (vd: field trong AC nhưng **data model thiếu cột** · AC cần API nhưng **arch §3 thiếu endpoint** · màn mockup nhưng **không FEAT/AC nào đứng sau**) — = **chưa xong**. Authority chỉ nói cái họ THẤY thiếu — **agent tự truy các doc liên đới**, không để họ dò lỗ hộ. *(Hook `trace_docsync` nhắc mỗi lần Edit spec doc ở DOCUMENT.)*

## Phân vai — mỗi mục tài liệu ĐÚNG MỘT vai viết
| Vai | Bước | Skill | Sở hữu (viết) |
|---|---|---|---|
| **PO** | 0–2 · 4 · 5 nhịp 1 | `discovery-hypothesis` · `capability-mapping` · `domain-po` | INTERVIEW khám phá · PRD (gồm §3 NFR, §6 nguồn, §7 dữ liệu mẫu) · CAPABILITIES-MAP · khung FEAT (mục tiêu · phạm vi) |
| **BA** | 3 · 5 nhịp 2–3 | `domain-ba` · `business-analysis` (tự rà) | bảng luồng + màn nháp · business-rule · PERSONAS + ma trận · FEAT §2 AC + §3 ràng buộc nghiệp vụ |
| **SA** | 6 · 7 · 7b | `event-storming` · `boundary-charter` · `system-design` · `technical-design` | OVERVIEW (§1–§5) · `arch/{name}.md` (gồm chặn ở đâu, `consumes`) · ADR · TECHSTACK (Authority chốt) · rà/chỉnh CONVENTIONS + SECURITY (7b) |
| **UX** | 8 | `ux-design` | DESIGN-SYSTEM · SCREEN-MAP · mockup |
| **PM** | 9 | `implementation-plan` | ROADMAP · cột Wave |
| **RV** | 10 · chốt | `business-analysis` (rà chéo) · agent `pre-mortem` | chỉ nghi vấn — không sửa doc |

`DECISIONS.md` là sổ chung — vai nào quyết thì ghi dòng của mình (cột Loại). MAIN đóng mọi vai nhưng mỗi lúc chỉ viết **mục của vai đang đóng**. Thấy lỗi ở mục vai khác → ghi nghi vấn, vai sở hữu sửa rồi CASCADE. PO/BA viết *cái gì · ai · vì sao*; SA viết *làm thế nào · ở đâu* — FEAT/PRD không chứa tên class, bảng, công nghệ.

## Bước 0 — Nhận diện đường vào
- `intake/` có tài liệu đã điền thật (không phải template `_*.md` trơ)? → **ĐƯỜNG INTAKE**: ghi marker
  `NGUỒN: INTAKE` (ngoài comment) vào `docs/INTERVIEW.md`.
- Không → **ĐƯỜNG INTERVIEW**.
Ghi kết quả vào `STATE.md` dòng `Đường vào`.

## Bước 1 — Nạp nguyên liệu (rẽ nhánh theo đường vào) · *PO*
- **INTERVIEW**: → **Nạp `Skill("discovery-hypothesis")` trước, đọc xong mới hỏi** (4 luật đào sâu + probe nghiệp vụ hóc búa + cược đo được). Authority không kể được nghiệp vụ / trả lời "không biết" → đi đường **§Authority chưa có kinh nghiệm** của skill (MAIN dẫn từ bản đồ nghiệp vụ xuống, hỏi bằng câu hỏi bối cảnh). Phỏng vấn Authority tới khi đủ dựng PRD/persona/capability (không trần số câu; đây là chỗ được hỏi). Kết tinh vào `docs/INTERVIEW.md` **theo đợt**: DOCUMENT đầu ghi khối `### Wave 1`; top-up sau
  `/next-wave` **thêm khối `### Wave N`** (không sửa khối cũ), mỗi mục có dòng `Bằng chứng:` + gắn FEAT nó phục vụ.
  > **Cách hỏi** (DOCUMENT = chỗ DUY NHẤT `AskUserQuestion` được phép — guard_ask cho qua):
  > · **Khám phá** (pain/persona/ca biên/rỗng-lỗi/gu giao diện lượt 1) → **hội thoại MỞ bằng lời**, KHÔNG dùng `AskUserQuestion` (option mớm lời → Authority bấm cái nghe hợp lý thay vì kể thật).
  > · **Quyết định** (phạm vi bản đầu/lựa chọn thiết kế/stack/auth/thu tiền/deploy) → `AskUserQuestion` với **option cụ thể + đánh đổi** ("Clerk 20' có phí vs Auth.js 1-2h free").
- **INTAKE**: đọc `intake/*.md` — **KHÔNG phỏng vấn lại**. Dịch/render sang doc set bên dưới, lập **bảng truy
  vết** `intake → FEAT` trong `docs/INTERVIEW.md`. `intake/TECHSTACK` **thắng** default của stack skill.
  > **Intake là LỜI KHAI, không phải SỰ THẬT ĐỦ — bỏ phỏng vấn ≠ bỏ RÀ.** Render xong vẫn chạy đủ: research domain **bắt buộc** (bảng 4 loại ở `Skill("discovery-hypothesis")` §Research) (tài liệu người ta đưa không thay được tra ngành — đổ ra danh sách luồng chuẩn ngành vào PRD §6 như đường interview) + lưới cạnh-có-chủ/seam (`domain-ba` D) + 6 họ phổ quát (`pre-mortem`). Lỗ tìm thấy → đang ở DOCUMENT, **được hỏi Authority** hoặc DECISIONS — xử tại chỗ. **Bảng "Lỗ hổng & cách xử" áp cho cả intake — bảng trống = CHƯA rà, không phải intake hoàn hảo.**

## Bước 2 — PRD (`docs/PRD.md`) · *PO*
Vấn đề (pain) + đối tượng cụ thể + **out-of-scope tường minh** + ≥1 success metric **có số**.

## Bước 3 — Phân tích BA: bảng luồng + màn nháp → business-rule → PERSONAS · *BA*  → **Nạp `Skill("domain-ba")` trước**
**Trình tự PO → BA → yêu cầu**: khám phá (Bước 1-2) là việc PO; Bước 3 là BA **phân tích quy trình TRƯỚC khi ai viết AC** — (A) dựng bảng luồng `Ai LÀM · Làm gì · Ai NHỜ/duyệt · Đầu vào→đầu ra · Bằng chứng` cho từng nghiệp vụ vào `docs/INTERVIEW.md §Luồng nghiệp vụ đã xác nhận`, ô `CHƯA HỎI` → hỏi Authority ngay (cả 2 đường vào) + **bảng chính sách từng hành động** (khi nào · ai · giới hạn · trùng gì · ngoại lệ — research lấy dấu vết + suy luận 4 phép thử → đề xuất mặc định, Authority chọn; Authority không cần biết trước luật), **Authority ký bảng** → (B) business-rule (sinh từ cả bảng chính sách) → (C) persona + ma trận sinh TỪ bảng. Từ đây actor của AC (Bước 5), ô ma trận, luồng nghiệp vụ mà build/verify/dogfood đi theo **chỉ lấy từ bảng** — chống suy diễn "người có nhu cầu = người thao tác".
Persona + năng lực được cấp + **ma trận vai × hành động** — mỗi ô `có`/`cấm`, **KHÔNG ô trống**
(đây là spec phân quyền khi code + nguồn TC âm khi test + danh sách phép thử của vai `breaker` ở dogfood).

## Bước 4 — CAPABILITIES-MAP (`docs/CAPABILITIES-MAP.md`) · *PO*  → **Nạp `Skill("capability-mapping")` trước**
`capability → outcome → FEAT`. **Mọi FEAT truy về ≥1 capability**; capability TRƯỚC feature. Cột `Wave giao` để trống (điền ở Bước 9).

## Bước 5 — FEAT (`docs/feat/FEAT-*.md`) — 3 nhịp, mỗi nhịp một vai
1. **PO** → **Nạp `Skill("domain-po")`**: cắt mỗi capability thành ≥1 FEAT, tạo **khung** (capability · has_ui · §1 Mục tiêu · §Ngoài phạm vi · §References dòng bảng luồng phủ).
2. **BA** → **Nạp `Skill("domain-ba")` phần D**: điền **§2 AC dạng BDD** (Given/When/Then) **gồm ca biên** (taxonomy đủ trục, `n/a` tường minh) + **§3 Ràng buộc nghiệp vụ** (điều không được xảy ra). Actor AC = cột Ai LÀM của bảng luồng.
3. **BA tự rà** → checklist **`Skill("business-analysis")`**: actor mỗi AC ↔ cột Ai LÀM, lệch = sai không phải nitpick. Con mắt độc lập là `pre-mortem` ở PRE-LOCK.

FEAT **không** chứa chặn ở đâu / contract / tên class-bảng-công nghệ — SA ghi ở Bước 6 (`arch §6` cột AC/BR · `consumes` ở frontmatter `arch`). Mỗi FEAT truy về ≥1 capability + ≥1 persona.

## Bước 6 — Architecture (`docs/arch/`) · *SA*  → **Nạp 4 skill THEO THỨ TỰ (vai SA): `Skill("event-storming")` → `Skill("boundary-charter")` → `Skill("system-design")` → `Skill("technical-design")`** (nạp từng cái đúng lúc dùng)
- Thứ tự + phân đất: `event-storming` ghi **OVERVIEW §4** (events/aggregates/hot-spots per domain) → `boundary-charter` đọc §4, ghi **OVERVIEW §1** (bản đồ target) + **khởi tạo** `arch/{name}.md` §Mission (target = boundary, cùng tên file) → `system-design` ghi **OVERVIEW §5** (NFR → ước lượng tải → thành phần → lưu trữ → nhất quán → chế độ lỗi → bảo mật → triển khai → ADR có số; tỉ lệ thuận quy mô) → `technical-design` điền **chi tiết** `arch/{name}.md`, phản ánh §5.
- **Rời bước 6 CHỈ KHI trace 6 chiều PASS** (`technical-design §Trọn vẹn` — chiều 1 gồm vế màn nháp BA ↔ API; vế mockup ↔ API (`data-api`) rà ở Bước 8) — **tự rà, KHÔNG để Authority phát hiện lỗ hộ**.
- `docs/arch/OVERVIEW.md`: topology — có target nào, ai gọi ai, ranh giới hệ.
- `docs/arch/<name>.md` **per target**: frontmatter **`kind`** (backend/web/bff/mobile/desktop) + **`stack`** + **`consumes`** → **data model** + **§3 API** (endpoint/method/field/error) + **§Events** (nếu phát/nhận) + **§Ranh giới** (logic ở tầng nào). Contract CỤ THỂ + chặn ở đâu (§6, cột AC/BR trỏ FEAT §3) + `consumes` (target gọi API của ai) nằm ở đây — FEAT không chứa.

## Bước 7 — TECHSTACK (`docs/TECHSTACK.md`) · *SA đề xuất · Authority chốt*
**Chỗ DUY NHẤT chốt tech** (Bước 6 chỉ đề xuất, không tự chốt). Lựa chọn Authority sẽ thấy / phải vận hành / tốn tiền (stack · UI kit · đăng nhập & phiên · lưu file · cache · email/SMS · build tool · deploy) mà Authority CHƯA nói → **hỏi bằng `AskUserQuestion`**, mỗi câu 2-3 option + đánh đổi 1 dòng + mặc định đề xuất. Authority đã nói / intake đã khai → giữ nguyên, không hỏi lại. Chi tiết thuần nội bộ → tự quyết, `DECISIONS` loại `kỹ-thuật`. Kết quả → `docs/TECHSTACK.md` + ADR.
> **Có UI → hỏi gu giao diện TRƯỚC khi hỏi UI kit** (`ux-design` Phương pháp bước 0, lượt 1). Hỏi mở bằng lời, không dùng `AskUserQuestion`: Authority có bộ nhận diện, template đã mua, bản thiết kế hay ứng dụng mẫu nào muốn bám theo không? Gu quyết UI kit, nên hỏi ngược lại sẽ phải sửa TECHSTACK và ADR. Ghi câu trả lời vào `INTERVIEW §1` (khối wave hiện tại, dòng `Bằng chứng:`); Bước 8 chép sang `DESIGN-SYSTEM §1`.
> **VERSION mỗi stack: lấy default ở dòng `description` của skill `stack-<tên>` nếu có (kèm ghi chú EOL); skill chưa ghi thì tra WebSearch (trang chính thức, npm, pub.dev). CẤM điền version từ trí nhớ.** Knowledge cutoff của model CŨ hơn thực tại: "version mình nhớ là mới nhất" thường đã lỗi thời/EOL. Authority không chỉ định version → dùng default của skill (hoặc bản ổn định mới nhất tra được) + 1 dòng `DECISIONS.md` nêu nguồn; Authority chỉ định khác default → theo Authority, ghi ADR.
> **Quét FEAT tìm feature NGẦM đòi tech/infra chưa chốt** (danh sách: `pre-mortem` mục "Feature NGẦM ĐÒI tech/infra") → đưa vào lượt hỏi ở trên.

## Bước 7b — Quy ước chung  *(đã có sẵn — framework default, KHÔNG author lại)*
`docs/CONVENTIONS.md` + `docs/SECURITY.md` là **doc framework cố định**. Chỉ **rà + chỉnh §API error-envelope/header/versioning**
nếu project khác default → sửa thẳng file + ghi `DECISIONS.md`.
- Contract **CỤ THỂ** từng target (endpoints) → `arch/<name>.md §3 API`; target consumer khai `consumes` ở frontmatter `arch/<name>.md`;
  đồng bộ bằng **contract-test** (VERIFY) + **BACKWARD-COMPAT** (SHIP). (Skill `stack-*` lo idiom CODE.)

## Bước 8 — Design system + UX · *UX*  → **Nạp `Skill("ux-design")` trước** (nếu có UI; backend-only → ghi marker `KHÔNG CÓ UI`, bỏ qua bước này)
**Việc đầu tiên: đọc gu giao diện Authority đã nói ở Bước 7** (`INTERVIEW §1`) rồi chép vào `DESIGN-SYSTEM §1`. Chưa hỏi được ở Bước 7 thì hỏi ngay bây giờ (`ux-design` Phương pháp bước 0). Authority không có gì để bám thì MAIN tra rồi đề xuất 2–3 hướng cho Authority chọn. Gu là sở thích của Authority, không đoán rồi chờ chốt cuối. Thứ tự bắt buộc: `docs/DESIGN-SYSTEM.md` (token — **khoá TRƯỚC**, cả dự án) → `docs/ux/SCREEN-MAP.md` (mục lục
**mọi màn** ↔ target ↔ FEAT ↔ wave, cả dự án) → **DỪNG, sang Bước 9 chia wave** (cột `Wave` của SCREEN-MAP điền ở Bước 9) → quay lại dựng `docs/ux/mockups/<target>/<module>.html` **chỉ màn in-scope
wave đang mở** (ở DOCUMENT = wave 1; màn wave sau để trống, `/document` top-up khi `/next-wave` mở wave đó —
vẽ tới đâu duyệt tới đó, không phí công mockup wave xa dễ đổi) → **rà nhất quán cross-màn** (app shell — sidebar/nav/logo/user-menu — phải giống hệt mọi mockup; lệch = sửa khớp `_shell.html` canonical, xem `ux-design §Nhất quán cross-màn`) → **Authority chốt mockup của wave đó**.
Token là thứ **DUY NHẤT chép nguyên** sang code ở BUILD.

## Bước 9 — Chia wave (`docs/ROADMAP.md`) · *PM*
Bảng wave: mỗi wave khai **target** (kind: backend/web/bff/mobile/desktop) + **phases chạy** (`BUILD,VERIFY[,SHIP]`) + **AC in-scope**.
**FEAT-cap** = `feat_cap_per_wave` (frontmatter `docs/ROADMAP.md`, **mặc định ~3-4 FEAT/wave ≈ 15-20 AC**) — ngưỡng để **một phiên BUILD của MAIN làm nổi** (MAIN tự code hết). KHUYẾN KHÍCH, **tròn luồng thắng con số**: tách mà đứt luồng → giữ tròn + 1 dòng `DECISIONS.md` nêu lý do; 1 FEAT quá to (nhiều AC) → **báo PO tách** (`domain-po`), PM không tự tách. **SỐ WAVE = số dòng §1** (phái sinh từ scope ÷ cap + phụ thuộc — không đặt tay). → **Nạp `Skill("implementation-plan")` để chia**. Điền cột
`Wave giao` ở CAPABILITIES-MAP + cột `Wave` ở SCREEN-MAP. Để trống `§backlog` (amendment tương lai đổ vào đây).
Có UI → **quay lại Bước 8 dựng mockup màn wave 1** (ux-design) rồi mới sang Bước 10.

## Bước 10 — Challenge DOCUMENT (luật #8 — tới khi hiểu ĐÚNG Ý AUTHOR) · *RV*  → **Nạp `Skill("business-analysis")` để rà chéo**
Tự ra **≥3 câu hỏi khó nhất**, trả lời **CHỈ bằng tài liệu vừa viết** — trong đó **≥1 câu dạng JOURNEY-WALK**: lấy persona + dữ liệu mẫu PRD §7, đi bộ xuyên doc *"dẫn 〈persona X〉 từ zero đến làm được 〈việc Y〉 — từng bước trích doc"* (câu hỏi ĐIỂM bắt lỗ cục bộ; walk bắt luồng đứt/vắng — kẹt ở bước không trích được = lỗ ngay tại đó). Câu nào phải đoán = **một lỗ tài liệu** →
vá (INTERVIEW: **hỏi Authority thêm** · INTAKE: dịch lại + vá lỗ) — vá theo **luật CASCADE** (đầu file): mỗi vá lan hết doc liên đới, không point-edit. **Lặp tới khi tài liệu trả lời được HẾT và
phản ánh ĐÚNG ý Authority** (không còn chỗ đoán, không còn lệch ý) — **không giới hạn số vòng**. **PASS** mới đi tiếp.
Ghi mỗi vòng vào `STATE.md §Challenge log`.

**PRE-LOCK AUDIT (bắt buộc — ĐIỂM KÍCH HOẠT: Authority nói "chốt scope"/"chốt tài liệu" ở Bước cuối. LUÔN chạy tại lời chốt, KỂ CẢ ô `PRE-LOCK AUDIT PASS` đang tick — tick là dấu ghi nhận, KHÔNG phải vé skip: bịt tick chay + sửa doc ngoài tool mà hook không thấy. Chạy sớm hơn lời chốt chỉ phí: doc còn đổi theo nhận xét thì audit trên bản trung gian là audit vứt đi) — 2 phần:**

**(1) Khớp nhau — consistency** (đọc TRỌN doc set, báo mọi **tham chiếu treo**):
- **Trace 6 chiều** (`technical-design §Trọn vẹn` — gồm chiều 6 lifecycle & seam) + **mỗi vùng dữ liệu/thao tác trên màn có API** (`data-api` trên mockup ↔ `arch §3` — gate `mockup_api_gaps` soi máy).
- **UI↔AC 2 chiều — chấm TỪNG AC, không chấm gộp per-FEAT**: lập danh sách 2 cột **mọi AC `has_ui` in-scope** ↔ **màn + phần tử/khuôn xử nó** (từ SCREEN-MAP) — AC không có dòng = **màn con thiếu** (form/detail/modal bị lười), bổ sung mockup + API cho nó TRƯỚC khi khoá ("FEAT có 1 màn list" KHÔNG phải bằng chứng phủ). Chiều ngược: mỗi phần tử tương tác trong mockup (search/filter/sort/nút/phân trang) có 1 AC — phần tử **không AC = quyết NGAY** (thêm AC · hoặc bỏ khỏi mockup), **KHÔNG silent-defer wave sau**. Kèm: mỗi **vùng dữ liệu** trên mockup (kể cả read-only) có API fetch trong `arch §3` (khai ở SCREEN-MAP behavior).

**(2) Không thiếu — completeness** (con mắt ĐỘC LẬP, bù điểm mù Authority + MAIN-tự-vấn):
- **Spawn `pre-mortem`** (sub-agent độc lập MAIN) → quét mỗi FEAT/luồng qua **taxonomy ca biên** (`domain-ba` D) + 4 câu xuyên-luồng + 6 họ luồng phổ quát + đối chiếu ngành → trả **nghi vấn case Authority MISS**.
- MAIN nhận nghi vấn → mỗi cái **quyết**: thêm AC (CASCADE) · hỏi Authority (còn DOCUMENT nên được hỏi) · chuẩn ngành có link → `DECISIONS` (PROTOCOL §2.3). **KHÔNG bỏ lửng, không đoán.**
- Nghi vấn **đổi luồng** (thiếu bước · sai Ai LÀM · thiếu nhánh) → **sửa bảng luồng `INTERVIEW` TRƯỚC** (thêm dòng, Bằng chứng = câu Authority vừa trả lời), Authority **ký lại** bảng đó (cập nhật ngày `chốt bởi Authority`) → rồi mới CASCADE xuống AC · ma trận · SCREEN-MAP. Chỉ thêm AC mà bảng không đổi = vai/màn/luồng dogfood thiếu theo.

> Cả 2 phần là việc **NGỮ NGHĨA** — làm bằng đọc/đối chiếu + agent độc lập, **KHÔNG** phải hook. Hook `trace_docsync` chỉ TRIGGER nhắc; audit này mới KIỂM. Còn tham chiếu treo HOẶC nghi vấn pre-mortem chưa xử = **chưa được khoá scope**.
>
> **Tick ô `PRE-LOCK AUDIT PASS` (STATE §Gate DOCUMENT) CHỈ khi xong CẢ 2 phần** — xong mỗi (1) chưa được tick. Tick rồi mà còn sửa spec doc (Authority nhận xét thêm) → `trace_docsync` TỰ BỎ TICK: xử CASCADE xong, tới lời chốt kế phải **re-run audit trên bản mới** rồi mới tick lại.
>
> **Re-run có trọng tâm** (đỡ phí — tick rụng như nhau, khác độ SÂU lượt audit lại): sửa chữ nghĩa/trình bày không đổi AC/field/luồng → re-trace quanh vùng đổi là đủ, khỏi re-spawn. Đổi AC/luồng/field/màn → re-trace + spawn `pre-mortem` quét lại FEAT/luồng bị ảnh hưởng (+4 câu xuyên-luồng nếu luồng đổi).

## Bước cuối — Chốt + khoá scope
1. **Trình Authority đọc** toàn bộ doc set → nhận xét → sửa (CASCADE, `trace_docsync` nhắc + rụng tick nếu có) → lặp tới khi Authority nói **"chốt scope" / "chốt tài liệu"**.
2. **Ngay khi nghe lời chốt: làm nốt việc sửa spec doc, TRƯỚC khi audit.** Sửa spec doc nào cũng làm hook bỏ tick `PRE-LOCK AUDIT PASS`, nên hai việc này phải xong trước: ≥2 dòng `docs/DECISIONS.md` (sổ sống, không làm rụng tick), và **PO** đổi `status` mọi FEAT in-scope `DRAFT → APPROVED` (Authority đã đọc và chốt).
3. **Lời chốt = ỦY QUYỀN, không phải bằng chứng** — nó KÍCH HOẠT lượt kiểm cuối, không nhảy cóc qua được:
   · `python scripts/gate.py` (phase DOCUMENT) phải **xanh mọi mục TRỪ dòng `Scope khoá`** (ô đó tick cuối cùng, bước 4).
   · **CHẠY PRE-LOCK AUDIT NGAY LÚC NÀY — LUÔN LUÔN, kể cả ô đang tick** (tick không phải vé skip — có thể là tick chay đời trước, hoặc doc bị sửa ngoài tool mà hook không thấy). Trên ĐÚNG bản sẽ khoá (khối Bước 10: trace 6 chiều + UI↔AC + spawn `pre-mortem`). Độ sâu: lời chốt ĐẦU → đủ CẢ 2 phần; lời chốt lặp (đã audit đủ ở lời chốt trước, chỉ sửa theo nhận xét) → re-run có trọng tâm (khối Bước 10). Nghi vấn xử hết (thêm AC / hỏi Authority — vẫn DOCUMENT nên còn được hỏi / DECISIONS) → mới tick. KHÔNG tick chay.
4. Rà TỪNG ô gate DOCUMENT — ô nào chưa tick thì **làm cho đạt rồi mới tick** (KHÔNG tick gộp cho đủ bộ) → cuối cùng tick `Scope khoá` trong `STATE.md`. **Từ đây không hỏi Authority nữa.**
5. Báo: tài liệu xong — **đã chia thành N wave** (đọc `docs/ROADMAP.md §1`, liệt kê `w1: <target/FEAT> · w2: … · wN: …`), chạy `/build 1` để vào wave đầu.

## Ranh giới
- **Không viết code sản phẩm** ở phase này. Không dựng `services/`. Ngoại lệ duy nhất: **khung** `deployment/local/docker-compose.yml` (SA — `technical-design`) — dựng sẵn service + hạ tầng; `/build` (`infra-local-dev`) làm nốt chi tiết.
- INTAKE: **không tự đẻ target** ngoài `intake/ARCHITECTURE`, **không đổi** lựa chọn intake cho hợp default skill.
- Không bỏ qua challenge cho nhanh — cái giá trả ở BUILD/dogfood.
- Không khoá scope khi Authority chưa đọc + chưa tick `Scope khoá`.
