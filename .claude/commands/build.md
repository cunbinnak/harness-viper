---
description: BUILD — MAIN tự code 1 wave: đọc KG/context → challenge → scaffold → walking skeleton → luồng lõi → chạy thật
---
# /build [<wave>] — Phase BUILD

> Sau khoá scope: **TOÀN QUYỀN, KHÔNG hỏi Authority.** Mơ hồ → tự quyết theo doc → 1 dòng `docs/DECISIONS.md` → đi tiếp.
> Ngoài scope → `docs/ROADMAP.md §backlog`, không hỏi. Chặn cứng → `STATE.md §Blocker`, báo gộp cuối buổi.
> Ngoại lệ DUY NHẤT được hỏi: hành động **không đảo ngược / hướng ra ngoài** (xoá data prod, tiêu tiền, đăng ký dịch vụ).
> **MAIN tự viết 100% product code + unit/integration test. Ở BUILD KHÔNG spawn agent NÀO** — không chỉ "dev-agent": cấm mọi Task subagent để code/scaffold/viết test/"phụ một tay", dù đặt tên gì. MAIN gõ từng dòng. Agent (review/test-writer/persona) **chỉ xuất hiện ở `/verify`**, và chỉ verification — không đụng product code.

**Việc ĐẦU TIÊN**: sửa `STATE.md` → `Phase hiện tại: BUILD` + `Wave: <N>` (arg `<wave>`, hoặc dòng `Wave` sẵn có).
`guard_ask` + `gate.py` đọc dòng này — không sửa thì máy tưởng còn phase cũ, luật "không hỏi" mất hiệu lực.

> **Wave ≥2**: trước khi code, gate `wave_reviewed` đòi `docs/ROADMAP.md` có dòng `Rà lại wave N: <ngày>` (do `/next-wave`
> stamp lúc mở wave) — thiếu = chưa rà lại kế hoạch, KHÔNG cho vào BUILD (quay lại `/next-wave`). **Wave 1 MIỄN** — kế
> hoạch vừa lập + Authority duyệt ở DOCUMENT.

## Bước 1 — Nạp context (CHỈ slice của wave — targeted, chống lost-in-middle)
Đọc **đúng phần của wave**, KHÔNG đọc cả `docs/`:
- `docs/ROADMAP.md` wave-N: **target** (kind: backend/web/bff/mobile) + **AC in-scope** + phases khai
- `docs/feat/FEAT-*` của các AC in-scope (AC + ca biên + field kỹ thuật)
- `docs/arch/{name}.md` của target — **đọc frontmatter lấy `kind`** (backend/web/bff/mobile) + `stack` + data/API/ranh giới (KHÔNG đọc target khác). `kind` quyết định scaffold ở đâu · skeleton kiểu gì · chạy thật ra sao.
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

## Bước 3 — Scaffold
**Bốn nguồn ràng buộc — theo ĐÚNG, KHÔNG tự chế / KHÔNG lệch** (đây là chỗ hay đi lệch nhất):
1. **`docs/TECHSTACK.md`** — stack + **VERSION đã chốt**: dùng ĐÚNG framework/lib/version đó. **KHÔNG** tự nâng/hạ version · **KHÔNG** thêm dependency ngoài danh sách · **KHÔNG** đổi build tool. Cần lib mới thật sự bất khả thiếu → `DECISIONS.md` 1 dòng lý do trước, rồi mới thêm.
2. **`docs/adr/*`** — mọi quyết định kiến trúc đã chốt (ui-kit · Layered vs Hexagonal · auth · caching...). **ADR THẮNG default của skill**: skill mặc định Layered mà ADR khai Hexagonal → theo ADR.
3. **Skill pattern (gọi TÊN cụ thể, không mơ hồ "skill"):**
   · **`stack-<tên>`** (`stack-spring-boot`/`stack-nextjs`/`stack-flutter`/`stack-bff`) — idiom CODE + `§review`
   · **`ref-<kind>-pattern`** — CẤU TRÚC: `ref-backend-pattern` (Layered mặc định · JPA `@Entity` ở package `entities/` tên `{Resource}Entity` · layer trách nhiệm · interface/impl · response & error shape · forbidden patterns) · `ref-frontend-pattern` (layout thư mục + tổ chức component)
   · **`ref-backend-{config,kafka,redis,logging,restclient}`** — nạp khi target dùng đúng mảnh đó
   → TÔN TRỌNG cấu trúc thư mục · layer · error shape · forbidden patterns của chúng. **KHÔNG tự chế cấu trúc riêng.**
4. **`docs/CONVENTIONS.md`** (đặt tên · error envelope · API design — mọi target theo) + **`docs/SECURITY.md`** (baseline).

Scaffold vào **đúng nhóm theo `kind`** bằng **CLI chính chủ** (không chép boilerplate):
· `backend` → `services/boundaries/{name}/` · `web` → `services/web/{name}/` · `bff` → `services/bff/{name}/` · `mobile` → `services/mobile/{name}/`
**Có KG** → áp lại NGAY §Invariants + §Gotchas (chống lặp bug cũ: env tường minh, JWT local, soft-delete...).
Artifact chạy local → `deployment/local/` (docker-compose · `.env` từ `.env.example` · seed theo PRD). Điền `make` 6 lệnh.
Xong → `git add -A && git commit`.

## Bước 4 — Walking skeleton (thông 1 đường TRƯỚC, đắp thịt sau)
Bản mỏng nhất **CHẠY được**, theo `kind`:
- **backend / bff**: `make dev` (app+db lên) → health 200 → 1 thao tác **ghi→đọc DB** (dù xấu)
- **web**: `make dev` (dev server) → 1 màn rỗng render → **gọi 1 API thật** (backend đã có) hiện dữ liệu
- **mobile**: build + chạy **emulator** → 1 màn render → gọi 1 API

→ `git commit`. Chưa thông đường mỏng này thì **KHÔNG** làm gì khác — đừng đắp UI đẹp lên đường chưa thông.
**Wave nhiều target — THỨ TỰ theo chiều phụ thuộc, KHÔNG song song:** **provider TRƯỚC, consumer SAU.**
Backend (cấp API theo `arch §3`) phải có **endpoint THẬT chạy được** (health 200 + gọi được) TRƯỚC → rồi web/bff/mobile mới build **gọi API thật đó** (FE consume `consumes_contracts`). Skeleton = **1 đường xuyên suốt qua cụm ĐÚNG chiều phụ thuộc** (backend luồng lõi → frontend luồng lõi), nhánh còn lại nối sau.
**CẤM code BE và FE "song song mỗi cái một nửa"** · **CẤM mock API để FE chạy trước** khi backend chưa có endpoint thật — FE dựng trên contract chưa chạy = đường CHƯA THÔNG, đắp thịt lên đó là retro. Provider chưa thông thì consumer chưa được bắt đầu.

## Bước 5 — Luồng lõi (mỗi AC in-scope)
`làm → tự bấm thử ở local → tick ROADMAP → commit`. Trong lúc làm:
- **UI**: bám mockup `docs/ux/`, đổ **token** vào theme (thứ DUY NHẤT chép nguyên từ DOCUMENT), đủ trạng thái rỗng/lỗi
- **Phân quyền**: mỗi ô `cấm` trong ma trận vai phải bị chặn ở **server**, không tự quyết lại
- **Ranh giới module** theo `arch/{name}.md` — logic sai tầng là lỗi, không phải phong cách
- **Ca biên** (trong AC): xử **ngay khi làm phần liên quan**, đừng để cuối
- **Doc spec lệch thực tế** (vd đổi tên field) → **KHÔNG sửa doc đã khoá** (guard_doc chặn — doc đóng băng lúc BUILD); ghi `ROADMAP §backlog`, wave sau `/document` top-up đồng bộ. Mơ hồ trong AC → `DECISIONS.md` 1 dòng (sổ sống). Thêm AC/luồng MỚI cũng → `ROADMAP §backlog`.
- Mơ hồ → `DECISIONS.md` 1 dòng · ngoài AC → `ROADMAP §backlog` · commit nhỏ, message tiếng Việt
- **Gặp gotcha / vá bug lúc code** (env nông · config · quirk contract · schema drift...) → **append NGAY** `knowledge-base/{name}.md` §Gotchas/§Failure-modes. Đây là **nguồn KG nhiều nhất** (lúc code mới va) — không ghi = mất, wave/rebuild sau lặp lại (retro B3).

**Viết unit/integration test CÙNG LÚC code** (chạy `make test` — lưới an toàn của MAIN; code smell/checkstyle sạch).
**KHÔNG** làm ở phase này: tối ưu hiệu năng · UI đẹp quá mức đủ dùng · **black-box test-case + dogfood (để VERIFY — `test-writer` chủ trì)** · tính năng "tiện tay".

## Bước 6 — Chạy thật (theo `kind` — VERIFY sẽ đánh trên đây)
- **backend / bff**: `docker compose -f deployment/local/docker-compose.yml up -d --build` → health 200
- **web**: dev/preview server chạy (trỏ backend thật)
- **mobile**: build + chạy **emulator** (KHÔNG docker)

## Bước cuối — Chốt
1. `make check` xanh
2. **Đã commit** mọi thứ (build/test pass mà không commit = coi như CHƯA làm — đây là nguyên nhân từng mất code)
3. **`python scripts/capture_proof.py`** → sinh `tracking/wave-N/proof.json` (**make check + health THẬT** — máy verify, không tin tick tay)
4. `python scripts/gate.py` (phase BUILD) xanh (đọc `proof.json`) → tick gate BUILD trong `STATE.md` → gợi ý `/verify`

## Ranh giới
- Không sửa AC (`docs/feat/**`) cho dễ làm — không làm được → `STATE.md §Blocker`, báo cuối buổi
- **Không đổi stack / version / bỏ ADR** (đã chốt ở DOCUMENT = phá luật): dùng đúng `TECHSTACK.md` version + `docs/adr/*` + skill `stack-<tên>`/`ref-<kind>-pattern`. Bất khả thi → ghi đánh đổi rõ `DECISIONS.md`, KHÔNG tự lệch.
- **Nhiều target: KHÔNG code BE+FE song song** (Bước 4) — provider (API thật, health 200) trước, consumer sau. FE bám contract đã chạy, KHÔNG mock để chạy trước.
- Viết unit/integration (lưới an toàn MAIN) — nhưng **black-box test-case + dogfood để VERIFY** (`test-writer`); không tối ưu sớm
- **Không spawn agent NÀO ở BUILD để code/scaffold/viết test** (dev-agent hay bất kỳ tên nào) — MAIN tự viết hết; agent chỉ ở `/verify` và chỉ verification. Spawn bằng **Task tool + prompt ngắn tay**, **KHÔNG `build_prompt`**.
