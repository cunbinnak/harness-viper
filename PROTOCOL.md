# PROTOCOL — {{PROJECT_NAME}}

> Định nghĩa CHUẨN của quy trình. [STATE.md](STATE.md) là bản thao tác; lệch nhau thì **PROTOCOL.md thắng**.
> Router ngắn mỗi phiên: `CLAUDE.md`.
>
> **Trạng thái: HOÀN THIỆN — khung đã dựng, selftest xanh** (7 command · gate.py · 9 agent · hooks · skill library).
> Bộ khung này là bản refactor tinh gọn (1 lớp doc · MAIN tự code · inline prompt
> · ít script + gate nhìn thấy được), thay cho harness cũ (17 state · ~58 gate · build_prompt · 2 lớp doc).

---

## §0 — Hai đường vào (entry paths)

Nhận diện bằng đúng một dấu hiệu: `docs/INTERVIEW.md` có marker `NGUỒN: INTAKE` (ngoài comment) hay không.

| | **Đường INTERVIEW** | **Đường INTAKE** |
|---|---|---|
| Khi nào | Ý tưởng mới, chưa có tài liệu phân tích (greenfield, project nhỏ) | Đã có tài liệu MESH-render/phân tích sẵn ở `intake/` |
| MAIN làm | **Phỏng vấn Authority** → `docs/INTERVIEW.md` đủ dòng bằng chứng → suy ra PRD/personas/… | **Dịch/render** `intake/*.md` vào doc set + bảng truy vết + marker `NGUỒN: INTAKE` — KHÔNG phỏng vấn lại |
| Cỡ | nhỏ: 1 app, 3–7 AC, 2–3 persona | không trần: multi-boundary, AC truy về `CAPABILITIES-MAP.md` |

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
| **BUILD** | challenge → đọc KG → scaffold → walking skeleton → luồng lõi → **chạy thật (docker up)** | **MAIN tự code** | KHÔNG — tự quyết → DECISIONS.md | skeleton thông · make check xanh · đã commit · health 200 |
| **VERIFY** | 3 bước: **code review** (2 vai) + **`test-writer` thiết kế/chạy black-box test-case** + **dogfood** (6 persona 2 đợt) | MAIN + reviewer/bug-hunter/test-writer + 6 persona | KHÔNG | make test xanh · test-cases PASS · dogfood xong · hết finding BLOCKER/MAJOR |
| **SHIP** | prod-ready → deploy → smoke → rollback thử → dogfood prod | MAIN | KHÔNG (deploy = ngoại lệ "hỏi thật") | chỉ chạy khi wave khai SHIP; prod sống · rollback thử |
| **NEXT-WAVE** | go/pivot/kill → snapshot archive → mở wave kế (không reset) | MAIN | (go/pivot/kill) | backlog gộp · snapshot · wave kế mở hoặc teardown |

**Wave**: DOCUMENT chạy 1 lần cho cả dự án (sinh kế hoạch mọi wave). BUILD/VERIFY/SHIP chạy **per wave**.
Mỗi wave **khai báo phases nó chạy** trong `docs/ROADMAP.md` — wave nội bộ có thể bỏ SHIP; không ép mọi wave đủ phase.
**FEAT-cap per wave**: DOCUMENT chia wave giới hạn **~3-4 FEAT/wave** 
context của MAIN (MAIN-code-hết, không dev-agent). Ngưỡng mềm, gate wave-plan cảnh báo khi vượt.

**Loop engineering** (mở wave = RÀ LẠI): kế hoạch mọi wave lập 1 lần ở DOCUMENT (Authority ký 1 lần),
NHƯNG mở wave nào `/next-wave` phải **rà lại kế hoạch wave đó đối chiếu KẾT QUẢ wave trước + §backlog**, chỉnh nếu
lệch, rồi stamp `Rà lại wave N: <ngày>`. Gate `wave_reviewed` đòi dòng đó (ngày ≥ lúc mở wave) — thiếu = đang chạy
mù theo kế hoạch cũ đã lệch. ROADMAP mỗi wave khai thêm: `phụ thuộc wave trước` · `legacy được phép phá`
(nối BACKWARD-COMPAT/guard_bc) · `điều chỉnh khi mở`. **RÀ LẠI định đoạt RÕ từng backlog/finding treo** (xử/hoãn-lý-do/bỏ-lý-do —
không để trôi, vá retro D1); go/pivot/kill so **ngưỡng ghi trước** (không sửa sau khi nhìn số).

---

## §2 — Luật nền

1. **Scope khoá sau DOCUMENT.** Phát sinh → `docs/ROADMAP.md §backlog`, không chèn vào wave này.
2. **Sau khi khoá scope: toàn quyền, không hỏi lại.** `AskUserQuestion` **chỉ ở DOCUMENT** (trước khoá scope — phỏng vấn/quyết định); BUILD/VERIFY/SHIP/NEXT-WAVE bị `guard_ask` chặn (ô Scope khoá tick = chốt, chặn luôn dù phase còn ghi DOCUMENT). Ngoại lệ ra-ngoài/không-đảo-ngược: hỏi bằng lời.
3. **Mơ hồ → 1 dòng `docs/DECISIONS.md` (cột giả định + đảo-ngược-được-không) TRƯỚC khi code.**
4. **Doc là nguồn sự thật — ĐÓNG BĂNG sau khoá scope.** Code lệch doc (trong AC đã khoá) → **KHÔNG sửa doc spec lúc BUILD** (guard_doc chặn); ghi `ROADMAP §backlog` → wave sau `/document` top-up đồng bộ. Mơ hồ → `DECISIONS.md` (sổ sống, được ghi). Giữ hợp đồng ổn định để review/dogfood đánh, tránh "vừa code vừa vặn doc".
5. **Cỡ sản phẩm theo đường vào** (§0).
6. **Không secret trong code, không bypass test/lint. Đã code xong → git commit** (không commit = coi như chưa làm).
7. **Tiếng Việt có dấu** cho văn bản người đọc (giữ tiếng Anh cho identifier/API/schema/tên lệnh/tên file).
8. **Im lặng với Authority, đối kháng nội bộ.** Challenge trước khi code + dogfood trước khi báo xong. Dogfood = **trình duyệt thật** (skill `browse`) — **curl không tính** (trừ target `KHÔNG CÓ UI`); MAIN tự dùng trước rồi mới spawn persona.
9. **Dọn rác tạm.** Artifact tạm (screenshot/trace/log/temp phân tích) dùng xong **dọn ngay** — không commit, không tích tụ, để scratch dir. Build artifact (node_modules/target/dist…) trong `.gitignore`. Docker/seed → teardown ở `/next-wave`.

---

## §3 — Amendment = wave sau (sửa doc sau khi đã chốt)

Chỉ doc của wave **ĐÃ SHIP** mới đóng băng (nằm trong `archive/`). Doc wave **đang mở** vẫn sửa được — nhưng
chỉ để đúng sự thật *trong scope đã khoá*, KHÔNG thêm scope. Khi đang BUILD/VERIFY mà phát hiện vấn đề:

```
├─ Code sai so với spec đã chốt              → sửa CODE. Xong. (không đụng doc)
├─ Spec mơ hồ (không nói rõ ca này)          → DECISIONS.md 1 dòng, tự quyết, đi tiếp. KHÔNG hỏi
├─ Doc wave HIỆN TẠI lệch thực tế, vẫn trong
│  AC đã khoá (đổi tên field, thêm chi tiết
│  kỹ thuật của AC đang làm)                 → sửa DOC cùng commit (doc wave đang mở CHƯA đóng băng)
├─ THIẾU HẲN luồng / scope MỚI (ngoài AC khoá) → docs/ROADMAP.md §backlog (thiếu gì · đụng FEAT nào ·
│                                              wave phát hiện) → KHÔNG build → wave sau top-up
└─ Luồng thiếu CHẶN CỨNG luồng lõi wave này   → STATE.md §Blocker, báo cuối buổi; buộc phải có →
                                               back-edge DOCUMENT top-up cho wave này (hiếm — DOCUMENT hụt)
```

Ranh giới 1 câu: **sửa cho doc khớp thực tế trong AC đã khoá = OK tại chỗ; thêm AC/luồng mới = backlog → wave sau.**
`/next-wave` snapshot doc wave → `archive/wave-N/` → từ đó **bất biến**; đổi = FEAT version mới ở wave tương lai.

---

## §4 — Doc set (1 lớp `docs/`) + KG

Nguồn sự thật gom về `docs/` — KHÔNG còn 2 lớp business↔eng, KHÔNG còn chuỗi discovery→domain→architecture.

| File | Vai trò |
|---|---|
| `docs/PRD.md` | vấn đề · đối tượng · out-of-scope · success metric |
| `docs/INTERVIEW.md` | bằng chứng phỏng vấn (+ marker `NGUỒN: INTAKE` nếu đường intake) |
| `docs/PERSONAS.md` | persona + ma trận vai×hành động (nguồn phân quyền + TC âm) |
| `docs/CAPABILITIES-MAP.md` | capability→outcome→FEAT (truy vết) |
| `docs/TECHSTACK.md` | stack chốt + biến môi trường |
| `docs/feat/FEAT-*.md` | AC (BDD, gồm ca biên hành vi + hệ thống) + field kỹ thuật CHUNG file (bỏ translate) |
| `docs/arch/OVERVIEW.md` + `docs/arch/{name}.md` | **per target**: frontmatter `kind`(backend/web/bff/mobile)·`stack`·`consumes` + data model · luồng · API · §ranh-giới (fold hld/api/data/events/integ). BUILD nạp đúng slice |
| `docs/CONVENTIONS.md` **(framework)** | quy ước chung + §API error-envelope/header **default** (project chỉnh nếu khác) — KHÔNG author lại |
| `docs/SECURITY.md` **(framework)** | baseline bảo mật — tick ở PRODUCTION-READY khi SHIP |
| `docs/DESIGN-SYSTEM.md` + `docs/ux/` | token (khoá trước, cả dự án) + SCREEN-MAP (mọi màn) + mockups HTML **dựng theo wave** (màn wave đang mở; wave sau `/document` top-up) |
| `docs/ROADMAP.md` | wave plan (target + phases mỗi wave) + §backlog (amendment) |
| `docs/DECISIONS.md` | 1 dòng/quyết định (append cả dự án, đánh dấu `(wave N)`) |
| `docs/BACKWARD-COMPAT.md` · `docs/PRODUCTION-READY.md` | sổ hợp đồng + checklist SHIP |
| `docs/adr/ADR-*.md` | quyết định kiến trúc (nhẹ) |
| `knowledge-base/{name}.md` | **KG** (per target): §Invariants · §Gotchas · §Failure-modes · §Key-decisions. KHÔNG phase-lock · sống sót qua mất code · MAIN đọc TRƯỚC khi code target |

> **Tracking wave-scoped** (không phải spec; `/next-wave` gom vào `archive/wave-N/`): `tracking/wave-{N}/test-cases.md`
> — MỘT bảng = TC · **loại** · AC · cách chạy · kết quả PASS/FAIL · nguyên nhân — **`test-writer` thiết kế + chạy** (gộp registry + report + bug làm một, chống "3 bản sao").
>
> **Quy ước template** (gom ở **`templates/`** — xem `templates/README.md`; gate KHÔNG quét folder này): guidance trong `<!-- -->` (gate `read_live` strip → không đếm nhầm) ·
> placeholder `{{...}}` (gate check "còn `{{` = chưa xong") · tiêu đề `## §` = **mỏ neo cố định** (không đổi tuỳ tiện) ·
> bảng markdown sạch (ma trận/wave/enforcement — không ô trống ở bảng bắt buộc) · frontmatter máy-đọc (`status·capability·phases·consumes`).
>
> **Code** (`services/`, gitignored ở repo khung) chia nhóm theo `kind`: `services/boundaries/` (backend) · `services/web/` ·
> `services/bff/` · `services/mobile/`. `kind` (khai ở frontmatter `arch/{name}.md`) quyết định: stack skill · nơi scaffold ·
> cách "chạy thật" (backend/bff/web `docker up` — web = nginx container · mobile emulator) · review checklist. Bộ kind = **backend·web·bff·mobile**.

---

## §5 — Command (inline prompt, không build_prompt)
> 7 lệnh, prompt viết THẲNG trong `.claude/commands/<tên>.md` (không sinh động qua `build_prompt`). Spine:
> DOCUMENT → BUILD → VERIFY → [SHIP] → NEXT-WAVE (+ `/status`, `/dogfood` mọi lúc). Việc ĐẦU của mỗi lệnh = set
> `Phase hiện tại` ở STATE (gate/guard đọc dòng này). Chi tiết từng bước = chính file command; bảng tóm ở `CLAUDE.md`.

## §6 — Gate evidence (gate.py đọc gì mỗi phase)
> Danh sách gate cần dựng (thu từ thiết kế command):
> - **DOCUMENT**: doc set đủ mục · challenge PASS · ≥2 decisions · scope khoá (Authority duyệt)
> - **BUILD**: `wave_reviewed` (**wave ≥2**: ROADMAP có `Rà lại wave N` ngày ≥ lúc mở; **wave 1 miễn**) · **`make check` qua `proof.json`** (`capture_proof.py` MÁY-sinh — gate KHÔNG tin tick tay, chống "test xanh nhờ H2"/"dev-done ≠ runnable") · **target phủ đủ wave**: mỗi target ROADMAP §1 cột Target khai (kind container hoá: backend/bff/web) có entry `healthy` trong `proof.json` (capture_proof đọc `docker compose ps` per-target) — **thiếu/không-healthy target nào = đỏ** (chống "khai 2 làm 1, nhảy VERIFY"); mobile tick tay (emulator) · **đã commit**
> - **VERIFY**: `test-cases.md` mọi AC **PASS** + không **FAIL** · §Findings hết BLOCKER/MAJOR · dogfood xong ·
>   **(web/mobile) BACKSTOP fidelity**: đòi bằng chứng dogfood `picky` đã screenshot-diff **cấu trúc** vs mockup (không skip — chống E1 "demo đẹp chạy xấu"). Format bằng chứng: `persona-picky` §E1 (BACKSTOP screenshot-diff cấu trúc component).
> - **SHIP** (gate đọc ROADMAP `phases` — wave **không khai SHIP** thì **skip** cả nhóm — G3): prod-ready 4 nhóm · BC §3 xanh · rollback thử
> - **Cross**: contract-test present cho consumer · BACKWARD-COMPAT so `arch §API` (G4) · **phase-lock MIỄN tick tiến-độ ROADMAP lúc BUILD** (E, không phải đổi scope)
>
> **Kiến trúc gate.py** (1 file): shared readers `read/filled/read_live/count_rows/section/table_cells/challenge_last`
> + 1 hàm/phase `gate_document/build/verify/ship/next_wave` + `phase_from_state()` đọc `STATE.md`. In đạt/thiếu từng mục, exit 1 nếu thiếu — KHÔNG chặn tool.
## §7 — Agents (MAIN tự code; agent CHỈ để verification + dogfood)

MAIN viết **toàn bộ code sản phẩm**. Agent chỉ để **góc nhìn độc lập** (*fresh eyes* — review) + **dùng thử** (dogfood) — hai việc
hưởng lợi từ độc lập. Spawn bằng **Task tool** + `subagent_type` + prompt NGẮN tay (KHÔNG `build_prompt`); phương pháp
nằm ở `.claude/agents/<name>.md`.

**Bộ agent (9):**
| Agent | Vai | Tools | Ghi được |
|---|---|---|---|
| `reviewer` | code AN TOÀN + BẢO TRÌ (trục A an toàn: bảo mật/dữ liệu/forbidden · trục B bảo trì: structure/pattern/convention/naming) | read-only | — (trả finding) |
| `bug-hunter` | code ĐÚNG SPEC (AC có impl? ca biên chặn server? phân quyền owner-condition?) | read-only | — (trả finding) |
| `test-writer` | QA độc lập: thiết kế + chạy black-box `test-cases.md` (từ AC) + test adversarial | +Write/Edit **test/ + tracking/wave-N/test-cases.md** | test/ · test-cases.md |
| `persona-{newbie,edge,picky,rushed,breaker,mobile}` | dogfood 2 đợt (đóng persona thật) | browse/Playwright | — (trả finding) |

**Luật chung mọi agent:** KHÔNG hỏi Authority · KHÔNG sửa product code (trừ test-writer chỉ `test/`) · **TRẢ VỀ finding,
MAIN ghi `STATE §Findings`** (chống retro B1 hai agent đè file) · report `[nặng/vừa/nhẹ] + file:dòng + "hỏng thế nào" + đề xuất 1 câu` ·
nêu **hậu quả THẬT** (trục A: mất/lộ data · sai kết quả · chặn AC) **HOẶC chi phí bảo trì cụ thể** (trục B), "trục ổn" thì nói ổn, **đừng bịa finding**.

**Kind-specific:** review agent đọc `stack-<tên>/SKILL.md §review` theo kind — 2 agent generic, không tách per-kind.
Mỗi `stack-<tên>` skill = **PORT** rules-<kind> + ref-<kind>-* cũ (idiom code · config · situational kafka/redis/logging/restclient)
+ **§review** = checklist + **bảng Forbidden patterns** (cho reviewer/bug-hunter soi từng dòng). **Giữ nguyên content, chỉ dời nhà** —
Java/Spring-specific KHÔNG mất, chỉ rời khỏi CONVENTIONS (cross-stack) sang đúng stack skill.

**Chất lượng bắt buộc (VERIFY = cổng chất lượng):** mỗi agent phải có **lệnh `grep` cụ thể** + thứ tự soi ưu tiên +
"**UI disable KHÔNG tính — phải server/DB**". KHÔNG checklist mơ hồ.
## §8 — Hooks (guard_ask / guard_bc / guard_ds + **reanchor**: nhồi lại luật sau compact)
> - **guard_ask**: `AskUserQuestion` **chỉ dùng được ở DOCUMENT** (phỏng vấn + quyết định, trước khoá scope). Chặn ở BUILD/VERIFY/SHIP/NEXT-WAVE; **ô Scope khoá tick = chặn luôn** dù dòng phase còn ghi DOCUMENT. go/pivot/kill (NEXT-WAVE) hỏi bằng LỜI.
> - **guard_bc**: chặn deploy khi BACKWARD-COMPAT §3 chưa xanh (wave ≥2). · **guard_ds**: chặn ghi mockup/token lệch design-system.
> - **guard_shell**: chặn ghi mockup có **app shell lệch `_shell.html` canonical** (nav items/thứ tự/nhóm/logo/user-menu/icon) — so khối `<!-- SHELL:START/END -->`, chuẩn hoá `aria-current`. Chặn chắc ở Write; Edit chạm khối = báo mềm. Chống shell trôi mỗi màn một kiểu.
> - **guard_archive**: chặn Write/Edit vào `archive/**` (wave đã đóng = hợp đồng bất biến — §3/§5).
> - **guard_proof**: chặn Write/Edit vào `*proof.json` (bằng chứng runtime CHỈ `capture_proof.py` sinh — agent không giả tick).
> - **guard_makefile**: chặn Write/Edit vào **ROOT `Makefile`** (hợp đồng 6 lệnh, bất biến) — MAIN điền THÂN ở per-target `services/<nhóm>/<tên>/Makefile`, không sửa root lúc BUILD.
> - **guard_doc**: chặn Write/Edit vào **doc SPEC** (`docs/**` trừ DECISIONS/ROADMAP/BACKWARD-COMPAT/PRODUCTION-READY) khi phase ≠ DOCUMENT — doc đóng băng sau khoá scope, lệch/thiếu dồn `ROADMAP §backlog` → wave sau top-up. Sổ sống + DOCUMENT/top-up vẫn sửa được.
> - **trace_docsync** (PostToolUse Edit|MultiEdit): sửa spec doc (`docs/feat|arch|ux/**` · PRD/PERSONAS/CAPABILITIES/DESIGN-SYSTEM) ở pha **DOCUMENT** (scope chưa khoá) → **nhắc CASCADE** (propagate FEAT↔arch data model↔§3 API↔mockup) + **re-run trace 5 chiều + UI↔AC** + **TỰ BỎ TICK ô `PRE-LOCK AUDIT PASS`** nếu đang tick (audit chấm trên bản cũ = tick ôi; re-run xong mới tick lại). Là **TRIGGER nhắc + vô hiệu tick cơ học**, KHÔNG trace hộ (việc ngữ nghĩa của LLM/pre-lock audit). exit 2 đưa nhắc lại model, không undo.
> - **reanchor**: SessionStart(compact) → nhồi lại §2 + STATE.
> Agent read-only (review/persona `disallowedTools: Write/Edit`) + `test-writer` chỉ `test/` → không cần hook owned_paths/kernel-protect như harness cũ.
## §9 — Failure modes (đã có cơ chế chặn)
> Kiểu hỏng gặp thật (retro) và chốt chặn tương ứng — mã trong ngoặc = ref rải rác trong doc.

| Triệu chứng | Chặn bởi |
|---|---|
| Backlog trôi (phát sinh không ai định đoạt) | `/next-wave` dispose cột `Xử` + `gate_next_wave` (D1) |
| 2 agent đè file findings → mất | agent chỉ TRẢ finding, MAIN ghi `§Findings` (B1) |
| KG bay hơi (va gotcha lúc code, không ghi) | `/build` Bước 5 append `knowledge-base/{name}.md` (B3) |
| Kẹt DRAFT (top-up doc mà không re-lock) | `/next-wave` 4.4 Authority duyệt lại = re-lock (F1) |
| Demo đẹp chạy xấu (UI khớp ảnh, cấu trúc sai) | `persona-picky` BACKSTOP screenshot-diff (E1) |
| App shell trôi (mỗi mockup một kiểu sidebar/nav/icon) | `guard_shell` (so khối SHELL vs `_shell.html`) + ux-design §Nhất quán cross-màn |
| Point-edit lệch doc (sửa FEAT quên arch/API/mockup) | `trace_docsync` nhắc CASCADE + pre-lock audit (trace 5 chiều + UI↔AC) trước khoá scope |
| Tick PRE-LOCK ôi (audit xong rồi doc còn đổi tiếp, tick cũ thành bằng chứng giả) | `trace_docsync` TỰ BỎ TICK khi sửa spec doc sau tick + **lời chốt LUÔN chạy audit kể cả đang tick** (bịt tick chay + sửa ngoài tool hook không thấy) |
| Test xanh giả (pass nhờ H2/mock, không chạy thật) | `capture_proof.py` MÁY-sinh `proof.json` — gate không tin tick |
| Chạy mù kế hoạch cũ | `wave_reviewed` + RÀ LẠI (loop engineering) |
| Agent giả tick proof | `guard_proof` chặn Write/Edit `*proof.json` |
| Hỏi lại Authority sau khoá scope | `guard_ask` (chặn AskUserQuestion khi Scope khoá đã tick / ngoài DOCUMENT) |
| Deploy khi hợp đồng vỡ | `guard_bc` (BACKWARD-COMPAT §3 đỏ, G4) |
| Ghi đè wave đã đóng | `guard_archive` chặn `archive/**` |
| Mockup hardcode màu (hex thô) | `guard_ds` (ngoài token :root) |

## §10 — Quản lý context (van an toàn cho MAIN-code-hết)
> - **reanchor** — hook `SessionStart(compact)`: sau compact, đọc lại PROTOCOL §2 + STATE → inject. BẮT BUỘC.
> - **compact.py** — report CHỈ-ĐỌC doc phình (DECISIONS/ROADMAP backlog), gấp tay sang `archive/ledger/`, KHÔNG `--go`. STATE wave-scoped, không phình theo thời gian. Chạy ở next-wave.
> - **FEAT-cap per wave** — xem §1.
