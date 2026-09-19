---
name: implementation-plan
description: Phương pháp chia wave cho /document — plan toàn dự án vào docs/ROADMAP.md §1 (wave + phases + phụ thuộc + legacy) + KG skeleton knowledge-base/{name}.md. Nhiều wave=sprint phụ thuộc nhau.
---

> Phương pháp cho /document (fork gộp DOMAIN/DESIGN/PLAN vào DOCUMENT, 1 lớp doc). Không stage riêng, không translate.

# Chia-wave Method (bước chia wave của /document)

## Khi dùng
Bước chia wave của `/document` — vai **program planner**. Sau khi FEAT (`docs/feat/`) + architecture (`docs/arch/`) đủ.
Input: `docs/PRD.md` + `docs/feat/*` (AC + business-rule + field kỹ thuật) + `docs/arch/OVERVIEW.md` + `docs/arch/{name}.md` (kind/stack/consumes) + `docs/CAPABILITIES-MAP.md` (persona × capability → wave giao).

## Wave = sprint — dự án chia thành NHIỀU wave
- **1 wave = 1 sprint** giao được 1 lát sản phẩm chạy end-to-end.
- **Dự án luôn chia thành nhiều wave** (≥ 2 khi có phụ thuộc) — KHÔNG gom hết mọi target/FEAT vào 1 wave.
- **Wave sau phụ thuộc wave trước**: vd `order` chờ `auth` + `catalog`; `payment` chờ `order`; `customer-app` chờ API order/catalog.
- **Sinh FULL PLAN toàn dự án** ngay từ đầu: mọi wave khai trong `docs/ROADMAP.md §1`.

## Deliverable
1. **`docs/ROADMAP.md §1`** (copy từ `templates/TEMPLATE.roadmap.md` — frontmatter `feat_cap_per_wave` sẵn; **số wave = số dòng §1**) — roadmap toàn dự án: chia **toàn bộ** target/FEAT thành **nhiều wave** theo phụ thuộc. Mỗi wave khai:
   - `goal` + `targets[]` (name từ `docs/arch/`) + `features[]` (FEAT-id) + `phases` (thứ tự dev trong wave: foundation trước) + **`dependencies` (cần gì từ wave trước)** + `legacy` (surface đã giao ở wave trước mà wave này build tiếp — additive) + `exit_criteria`.
   - Wave nào **opt-in SHIP** → khai `ship: true` (mặc định không ship).
   - `features_by_wave`: nếu 1 target sống qua ≥2 wave, tách rõ FEAT nào thuộc wave nào (tránh FEAT wave sau lọt vào scope wave hiện tại).
2. **`docs/ROADMAP.md §backlog`** — chỗ chứa scope hoãn / phát sinh sau (sửa doc đã chốt = wave sau đổ về đây).
3. **KG skeleton per target** — `knowledge-base/{name}.md` (chỉ metadata; section va-vấp còn RỖNG). **KHÔNG điền entities/rules/events** — docs còn sửa qua `/document`. Phần va vấp do MAIN append lúc BUILD/VERIFY.

## Phương pháp chia wave (giá trị — giữ nguyên)
1. **Map FEAT → target**: từ `docs/arch/` (kind/consumes) + FEAT `epic` + decomposition.
2. **Dựng đồ thị phụ thuộc** target/FEAT (`depends_on` từ `docs/arch/{name}.md consumes` + OVERVIEW): cái gì cần cái gì ready trước.
3. **Topological → wave** (sprint):
   - **Wave 1 = foundation mỏng** (auth/shared + 1–2 capability core) đủ chạy **E2E sớm** (login + 1 luồng nghiệp vụ chính).
   - **Wave kế** = target/FEAT phụ thuộc wave trước, nhóm theo lát giá trị ship được cùng nhau; ghi rõ `dependencies` từ wave trước.
   - **Kích thước wave: ~3-4 FEAT/wave** (`feat_cap_per_wave`, frontmatter `ROADMAP.md`, không khai → mặc định **4**; đối chiếu ≈15-20 AC — **1 FEAT quá to (nhiều AC) thì tách nhỏ**). Mỗi wave là một vòng đầy đủ build → review → dựng Docker → test → dogfood 6 vai × 2 đợt: ngưỡng quá nhỏ đẻ hàng chục wave nuốt hết thời gian, quá lớn thì vỡ context 1 phiên BUILD của MAIN.
     - **Ngưỡng là KHUYẾN KHÍCH, luồng mới là luật.** Tách ra mà **đứt luồng** (nửa luồng ở wave này, nửa kia wave sau, không demo được luồng nào trọn) → **giữ tròn luồng**, vượt ngưỡng cũng được — ghi `rationale` (≥20 ký tự) nói luồng nào sẽ đứt nếu tách.
     - "Nhét cho gọn số wave" KHÔNG phải lý do. Ít quá (1 FEAT lẻ) không cần tách.
   - Lặp tới khi **mọi** target/FEAT đã vào 1 wave.
4. **Viết ROADMAP §1** đủ mọi wave (goal/targets/features/phases/dependencies/legacy/exit_criteria).
5. **KG skeleton** per target.

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
2. **Phần bù** = FEAT mới + FEAT đã giao có AC mới → đặt ở **wave k+1**. Đặt xa hơn chỉ khi có lý do thật — ghi `placement_rationale` trong wave của ROADMAP:
   ```yaml
   placement_rationale:
     FEAT-hrm-044: "cần FEAT-hrm-031 (bảng lương) giao ở wave 4 mới tính được"
   ```
3. **Đẩy lùi giữ luật chia wave** — thứ tự phụ thuộc, ngưỡng AC (khuyến khích; tròn luồng thắng con số). Tràn → thêm wave mới ở cuối (ROADMAP §1 + `features_by_wave`).
4. **Không rơi mất** — mọi FEAT đã xếp wave sau trong kế hoạch cũ phải còn chỗ, hoặc ghi `status: deferred|dropped` ở FEAT kèm lý do. Nguồn phần bù cần quét: `tracking/wave-*/dogfood-report.md` dòng `wave sau`, `STATE.md §Blocker`, chỗ thiếu người vận hành báo.

## Quality checklist
- [ ] ROADMAP §1 phủ **100% target + FEAT** (không sót, KHÔNG gom hết vào 1 wave). FEAT không nằm trong `features[]` wave nào = MỒ CÔI (chủ động hoãn/bỏ → frontmatter FEAT `status: deferred|dropped` + vào §backlog).
- [ ] `dependencies`/`legacy` mỗi wave khớp `consumes` trong `docs/arch/{name}.md` + OVERVIEW — cạnh gọi nhau phải có contract doc ghi nhận.
- [ ] Mỗi capability (`CAPABILITIES-MAP`) có wave; không capability mồ côi.
- [ ] Chia **≥ 2 wave** khi có phụ thuộc; thứ tự topological (không phụ thuộc ngược/vòng).
- [ ] Mỗi wave có goal + targets + features + phases + **dependencies từ wave trước** + exit_criteria.
- [ ] Wave 1 mỏng, chạy được **E2E** (foundation + 1 lát core).
- [ ] Mỗi wave trong ngưỡng `feat_cap_per_wave` (~3-4 FEAT). Vượt vì tách sẽ đứt luồng → điền `rationale`.
- [ ] Chia lại sau khi đóng wave (có `archive/wave-*`): wave đã đóng không đổi · phần bù ở wave kế (hoặc `placement_rationale`) · không FEAT nào rơi mất.
- [ ] **Deferred-scope tường minh**: AC/feature chủ động hoãn (auth/idempotency/event ở wave CRUD…) ghi vào wave §Deferred (token `FEAT-NNN[:AC-M]`/`BR-NNN`) — SoT để test skip.
- [ ] KG skeleton mọi target (`knowledge-base/{name}.md`, metadata; section va-vấp rỗng).
- [ ] **Không `TBD` / section trống mơ hồ** — chỗ chưa chốt ghi `Open question` (cần ai quyết + vì sao) hoặc dòng `docs/DECISIONS.md`.

## Done
- `docs/ROADMAP.md §1` đủ mọi wave (goal/targets/features/phases/dependencies/legacy/exit_criteria) + §backlog + KG skeleton mọi target. Tiếp: **khoá scope** (kết `/document`) → `/build`.
