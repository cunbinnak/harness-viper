# STATE — {{PROJECT_NAME}}

> Trạng thái sống. Người + agent cùng đọc/ghi. Đổi phase hoặc tick gate là cập nhật NGAY.
> Định nghĩa CHUẨN của phase + gate ở [PROTOCOL.md](PROTOCOL.md) — lệch nhau thì sửa chỗ này cho khớp.

```
Phase hiện tại  : DOCUMENT
Wave            : —            (DOCUMENT xong mới chia wave)
Đường vào       : —            (interview | intake — chốt ở DOCUMENT Bước 0;
                                nguồn sự thật = marker "NGUỒN: INTAKE" trong docs/INTERVIEW.md)
Stack           : —            (chốt ở DOCUMENT → docs/TECHSTACK.md)
Phases wave này : —            (khai khi mở wave: BUILD,VERIFY[,SHIP])
URL local       : —
URL production  : —
```

> **Wave** = một lượt BUILD→VERIFY→(SHIP). Mở wave kế bằng `/next-wave` — KHÔNG reset, chỉ
> snapshot theo wave. DOCUMENT chạy 1 lần cho cả dự án (wave sau thiếu gì thì top-up).

---

## Gate

> Bản thao tác — checkbox tick tay khi đạt. `gate.py` đọc dòng "Phase hiện tại" rồi chấm đúng phase đó.
> BUILD / VERIFY / SHIP là **WAVE-SCOPED** (của wave đang mở); `/next-wave` snapshot rồi **xoá trắng**
> phần này cho wave kế. DOCUMENT tick **1 lần** cho cả dự án.

### DOCUMENT — rời phase khi:
- [ ] Đường vào xác định (Bước 0):
      · (INTERVIEW) `docs/INTERVIEW.md` đủ dòng bằng chứng — từ phỏng vấn Authority
      · (INTAKE) `intake/*.md` render thật + marker `NGUỒN: INTAKE` + bảng truy vết intake→FEAT
- [ ] `docs/PRD.md`: vấn đề + đối tượng + out-of-scope + ≥1 success metric có số
- [ ] `docs/PERSONAS.md`: persona + ma trận vai×hành động (không ô trống)
- [ ] `docs/CAPABILITIES-MAP.md`: capability→outcome→FEAT; mọi FEAT truy về 1 capability
- [ ] `docs/feat/FEAT-*.md`: mỗi FEAT có AC (BDD, **gồm ca biên**) + field kỹ thuật (enforcement/consumes) điền
- [ ] `docs/arch/OVERVIEW.md` + `docs/arch/{name}.md`: frontmatter **`kind`/`stack`/`consumes`** + data model + luồng + API + §ranh-giới (**per target**)
- [ ] `docs/TECHSTACK.md` chốt + 1 dòng lý do ở `docs/DECISIONS.md`
- [ ] `docs/CONVENTIONS.md` + `docs/SECURITY.md` (**framework có sẵn**) — rà; chỉnh §API error-envelope/header nếu project khác default
- [ ] Design system: có UI → `docs/DESIGN-SYSTEM.md` (token) + `docs/ux/` (SCREEN-MAP + mockups)
      khoá TRƯỚC, Authority chốt · backend-only → marker `KHÔNG CÓ UI`
- [ ] `docs/ROADMAP.md`: chia wave; mỗi wave khai **target** + **phases chạy** (BUILD,VERIFY[,SHIP])
- [ ] Challenge DOCUMENT **PASS** (≥3 câu khó, trả lời CHỈ bằng tài liệu) — §Challenge log
- [ ] ≥2 dòng `docs/DECISIONS.md`
- [ ] **Scope khoá** — từ đây không hỏi Authority nữa (trừ ngoại lệ "hỏi thật", xem PROTOCOL §3)

### BUILD (wave hiện tại) — rời phase khi:
- [ ] Đã set `Phase hiện tại: BUILD` (việc ĐẦU TIÊN khi vào phase)
- [ ] Đọc `knowledge-base/{name}.md` nếu có → áp lại §Invariants/§Gotchas (chống lặp bug cũ)
- [ ] Challenge **PASS** (trước dòng code đầu) — §Challenge log
- [ ] `make dev` · `make check` · `make migrate` có thân
- [ ] Walking skeleton: app+db lên · health 200 · 1 thao tác ghi→đọc DB được (dù xấu)
- [ ] Luồng lõi end-to-end bấm được ở local (theo AC in-scope wave)
- [ ] `make check` xanh + health 2xx → **`python scripts/capture_proof.py`** sinh `proof.json` (gate đọc, MÁY-verify không tin tick)
- [ ] **Đã commit code** (ngoài commit khởi tạo) — build/test pass mà không commit = coi như CHƯA làm
- [ ] Chạy thật: `docker up`, health 200 (để VERIFY có hệ mà đánh)

### VERIFY (wave hiện tại) — rời phase khi:
- [ ] **auto-test**: `tracking/wave-N/test-cases.md` — mọi AC in-scope có TC **PASS**, không TC **FAIL** · black-box hệ đang chạy · `make test` xanh · contract-test cho consumer
- [ ] **dogfood**: 6 persona 2 đợt (DB sạch / DB có data) + tự dùng · phát hiện đã xử hoặc đã ghi §Dogfood
- [ ] Không còn finding BLOCKER/MAJOR open

### SHIP (chỉ khi `Phases wave này` có SHIP) — rời phase khi:
- [ ] `docs/PRODUCTION-READY.md` 4 nhóm xanh
- [ ] `docs/BACKWARD-COMPAT.md` xanh (wave ≥2) — `guard_bc` chặn deploy tới khi xanh
- [ ] `make deploy` · `make doctor` có thân · production sống · smoke pass · đã **thử** rollback
- [ ] dogfood lần 2 trên production

### NEXT-WAVE — rời phase khi:
- [ ] go/pivot/kill ghi `docs/DECISIONS.md` (nếu wave có metric)
- [ ] `docs/ROADMAP.md §backlog` đã gộp phát sinh của wave này (amendment → wave sau)
- [ ] Snapshot STATE.md + docs của wave → `archive/wave-<N>/` (KHÔNG reset)
- [ ] Mở wave kế (xoá trắng gate BUILD/VERIFY + 3 log dưới) · hết wave → teardown

---

## Challenge log
> Meta ra câu hỏi khó dựa trên context, chấm PASS/FAIL. DOCUMENT: ≥3 câu trước khi khoá scope.
> BUILD: trước mỗi mảng việc lớn. FAIL → đọc lại context, trả lời lại, KHÔNG được code.
> (Của wave đang mở — `/next-wave` snapshot rồi xoá.)

| Ngày | Phase | Câu hỏi khó | PASS/FAIL | Ghi chú |
|---|---|---|---|---|

## Blocker
> Chặn cứng SAU KHI đã tự thử hết cách. Không hỏi giữa chừng — dồn vào đây, báo gộp cuối buổi.
> Cột "Đã thử gì" trống = chưa phải blocker.

| Ngày | Blocker | Đã thử gì | Trạng thái |
|---|---|---|---|

## Findings — review + dogfood chưa xử
> Finding từ review agent (reviewer/bug-hunter) + dogfood persona ở VERIFY. **BLOCKER/MAJOR phải xử trước khi rời VERIFY.**
> Nhỏ → sửa ngay · ngoài scope → `docs/ROADMAP.md §backlog`. (TC FAIL nằm ở `tracking/wave-N/test-cases.md`, không lặp ở đây.)

| Ngày | Nguồn | Severity | Vấn đề | Xử lý |
|---|---|---|---|---|
