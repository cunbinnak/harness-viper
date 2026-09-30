---
name: business-analysis
description: "Lens RÀ AC/BR cho /document (Bước 5 sau viết FEAT + Bước 10 challenge) — đối chiếu actor AC với bảng luồng Authority đã ký (domain-ba A), AC testable, BR logical, scope rõ. KHÔNG phân tích, KHÔNG author — phân tích là domain-ba Bước 3."
---

# Business Analysis Skill

## Khi load
- **`/document` Bước 5** (ngay sau viết FEAT — rà AC testable/BR logical trước khi sang arch) + **Bước 10** (challenge — rà chéo toàn lớp doc). LENS review, KHÔNG author.

Input: `docs/{PRD.md, feat/FEAT-*.md}` (BR nằm trong FEAT §field hoặc `docs/adr/`).

## Cái cần đảm bảo (chất lượng AC/BR — FEAT do domain-po viết)
1. **AC testable** — Given/When/Then (Cho/Khi/Thì) hoặc condition đo được; mỗi FEAT ≥ 1 AC; cover cả non-happy-path.
2. **Business rules `BR-*`** — phát biểu rõ + nguồn (policy/regulation/stakeholder) + ≥2 ví dụ; `related_features` ≥1.
3. **Scope rõ** — §Ngoài phạm vi đủ để QC biết KHÔNG test gì; bounded context rõ (boundary thật chốt ở bước boundary-charter/technical-design trong DOCUMENT).

> `domain-po`/`domain-ba` (trong `/document`) sở hữu FEAT/BR; skill này là LENS kiểm chất lượng (review) — KHÔNG tự author FEAT.

## Phân tích nằm ở đâu
Phương pháp phân tích (research ngành · actor · bảng luồng · use case · edge case) là việc BA ở **Bước 3 `domain-ba` mục A** — chạy TRƯỚC khi viết AC. Skill này KHÔNG phân tích lại; nó **đối chiếu AC/BR với kết quả phân tích đã ký** (bảng luồng `INTERVIEW §Luồng nghiệp vụ đã xác nhận`). Rà mà không có bảng ký để đối chiếu = tự chấm bài mình, không bắt được sai actor.

## Flow
- **review**: soi → trả `issues[]` (file + concern) cho user; KHÔNG tự sửa product (domain-po/ba author sửa, hoặc revision loop).
- **rà chéo**: soi gap/độ phủ giữa các lớp doc.

## Quality checklist (khi review / phân tích)
- [ ] **Actor mỗi AC = cột Ai LÀM của bảng luồng đã ký** (`INTERVIEW §Luồng nghiệp vụ đã xác nhận`); ô `có` ma trận PERSONAS §2 trỏ được về dòng bảng. Lệch = SAI (báo, sửa AC/ma trận), không phải nitpick — đây là kiểm "đúng với Authority", các trace khác chỉ kiểm "đúng với nhau".
- [ ] Mỗi FEAT có ≥ 1 AC testable (Cho/Khi/Thì), gồm non-happy-path.
- [ ] BR-* có nguồn tham chiếu + ≥2 ví dụ + `related_features` ≥1.
- [ ] Scope rõ (§Ngoài phạm vi đủ cho QC); bounded context rõ.
- [ ] Ca biên/nhánh use case ở bảng luồng (domain-ba A.4) đều có AC tương ứng — không sót nhánh.

## Done
- rà chéo: trả issues list cho user feedback. Ghi vào `docs/DECISIONS.md` nếu là quyết định non-trivial.
