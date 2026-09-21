---
description: VERIFY — code review + auto-test (black-box) + dogfood 6 persona → MAIN sửa finding tới sạch
---
# /verify [<wave>] — Phase VERIFY

> Kiểm trên hệ **ĐANG CHẠY** (BUILD đã đưa hệ chạy thật theo `kind`). Agent (review + persona) **CHỈ trả finding — MAIN sửa**.
> Không hỏi Authority (mơ hồ → `DECISIONS.md` · ngoài scope → `ROADMAP §backlog` · chặn cứng → `STATE §Blocker`).

**Việc ĐẦU TIÊN**: sửa `STATE.md` → `Phase hiện tại: VERIFY`.

## Bước 1 — Nạp + xác nhận hệ đang chạy
- `docs/ROADMAP.md` wave-N (AC in-scope) + `docs/feat/FEAT-*` (AC + ca biên) + `docs/CONVENTIONS.md §API` + `arch/{name}.md` (**`kind`** + §API)
- Hệ chạy thật (từ BUILD), theo `kind`: backend/bff → `docker ps` + health 200 · web → dev server chạy · mobile → emulator. Chưa chạy → đưa lên trước.

## Bước 2 — Code review (2 vai mắt-tươi, checklist đúng `kind` — KHÔNG sửa)
Spawn 2 agent, **chỉ đọc code, trả finding** — hai vai soi hai câu hỏi KHÁC nhau:
> **Cả 2 agent nạp thêm skill `review-<kind>`** (review-backend/web/bff/mobile — checklist review theo `kind` của target đang review) BÊN CẠNH `stack-<x> §review`.

**`reviewer` — code có AN TOÀN chạy + BẢO TRÌ được không?** (senior/team-lead, **2 trục** — chi tiết `.claude/agents/reviewer.md`)
- **Trục A · An toàn/đúng** (hỏng = hại NGAY → BLOCKER/MAJOR): bảo mật (secret · validate **server** · SQL nối chuỗi · lộ entity/lỗi nội bộ) · phân quyền dữ liệu (id kèm owner/tenant) · **forbidden patterns** stack · toàn vẹn transaction · lệch `DECISIONS`/`arch` đã chốt.
- **Trục B · Bảo trì/nhất quán** (vẫn chạy nhưng đắt MAI SAU → MAJOR/MINOR, **không chặn**): cấu trúc khớp **kiến trúc đã chốt** (`arch §4` — Layered/DDD, không trộn) · convert DTO map tay nhiều → MapStruct · logic đúng tầng · naming khớp Glossary · **chất lượng test**. Chỉ báo khi nêu **chi phí bảo trì cụ thể**; style tùy-ca (`var`…) **mặc định tha**.

**`bug-hunter` — code có LÀM ĐÚNG như DOC không?** (đối chiếu spec, soi theo thứ tự)
1. Mỗi AC in-scope → tìm code hiện thực: **có tồn tại? đúng mô tả? hay chỉ nửa vời?**
2. Mỗi ca biên trong AC → tìm chỗ code chặn. **Chặn ở UI (disable nút) KHÔNG TÍNH — phải ràng buộc DB hoặc kiểm ở server.**
3. Phân quyền: **mọi truy vấn lấy bản ghi theo id có kèm điều kiện chủ sở hữu không?** (lỗ hay gặp + nặng nhất)
4. Việc dở (TODO/FIXME) chặn AC · lỗi bị nuốt (`catch{}` rỗng) · secret hardcode

**Cả hai** → `STATE.md §Findings`, format `[nặng/vừa/nhẹ] (+trục A|B nếu reviewer) + file:dòng + "hỏng/tốn thế nào" + đề xuất 1 câu`.
- **Trục A · bug-hunter**: chỉ nêu **hậu quả THẬT** (mất/lộ dữ liệu · sai kết quả · chặn AC).
- **Trục B**: nêu **chi phí bảo trì CỤ THỂ** — **vẫn cấm** khẩu vị thuần (tên đẹp không lý do · abstraction "để sau" · perf chưa đo · coverage%) + style tùy-ca **tha**.
- **"Trục nào ổn → nói ổn, đừng bịa finding."** Lệnh `grep` cụ thể ở `.claude/agents/reviewer.md` · `bug-hunter.md`.
Học được điều mới về target → append `knowledge-base/{name}.md`.

## Bước 3 — Thiết kế + chạy test case (black-box)

### 3a — THIẾT KẾ (dẫn xuất từ AC — ưu-tiên-trước-phủ-sau)
Điền `tracking/wave-N/test-cases.md` (`TC | AC | mô tả | cách chạy | kết quả | nguyên nhân`), kết quả = "chưa chạy".
Thứ tự **ưu tiên** (VIPER "ít test đúng chỗ" — hết giờ vẫn có cái giá trị nhất):
1. **Smoke luồng lõi** — 1 TC đi hết luồng chính đầu→cuối (giá trị hơn 50 TC vụn)
2. **Tiền / dữ liệu** — tính tiền · trừ kho · huỷ/hoàn · xoá · cập nhật đồng thời
3. **Ca biên** trong AC — đặc biệt **gửi 2 lần** (lần 2 KHÔNG tạo bản ghi trùng)
4. **Phân quyền** — B không chạm dữ liệu A. **Chặn ở UI KHÔNG TÍNH → phải server/DB** (mỗi ô `cấm` ma trận vai = 1 TC âm)
5. **Validate đầu vào** — rỗng · quá dài · sai kiểu · số âm
+ **Phủ doanh nghiệp** (đan vào): tenant isolation · idempotency · rate limit · concurrency · **contract-test** (consumer gọi provider THẬT, đối chiếu `arch §API`)

Tên TC nói **hỏng gì khi đỏ** ("2 order cùng bàn", không "test order 2").

### 3b — CHẠY (black-box, hệ đang chạy)
Chạy từng TC qua giao diện THẬT (API `curl`/REST · UI Playwright · perf k6) → điền `kết quả` PASS/FAIL + nguyên nhân **tại dòng**.
`make test` xanh (unit/integration trong source, MAIN đã viết ở BUILD). **KHÔNG sửa source để test xanh** (→ Bước 5).
*(tuỳ)* spawn `test-writer` viết thêm test adversarial cho AC dễ vỡ (nó sửa được **thư mục test**, KHÔNG sửa product code).

## Bước 4 — Dogfood (2 đợt — hệ đang chạy)
6 persona (mỗi vai đóng 1 persona THẬT ở `docs/PERSONAS.md`), **2 đợt tránh đè trạng thái** (server + DB dùng chung):
- **Đợt 1 (DB sạch)**: `edge` (rỗng/lỗi) · `newbie` · `picky` (đo giao diện thật vs mockup + token)
- **seed lại** `deployment/local/`
- **Đợt 2 (DB có data)**: `rushed` · `breaker` (chạy đủ **ma trận vai×hành động**) · `mobile`

+ MAIN **tự dùng** đi hết luồng lõi ở localhost (qua Playwright/trình duyệt). Phát hiện → `STATE.md §Findings` (Nguồn = tên vai).

## Bước 5 — Sửa tới sạch (MAIN)
- TC **FAIL** hoặc finding **BLOCKER/MAJOR** → **MAIN sửa code** → **re-run** TC + dogfood liên quan → cập nhật
  `test-cases.md` thành PASS, đánh dấu finding đã xử.
- **Không hội tụ** — finding mới cứ nảy sau **~3 vòng** sửa→re-test → DỪNG, ghi `STATE.md §Blocker`, báo cuối buổi (đừng sửa vô hạn — max-turns safety, học từ loop-engineering).
- Nhỏ / ngoài scope → `docs/ROADMAP.md §backlog` (wave sau).
- `git commit` sau mỗi fix. Học được gì mới → `knowledge-base/{name}.md`.

## Bước cuối — Chốt
1. `tracking/wave-N/test-cases.md`: mọi AC in-scope có TC **PASS**, không TC **FAIL**.
2. `STATE.md §Findings`: hết finding **BLOCKER/MAJOR** open.
3. `python scripts/gate.py` (VERIFY) xanh → tick gate VERIFY → gợi ý `/ship` (nếu wave khai SHIP) hoặc `/next-wave`.

## Ranh giới
- **KHÔNG build/sửa source để test qua** — test black-box đo hành vi thật; lỗi thì sửa ở Bước 5 rồi re-test.
- Agent (review/persona) **chỉ trả finding** — chỉ MAIN sửa (giữ "mắt tươi" độc lập).
- Không thả 6 persona cùng lúc (đè trạng thái nhau + trạng thái rỗng chết khi có bản ghi đầu tiên).
- **Dọn rác**: screenshot/trace/video Playwright chụp để phân tích → **xoá sau khi xong**, KHÔNG commit, để scratch dir (không tích tụ). Seed test-data → cleanup cuối phase. test-logs/k6 output → archive theo wave hoặc xoá.
