---
description: SHIP — (opt-in theo wave) prod-ready → deploy production → smoke → thử rollback
---
# /ship [<wave>] — Phase SHIP  *(chỉ chạy khi ROADMAP wave khai `SHIP`)*

> Phase **opt-in**: chỉ khi `docs/ROADMAP.md` wave này khai `phases` có `SHIP`. Không khai → báo đi thẳng `/next-wave`.
> Deploy = **ngoại lệ được hỏi** (hành động ra ngoài, không đảo ngược) — xác nhận Authority trước khi đẩy production.
> **Target desktop**: không deploy lên server — Bước 3 `make deploy` = **phát hành bản mới** (bộ cài lên nơi phát hành theo ADR) · Bước 4 smoke = cài bản vừa phát hành trên máy giả lập sạch (nếu có) + `--smoke` · **rollback = phát hành lại bản trước**. PRODUCTION-READY thêm nhóm 5 *Phát hành desktop*.

**Việc ĐẦU TIÊN**: kiểm ROADMAP wave có `SHIP` không? Không → **dừng**, gợi ý `/next-wave`. Có → sửa `STATE.md` → `Phase hiện tại: SHIP`.

## Bước 1 — Production-ready
`docs/PRODUCTION-READY.md` 4 nhóm xanh (secret/env · bảo mật theo `SECURITY.md` · observability · vận hành · *phát hành desktop* nếu có target desktop) — mục *(sau deploy)* tick sau Bước 4 (gate SHIP đòi đủ).
*(tuỳ)* spawn `reviewer`/`bug-hunter` lượt cuối — trả finding, MAIN sửa.

## Bước 2 — Backward-compat (wave ≥2)
`docs/BACKWARD-COMPAT.md §3` xanh — mọi surface đã giao vẫn **additive** (đối chiếu §1 + `arch §API`). `guard_bc` **chặn deploy** tới khi §3 xanh.

## Bước 3 — Deploy (NGOẠI LỆ ĐƯỢC HỎI)
**Xác nhận Authority** (deploy = ra ngoài, không đảo ngược) → `make deploy` → production sống → health 200.

## Bước 4 — Smoke + rollback
- Smoke test luồng nghiệp vụ trên **production THẬT** (không phải staging/local). Dùng tài khoản và dữ liệu thử gỡ được, hoặc chỉ đi luồng đọc; ghi cách dọn dữ liệu smoke vào báo cáo.
- **Thử rollback MỘT lần** theo đường rollback ghi ở `docs/arch/OVERVIEW.md §5.8` → `make doctor` kiểm hệ sau rollback — chưa thử = chưa chắc rollback được.

## Bước cuối — Chốt
`python scripts/gate.py` (SHIP) xanh → tick gate SHIP trong `STATE.md` → gợi ý `/next-wave`.

## Ranh giới
- KHÔNG deploy khi `PRODUCTION-READY` / `BACKWARD-COMPAT §3` còn đỏ (`guard_bc` chặn ở NGUỒN).
- KHÔNG bỏ qua thử rollback — "deploy được" ≠ "rollback được".
- Deploy · đổi DNS · tiêu tiền · đăng ký dịch vụ = **hỏi thật** (ra ngoài / không đảo ngược), không tự quyết.
