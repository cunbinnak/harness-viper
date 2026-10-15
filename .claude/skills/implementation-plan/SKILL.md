---
name: implementation-plan
description: Phương pháp chia wave cho /document — plan toàn dự án vào docs/ROADMAP.md §1 (wave + phases + phụ thuộc + legacy)
---

# Chia-wave Method (bước chia wave của /document)

> **Vai: PM** · **Viết**: `docs/ROADMAP.md` · cột Wave giao (CAPABILITIES-MAP) · cột Wave (SCREEN-MAP)
> **KHÔNG viết**: nội dung FEAT / AC / arch — FEAT quá to cần tách thì báo PO

## Khi dùng
Bước chia wave của `/document` — vai **program planner**. Sau khi FEAT (`docs/feat/`) + architecture (`docs/arch/`) đủ.
Input: `docs/PRD.md` + `docs/feat/*` (AC + §3 Ràng buộc nghiệp vụ) + `docs/arch/OVERVIEW.md` + `docs/arch/{name}.md` (kind/stack/consumes) + `docs/CAPABILITIES-MAP.md` (persona × capability → wave giao).

## Wave = sprint — dự án chia thành NHIỀU wave
- **1 wave = 1 sprint** giao được 1 lát sản phẩm chạy end-to-end.
- **Dự án luôn chia thành nhiều wave** (≥ 2 khi có phụ thuộc) — KHÔNG gom hết mọi target/FEAT vào 1 wave.
- **Wave sau phụ thuộc wave trước**: vd `order` chờ `auth` + `catalog`; `payment` chờ `order`; `customer-app` chờ API order/catalog.
- **Sinh FULL PLAN toàn dự án** ngay từ đầu: mọi wave khai trong `docs/ROADMAP.md §1`.

## Deliverable
1. **`docs/ROADMAP.md §1`** (copy từ `templates/TEMPLATE.roadmap.md` — frontmatter `feat_cap_per_wave` sẵn; **số wave = số dòng §1**) — roadmap toàn dự án: chia **toàn bộ** target/FEAT thành **nhiều wave** theo phụ thuộc. Mỗi wave khai:
   - đúng cột `TEMPLATE.roadmap.md §1`: **Target (kind)** (name từ `docs/arch/`) · **AC in-scope** (FEAT-id/AC) · **phases** (BUILD,VERIFY[,SHIP]) · **Phụ thuộc wave trước** (cần gì từ wave trước) · **Legacy được phép phá** · **Rà lại** · **Trạng thái**.
   - Wave nào **opt-in SHIP** → cột `phases` thêm `SHIP` (mặc định không ship).
   - Cột **AC in-scope** ghi rõ FEAT + AC của ĐÚNG wave đó (`FEAT-x AC-1..3`) — 1 target sống qua ≥2 wave thì mỗi wave chỉ liệt kê AC của nó (tránh AC wave sau lọt vào scope wave hiện tại; gate VERIFY đọc cột này để đếm AC).
2. **`docs/ROADMAP.md §backlog`** — chỗ chứa scope hoãn / phát sinh sau (sửa doc đã chốt = wave sau đổ về đây).

## Phương pháp chia wave (giá trị — giữ nguyên)
1. **Map FEAT → target**: từ `docs/arch/` (kind/consumes) + decomposition.
2. **Dựng đồ thị phụ thuộc** target/FEAT (`depends_on` từ `docs/arch/{name}.md consumes` + OVERVIEW): cái gì cần cái gì ready trước.
3. **Topological → wave** (sprint):
   - **Wave 1 = foundation mỏng** (auth/shared + 1–2 capability core) đủ chạy **E2E sớm** (login + 1 luồng nghiệp vụ chính).
   - **Wave kế** = target/FEAT phụ thuộc wave trước, nhóm theo lát giá trị ship được cùng nhau; ghi rõ `dependencies` từ wave trước.
   - **Kích thước wave: ~3-4 FEAT/wave** (`feat_cap_per_wave`, frontmatter `ROADMAP.md`, không khai → mặc định **4**; đối chiếu ≈15-20 AC — **1 FEAT quá to (nhiều AC) thì báo PO tách**, PM không tự tách). Mỗi wave là một vòng đầy đủ build → review → dựng Docker → test → dogfood 6 vai × 2 đợt: ngưỡng quá nhỏ đẻ hàng chục wave nuốt hết thời gian, quá lớn thì vỡ context 1 phiên BUILD của MAIN.
     - **Ngưỡng là KHUYẾN KHÍCH, luồng mới là luật.** Tách ra mà **đứt luồng** (nửa luồng ở wave này, nửa kia wave sau, không demo được luồng nào trọn) → **giữ tròn luồng**, vượt ngưỡng cũng được — ghi 1 dòng `docs/DECISIONS.md` (loại `kỹ-thuật`) nói luồng nào sẽ đứt nếu tách.
     - "Nhét cho gọn số wave" KHÔNG phải lý do. Ít quá (1 FEAT lẻ) không cần tách.
   - Lặp tới khi **mọi** target/FEAT đã vào 1 wave.
4. **Viết ROADMAP §1** đủ mọi wave — đúng các cột của `TEMPLATE.roadmap.md §1`, không thêm trường ngoài template.

## Chia lại sau khi đã chạy wave (giá trị — giữ nguyên)
Kế hoạch không cố định. Chạy xong wave k (`/next-wave` đã lưu `archive/wave-k/`) mà phát hiện thiếu → quay lại `/document` bổ sung, rồi tới đây **chia lại**. Nhận biết: có thư mục `archive/wave-*`. Wave kế = wave đóng gần nhất + 1.

**Phần bù CHEN VÀO NGAY WAVE KẾ, tính năng đã xếp LÙI DẦN ra sau.** Không gom phần bù thành một wave cuối — các wave giữa sẽ xây trên nền đang thiếu, luồng đứt.

```
Kế hoạch cũ          Sau khi chia lại (vừa đóng wave 2, phát hiện thiếu X)
wave 3: A, B, C      wave 3: X, A, B     ← X chen vào wave kế
wave 4: D, E         wave 4: C, D        ← C bị đẩy xuống
                     wave 5: E           ← tràn qua wave cuối → sinh wave mới
```

1. **Wave đã đóng bất biến** — không đổi FEAT của wave ≤ k. Cần sửa thứ đã giao → phần bù (FEAT mới, hoặc thêm AC vào FEAT cũ) xếp vào wave kế; đổi surface đã giao = **additive** (`docs/BACKWARD-COMPAT.md`).
2. **Phần bù** = FEAT mới + FEAT đã giao có AC mới → đặt ở **wave k+1**. Đặt xa hơn chỉ khi có lý do thật — ghi 1 dòng `ROADMAP §2 Điều chỉnh khi mở wave` (cột Đổi gì · Vì sao), vd `FEAT-hrm-044 → wave 5 · cần FEAT-hrm-031 (bảng lương) giao ở wave 4 mới tính được`.
3. **Đẩy lùi giữ luật chia wave** — thứ tự phụ thuộc, ngưỡng AC (khuyến khích; tròn luồng thắng con số). Tràn → thêm dòng wave mới ở cuối ROADMAP §1.
4. **Không rơi mất** — mọi FEAT đã xếp wave sau trong kế hoạch cũ phải còn chỗ, hoặc vào `§backlog` kèm lý do đề xuất hoãn/bỏ — **PO** đổi `status: deferred|dropped` ở FEAT (PM không sửa FEAT). Nguồn phần bù cần quét: `docs/ROADMAP.md §backlog` (gồm `nghi thiếu AC` · `CHƯA CÓ QUY ĐỊNH` gom từ VERIFY), `STATE.md §Blocker` / `§Findings` của wave vừa đóng (trong `archive/wave-N/STATE.md`), chỗ thiếu người vận hành báo.

## Quality checklist
- [ ] ROADMAP §1 phủ **100% target + FEAT** (không sót, KHÔNG gom hết vào 1 wave). FEAT không nằm trong cột AC in-scope của wave nào = MỒ CÔI (chủ động hoãn/bỏ → vào §backlog, PO đổi `status` FEAT).
- [ ] Cột `Phụ thuộc wave trước` / `Legacy được phép phá` mỗi wave khớp `consumes` trong `docs/arch/{name}.md` + OVERVIEW — cạnh gọi nhau phải có contract doc ghi nhận.
- [ ] Mỗi capability (`CAPABILITIES-MAP`) có wave; không capability mồ côi.
- [ ] Chia **≥ 2 wave** khi có phụ thuộc; thứ tự topological (không phụ thuộc ngược/vòng).
- [ ] Mỗi wave điền đủ các cột template: Target (kind) · AC in-scope · phases · **Phụ thuộc wave trước** · Legacy được phép phá.
- [ ] Wave 1 mỏng, chạy được **E2E** (foundation + 1 lát core).
- [ ] Mỗi wave trong ngưỡng `feat_cap_per_wave` (~3-4 FEAT). Vượt vì tách sẽ đứt luồng → 1 dòng `DECISIONS.md` nêu lý do.
- [ ] Chia lại sau khi đóng wave (có `archive/wave-*`): wave đã đóng không đổi · phần bù ở wave kế (đặt xa hơn → dòng `ROADMAP §2` nêu lý do) · không FEAT nào rơi mất.
- [ ] **Hoãn tường minh**: AC/NFR chủ động hoãn (auth/idempotency/event ở wave CRUD…) → KHÔNG ghi vào cột AC in-scope wave đó + 1 dòng `ROADMAP §3 Backlog` (cột Xử = wave dự kiến). AC đã ghi in-scope thì phải có TC PASS ở VERIFY — không có "hoãn ngầm để test bỏ qua".
- [ ] **Không `TBD` / section trống mơ hồ** — chỗ chưa chốt ghi `Open question` (cần ai quyết + vì sao) hoặc dòng `docs/DECISIONS.md`.

## Done
- `docs/ROADMAP.md §1` đủ mọi wave (đúng cột template) + §backlog + cột Wave giao (CAPABILITIES) + cột Wave (SCREEN-MAP). Tiếp: có UI → quay Bước 8 dựng mockup wave 1 → Bước 10 challenge → khoá scope → `/build`.
