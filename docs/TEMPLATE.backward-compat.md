<!-- gate bỏ qua TEMPLATE.* — copy thành docs/BACKWARD-COMPAT.md. Sổ hợp đồng surface đã giao. -->
# BACKWARD-COMPAT — {{PROJECT_NAME}}

<!-- §1: SỔ HỢP ĐỒNG — surface đã ship (API/bảng/event/webhook/format export). TÍCH LUỸ VĨNH VIỄN, không wave nào xoá.
     Mỗi surface TRỎ VỀ `arch/<target>.md §3 API` (nguồn contract — G4). Thêm dòng khi ship, KHÔNG xoá dòng cũ. -->
## §1 Sổ hợp đồng (tích luỹ)
| Surface | Loại | Nguồn (arch §3 API) | Wave giao | Ghi chú |
|---|---|---|---|---|
| `POST /orders` | API | `arch/order-service.md §3` | 1 | |

<!-- §2: luật đổi surface đã giao — additive-first. -->
## §2 Luật additive-first
- **API**: thêm field optional OK · đổi/xoá field đang dùng đi **2 bước** (thêm mới → chuyển dữ liệu → wave sau mới xoá).
- **DB**: thêm bảng / cột nullable / index OK · đổi/xoá cột đang dùng đi 2 bước.
- **Event / webhook / format export**: y hệt — thêm được, đổi/xoá phải migrate + ghi `DECISIONS.md` + đường rollback.

<!-- §3: CHECKLIST rà mỗi wave (≥2). /next-wave RE-ARM (bỏ tick §3, KHÔNG đụng §1). guard_bc chặn deploy tới khi §3 xanh. -->
## §3 Checklist rà tương thích (wave hiện tại)
- [ ] Mọi surface §1 mà wave này ĐỤNG vẫn additive (đối chiếu §2)
- [ ] TC / contract-test của consumer cũ vẫn **PASS** (regression)
- [ ] Đổi/xoá surface đang dùng → có khai ở `ROADMAP §1 Legacy được phép phá` + đường di trú
