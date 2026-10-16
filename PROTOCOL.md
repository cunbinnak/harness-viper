# PROTOCOL — {{PROJECT_NAME}}

> Định nghĩa CHUẨN của quy trình. [STATE.md](STATE.md) là bản thao tác; lệch nhau thì **PROTOCOL.md thắng**.
> Router ngắn mỗi phiên: `CLAUDE.md`.
> **Authority** = chủ dự án (MỘT người) — gọi lệnh, quyết nghiệp vụ · phạm vi · go/pivot/kill. MAIN = phiên Claude chính (viết tài liệu + code); agent = phiên phụ chỉ để kiểm.
>
> **Trạng thái: HOÀN THIỆN — khung đã dựng, selftest xanh** (7 command · gate.py · 10 agent · hooks · skill library).
> Bộ khung tinh gọn: 1 lớp doc · MAIN tự code · inline prompt · ít script + gate nhìn thấy được.

---

## §0 — Hai đường vào (entry paths)

Nhận diện bằng đúng một dấu hiệu: `docs/INTERVIEW.md` có marker `NGUỒN: INTAKE` (ngoài comment) hay không.

| | **Đường INTERVIEW** | **Đường INTAKE** |
|---|---|---|
| Khi nào | Ý tưởng mới, chưa có tài liệu phân tích (greenfield, project nhỏ) | Đã có tài liệu MESH-render/phân tích sẵn ở `intake/` |
| MAIN làm | **Phỏng vấn Authority** → `docs/INTERVIEW.md` đủ dòng bằng chứng → suy ra PRD/personas/… | **Dịch/render** `intake/*.md` vào doc set + bảng truy vết + marker `NGUỒN: INTAKE` — không hỏi lại điều intake đã trả lời; chỗ intake không có → hỏi như đường interview |
| Cỡ | nhỏ: 1 app, 2–3 persona — số AC theo mức tối thiểu chung (≥5 capability · ≥4 AC/FEAT), không có trần | không trần: multi-boundary, AC truy về `CAPABILITIES-MAP.md` |

Cả hai **hội tụ về cùng doc set** (`docs/`) rồi chảy xuống BUILD/VERIFY như nhau — chỉ khác cách nạp nguyên liệu đầu vào. Đường vào quyết định ràng buộc cỡ, không phải quy trình.

---

## §1 — Năm phase (4 cứng + 1 opt-in)

```
  ┌──────────┐ khoá  ┌────────┐ chạy  ┌────────┐      ┌──────────┐ xong ┌───────────┐
  │ DOCUMENT │──────>│ BUILD  │──────>│ VERIFY │─────>│ [SHIP?]  │─────>│ NEXT-WAVE │
  │ tài liệu │ scope │MAIN code│ thật  │test+   │      │ opt-in   │ wave │ wave kế   │
  └──────────┘       └────────┘       │dogfood │      │ theo wave│      └─────┬─────┘
       ^                              └────────┘      └──────────┘            │
       └──────── cần capability/boundary mới → top-up DOCUMENT <──────────────┘
```

| Phase | Làm gì | Ai | Hỏi Authority? | Gate rời phase (chuẩn ở STATE.md §Gate) |
|---|---|---|---|---|
| **DOCUMENT** | interview\|intake → PRD·PERSONAS·CAPABILITIES·FEAT·ARCHITECTURE·DESIGN-SYSTEM·ux → chia wave → **khoá scope** | MAIN viết | CÓ — chỗ duy nhất | doc set đủ mục · challenge PASS · ≥2 decisions · scope khoá |
| **BUILD** | challenge → đọc KG → scaffold → walking skeleton → luồng nghiệp vụ → **chạy thật (docker up)** | **MAIN tự code** | KHÔNG — tự quyết → DECISIONS.md | skeleton thông · make check xanh · đã commit · health 200 |
| **VERIFY** | **code review** (2 vai) → **test case: `test-writer` viết đề** (AC + bảng chính sách + thăm dò + regression) → **`bug-hunter` rà đề** → **`test-writer` sửa đề + chạy** → **dogfood** (6 persona 2 đợt) → vòng sửa: MAIN sửa, agent tìm lại | MAIN sửa + reviewer/bug-hunter/test-writer + 6 persona kiểm | KHÔNG | mỗi AC có TC PASS · không FAIL/BLOCKED · regression PASS · dogfood xong · hết finding BLOCKER/MAJOR · kết luận QC 3 mức |
| **SHIP** | prod-ready → deploy → smoke → rollback thử | MAIN | KHÔNG (deploy = ngoại lệ "hỏi thật") | chỉ chạy khi wave khai SHIP; prod sống · rollback thử |
| **NEXT-WAVE** | go/pivot/kill → snapshot archive → mở wave kế (không reset) | MAIN | (go/pivot/kill) | backlog gộp · snapshot · wave kế mở hoặc teardown |

**Wave**: DOCUMENT chạy 1 lần cho cả dự án (sinh kế hoạch mọi wave). BUILD/VERIFY/SHIP chạy **per wave**.
Mỗi wave **khai báo phases nó chạy** trong `docs/ROADMAP.md` — wave nội bộ có thể bỏ SHIP; không ép mọi wave đủ phase.
**FEAT-cap per wave**: DOCUMENT chia wave giới hạn **~3-4 FEAT/wave** để BUILD vừa context của MAIN (MAIN-code-hết, không dev-agent). Ngưỡng mềm (`implementation-plan`), không gate cứng.

**Loop engineering** (mở wave = RÀ LẠI): kế hoạch mọi wave lập 1 lần ở DOCUMENT (Authority ký 1 lần),
NHƯNG mở wave nào `/next-wave` phải **rà lại kế hoạch wave đó đối chiếu KẾT QUẢ wave trước + §backlog**, chỉnh nếu
lệch, rồi stamp ngày vào ô `Rà lại` của wave N (ROADMAP §1). Gate `wave_reviewed` đòi ô đó đã điền — còn trống = đang chạy
mù theo kế hoạch cũ đã lệch. ROADMAP mỗi wave khai thêm: `phụ thuộc wave trước` · `legacy được phép phá`
(nối BACKWARD-COMPAT/guard_bc) · `điều chỉnh khi mở`. **RÀ LẠI định đoạt RÕ từng backlog/finding treo** (xử/hoãn-lý-do/bỏ-lý-do —
không để trôi); go/pivot/kill so **ngưỡng ghi trước** (không sửa sau khi nhìn số).

---

## §2 — Luật nền

1. **Scope khoá sau DOCUMENT.** Phát sinh → `docs/ROADMAP.md §backlog`, không chèn vào wave này.
2. **Sau khi khoá scope: toàn quyền, không hỏi lại.** `AskUserQuestion` **chỉ ở DOCUMENT** (trước khoá scope — phỏng vấn/quyết định); BUILD/VERIFY/SHIP/NEXT-WAVE bị `guard_ask` chặn (ô Scope khoá tick = chốt, chặn luôn dù phase còn ghi DOCUMENT). **Hỏi bằng LỜI cũng là hỏi** — sau khoá scope chỉ được DỪNG chờ Authority ở 2 chỗ: (a) đóng wave (go/pivot/kill, `/next-wave`) · (b) hành động ra-ngoài/không-đảo-ngược (deploy, xoá dữ liệu thật, gửi ra ngoài). Mọi thứ khác — thứ tự làm, có chạy bước kế không, có ghi backlog không, sửa hết hay để lại, nới tiêu chí gate, mockup hay app đúng — **tự quyết theo §2.3, ghi lại, làm tiếp**. Kết lượt giữa phase bằng "bạn muốn…?" / "khi bạn muốn" / "cần bạn quyết" = vi phạm.
3. **Chỗ chưa rõ → phân loại theo bảng dưới, rồi research + suy luận. CẤM đoán không nguồn.**

| Loại chỗ chưa rõ | Ví dụ | Ở DOCUMENT | Sau khoá scope (BUILD trở đi) |
|---|---|---|---|
| **Đã có bằng chứng** | INTERVIEW · bảng luồng đã ký · mockup · AC đã khoá | Làm theo | Làm theo |
| **Quy định bên ngoài** — ràng buộc có sẵn, không phụ thuộc Authority | luật · nghị định · chuẩn kỹ thuật bắt buộc | Research **phải ra văn bản nguồn** → suy luận áp vào sản phẩm ("luật nói X → hệ thống phải chặn Y"). Không tìm được văn bản → ghi `chưa xác minh — <điều nhớ được>`, Authority xác nhận | Có văn bản → làm theo + `DECISIONS` loại `chuẩn-ngành` kèm link · không có → `ROADMAP §backlog` |
| **Lựa chọn thiết kế** — đụng luật nghiệp vụ hoặc phạm vi; Authority không đủ chuyên môn để tự quyết | hạn chót · hạn mức · ngoại lệ · thứ tự làm các mảng · ngưỡng go/pivot/kill · NFR có số | Research → **suy luận ra đề xuất** (vai sở hữu mục đó: PO — phạm vi · thứ tự mảng · ngưỡng · NFR · BA — luật từng hành động) → Authority chọn | `ROADMAP §backlog` — KHÔNG chọn thay Authority |
| **Chỉ Authority biết** | chính sách riêng của đơn vị · cách đơn vị đang làm · sở thích · ngân sách | Hỏi Authority bằng **câu hỏi bối cảnh** (`discovery-hypothesis`) | `STATE §Blocker` / `ROADMAP §backlog` |
| **Kỹ thuật nội bộ** — chi tiết KHÔNG đụng luật nghiệp vụ (ai được làm gì · khi nào · bao nhiêu) | tên field · cấu trúc code · thư viện có trong TECHSTACK · chi tiết hiển thị (cỡ trang mặc định · thứ tự sắp xếp mặc định) | MAIN tự quyết (lựa chọn Authority sẽ thấy / phải vận hành / tốn tiền → hỏi ở `/document` Bước 7) | MAIN tự quyết + `DECISIONS` loại `kỹ-thuật` kèm lý do |

**Research luôn đi kèm suy luận.** Research chỉ là nguyên liệu: không ai công bố cách làm sản phẩm của họ, kết quả tìm kiếm thường chung chung. Suy luận là bước **bắt buộc ngay sau research**, không phải bước dự phòng khi research thiếu. Có hai loại:
- **Suy luận ra đề xuất** (trước khi hỏi Authority): nguyên liệu research + **kiến thức chuyên môn đã có** → áp vào bối cảnh của Authority qua bộ phép thử của chỗ đó (chính sách: `domain-ba` A.6 · thứ tự mảng: `discovery-hypothesis`) → đề xuất.
- **Suy luận lắp ráp** (sau mỗi lượt Authority trả lời): ghép các câu trả lời với nhau qua 4 phép thử — **kéo theo** (câu trả lời đòi thêm dữ liệu / chức năng nào chưa ai nhắc) · **chọi nhau** (hai câu trả lời mâu thuẫn) · **chỗ nối** (đầu ra phần này đi vào phần nào, bằng cách gì, lúc nào) · **còn hở** (thiếu mảnh nào thì luồng không chạy tròn) → bức tranh tổng + câu hỏi mới → đọc lại cho Authority, hỏi tiếp. Dừng khi một lượt lắp ráp không sinh câu hỏi mới.

**Mỗi đề xuất trình đủ 3 phần**: (1) research cho thấy gì — link, hoặc ghi "không tìm thấy" · (2) áp vào bối cảnh này ra sao — trích phép thử nào · (3) đề xuất mặc định + phương án khác + hệ quả nếu chọn sai. Thiếu phần (2) = chép lại research hoặc đoán, chưa phải suy luận.

**Nhãn nguồn chung** (mọi cột Bằng chứng / Nguồn): `Authority` (kèm vị trí, vd `§1 dòng N`) · `[quy định] <link>` · `research <link> + suy luận` · `suy luận` (research không ra gì) · `intake/<file>` · `chưa xác minh — <điều nhớ được>`. Lựa chọn thiết kế đã được chọn → thêm `→ Authority chọn`. KHÔNG gọi suy luận là chuẩn ngành; KHÔNG gắn link chung chung để thành `[quy định]`.

**Authority không cần biết trước — MAIN mang chuyên môn, Authority chỉ quyết.** **Vòng đời `DECISIONS`**: trước khoá scope **sửa tại chỗ** (1 chủ đề = 1 dòng, không thêm dòng lật dòng cũ); sau khoá **supersede** — dòng cũ `Trạng thái: thay bởi DEC-x`, dòng mới ghi `thay DEC-y`.
4. **Doc là nguồn sự thật — ĐÓNG BĂNG sau khoá scope.** Code lệch doc → **KHÔNG sửa doc spec lúc BUILD/VERIFY** (guard_doc chặn); ghi `ROADMAP §backlog` → wave sau `/document` top-up đồng bộ. **Ngoại lệ DUY NHẤT — `amend-arch`** (§3): `docs/arch/*.md` thiếu/sai KỸ THUẬT làm **kẹt luồng** của AC đã khoá → bổ sung `arch` tại chỗ theo 6 điều kiện ở §3. Mơ hồ → `DECISIONS.md` (sổ sống, được ghi). Giữ hợp đồng ổn định để review/dogfood đánh, tránh "vừa code vừa vặn doc".
5. **Cỡ sản phẩm theo đường vào** (§0).
6. **Không secret trong code, không bypass test/lint. Đã code xong → git commit** (không commit = coi như chưa làm).
7. **Tiếng Việt có dấu** cho văn bản người đọc (giữ tiếng Anh cho identifier/API/schema/tên lệnh/tên file).
8. **Sau khoá scope im lặng với Authority, đối kháng nội bộ.** Challenge trước khi code + dogfood trước khi báo xong. Dogfood = **trình duyệt thật** (skill `browse`) — **curl không tính** (trừ target `KHÔNG CÓ UI`); MAIN tự dùng trước rồi mới spawn persona.
9. **Dọn rác tạm.** Artifact tạm — **script chạy thử** (Playwright `.mjs` · k6 · shell) · screenshot · trace · video · log · temp phân tích · `.playwright-mcp/` — để ở **thư mục tạm NGOÀI repo**, dùng xong **dọn ngay** — không commit, không tích tụ, **không đẻ thư mục mới trong repo để cất**. `tracking/wave-N/` chỉ có đúng 3 file: `test-cases.md` · `fidelity.md` · `proof.json`. Build artifact (node_modules/target/dist…) trong `.gitignore`. Docker/seed → teardown ở `/next-wave`.

---

## §3 — Amendment = wave sau (sửa doc sau khi đã chốt)

Sau khoá scope doc spec **đóng băng** (§2.4 — guard_doc chặn); doc wave đã đóng (`archive/`) **bất biến hẳn**. Khi đang BUILD/VERIFY mà phát hiện vấn đề:

```
├─ Code sai so với spec đã chốt                → sửa CODE. Xong. (không đụng doc)
├─ Spec mơ hồ (không nói rõ ca này)            → bảng §2.3 cột "Sau khoá scope": quy định có văn bản / kỹ thuật nội bộ → DECISIONS, đi tiếp · đụng luật nghiệp vụ → backlog, KHÔNG tự bịa. KHÔNG hỏi
├─ (A) arch lệch thực tế, KHÔNG kẹt luồng      → code bám arch đã khoá · DECISIONS `kỹ-thuật` + backlog đồng bộ doc wave sau
│      (tên field, kiểu dữ liệu, index…)
├─ (B) arch thiếu/sai KỸ THUẬT làm KẸT luồng   → `amend-arch`: bổ sung docs/arch/*.md tại chỗ, cùng commit với code
│      của AC đã khoá (thiếu cột/field/endpoint/    (6 điều kiện dưới)
│      mã lỗi mà AC/màn đã chốt cần)
└─ (C) THIẾU HẲN hành vi/luồng (không AC nào phủ) → không kẹt luồng: docs/ROADMAP.md §backlog (thiếu gì · FEAT · wave phát hiện), KHÔNG build
                                                 · kẹt luồng: STATE.md §Blocker → MAIN DỪNG, gợi ý Authority gọi `/document` top-up
```

**6 điều kiện `amend-arch`** (thiếu 1 = không phải amend-arch, quay về A hoặc C):
1. **Chỉ `docs/arch/*.md`** (§1 data model · §3 API · §5 events · §6 ca biên · `consumes`). AC · mockup · PRD · PERSONAS · DESIGN-SYSTEM **không** — đó là hợp đồng với Authority, đổi qua top-up.
2. **Truy ngược về AC/Mã màn đã khoá** mà nó phục vụ — không truy được = (C).
3. **Chỉ THÊM** (cột · field · endpoint · mã lỗi) — không đổi nghĩa/xoá thứ đã có; đụng surface wave trước đã giao → BACKWARD-COMPAT.
4. **Lan trong arch**: target consumer (`consumes`) cập nhật cùng commit.
5. **Ghi dấu**: 1 dòng `docs/DECISIONS.md` loại `amend-arch` (đổi gì ở arch §nào · phục vụ AC/Mã màn nào · vì sao kẹt luồng), cùng commit với code.
6. **QC kiểm ở VERIFY**: reviewer soi `git log -- docs/arch` của wave theo 5 điều trên (`review-<kind>` mục Lệch thứ đã chốt).

Ranh giới 1 câu: **AC · mockup · PRD · PERSONAS = hợp đồng với Authority → chỉ đổi qua top-up; `arch` = thiết kế kỹ thuật của SA → được BỔ SUNG tại chỗ khi kẹt luồng (amend-arch), additive + truy về AC + QC kiểm.**
`/next-wave` snapshot doc wave → `archive/wave-N/` → từ đó **bất biến**; đổi = FEAT version mới ở wave tương lai.

---

## §4 — Doc set (1 lớp `docs/`) + KG

Nguồn sự thật gom về `docs/` — KHÔNG còn 2 lớp business↔eng, KHÔNG còn chuỗi discovery→domain→architecture.

| File | Vai trò |
|---|---|
| `docs/PRD.md` | vấn đề · đối tượng · out-of-scope · success metric |
| `docs/INTERVIEW.md` | bằng chứng phỏng vấn (+ marker `NGUỒN: INTAKE` nếu đường intake) + **§Luồng nghiệp vụ đã xác nhận = "luồng nghiệp vụ"**: từng bước ai làm gì, bằng lời nghiệp vụ, Authority ký. Mọi chỗ nói "luồng nghiệp vụ" (build · verify · dogfood · test-writer) trỏ về đây, lọc theo wave qua màn/AC |
| `docs/PERSONAS.md` | persona + ma trận vai×hành động (nguồn phân quyền + TC âm) |
| `docs/CAPABILITIES-MAP.md` | capability→outcome→FEAT (truy vết) |
| `docs/TECHSTACK.md` | stack chốt + biến môi trường |
| `docs/feat/FEAT-*.md` | Khung PO (mục tiêu · phạm vi) + AC (BDD, gồm ca biên) + ràng buộc nghiệp vụ của BA — KHÔNG chứa chặn ở đâu/contract (SA ở `arch`) |
| `docs/arch/OVERVIEW.md` + `docs/arch/{name}.md` | **per target**: frontmatter `kind`(backend/web/bff/mobile/desktop)·`stack`·`consumes` + data model · luồng xử lý (kỹ thuật) · API · §ranh-giới (fold hld/api/data/events/integ). BUILD nạp đúng slice |
| `docs/CONVENTIONS.md` **(framework)** | quy ước chung + §API error-envelope/header **default** (project chỉnh nếu khác) — KHÔNG author lại |
| `docs/SECURITY.md` **(framework)** | baseline bảo mật — tick ở PRODUCTION-READY khi SHIP |
| `docs/DESIGN-SYSTEM.md` + `docs/ux/` | token (khoá trước, cả dự án) + SCREEN-MAP (mọi màn) + mockups HTML **dựng theo wave** (màn wave đang mở; wave sau `/document` top-up) |
| `docs/ROADMAP.md` | wave plan (target + phases mỗi wave) + §backlog (amendment) |
| `docs/DECISIONS.md` | 1 dòng/quyết định (append cả dự án, đánh dấu `(wave N)`) |
| `docs/BACKWARD-COMPAT.md` · `docs/PRODUCTION-READY.md` | sổ hợp đồng + checklist SHIP |
| `docs/adr/ADR-*.md` | quyết định kiến trúc (nhẹ) |
| `knowledge-base/{name}.md` | **KG** (per target): §Invariants · §Gotchas · §Failure-modes · §Key-decisions. KHÔNG phase-lock · sống sót qua mất code · MAIN đọc TRƯỚC khi code target |

> **Tracking wave-scoped** (không phải spec; `/next-wave` gom vào `archive/wave-N/`): `tracking/wave-{N}/test-cases.md`
> — MỘT bảng theo khung `templates/TEMPLATE.test-cases.md` (TC · loại · nguồn · AC · tag · mô tả · cách chạy · kết quả · thực tế / bằng chứng) — **`test-writer` thiết kế + chạy** (gộp registry + report + bug làm một, chống "3 bản sao"); TC `@regression` cộng dồn qua wave (chạy lại từ `archive/`).
>
> **Quy ước template** (gom ở **`templates/`** — xem `templates/README.md`; gate KHÔNG quét folder này): guidance trong `<!-- -->` (gate `read_live` strip → không đếm nhầm) ·
> placeholder `{{...}}` (gate check "còn `{{` = chưa xong") · tiêu đề `## §` = **mỏ neo cố định** (không đổi tuỳ tiện) ·
> bảng markdown sạch (ma trận/wave/enforcement — không ô trống ở bảng bắt buộc) · frontmatter máy-đọc (`status·capability·phases·consumes`).
>
> **Code** (`services/`, track trong git) chia nhóm theo `kind`: `services/boundaries/` (backend) · `services/web/` ·
> `services/bff/` · `services/mobile/` · `services/desktop/`. `kind` (khai ở frontmatter `arch/{name}.md`) quyết định: stack skill · nơi scaffold ·
> cách "chạy thật" (backend/bff/web `docker up` — web = nginx container · mobile emulator · desktop bản đóng gói `--smoke`) · review checklist. Bộ kind = **backend·web·bff·mobile·desktop** (desktop: Electron, Windows trước).

---

## §5 — Command (inline prompt, không build_prompt)
> 7 lệnh, prompt viết THẲNG trong `.claude/commands/<tên>.md` (không sinh động qua `build_prompt`). Spine:
> DOCUMENT → BUILD → VERIFY → [SHIP] → NEXT-WAVE (+ `/status`, `/dogfood` mọi lúc). Việc ĐẦU của mỗi lệnh = set
> `Phase hiện tại` ở STATE (gate/guard đọc dòng này). Chi tiết từng bước = chính file command; bảng tóm ở `CLAUDE.md`.

## §6 — Gate evidence (gate.py đọc gì mỗi phase)
> Danh sách gate cần dựng (thu từ thiết kế command):
> - **DOCUMENT**: doc set đủ mục · **bảng luồng nghiệp vụ Authority ký, không ô CHƯA HỎI** · **OVERVIEW §5 system design đủ 5.1–5.9, 5.7/5.8 có dòng** · challenge ≥3 câu PASS · ≥2 decisions · mọi ô STATE §Gate DOCUMENT đã tick (gồm PRE-LOCK AUDIT) · **mockup màn UI in-scope wave đầu đều có file** (`missing_wave_mockups` — chống khai màn trong SCREEN-MAP nhưng lười không vẽ .html) · **mọi thao tác/vùng dữ liệu trên mockup khai `data-api` có trong arch §3** (`mockup_api_gaps` — chống màn có nút Tải xuống mà không có API) · scope khoá (Authority duyệt)
> - **BUILD**: không còn ô VERIFY/SHIP đã tick (= sót wave trước) · wave ≥2: `archive/wave-(N-1)` tồn tại + đã commit · `wave_reviewed` (**wave ≥2**: ô `Rà lại` của wave N ở ROADMAP §1 đã điền ngày; **wave 1 miễn**) · **mockup màn UI in-scope wave đều có file** (`missing_wave_mockups` — chặn code chay theo màn không bản chốt; màn thuộc wave xác định bởi tag `(Wave N)` ô Mockup › FEAT › tên màn trong hàng ROADMAP — phủ cả wave làm mịn UI-only) · `mockup_api_gaps` như DOCUMENT · **backlog xếp wave này cần top-up đều `đã top-up`** (`pending_topup` — item `thiếu AC`/cần mockup không được code thẳng) · **`make check` qua `proof.json`** (`capture_proof.py` MÁY-sinh — gate KHÔNG tin tick tay, chống "test xanh nhờ H2"/"dev-done ≠ runnable") · **target phủ đủ wave**: mỗi target ROADMAP §1 cột Target khai có entry `healthy` trong `proof.json` (backend/bff/web: capture_proof đọc `docker compose ps` per-target · desktop: chạy `make doctor` bản đóng gói `--smoke`) — **thiếu/không-healthy target nào = đỏ** (chống "khai 2 làm 1, nhảy VERIFY"); mobile tick tay (emulator) · **proof chụp trên code đã commit, đúng commit mới nhất của `services/`** (sửa dở / đổi code sau lần chụp = đỏ)
> - **VERIFY**: `test-cases.md` — **mỗi AC in-scope có TC PASS** (tính từng cặp FEAT·AC) · không TC **FAIL / BLOCKED / CHƯA CHẠY** (kết quả trống = CHƯA CHẠY) · **AC in-scope không bị rút** so với bản chốt (khoá scope / đóng wave trước) trừ khi có dòng ROADMAP §2 · wave ≥2: mọi TC `@regression` của wave trước PASS (hoặc `ĐÃ THAY`) · `CHƯA CÓ QUY ĐỊNH` chỉ báo, không chặn · §Findings hết BLOCKER/MAJOR (đã xử = `fixed — <agent> xác nhận` hoặc `backlog`) · `fidelity.md` đủ mọi Mã màn in-scope + không LỆCH · **proof chụp lại sau vòng sửa** (đúng commit mới nhất) · dogfood xong (tick STATE) ·
>   Bằng chứng fidelity (web/mobile/desktop) = `tracking/wave-N/fidelity.md` — MAIN chép nguyên bảng của `persona-picky` (đo cấu trúc component vs mockup, không chỉ màu).
> - **SHIP** (gate đọc cột `phases` ROADMAP — wave **không khai SHIP** thì **skip**): PRODUCTION-READY đủ **cả mục (sau deploy)** (gate chạy sau deploy) · BACKWARD-COMPAT §3 xanh (wave ≥2) · deploy/smoke/rollback tick STATE
> - **NEXT-WAVE** (chấm SAU `next_wave.py --go`): `archive/wave-(N-1)` đã commit · ROADMAP §3 mọi item có cột Xử · wave mới đã stamp `Rà lại` (hết wave → teardown). Chốt TRƯỚC khi đóng nằm trong script: gate VERIFY (+ SHIP nếu khai) đỏ → từ chối, trừ `--accept-red=<DEC-id>` (Authority quyết, phần đỏ sang backlog wave kế).
> - **Tick tay, gate không đọc**: contract-test cho consumer · BACKWARD-COMPAT so `arch §API` · phase-lock MIỄN tick tiến-độ ROADMAP lúc BUILD (không phải đổi scope)
>
> **Kiến trúc gate.py** (1 file): shared readers `read/filled/read_live/count_rows/section/table_rows/challenge_count`
> + 1 hàm/phase `gate_document/build/verify/ship/next_wave` + `phase_from_state()` đọc `STATE.md`. In đạt/thiếu từng mục, exit 1 nếu thiếu — KHÔNG chặn tool.
## §7 — Agents (MAIN tự code; agent CHỈ để verification + dogfood)

MAIN viết **toàn bộ code sản phẩm**. Agent chỉ để **góc nhìn độc lập** (*fresh eyes* — review) + **dùng thử** (dogfood) — hai việc
hưởng lợi từ độc lập. MAIN **vẫn tự test** (BUILD: unit/integration + tự bấm thử · dogfood: đóng persona chính dùng trước) — đó là kiểm
của người làm, không phải nghiệm thu: ra đề + chạy + chấm `test-cases.md` là của `test-writer`. Spawn bằng **Task tool** + `subagent_type` + prompt NGẮN tay (KHÔNG `build_prompt`); phương pháp
nằm ở `.claude/agents/<name>.md`.

**Bộ agent (10):**
| Agent | Vai | Tools | Ghi được |
|---|---|---|---|
| `pre-mortem` | DOCUMENT (trước khoá scope): đối kháng SPEC — săn case Authority miss · mảng ngành thiếu · bảng chính sách (4 phép thử) | read-only (không Bash) | — (trả nghi vấn) |
| `reviewer` | code AN TOÀN + BẢO TRÌ (trục A an toàn: bảo mật/dữ liệu/forbidden · trục B bảo trì: structure/pattern/convention/naming) | read-only | — (trả finding) |
| `bug-hunter` | 2 chế độ: (1) code ĐÚNG SPEC (AC có impl? ca biên chặn server? phân quyền owner-condition?) · (2) RÀ ĐỀ TEST của `test-writer` trước khi chạy (VERIFY 3b) | read-only | — (trả finding) |
| `test-writer` | QA độc lập: viết đề black-box `test-cases.md` (AC + bảng chính sách + thăm dò ngoài tài liệu + regression) → **người duy nhất sửa đề** theo danh sách rà của `bug-hunter` → chạy. **KHÔNG viết code, kể cả test code** — script chạy TC là file tạm ngoài repo, dọn ngay | +Write/Edit **CHỈ `tracking/wave-N/test-cases.md`** | test-cases.md |
| `persona-{newbie,edge,picky,rushed,breaker,mobile}` | dogfood 2 đợt (đóng persona thật) | browse/Playwright | — (trả finding) |

**Luật chung mọi agent:** KHÔNG hỏi Authority · KHÔNG viết/sửa code (test-writer chỉ ghi `test-cases.md`) · **TRẢ VỀ finding,
MAIN ghi `STATE §Findings`** (chống hai agent đè file) · report `[BLOCKER/MAJOR/MINOR] + file:dòng + "hỏng thế nào" + đề xuất 1 câu` ·
nêu **hậu quả THẬT** (trục A: mất/lộ data · sai kết quả · chặn AC) **HOẶC chi phí bảo trì cụ thể** (trục B), "trục ổn" thì nói ổn, **đừng bịa finding**.

**Kind-specific:** 2 agent review generic, không tách per-kind — nạp `review-<kind>` (checklist + lệnh grep theo kind) + `stack-<tên>/SKILL.md §review` theo stack.
Mỗi `stack-<tên>` skill = idiom code · config · situational kafka/redis/logging/restclient (+ `ref-<kind>-*`)
+ **§review** = checklist + **bảng Forbidden patterns** (cho reviewer/bug-hunter soi từng dòng).
Luật riêng stack (Java/Spring…) ở stack skill, KHÔNG ở CONVENTIONS (cross-stack).

**Chất lượng bắt buộc (VERIFY = cổng chất lượng):** mỗi agent phải có **lệnh `grep` cụ thể** + thứ tự soi ưu tiên +
"**UI disable KHÔNG tính — phải server/DB**". KHÔNG checklist mơ hồ.
## §8 — Hooks (10 hook: 7 guard chặn · `guard_shell` + `trace_docsync` nhắc sau khi ghi · `reanchor` nhồi lại luật sau compact)
> - **guard_ask**: `AskUserQuestion` **chỉ dùng được ở DOCUMENT** (phỏng vấn + quyết định, trước khoá scope). Chặn ở BUILD/VERIFY/SHIP/NEXT-WAVE; **ô Scope khoá tick = chặn luôn** dù dòng phase còn ghi DOCUMENT. go/pivot/kill (NEXT-WAVE) hỏi bằng LỜI.
> - **guard_bc**: mọi lệnh `make … deploy` → buộc hỏi Authority; chặn khi PRODUCTION-READY (trừ mục *(sau deploy)*) hoặc BACKWARD-COMPAT §3 (wave ≥2) chưa xanh. · **guard_ds**: chặn ghi mockup/token lệch design-system.
> - **guard_shell** (PostToolUse — sau khi ghi): mockup có **app shell lệch `_shell.html` canonical** (nav items/thứ tự/nhóm/logo/user-menu/icon) — so khối `<!-- SHELL:START/END -->` của TRỌN file trên đĩa, chuẩn hoá `aria-current` → CẢNH BÁO cho model (exit 2, file vẫn ghi, KHÔNG undo) để tự sửa. Chống shell trôi mỗi màn một kiểu.
> - **guard_archive**: chặn Write/Edit vào `archive/**` (wave đã đóng = hợp đồng bất biến — §3/§5).
> - **guard_proof**: chặn Write/Edit vào `*proof.json` (bằng chứng runtime CHỈ `capture_proof.py` sinh — agent không giả tick).
> - **guard_makefile**: chặn Write/Edit vào **ROOT `Makefile`** (hợp đồng 6 lệnh, bất biến) — MAIN điền THÂN ở per-target `services/<nhóm>/<tên>/Makefile`, không sửa root lúc BUILD.
> - **guard_doc**: chặn Write/Edit vào **doc SPEC** (`docs/**` trừ DECISIONS/ROADMAP/BACKWARD-COMPAT/PRODUCTION-READY) khi phase ≠ DOCUMENT — doc đóng băng sau khoá scope, lệch/thiếu dồn `ROADMAP §backlog` → wave sau top-up. Sổ sống + DOCUMENT/top-up vẫn sửa được. **Ngoại lệ `amend-arch`**: `docs/arch/*.md` ở BUILD/VERIFY cho qua (điều kiện §3 — `trace_docsync` nhắc, reviewer kiểm).
> - **trace_docsync** (PostToolUse Write|Edit|MultiEdit): sửa spec doc ở DOCUMENT → nhắc CASCADE (đầu `/document`) + tự bỏ tick PRE-LOCK nếu đang tick. Trigger, không trace hộ → lời chốt LUÔN re-run audit. Sửa `docs/arch/*.md` ở BUILD/VERIFY → nhắc 6 điều kiện `amend-arch` (§3).
> - **reanchor**: SessionStart(compact) → nhồi lại §2 + STATE.
> Agent read-only (review/persona `disallowedTools: Write/Edit`) + `test-writer` chỉ ghi `tracking/wave-N/test-cases.md` → không cần hook giữ vùng ghi riêng.
## §9 — Failure modes (đã có cơ chế chặn)
> Kiểu hỏng gặp thật và chốt chặn tương ứng.

| Triệu chứng | Chặn bởi |
|---|---|
| Backlog trôi (phát sinh không ai định đoạt) | `/next-wave` dispose cột `Xử` + `gate_next_wave` |
| 2 agent đè file findings → mất | agent chỉ TRẢ finding, MAIN ghi `§Findings` |
| KG bay hơi (va gotcha lúc code, không ghi) | `/build` Bước 5 append `knowledge-base/{name}.md` |
| Kẹt chưa khoá (top-up doc mà không re-lock) | `/next-wave` 4.4 Authority duyệt lại = re-lock |
| Demo đẹp chạy xấu (UI khớp ảnh, cấu trúc sai) | `persona-picky` đo cấu trúc component vs mockup → `fidelity.md` |
| App shell trôi (mỗi mockup một kiểu sidebar/nav/icon) | `guard_shell` (so khối SHELL vs `_shell.html`) + ux-design §Nhất quán cross-màn |
| Point-edit lệch doc (sửa FEAT quên arch/API/mockup) | `trace_docsync` nhắc CASCADE + pre-lock audit (trace 6 chiều + UI↔AC) trước khoá scope |
| Tick PRE-LOCK ôi (audit xong rồi doc còn đổi tiếp, tick cũ thành bằng chứng giả) | `trace_docsync` TỰ BỎ TICK khi sửa spec doc sau tick + **lời chốt LUÔN chạy audit kể cả đang tick** (bịt tick chay + sửa ngoài tool hook không thấy) |
| Test xanh giả (pass nhờ H2/mock, không chạy thật) | `capture_proof.py` MÁY-sinh `proof.json` — gate không tin tick · proof ghi commit code, sửa sau lần chụp = đỏ |
| Chạy mù kế hoạch cũ | `wave_reviewed` + RÀ LẠI (loop engineering) |
| Agent giả tick proof | `guard_proof` chặn Write/Edit `*proof.json` |
| Hỏi lại Authority sau khoá scope | `guard_ask` (chặn AskUserQuestion khi Scope khoá đã tick / ngoài DOCUMENT) |
| Deploy khi hợp đồng vỡ | `guard_bc` (PRODUCTION-READY / BACKWARD-COMPAT §3 đỏ) · deploy luôn hỏi Authority |
| Ghi đè wave đã đóng | `guard_archive` chặn `archive/**` |
| Mockup hardcode màu (hex thô) | `guard_ds` (ngoài token :root) |
| Đóng wave khi VERIFY còn đỏ | `next_wave.py` chạy lại gate VERIFY (+ SHIP) — đỏ thì từ chối, trừ `--accept-red=<DEC-id>` (Authority quyết, phần đỏ sang backlog) |
| Finding nặng lọt gate (lệch nhãn mức độ) | mọi agent chung nhãn BLOCKER/MAJOR/MINOR · gate chỉ coi đã xử khi `fixed — <agent> xác nhận` / `backlog` |

## §10 — Quản lý context (van an toàn cho MAIN-code-hết)
> - **reanchor** — hook `SessionStart(compact)`: sau compact, đọc lại PROTOCOL §2 + STATE → inject. BẮT BUỘC.
> - **compact.py** — report CHỈ-ĐỌC doc phình (DECISIONS/ROADMAP backlog), gấp tay sang `archive/ledger/`, KHÔNG `--go`. STATE wave-scoped, không phình theo thời gian. Chạy ở next-wave.
> - **FEAT-cap per wave** — xem §1.
