---
description: "BUILD — MAIN tự code 1 wave: đọc KG/context → challenge → scaffold → walking skeleton → luồng nghiệp vụ → chạy thật"
---
# /build [<wave>] — Phase BUILD

> Sau khoá scope: **TOÀN QUYỀN, KHÔNG hỏi Authority.** Mơ hồ → tự quyết theo doc → 1 dòng `docs/DECISIONS.md` → đi tiếp.
> Ngoài scope → `docs/ROADMAP.md §backlog`, không hỏi. Chặn cứng → `STATE.md §Blocker`, báo gộp cuối buổi.
> Ngoại lệ DUY NHẤT được hỏi: hành động **không đảo ngược / hướng ra ngoài** (xoá data prod, tiêu tiền, đăng ký dịch vụ).
> **MAIN tự viết 100% product code + unit/integration test. Ở BUILD KHÔNG spawn agent NÀO** — cấm mọi subagent để code/scaffold/viết test/"phụ một tay", dù đặt tên gì. MAIN gõ từng dòng. Agent (review/test-writer/persona) **chỉ xuất hiện ở `/verify`**, và chỉ verification — không đụng product code. Hook `guard_agent` chặn mọi spawn ở BUILD.

**Việc ĐẦU TIÊN**: sửa `STATE.md` → `Phase hiện tại: BUILD` + `Wave: <N>` (arg `<wave>`, hoặc dòng `Wave` sẵn có).
`guard_ask` + `gate.py` đọc dòng này — không sửa thì máy tưởng còn phase cũ, luật "không hỏi" mất hiệu lực.

> **Wave ≥2**: trước khi code, gate `wave_reviewed` đòi ô `Rà lại` của wave N ở `docs/ROADMAP.md §1` đã điền ngày (do `/next-wave`
> stamp lúc mở wave) — còn trống = chưa rà lại kế hoạch, KHÔNG cho vào BUILD (quay lại `/next-wave`). **Wave 1 MIỄN** — kế
> hoạch vừa lập + Authority duyệt ở DOCUMENT.

## Bước 1 — Nạp context (CHỈ slice của wave — targeted, chống lost-in-middle)
Đọc **đúng phần của wave**, KHÔNG đọc cả `docs/`. File vừa Read còn **tươi trong context** (chưa qua compact) → **KHÔNG Read lại** — chỉ nạp phần thiếu/đã cũ:
- `docs/ROADMAP.md` wave-N: **target** (kind: backend/web/bff/mobile/desktop) + **AC in-scope** + phases khai
- `docs/feat/FEAT-*` của các AC in-scope (AC + ca biên + §3 Ràng buộc nghiệp vụ) — chặn ở đâu đọc ở `arch §6`
- `docs/arch/{name}.md` của **mỗi target wave khai** — **đọc frontmatter lấy `kind`** (backend/web/bff/mobile/desktop) + `stack` + data/API/ranh giới (KHÔNG đọc target **ngoài wave**). `kind` quyết định scaffold ở đâu · skeleton kiểu gì · chạy thật ra sao. **Wave nhiều target → phủ HẾT, đọc/làm TỪNG target một** theo chiều phụ thuộc (Bước 4), không chỉ 1 cái.
- **`docs/adr/*` liên quan target** — quyết định kiến trúc đã chốt (ui-kit nào · Layered vs Hexagonal · auth · caching...). Scaffold Bước 3 **phải theo ADR** — ADR thắng default của skill.
- **`knowledge-base/{name}.md`** nếu có → đọc hết §Invariants/§Gotchas/§Failure-modes/§Key-decisions
- có UI → `docs/DESIGN-SYSTEM.md` + `docs/ux/mockups/<target>/` các màn in-scope (mockup dựng theo wave — phải có TRƯỚC khi code UI; thiếu → quay `/document` top-up)
- `docs/TECHSTACK.md` + skill `stack-<tên>`
- `docs/CONVENTIONS.md` (nhỏ — error envelope · API design · đặt tên; mọi target theo) + `docs/SECURITY.md`
- `docs/PERSONAS.md §ma trận vai×hành động` (để code phân quyền)

Đọc thật, không lướt — Bước 2 kiểm.

## Bước 2 — Challenge (luật #8, trước dòng code đầu — CONFIRM ý hiểu)
Trước dòng code đầu, tự ra **1 câu hỏi khó** dựa trên context THẬT của wave (chỉ trả lời được nếu đã đọc FEAT/arch/KG) — confirm đã hiểu:
- mâu thuẫn giữa 2 AC · ca biên trong AC mà data model chưa chặn được · ô `cấm` trong ma trận vai mà thiết kế
  chưa chặn · màn cần thông tin mà data model chưa nuôi nổi · **invariant trong KG mà thiết kế sắp phạm**.

Trả lời thẳng, tự chấm PASS/FAIL trung thực. **FAIL** (đoán / phát hiện chưa đọc kỹ) → đọc lại, ra câu khác,
trả lời lại. **KHÔNG được code** khi chưa PASS. **PASS** → ghi `STATE.md §Challenge log` → đi tiếp.
> 1 câu/mảng việc lớn ở mức BUILD (confirm hiểu trước khi code). Việc soi lỗ tài liệu **3–5 câu** đã làm ở DOCUMENT.

> **Wave nhiều target — Bước 3-6 là VÒNG LẶP theo target, KHÔNG phải 1 lượt:** lặp scaffold→skeleton→luồng nghiệp vụ→chạy thật cho **MỖI target ROADMAP §1 cột Target khai**, theo thứ tự **provider→consumer** (Bước 4). BUILD **chưa xong** khi còn 1 target chưa chạy thật — làm BE xong nhảy VERIFY để quên FE là lỗi gate (đối chiếu ROADMAP↔proof). Nhớ đủ target: reanchor nhồi lại "Target còn nợ" sau mỗi compact.

## Bước 3 — Scaffold
**Bốn nguồn ràng buộc — theo ĐÚNG, KHÔNG tự chế / KHÔNG lệch** (đây là chỗ hay đi lệch nhất):
1. **`docs/TECHSTACK.md`** — stack + **VERSION đã chốt**: dùng ĐÚNG framework/lib/version đó. **KHÔNG** tự nâng/hạ version · **KHÔNG** thêm dependency ngoài danh sách · **KHÔNG** đổi build tool. Cần lib mới thật sự bất khả thiếu → `DECISIONS.md` 1 dòng lý do trước, rồi mới thêm.
2. **`docs/adr/*`** — mọi quyết định kiến trúc đã chốt (ui-kit · Layered vs Hexagonal · auth · caching...). **ADR THẮNG default của skill**: skill mặc định Layered mà ADR khai Hexagonal → theo ADR.
3. **Skill pattern (gọi TÊN cụ thể, không mơ hồ "skill"):**
   · **`stack-<tên>`** (`stack-spring-boot`/`stack-nextjs`/`stack-flutter`/`stack-bff`/`stack-electron`) — idiom CODE + `§review`
   · **`ref-<kind>-pattern`** — CẤU TRÚC: `ref-backend-pattern` (Layered mặc định · JPA `@Entity` ở package `entities/` tên `{Resource}Entity` · layer trách nhiệm · interface/impl · response & error shape · forbidden patterns) · `ref-frontend-pattern` (layout thư mục + tổ chức component)
   · **`ref-backend-{config,kafka,redis,logging,restclient}`** (backend) · **`ref-frontend-config`** (web — **Dockerfile FE multi-stage → nginx** + block compose service) — nạp khi target dùng đúng mảnh đó
   → TÔN TRỌNG cấu trúc thư mục · layer · error shape · forbidden patterns của chúng. **KHÔNG tự chế cấu trúc riêng.**
4. **`docs/CONVENTIONS.md`** (đặt tên · error envelope · API design — mọi target theo) + **`docs/SECURITY.md`** (baseline).

Scaffold vào **đúng nhóm theo `kind`** bằng **CLI chính chủ** (không chép boilerplate):
· `backend` → `services/boundaries/{name}/` · `web` → `services/web/{name}/` · `bff` → `services/bff/{name}/` · `mobile` → `services/mobile/{name}/` · `desktop` → `services/desktop/{name}/`
**Có KG** → áp lại NGAY §Invariants + §Gotchas (chống lặp bug cũ: env tường minh, JWT local, soft-delete...).
Artifact chạy local → `deployment/local/`: **làm nốt** khung docker-compose dựng sẵn từ DOCUMENT (skill `infra-local-dev`) · `.env` từ `.env.example` · seed theo PRD. **Mỗi target container hoá (backend/bff/web) phải có `Dockerfile` trong thư mục service + 1 service trong docker-compose** (mobile, desktop không container). Điền `make` 6 lệnh.
> **Máy thiếu `make`/`sh`** → MAIN **TỰ CÀI** bằng trình quản lý gói có sẵn (`README §Yêu cầu máy`: Windows `winget install ezwinports.make` + `winget install Git.Git` nếu chưa có Git Bash · macOS `brew install make` / `xcode-select --install` · Linux `sudo apt install make`), ghi `DECISIONS` loại `kỹ-thuật`. Windows: PATH chỉ nhận khi mở lại terminal → phiên hiện tại gọi thẳng đường dẫn `make.exe` vừa cài. **Chỉ báo Authority khi tự cài không được** (cần mật khẩu admin/sudo, không có trình quản lý gói) → cách chạy khác Authority cho phép. Cách nào thì `check` vẫn phải chạy đúng thân lệnh trong Makefile của target (proof không tính lệnh tự chế).
Xong → `git add -A && git commit`.

## Bước 4 — Walking skeleton (thông 1 đường TRƯỚC, đắp thịt sau)
Bản mỏng nhất **CHẠY được**, theo `kind`:
> `make dev` là dev server chạy mãi. Chạy từng target ở terminal riêng bằng `make -C services/<nhóm>/<tên> dev`; `make dev` ở gốc chỉ hợp khi wave có đúng 1 target.
- **backend / bff**: `make dev` (app+db lên) → health 200 → 1 thao tác **ghi→đọc DB** (dù xấu)
- **web**: `make dev` (dev server, hot-reload — chỉ để code/check nhanh; **hệ container hoá thật ở Bước 6**) → **app shell dịch từ `docs/ux/mockups/<target>/_shell.html`** (Read file đó → dựng Layout: nav items/thứ tự/nhóm/logo/user-menu/icon KHỚP khối SHELL — HTML→JSX, không hook nào chặn code FE) + 1 màn rỗng render TRONG shell → **gọi 1 API thật** (backend đã có) hiện dữ liệu
- **mobile**: build + chạy **emulator** → 1 màn render → gọi 1 API
- **desktop**: `make dev` (cửa sổ app mở) → app shell dịch từ `_shell.html` như web + 1 màn → gọi 1 kênh IPC thật (main làm việc thật, vd đọc 1 file) → `npm run package` + `make doctor` (`--smoke`) exit 0

→ `git commit`. Chưa thông đường mỏng này thì **KHÔNG** làm gì khác — đừng đắp UI đẹp lên đường chưa thông.
**Wave nhiều target — THỨ TỰ theo chiều phụ thuộc, KHÔNG song song:** **provider TRƯỚC, consumer SAU.**
Backend (cấp API theo `arch §3`) phải có **endpoint THẬT chạy được** (health 200 + gọi được) TRƯỚC → rồi web/bff/mobile/desktop mới build **gọi API thật đó** (FE gọi theo `consumes` ở frontmatter `arch` của nó). Skeleton = **1 đường xuyên suốt qua cụm ĐÚNG chiều phụ thuộc** (backend luồng nghiệp vụ → frontend luồng nghiệp vụ), nhánh còn lại nối sau.
**CẤM code BE và FE "song song mỗi cái một nửa"** · **CẤM mock API để FE chạy trước** khi backend chưa có endpoint thật — FE dựng trên contract chưa chạy = đường CHƯA THÔNG, đắp thêm code lên đó là xây trên nền chưa vững. Provider chưa thông thì consumer chưa được bắt đầu.

## Bước 5 — Luồng nghiệp vụ (mỗi AC in-scope)
`làm → tự bấm thử ở local → tick ROADMAP → commit`. Trong lúc làm:
- **UI = HỢP ĐỒNG HÌNH ẢNH** (mockup Authority đã chốt — code FE không hook nào canh, tự kỷ luật ở đây, backstop là `picky` ở VERIFY):
  - TRƯỚC khi code màn nào → **Read mockup màn đó** (ô Mockup SCREEN-MAP: `<module>.html#<Mã màn>`), nắm khối component (stat-card/toolbar/status-pill/cell-person...) — app phải dùng ĐÚNG khối đó, không thay bằng bảng/tag trần
  - **Token map vào theme config TRƯỚC màn đầu tiên** (Tailwind: `theme.extend.colors/spacing` từ `DESIGN-SYSTEM §2` · antd: `ConfigProvider` · plain-CSS: `:root`) — màu mặc định framework (Tailwind blue...) xuất hiện trên màn = CHƯA map, dừng lại map đã
  - **Mỗi mockup in-scope = 1 route thật** — thiếu màn = AC chưa xong; màn KHÔNG có mockup = ngoài scope, muốn thêm → `ROADMAP §backlog`, KHÔNG tự chế
  - Gắn `data-screen`/`data-ds` đúng mã mockup (`stack-nextjs`) · đủ trạng thái rỗng/lỗi — so khớp là việc `picky` ở VERIFY
- **Phân quyền**: mỗi ô `cấm` trong ma trận vai phải bị chặn ở **server**, không tự quyết lại
- **Ranh giới module** theo `arch/{name}.md` — logic sai tầng là lỗi, không phải phong cách
- **Ca biên** (trong AC): xử **ngay khi làm phần liên quan**, đừng để cuối
- **Doc lệch thực tế** → theo PROTOCOL §3: (A) `arch` lệch nhưng **không kẹt luồng** (tên field, kiểu, index) → code bám `arch` + `DECISIONS` `kỹ-thuật` + `ROADMAP §backlog` · (B) `arch` thiếu/sai kỹ thuật làm **kẹt luồng** của AC đã khoá → **`amend-arch`**: bổ sung `docs/arch/*.md` tại chỗ, cùng commit, đủ 6 điều kiện §3 · (C) thiếu hẳn hành vi/luồng → `ROADMAP §backlog` (kẹt luồng → `STATE §Blocker`, dừng gợi ý Authority gọi `/document` top-up). AC · mockup · PRD **không** sửa (guard_doc chặn). Mơ hồ trong AC → `DECISIONS.md` 1 dòng.
- Mơ hồ → `DECISIONS.md` 1 dòng · ngoài AC → `ROADMAP §backlog` · commit nhỏ, message tiếng Việt
- **Gặp gotcha / vá bug lúc code** (env nông · config · quirk contract · schema drift...) → **append NGAY** `knowledge-base/{name}.md` §Gotchas/§Failure-modes. Đây là **nguồn KG nhiều nhất** (lúc code mới va) — không ghi = mất, wave/rebuild sau lặp lại.

**Viết unit/integration test CÙNG LÚC code** (chạy `make test` — lưới an toàn của MAIN; code smell/checkstyle sạch) — nạp **`ref-<kind>-test`** (`ref-backend-test` · `ref-frontend-test` · `ref-bff-test` · `ref-desktop-test`; mobile dùng `flutter_test` theo `stack-flutter`): tầng test · đặt tên · mẫu · đồng hồ tiêm được (để QC test hạn chót trên hệ thật) · mock khớp contract.
**KHÔNG** làm ở phase này: tối ưu hiệu năng · UI đẹp quá mức đủ dùng · **black-box test-case + dogfood (để VERIFY — `test-writer` chủ trì)** · tính năng "tiện tay".

## Bước 6 — Chạy thật (theo `kind` — VERIFY sẽ đánh trên đây)
- **backend / bff**: `docker compose -f deployment/local/docker-compose.yml up -d --build` → health 200
- **web**: `docker compose -f deployment/local/docker-compose.yml up -d --build` → health 200 (nginx serve `dist/`, trỏ backend thật)
- **mobile**: build + chạy **emulator** (KHÔNG docker; VERIFY mobile chưa tự động, xem `dogfood.md`)
- **desktop**: `npm run package` → mở bản đóng gói (`env -u ELECTRON_RUN_AS_NODE "out/<App>-win32-x64/<App>.exe"`) · `make doctor` exit 0 (KHÔNG docker)

## Bước cuối — Chốt
1. `make check` xanh
2. **Đã commit** mọi thứ (build/test pass mà không commit = coi như CHƯA làm — đây là nguyên nhân từng mất code)
3. **`python scripts/capture_proof.py`** → sinh `tracking/wave-N/proof.json` (ghi commit code — sửa code sau đó phải commit + chụp lại · make check + **health per-target tự đọc `docker compose ps`** — không cần gõ URL; máy verify, không tin tick tay). Mọi target container hoá của wave phải **đang chạy** (Bước 6 `up -d --build` cho HẾT) để capture bắt được `healthy`. Desktop: capture_proof tự chạy `make doctor` (bản đóng gói `--smoke`).
4. `python scripts/gate.py` (phase BUILD) xanh (đọc `proof.json`, **đối chiếu ROADMAP §1 cột Target — thiếu/không-healthy target nào = đỏ**) → tick gate BUILD (gồm ô "mọi target đã build") trong `STATE.md` → gợi ý `/verify`

## Ranh giới
- Không sửa AC (`docs/feat/**`) cho dễ làm — không làm được → `STATE.md §Blocker`, báo cuối buổi
- **Không đổi stack / version / bỏ ADR** (đã chốt ở DOCUMENT = phá luật): dùng đúng `TECHSTACK.md` version + `docs/adr/*` + skill `stack-<tên>`/`ref-<kind>-pattern`. Bất khả thi → ghi đánh đổi rõ `DECISIONS.md`, KHÔNG tự lệch.
- **Nhiều target: KHÔNG code BE+FE song song** (Bước 4) — provider (API thật, health 200) trước, consumer sau. FE bám contract đã chạy, KHÔNG mock để chạy trước.
- Viết unit/integration (lưới an toàn MAIN) — nhưng **black-box test-case + dogfood để VERIFY** (`test-writer`); không tối ưu sớm
- **Không spawn agent NÀO ở BUILD để code/scaffold/viết test** (bất kỳ tên nào) — MAIN tự viết hết; agent chỉ ở `/verify` và chỉ verification. Spawn bằng tool Agent với prompt ngắn viết tay, truyền `run_in_background: false`.
