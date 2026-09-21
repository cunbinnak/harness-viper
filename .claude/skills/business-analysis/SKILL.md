---
name: business-analysis
description: Lens phân tích AC/BR cho /document — kiểm AC testable + BR logical + scope rõ. Dùng ở chốt rà chéo và chốt viết nghiệp vụ. Process flow / use case / edge case làm phương pháp.
---

> Phương pháp cho /document (fork gộp discovery vào DOCUMENT). Không phải stage riêng.

# Business Analysis Skill

## Khi load
- **`/document` Bước 5** (ngay sau viết FEAT — rà AC testable/BR logical trước khi sang arch) + **Bước 10** (challenge — rà chéo toàn lớp doc). LENS review, KHÔNG author.

Input: `docs/{PRD.md, feat/FEAT-*.md}` (BR nằm trong FEAT §field hoặc `docs/adr/`).

## Cái cần đảm bảo (chất lượng AC/BR — FEAT do DOMAIN author)
1. **AC testable** — Given/When/Then (Cho/Khi/Thì) hoặc condition đo được; mỗi user story ≥ 1 AC; cover cả non-happy-path.
2. **Business rules `BR-*`** — phát biểu rõ + nguồn (policy/regulation/stakeholder) + ≥2 ví dụ; `related_features` ≥1.
3. **Scope rõ** — §Ngoài phạm vi đủ để QC biết KHÔNG test gì; bounded context rõ (boundary thật chốt ở bước boundary-charter/technical-design trong DOCUMENT).

> `domain-po`/`domain-ba` (trong `/document`) sở hữu FEAT/BR; skill này là LENS kiểm chất lượng (review) + phân tích thay đổi — KHÔNG tự author FEAT.

## Phương pháp phân tích (để ra AC/BR/boundaries chất lượng)
1. **Research — MẶC ĐỊNH LÀM TRƯỚC** (module/domain mới chưa biết đi thế nào → research là bước đầu, đừng bịa): business process pattern của industry, cách sản phẩm cùng ngành giải, edge case/failure đã documented, compliance/regulatory. Domain quá quen mới được bỏ qua (ghi 1 dòng lý do). KHÔNG bịa nguồn.
2. **Actor & bounded context** — liệt kê tác nhân (role/system/external) → suy ra bounded context (gợi ý boundary; chốt ở bước boundary-charter/technical-design trong DOCUMENT).
3. **Process flow (Mermaid)** — As-Is (nếu có hệ thống cũ) + To-Be (theo PRD). Happy path + nhánh ngoại lệ → giúp tìm AC + edge case.
   ```mermaid
   flowchart TD
     A[Actor gửi request] --> B{Hợp lệ?}
     B -- No --> E[Lỗi VALIDATION]
     B -- Yes --> C[Service xử lý] --> D[(DB)] --> F[Phản hồi]
   ```
4. **Use case** — actor · precondition · main flow · alternate · postcondition → mỗi use case sinh ≥ 1 AC.
5. **Edge case & failure** — entity không tồn tại; trạng thái final; request trùng; thiếu quyền; tenant khác; external fail/timeout → thành AC + BR.
6. **Gap analysis** — current vs target: thiếu gì, assumption, constraint.

> Process flow / use case / edge case có thể **ghi kèm vào FEAT** (section phụ trợ sau Business rules) — không bắt buộc verify, nhưng giúp dev/test/reviewer hiểu rõ.

## Flow
- **review**: soi → trả `issues[]` (file + concern) cho user; KHÔNG tự sửa product (domain-po/ba author sửa, hoặc revision loop).
- **rà chéo**: soi gap/độ phủ giữa các lớp doc + báo `affected_docs`/`boundaries_affected`.

## Quality checklist (khi review / phân tích)
- [ ] Mỗi user story có ≥ 1 AC testable (Cho/Khi/Thì), gồm non-happy-path.
- [ ] BR-* có nguồn tham chiếu + ≥2 ví dụ + `related_features` ≥1.
- [ ] Scope rõ (§Ngoài phạm vi đủ cho QC); bounded context rõ.
- [ ] (Phương pháp) process flow / use case / edge case đã cân nhắc để không sót AC.
- [ ] (Nếu research) ≥ 1 nguồn thật, ghi link.

## Done
- rà chéo: trả issues list cho user feedback. Ghi vào `docs/DECISIONS.md` nếu là quyết định non-trivial.
