---
description: BUILD — MAIN tự code 1 wave: đọc KG/context → challenge → scaffold → walking skeleton → luồng lõi → chạy thật
---
# /build [<wave>] — Phase BUILD

> Sau khoá scope: **TOÀN QUYỀN, KHÔNG hỏi Authority.** Mơ hồ → tự quyết theo doc → 1 dòng `docs/DECISIONS.md` → đi tiếp.
> Ngoài scope → `docs/ROADMAP.md §backlog`, không hỏi. Chặn cứng → `STATE.md §Blocker`, báo gộp cuối buổi.
> Ngoại lệ DUY NHẤT được hỏi: hành động **không đảo ngược / hướng ra ngoài** (xoá data prod, tiêu tiền, đăng ký dịch vụ).
> **MAIN tự code — KHÔNG spawn dev-agent** (review + dogfood để dành `/verify`).

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
Theo `stack-<tên>/SKILL.md` — **TÔN TRỌNG đúng pattern/convention của skill** (cấu trúc thư mục · layer · error
shape · forbidden patterns), KHÔNG tự chế cấu trúc riêng. Tuân thêm `docs/CONVENTIONS.md` (đặt tên · error envelope · API).
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
**Wave nhiều target**: skeleton = **1 đường xuyên suốt qua cụm** (1 backend + 1 web/frontend cho luồng lõi) trước,
target còn lại nối sau — không dựng đầy đủ từng cái một.

## Bước 5 — Luồng lõi (mỗi AC in-scope)
`làm → tự bấm thử ở local → tick ROADMAP → commit`. Trong lúc làm:
- **UI**: bám mockup `docs/ux/`, đổ **token** vào theme (thứ DUY NHẤT chép nguyên từ DOCUMENT), đủ trạng thái rỗng/lỗi
- **Phân quyền**: mỗi ô `cấm` trong ma trận vai phải bị chặn ở **server**, không tự quyết lại
- **Ranh giới module** theo `arch/{name}.md` — logic sai tầng là lỗi, không phải phong cách
- **Ca biên** (trong AC): xử **ngay khi làm phần liên quan**, đừng để cuối
- **Doc wave đang mở lệch thực tế** (trong AC đã khoá — vd đổi tên field, thêm chi tiết kỹ thuật) → **sửa doc CÙNG commit** (luật #4, doc = nguồn sự thật). Thêm AC/luồng MỚI thì không → `ROADMAP §backlog`.
- Mơ hồ → `DECISIONS.md` 1 dòng · ngoài AC → `ROADMAP §backlog` · commit nhỏ, message tiếng Việt
- **Gặp gotcha / vá bug lúc code** (env nông · config · quirk contract · schema drift...) → **append NGAY** `knowledge-base/{name}.md` §Gotchas/§Failure-modes. Đây là **nguồn KG nhiều nhất** (lúc code mới va) — không ghi = mất, wave/rebuild sau lặp lại (retro B3).

**KHÔNG** làm ở phase này: tối ưu hiệu năng · UI đẹp quá mức đủ dùng · viết test formal (để VERIFY) · tính năng "tiện tay".

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
- Không đổi stack (đổi sau khoá scope = phá luật; cần thì ghi đánh đổi rõ ở `DECISIONS.md`)
- Không viết test formal / không tối ưu sớm (để VERIFY)
- **Không spawn dev-agent** — MAIN tự code; agent chỉ xuất hiện ở `/verify`
