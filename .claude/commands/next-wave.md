---
description: NEXT-WAVE — đóng wave (snapshot, KHÔNG reset) → rà lại + mở wave kế (loop engineering) → teardown khi hết
---
# /next-wave — Phase NEXT-WAVE

> Khép vòng: đóng wave hiện tại + mở wave kế. **KHÔNG reset gì** — chỉ snapshot theo wave (reset = mất trí nhớ giữa wave).
> **Loop engineering**: mở wave nào phải **rà lại kế hoạch wave đó đối chiếu KẾT QUẢ wave trước** (không chạy mù kế hoạch cũ).

**Việc ĐẦU TIÊN**: sửa `STATE.md` → `Phase hiện tại: NEXT-WAVE`.

## Bước 1 — Chốt kết quả wave vừa xong
- Xác nhận đã qua VERIFY: `tracking/wave-N/test-cases.md` mọi AC **PASS** · `STATE §Findings` hết BLOCKER/MAJOR.
- (nếu wave có metric) trình Authority **go / pivot / kill** — so **số thật vs ngưỡng ghi TRƯỚC** (ở FEAT/ROADMAP), **KHÔNG chỉnh ngưỡng sau khi nhìn số** → `docs/DECISIONS.md`.
- Gom vào `docs/ROADMAP.md §backlog` **TRƯỚC khi xoá trắng STATE** (không để mất): amendment trong wave (luồng thiếu, scope mới) + **finding minor còn lại** ở §Findings + blocker treo.

## Bước 2 — Snapshot (KHÔNG reset, copy HẾT)
Copy vào `archive/wave-N/` — **snapshot TRỌN lát cắt wave, không chọn lọc** ("chép doc nào" là phán đoán sẽ mục): `STATE.md` (gate+logs) ·
`tracking/wave-N/test-cases.md` · **phần `docs/` in-scope wave**. **Lát cắt lấy từ `ROADMAP.md §1` wave-N**: cột `Target (kind)` → `arch/{target}.md` của đúng target đó · cột `AC in-scope` → các `FEAT` chứa AC đó. (Wave BE-only → chỉ `arch/backend.md` + FEAT-BE, KHÔNG kéo target khác vào.) Từ đây **BẤT BIẾN — là hợp đồng**.
- **`archive/wave-N/` tồn tại = cờ "wave đã đóng"** → có rồi thì TỪ CHỐI đóng lại (đóng 2 lần = ghi đè, mất vết).
- **Shipped surface** (test-cases PASS + `arch §API`) = hợp đồng wave sau phải giữ → wave sau **chỉ THÊM** (additive), ghi vào `docs/BACKWARD-COMPAT.md §1` (sổ tích luỹ, **không wave nào xoá**).

## Bước 3 — Dọn rác (luật #9)
- **Còn wave** → `docker compose stop` (**giữ image + volume** để wave sau khởi động nhanh, chỉ target mới/đổi build lại).
- **Hết wave** → `docker compose down --volumes`.
- Dọn build artifact tạm + screenshot/trace Playwright còn sót.

## Bước 4 — Mở wave kế HAY teardown

**Còn wave trong `docs/ROADMAP.md`:**
1. **RÀ LẠI kế hoạch wave kế** (loop engineering — bắt buộc): đọc **đủ nguồn** — kết quả wave (test-cases + metric) + `§backlog` + finding/blocker treo →
   **định đoạt RÕ TỪNG item**: `xếp wave N+1` / `hoãn (ghi lý do)` / `bỏ (ghi lý do)` — **không item nào lửng lơ** (chống backlog trôi, vá retro D1) →
   chỉnh ROADMAP wave kế nếu lệch (**phần bù chen vào wave kế, tính năng đã xếp lùi ra sau — không dồn ra cuối**) →
   ghi dòng `điều chỉnh khi mở` nếu có đổi → **stamp `Rà lại wave N+1: <ngày ISO>`** vào ROADMAP.
   *(Gate `wave_reviewed` ở `/build` đòi đúng dòng này, ngày ≥ lúc mở — thiếu = chạy mù, không cho code.)*
2. **Re-arm `BACKWARD-COMPAT.md §3`** (checklist rà mỗi wave): bỏ tick §3 để wave mới rà lại. **§1 (sổ hợp đồng) KHÔNG đụng** — surface wave 1 giao vẫn là hợp đồng ở wave 9.
3. Xoá trắng phần **wave-scoped** của `STATE.md`: gate BUILD/VERIFY + `§Findings` + 3 log → set `Wave: N+1`.
4. **Amendment thành hiện thực** (đây là điểm định tuyến của "sửa doc = wave sau" — PROTOCOL §3):
   - **Chỉ đổi thứ tự / phạm vi wave** (không đổi nội dung FEAT) → đã chỉnh ROADMAP ở 4.1 → `/build <N+1>`.
   - **Wave kế có màn UI chưa dựng mockup** (SCREEN-MAP đã khai từ DOCUMENT, mockup để trống — mockup dựng theo wave) →
     `/document` top-up: dựng mockup các màn in-scope wave kế **từ token đã chốt** → **Authority chốt mockup wave đó** → `/build`.
   - **Cần FEAT / arch / capability MỚI hoặc SỬA** → `/document` (top-up): re-enter DOCUMENT → sửa **docs SỐNG** (`docs/`)
     theo `§backlog` → re-challenge → **Authority duyệt lại = re-lock scope** (đóng back-edge — chống retro F1 kẹt DRAFT).
     · Docs đã ship ở `archive/` **BẤT BIẾN** — chỉ sửa `docs/` sống. · Đổi surface đã giao phải **additive** (BACKWARD-COMPAT §1).
     Xong `/document` → `/build`.

**Hết wave trong ROADMAP:**
- Teardown toàn bộ: `docker compose down --volumes` + dọn build artifact. Báo: **dự án xong**.
- Muốn tăng trưởng tiếp (feature mới) → `/document` top-up (đọc `§backlog`) mở kế hoạch wave mới.

## Ranh giới
- **KHÔNG reset `docs/`** — chỉ snapshot + xoá phần wave-scoped của STATE. Docs sống giữ nguyên (trí nhớ qua wave).
- **KHÔNG sửa tay / xoá `archive/`** — wave đã đóng bất biến; xoá = mất cờ "đã đóng".
- **KHÔNG bỏ qua RÀ LẠI** để mở wave cho nhanh — chạy mù kế hoạch cũ là đúng cái loop engineering chống.
- Chỉ được phá legacy wave trước nếu ROADMAP wave kế khai `legacy được phép phá` (nếu không → `guard_bc` chặn ở SHIP).
- KHÔNG đóng wave khi gate VERIFY còn đỏ.
