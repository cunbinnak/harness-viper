---
description: SHIP — (opt-in theo wave) prod-ready → deploy production → smoke → thử rollback → dogfood lần 2
---
# /ship [<wave>] — Phase SHIP  *(chỉ chạy khi ROADMAP wave khai `SHIP`)*

> Phase **opt-in**: chỉ khi `docs/ROADMAP.md` wave này khai `phases` có `SHIP`. Không khai → báo đi thẳng `/next-wave`.
> Deploy = **ngoại lệ được hỏi** (hành động ra ngoài, không đảo ngược) — xác nhận Authority trước khi đẩy production.

**Việc ĐẦU TIÊN**: kiểm ROADMAP wave có `SHIP` không? Không → **dừng**, gợi ý `/next-wave`. Có → sửa `STATE.md` → `Phase hiện tại: SHIP`.

## Bước 1 — Production-ready
`docs/PRODUCTION-READY.md` 4 nhóm xanh (secret/env · bảo mật theo `SECURITY.md` · observability · vận hành).
*(tuỳ)* spawn `reviewer`/`bug-hunter` lượt cuối — trả finding, MAIN sửa.

## Bước 2 — Backward-compat (wave ≥2)
`docs/BACKWARD-COMPAT.md §3` xanh — mọi surface đã giao vẫn **additive** (đối chiếu §1 + `arch §API`). `guard_bc` **chặn deploy** tới khi §3 xanh.

## Bước 3 — Deploy (NGOẠI LỆ ĐƯỢC HỎI)
**Xác nhận Authority** (deploy = ra ngoài, không đảo ngược) → `make deploy` → production sống → health 200.

## Bước 4 — Smoke + rollback
- Smoke test luồng lõi trên **production THẬT** (không phải staging/local).
- **Thử rollback MỘT lần** (`make doctor` + đường rollback ở deploy doc) — chưa thử = chưa chắc rollback được.

## Bước 5 — Dogfood lần 2 (trên production)
Chạy lại luồng lõi trên production (MAIN tự dùng + persona nếu cần). Phát hiện → `STATE §Findings` → sửa hoặc backlog.

## Bước cuối — Chốt
`python scripts/gate.py` (SHIP) xanh → tick gate SHIP trong `STATE.md` → gợi ý `/next-wave`.

## Ranh giới
- KHÔNG deploy khi `PRODUCTION-READY` / `BACKWARD-COMPAT §3` còn đỏ (`guard_bc` chặn ở NGUỒN).
- KHÔNG bỏ qua thử rollback — "deploy được" ≠ "rollback được".
- Deploy · đổi DNS · tiêu tiền · đăng ký dịch vụ = **hỏi thật** (ra ngoài / không đảo ngược), không tự quyết.
