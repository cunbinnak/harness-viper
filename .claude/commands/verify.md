---
description: VERIFY — code review (2 vai) → test case (test-writer viết đề → bug-hunter rà đề → test-writer sửa đề + chạy) → dogfood 6 persona → vòng sửa (MAIN sửa, agent tìm lại) → kết luận QC
---
# /verify [<wave>] — Phase VERIFY

> Kiểm trên hệ **ĐANG CHẠY** (BUILD đã đưa hệ chạy thật theo `kind`). Agent (review + persona) **CHỈ trả finding — MAIN sửa**.
> **Kỷ luật spawn** (mọi Bước dưới): spawn bằng **tool Agent + prompt ngắn viết tay**. **Mọi spawn truyền `run_in_background: false`** (công cụ Agent mặc định chạy nền; các bước ăn chung 1 hệ + 1 DB nên chạy chồng là đè trạng thái nhau). Đứng chờ nghĩa là lượt của MAIN dừng tới khi agent trả kết quả; hook `guard_agent` chặn spawn không truyền `false`. Ranh giới cấm là **PRODUCT code — chỉ MAIN viết/sửa** (không phải "cấm viết mọi thứ"). Phân vai ghi/đọc:
> · `reviewer` · `bug-hunter` · `persona-*` → **READ-ONLY** — chỉ đọc, trả finding, không viết gì (frontmatter không cấp `Write`/`Edit`; còn `Bash` để chạy lệnh kiểm — KHÔNG dùng để ghi file).
> · `test-writer` → **QA độc lập, chỉ ghi `tracking/wave-N/test-cases.md`** — **KHÔNG viết code, kể cả test code**; script cần để chạy TC (Playwright `.mjs` · k6) là file tạm ngoài repo, dọn ngay.
> Mọi agent thấy product code sai → **TRẢ finding**, MAIN sửa (**góc nhìn độc lập** — *fresh eyes*: người kiểm không phải người viết, nên MAIN không tự-chấm-bài-mình). *Không tự chấm* ≠ *không được test*: MAIN vẫn tự dùng (dogfood — đóng persona chính, Bước 4) — chỉ là kết quả nghiệm thu `test-cases.md` do `test-writer` ra đề + chạy + chấm.
> **THU ĐỦ → SỬA SAU**: finding từ Bước 2/3/4 chỉ **GOM** vào `STATE §Findings` — MAIN **CẤM đụng product code trước Bước 5**. Sửa sớm = phá snapshot mà test-writer/dogfood đang đo trên đó → finding các nguồn không map được nhau + rebuild lắt nhắt nhiều lượt thay vì 1 lượt batch.
> **Không dừng hỏi Authority, kể cả bằng lời** (PROTOCOL §2.2 — chỉ dừng ở Bước cuối báo kết quả): chỗ chưa rõ → bảng §2.3 cột "Sau khoá scope" · ngoài scope → `ROADMAP §backlog` · chặn cứng → `STATE §Blocker`. Bước kế bắt buộc (dogfood, re-run, re-review) thì **LÀM**, không mời Authority quyết.

**Việc ĐẦU TIÊN**: sửa `STATE.md` → `Phase hiện tại: VERIFY`.

## Bước 1 — Nạp + xác nhận hệ đang chạy
- `docs/ROADMAP.md` wave-N (AC in-scope) + `docs/feat/FEAT-*` (AC + ca biên) + `docs/CONVENTIONS.md §API` + `arch/{name}.md` (**`kind`** + §API)
- File nào vừa Read còn **tươi trong context** (chưa qua compact) → **KHÔNG Read lại** — chỉ nạp phần thiếu/đã cũ (nạp đúp = phí context, không thêm thông tin)
- Hệ chạy thật (từ BUILD), theo `kind`: backend/bff/web → `docker ps` + health 200 (web = nginx container) · mobile → emulator · desktop → app đã đóng gói đang mở với `--remote-debugging-port=9222` (skill `browse` §7). Chưa chạy → đưa lên trước.

## Bước 2 — Code review (2 vai góc-nhìn-độc-lập, checklist đúng `kind` — KHÔNG sửa)
Spawn 2 agent **cùng 1 message (song song), foreground**, **chỉ đọc code, trả finding** — hai vai soi hai câu hỏi KHÁC nhau:
> **Cả 2 agent nạp thêm skill `review-<kind>`** (review-backend/web/bff/mobile/desktop — checklist review theo `kind` của target đang review) BÊN CẠNH `stack-<x> §review`.
> **Phạm vi soi**: wave 1 soi cả target. Wave ≥2 chỉ soi phần code đổi từ lúc đóng wave trước (mốc: `git log -1 --format=%H -- archive/wave-<N-1>`) cộng chỗ cũ mà phần đổi gọi tới. Lượt re-review ở Bước 5 soi diff từ commit của lượt trước; MAIN ghi mốc vào prompt.

**`reviewer` — code có AN TOÀN chạy + BẢO TRÌ được không?** (senior/team-lead, **2 trục** — chi tiết `.claude/agents/reviewer.md`)
- **Trục A · An toàn/đúng** (hỏng = hại NGAY → BLOCKER/MAJOR): bảo mật (secret · validate **server** · SQL nối chuỗi · lộ entity/lỗi nội bộ) · phân quyền dữ liệu (id kèm owner/tenant) · **forbidden patterns** stack · toàn vẹn transaction · lệch `DECISIONS`/`arch`/`TECHSTACK` đã chốt (stack/version khớp mức TECHSTACK khai).
- **Trục B · Bảo trì/nhất quán** (vẫn chạy nhưng đắt MAI SAU → MAJOR/MINOR, **không chặn**): cấu trúc khớp **kiến trúc đã chốt** (`arch §4` — Layered/DDD, không trộn) · convert DTO map tay nhiều → MapStruct · logic đúng tầng · naming khớp Glossary · **chất lượng test**. Chỉ báo khi nêu **chi phí bảo trì cụ thể**; style tùy-ca (`var`…) **mặc định tha**.

**`bug-hunter` — code có LÀM ĐÚNG như DOC không?** (đối chiếu spec, soi theo thứ tự)
1. Mỗi AC in-scope → tìm code hiện thực: **có tồn tại? đúng mô tả? hay chỉ nửa vời?**
2. Mỗi ca biên trong AC → tìm chỗ code chặn. **Chặn ở UI (disable nút) KHÔNG TÍNH — phải ràng buộc DB hoặc kiểm ở server.**
3. Phân quyền: **mọi truy vấn lấy bản ghi theo id có kèm điều kiện chủ sở hữu không?** (lỗ hay gặp + nặng nhất)
4. Việc dở (TODO/FIXME) chặn AC · lỗi bị nuốt (`catch{}` rỗng) · secret hardcode

**Cả hai** → `STATE.md §Findings`, format `[BLOCKER/MAJOR/MINOR] (+trục A|B nếu reviewer) + file:dòng + "hỏng/tốn thế nào" + đề xuất 1 câu`. **1 dòng = 1 vấn đề** — agent trả finding gộp nhiều vế → MAIN **TÁCH** thành nhiều dòng khi ghi (dòng gộp = fix 1 vế rồi tick cả dòng, vế còn lại chết chìm).
- **Trục A · bug-hunter**: chỉ nêu **hậu quả THẬT** (mất/lộ dữ liệu · sai kết quả · chặn AC).
- **Trục B**: nêu **chi phí bảo trì CỤ THỂ** — **vẫn cấm** khẩu vị thuần (tên đẹp không lý do · abstraction "để sau" · perf chưa đo · coverage%) + style tùy-ca **tha**.
- **"Trục nào ổn → nói ổn, đừng bịa finding."** Lệnh `grep` cụ thể ở `.claude/agents/reviewer.md` · `bug-hunter.md`.
- **Wave ≥ 2 — `reviewer` ghi thêm mục `Chức năng cũ bị chạm`** (nghiệp vụ, không tên file; mỗi dòng xếp loại `A` code chỉ đi qua luồng cũ / `B` code sửa logic mà AC cũ dựa vào; chi tiết `reviewer.md`; lượt re-review ở Bước 5 ghi lại mục này cho diff của lượt sửa): MAIN **chuyển NGUYÊN VĂN** mục này cho `test-writer` ở 3a và cho `bug-hunter` ở 3b, không tự thêm hay bớt — QC không đọc code nên đây là tín hiệu độc lập về phụ thuộc ngầm trong code.
Học được điều mới về target → append `knowledge-base/{name}.md`.

> **MAIN chưa sửa gì.** Chờ cả hai agent trả finding → tổng hợp vào `STATE §Findings` → sang Bước 3. Sửa tập trung ở Bước 5 sau khi thu đủ finding từ tất cả góc.

## Bước 3 — Test case black-box: VIẾT ĐỀ → RÀ ĐỀ → CHẠY
> Thứ tự cố định — **đề phải được rà TRƯỚC khi chạy** (chạy trên đề thiếu = PASS giả về độ phủ). 3 lần spawn, foreground, lần lượt: `test-writer` (thiết kế) → `bug-hunter` (rà đề) → `test-writer` (chạy).
> **MAIN KHÔNG tự ra đề** (người code không tự-chấm-bài-mình) — MAIN chỉ SỬA ở Bước 5. Phương pháp: `specialist-testing` (`test-writer` LUÔN nạp).

### 3a — VIẾT ĐỀ (`test-writer` chế độ THIẾT KẾ — CHƯA chạy)
Điền `tracking/wave-N/test-cases.md` theo khung `templates/TEMPLATE.test-cases.md` (`TC | loại | nguồn | AC | tag | mô tả | cách chạy | kết quả | thực tế / bằng chứng`), mọi dòng `kết quả` = `CHƯA CHẠY`.
**Ba nguồn**: AC (+ ca biên · ô `cấm` · `arch §6`) · **bảng chính sách** từng hành động (INTERVIEW — có ngưỡng → giá trị biên) · **thăm dò ngoài tài liệu** (lên SẴN dòng nguồn `TD` — 4 phép thử ở chỗ bảng chính sách im lặng). Áp **kỹ thuật** (phân vùng tương đương · giá trị biên · bảng quyết định · chuyển trạng thái) + **dữ liệu đối kháng**; `mô tả` ghi rõ điểm kiểm theo **chuẩn kiểm** (đọc lại dữ liệu đã lưu · ca bị chặn không sinh dữ liệu). Wave ≥ 2: **trước khi viết TC mới**, phân tích phạm vi ảnh hưởng của wave (`specialist-testing §Regression theo phạm vi ảnh hưởng`; đầu vào có mục `Chức năng cũ bị chạm` của `reviewer`, MAIN chuyển nguyên văn) → ghi đoạn `Phạm vi ảnh hưởng` ở đầu đề → xếp mỗi thay đổi vào A / B / C, chỉ chép TC cũ cho loại B (NGUYÊN VĂN, nguồn `R`, `@regression`) cùng `@smoke` mỗi nghiệp vụ chính — KHÔNG chép cả FEAT / cả chức năng, KHÔNG thêm vế vào TC cũ; TC cũ hết hợp lệ vì AC đổi → `ĐÃ THAY` + TC thay thế. Wave có `SHIP` → thêm TC **đợt kiểm chuyên sâu** (`specialist-testing §Đợt kiểm chuyên sâu`).
Cột **`loại`**: `functional` / `contract` / `performance` / `security` / `e2e`… (taxonomy + rigor per loại: `specialist-testing`).
Thứ tự **ưu tiên** (test luồng nghiệp vụ + tiền/dữ liệu trước — thứ vỡ thì đau nhất):
1. **Smoke luồng nghiệp vụ** — 1 TC đi hết luồng chính đầu→cuối (giá trị hơn 50 TC vụn)
2. **Tiền / dữ liệu** — tính tiền · trừ kho · huỷ/hoàn · xoá · cập nhật đồng thời (**cần data tiền đề** như kỳ lương trước → **DỰNG nó rồi test**, đừng bỏ; cách dựng: `specialist-testing §Dựng tiền đề`)
3. **Ca biên** trong AC — đặc biệt **gửi 2 lần** (lần 2 KHÔNG tạo bản ghi trùng)
4. **Phân quyền** — B không chạm dữ liệu A. **Chặn ở UI KHÔNG TÍNH → phải server/DB** (mỗi ô `cấm` ma trận vai = 1 TC âm · mỗi ô `có` = 3 chiều: đúng phạm vi · sai phạm vi · sai trạng thái)
5. **Validate đầu vào** — rỗng · quá dài · sai kiểu · số âm + dữ liệu đối kháng (tiếng Việt có dấu · emoji · 29-02 · giờ UTC lệch giờ VN…)
+ **Phủ doanh nghiệp** (đan vào): tenant isolation · idempotency · rate limit · concurrency · **contract-test** (consumer gọi provider THẬT, đối chiếu `arch §API`)

Tên TC nói **hỏng gì khi đỏ** ("2 order cùng bàn", không "test order 2").

### 3b — RÀ ĐỀ (`bug-hunter` lần 2 — QC không tự chấm bài mình)
Spawn `bug-hunter` **chế độ RÀ ĐỀ TEST** (`bug-hunter.md`; lần 1 ở Bước 2 soi CODE, lần này soi ĐỀ, không đọc code): thiếu TC cho AC / ô chính sách / ô `cấm` / dòng `arch §6` · thiếu giá trị biên / cạnh cấm / 3 chiều phân quyền · `mô tả` thiếu điểm kiểm chuẩn kiểm · thiếu thăm dò · **phạm vi ảnh hưởng** (dòng `B` của reviewer chưa có TC trúng ca dễ vỡ · AC đổi chưa có `ĐÃ THAY` + TC mới · TC cũ chọn cho dòng `A` hoặc chọn cả FEAT = thừa · TC cũ bị thêm vế · "không ảnh hưởng" mà tài liệu đổi chạm vào · `ĐÃ THAY` không có TC thay thế) → trả **danh sách thiếu** (có thể rỗng). Wave ≥ 2: MAIN đưa kèm mục `Chức năng cũ bị chạm` của `reviewer` để đối chiếu.
**Ai sửa đề: `test-writer`** (người viết đề) — ở đầu 3c. `bug-hunter` chỉ trả danh sách, **không sửa file**. MAIN **chuyển NGUYÊN danh sách** cho `test-writer`, **không tự sửa đề, không lọc bớt mục**.

### 3c — SỬA ĐỀ + CHẠY (`test-writer` chế độ CHẠY, black-box, hệ đang chạy)
(1) **Sửa đề theo danh sách 3b** (nếu có; chỉ ở lượt spawn đầu của 3c): thêm TC thiếu · sửa TC đã có (thêm điểm kiểm / điểm biên) · mục không đồng ý → ghi lý do trong báo cáo, không bỏ im lặng. (2) **Chạy theo cụm, nhiều lượt spawn liên tiếp** (foreground, lần lượt — chung 1 hệ + 1 DB): MAIN chia đề thành cụm theo cột `AC` (mỗi cụm một nhóm FEAT, ≈ 40 TC; cụm đầu = TC nguồn `R` + `@smoke`, kế đến TC AC + CS, cuối cùng thăm dò) rồi spawn `test-writer` lần lượt từng cụm. Mỗi TC qua giao diện THẬT (API `curl`/REST · UI Playwright · perf k6) → điền `kết quả` + `thực tế / bằng chứng` **tại dòng, NGAY sau từng TC** (không dồn tới cuối); PASS chỉ khi bằng chứng khớp đủ điểm kiểm đã ghi ở `mô tả`. Spawn bị ngắt (lỗi xác thực, hết thời gian) → spawn lại đúng cụm đó: test-writer chỉ chạy các dòng còn `CHƯA CHẠY`, phần đã chạy không mất. Thăm dò: hệ cho phép điều có hại = `CHƯA CÓ QUY ĐỊNH` (không phải FAIL); lúc chạy lộ thêm ca đáng thăm dò → thêm dòng `TD`.
**FAIL = bug TÌM ĐƯỢC (finding hợp lệ), KHÔNG phải test dở** → báo cho MAIN sửa ở Bước 5; `test-writer` **KHÔNG sửa product code** (thấy code sai thì báo).
**Target mobile (chưa tự động)**: khung chưa có công cụ lái emulator. `test-writer` vẫn thiết kế đủ đề (cột `cách chạy` ghi bước làm tay) nhưng chỉ CHẠY phần gọi API của backend. TC UI của mobile do MAIN chạy tay trên emulator, ghi `kết quả` và `thực tế / bằng chứng` ngay tại dòng, gắn tag `@thủ-công`. Đây là ngoại lệ có chủ ý với nguyên tắc "MAIN không tự chấm bài mình": ghi 1 dòng `DECISIONS` ở wave đầu có target mobile để chấp nhận rủi ro đó.
**Hệ thật không dùng được** (login fail/seed lệch/service chết) = finding **BLOCKER trả MAIN** — TC bị chặn ghi `BLOCKED` + `hạ tầng: …`, **CẤM thay bằng test code/Testcontainers rồi ghi PASS** (context riêng + DB riêng ≠ bundle thật — image cũ/config sai chỉ lộ trên hệ thật).
`make test` xanh (unit/integration MAIN đã viết ở BUILD). **KHÔNG sửa source để test xanh** (→ Bước 5).

## Bước 4 — Dogfood
Trước tiên: DB đang đầy rác test của Bước 3 → **reset DB sạch + seed tối thiểu** (chi tiết trong `/dogfood` — đợt 1 cần rỗng thật). Việc nội bộ local, dựng lại được bằng seed — **KHÔNG hỏi Authority**.
**Chạy `/dogfood`** (Skill tool — NẠP TƯƠI chỉ dẫn tại thời điểm này; KHÔNG làm theo trí nhớ/tóm tắt, chỉ dẫn đầy đủ nằm trong file lệnh đó): MAIN **đóng persona chính** tự dùng bằng **trình duyệt thật** TRƯỚC, rồi mới spawn 6 persona × 2 đợt. **Chưa chạy `/dogfood` = chưa xong VERIFY.**
Bảng fidelity của `picky` (1 dòng/Mã màn) → MAIN chép nguyên vào `tracking/wave-N/fidelity.md` (gate VERIFY đọc: đủ mã in-scope + không còn LỆCH).
Phát hiện (MAIN + 6 vai) → MAIN ghi `STATE.md §Findings` (Nguồn = tên vai) → lập **mẫu tổng kết** (`/dogfood`) — **KHÔNG dừng báo Authority ở đây**: tổng kết đi chung báo cáo Bước cuối. Còn finding → Bước 5.

## Bước 5 — Fix-loop (MAIN) — lặp theo LƯỢT, mỗi lượt đủ 4 nhịp
> **PHÂN LOẠI finding trước khi xử — bug ≠ thiếu-AC:**
> - **Bug** (AC/spec ĐÃ có mà code sai) → **MAIN sửa code**, không đụng doc. Sửa mà `arch` thiếu/sai kỹ thuật làm kẹt luồng → `amend-arch` như BUILD (PROTOCOL §3, cùng commit) — reviewer soi ở lượt re-review.
> - **TC FAIL vì code lệch AC đã khoá → sửa CODE.** Chỉ được đổi kỳ vọng TC khi AC trái một nguồn bắt buộc **bên ngoài** (luật, hợp đồng khác đã khoá) — trích nguồn. **CẤM lấy `DECISIONS` do chính MAIN ghi làm căn cứ** (tự hợp thức hoá để gate xanh). AC sai mà không có nguồn ngoài → code theo AC + backlog top-up sửa AC.
> - **Tiêu chí LỆCH / dung sai / `MOCKUP-LỖI` cố định ở `persona-picky` bước 2** — không đổi theo wave, không hỏi Authority để nới.
> - **LỆCH MOCKUP ĐÃ CHỐT = BUG** (finding picky: thiếu khối/cột/nút mockup vẽ · token không apply · component trần) — mockup là **spec hình ảnh**, không cần AC chữ đứng sau. Sửa trong wave như mọi bug. **CẤM đổi nhãn thành "thiếu-AC" để đẩy backlog** — chỉ được backlog khi Authority quyết ĐỔI mockup (mà sau khoá scope thì không hỏi được → tức là sửa code cho khớp, hết đường xả).
> - **Finding cần UI mới** (hộp xác nhận · cảnh báo · khuôn lỗi / rỗng…) → dùng **component có sẵn ở `DESIGN-SYSTEM §3`** (xác nhận = hộp xác nhận của kho, rời màn khi chưa lưu = khuôn "chưa lưu"); **CẤM** hộp gốc của trình duyệt (`alert` / `confirm` / `prompt` — chặn công cụ tự động, `stack-nextjs §review`) và CẤM tự chế khối ngoài kho. UI đó chưa có trong mockup đã chốt → vẫn sửa bằng component kho cho đúng hành vi, rồi ghi `ROADMAP §backlog` ("vẽ mockup <khối> — top-up wave sau", cột Xử ghi `wave N+1 · top-up` để gate `pending_topup` thấy); kho không có component phù hợp → dùng component gần nhất của kho + ghi backlog để top-up thêm vào kho (doc đóng băng sau khoá scope).
> - **Thiếu-AC** (dogfood/bug-hunter chạm case **không AC/mockup nào phủ**, mà đáng ra phải có) → **tag `nghi thiếu AC`** vào `§Findings` + đẩy `ROADMAP §backlog` (ghi FEAT liên đới) → `/next-wave` cân nhắc `/document` top-up **thành AC mới** (spec giàu dần — loop engineering). **Vá code tạm CHỈ khi case chặn luồng nghiệp vụ wave này; không chặn → để nguyên tag + backlog, KHÔNG vá** (vá không có spec đỡ = spec rỗng dần).
> - **`CHƯA CÓ QUY ĐỊNH`** (TC thăm dò — tài liệu im lặng, hệ cho phép điều có hại; **khác `nghi thiếu AC`**: hành động ĐÃ có AC, chỉ thiếu quy định điều kiện — khi nào · bao nhiêu · trùng gì · ngoại lệ) → **KHÔNG phải bug, KHÔNG sửa code** (code đúng tài liệu; thêm quy định hay không là quyết định của Authority) → `ROADMAP §backlog` + liệt kê ở báo cáo Bước cuối để Authority quyết ở `/next-wave` (top-up thêm quy định vào bảng chính sách).

**1 lượt = tìm bug → sửa → tìm bug lại.** MAIN chỉ SỬA; **tìm lại + xác nhận đã hết là việc của agent** (người sửa không tự đóng bài mình):
(1) MAIN sửa batch finding open (TC FAIL + BLOCKER/MAJOR) → **`git commit`** → (2) target container hoá: **rebuild image + up lại** (sửa code mà re-test trên bundle cũ = CHƯA sửa) + **`python scripts/capture_proof.py`** (gate VERIFY đòi proof chụp đúng commit code mới nhất) → (3) MAIN tự bấm lại đúng màn/luồng vừa sửa — kiểm *của người sửa* (như ở BUILD), **KHÔNG dùng để đóng finding hay đổi kết quả TC** → (4) **verify lại bằng agent** (foreground; `reviewer`/`bug-hunter` chỉ đọc code → chạy song song được; agent chạm hệ/DB chạy lần lượt):
   - `test-writer` **chế độ CHẠY LẠI**: các TC FAIL + BLOCKED + `@smoke` của luồng bị chạm **+ TC (cũ và mới) thuộc vùng vừa sửa** (TC **ĐÃ CÓ**, không thiết kế mới) — vùng do chính `test-writer` suy từ các finding vừa sửa và dòng `B` của lượt re-review (MAIN chuyển nguyên danh sách mã finding và mục `Chức năng cũ bị chạm`, không tự khai vùng — người sửa không tự khoanh phạm vi kiểm bài mình) → **chính nó** cập nhật `test-cases.md`; bug đã sửa chưa có TC → `test-writer` viết 1 TC tái hiện.
   - Finding BLOCKER/MAJOR của `reviewer`/`bug-hunter` đã sửa → re-spawn **đúng agent đã báo**, re-review đúng `file:dòng` (cơ chế `review-<kind> §2`).
   - Finding BLOCKER/MAJOR của persona đã sửa → re-spawn **đúng vai đó**, chỉ với các finding đó (`picky`: chỉ các mã LỆCH, MAIN chép kết quả vào `fidelity.md`).
   - Agent xác nhận hết → MAIN đánh dấu §Findings `fixed — <agent> xác nhận`; còn lỗi hoặc lộ lỗi mới → lượt kế.
Học được gì → `knowledge-base/{name}.md`.
- **Sửa theo CHUẨN, không theo phỏng đoán**: trước khi sửa finding nào, **nạp đúng nguồn chuẩn finding đó trỏ tới** (ADR/`arch §4`/`stack-<x> §review`/`ref-<kind>-pattern §cây chuẩn`) — agent nạp trong cửa sổ RIÊNG của nó, MAIN không thừa hưởng; finding cấu trúc mà MAIN chưa Read cây chuẩn = sửa mù, dễ ra cấu trúc sai kiểu khác.
- **Finding không đo được bằng TC/browser** (cấu trúc/convention — trục B): cột Xử lý phải kèm **bằng chứng CÙNG LOẠI với cách phát hiện** — finding từ dump cây → fix xong dump cây lại đính vào; từ grep → chạy lại đúng lệnh grep đó. **Tick chay = CHƯA fix.**
- **Thoát vòng** (soi FILE, không theo trí nhớ): mở `tracking/wave-N/test-cases.md` — không còn dòng **FAIL / BLOCKED**; mở `STATE §Findings` — không còn BLOCKER/MAJOR **open**; mở `fidelity.md` — không còn **LỆCH**. Mọi dòng BLOCKER/MAJOR `fixed` phải có agent xác nhận ở nhịp (4) — MAIN tự đánh `fixed` không kèm xác nhận = CHƯA thoát → Bước cuối. (MINOR không đòi xác nhận riêng — xem dòng MINOR bên dưới.)
- **Cắt vòng**: hết lượt 3 mà vẫn còn BLOCKER/MAJOR / TC FAIL (cũ chưa hết hoặc mới lộ) → DỪNG (gate VERIFY báo khi `§Findings` ghi tới lượt 3), kết luận **KHÔNG ĐẠT** (Bước cuối), ghi `STATE §Blocker` + số lượt đã chạy (1 dòng §Findings), báo cuối buổi — đừng sửa vô hạn (max-turns safety, loop-engineering).
- **MINOR → backlog, không sửa trong wave, không spawn agent chỉ để xác nhận**: để nguyên trong `§Findings`, cột Xử lý = `backlog` (`/next-wave` Bước 1 gom vào `ROADMAP §backlog`). **Chỉ 3 trường hợp sửa trong wave**: (a) lệch mockup đã chốt (luật ở trên); (b) sửa chung với một MAJOR — cùng file, đang mở sẵn, vài dòng — Xử lý = `fixed — MAIN tự kiểm (<cách>)`; (c) thực chất chạm tiền / quyền / dữ liệu / AC → **nâng lên MAJOR** (reviewer và QC kiểm lại nhãn). Ngoài scope → `docs/ROADMAP.md §backlog` (wave sau).

## Bước cuối — Chốt
1. `tracking/wave-N/test-cases.md`: mọi AC in-scope có TC **PASS**, không TC **FAIL / BLOCKED / CHƯA CHẠY** · wave ≥ 2: đề có đoạn `Phạm vi ảnh hưởng`, mọi TC nguồn `R` (TC cũ được chọn) PASS hoặc `ĐÃ THAY`.
2. `STATE.md §Findings`: hết finding **BLOCKER/MAJOR** open.
   **Kết luận QC** (dòng đầu báo cáo gửi Authority; ghi luôn 1 dòng con cuối mục gate VERIFY trong `STATE.md`: `Kết luận QC: <mức> — <ngày>` → snapshot vào archive, `/next-wave` đọc lại) — đúng 1 trong 3:
   - **ĐẠT** — gate VERIFY xanh, không còn `CHƯA CÓ QUY ĐỊNH` nào chạm tiền · công · quyền.
   - **ĐẠT CÓ ĐIỀU KIỆN** — gate xanh nhưng còn thứ Authority phải biết trước khi dùng thật: `CHƯA CÓ QUY ĐỊNH` chạm tiền/công/quyền · finding MINOR đáng kể · NFR hoãn sang wave sau theo ROADMAP. **Liệt kê từng điều kiện** (1 dòng/điều kiện + hệ quả nếu bỏ qua).
   - **KHÔNG ĐẠT** — gate đỏ (vd đã cắt vòng sau 3 lượt): nêu thứ còn đỏ + đề xuất (sửa tiếp · đẩy wave sau · kill).
3. `python scripts/gate.py` (VERIFY): xanh → tick gate VERIFY; đỏ (cắt vòng) → KHÔNG tick. Cả hai trường hợp → **DỪNG — báo Authority kết quả VERIFY**: kết luận QC + mẫu tổng kết dogfood + trạng thái gate + **danh sách `CHƯA CÓ QUY ĐỊNH`** (hành động · hệ đang cho phép gì · hệ quả · quy định đề xuất — Authority quyết ở `/next-wave`). Authority bảo đóng wave (kể cả nói trong chat) → chạy **`/next-wave`** (script `next_wave.py`), KHÔNG đóng tay. **`/ship`/`/next-wave` do AUTHORITY gọi — MAIN KHÔNG tự chạy** (đóng wave = quyết định go/pivot/kill của Authority, kể cả wave không khai metric; MAIN tự đóng là chiếm quyền).

## Ranh giới
- **KHÔNG build/sửa source để test qua** — test black-box đo hành vi thật; lỗi thì sửa ở Bước 5 rồi re-test.
- Agent (review/persona) **chỉ trả finding** — chỉ MAIN sửa (giữ **góc nhìn độc lập** — *fresh eyes*).
- Không thả 6 persona cùng lúc (đè trạng thái nhau + trạng thái rỗng chết khi có bản ghi đầu tiên).
- **Dọn rác** — **luật #9 PROTOCOL §2** (script chạy thử · ảnh · trace · log ngoài repo, dọn ngay; `tracking/wave-N/` chỉ 3 file). Seed test-data → dọn tại **chuyển bước** (Bước 3→4: dogfood đợt 1 cần DB sạch) + cuối phase. Bản sao hệ của QA → `py -3 scripts/qa_iso.py clean --service <backend>` ở cùng hai thời điểm đó.
