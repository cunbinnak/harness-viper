<!-- gate bỏ qua TEMPLATE.* — copy thành docs/PRD.md. AC nằm ở docs/feat/FEAT-*, KHÔNG ở đây. -->
# PRD — {{PROJECT_NAME}}

<!-- §1: pain point + đối tượng cụ thể — ai đau, đau gì, hệ quả. Có bằng chứng (câu chuyện thật / con số / hiện vật). -->
## §1 Vấn đề (pain)
- **Ai đau**: {{đối tượng cụ thể · không phải "người dùng nói chung"}}
- **Đau gì**: {{pain point + status quo họ đang xoay xở bằng gì}}
- **Hệ quả (cost of inaction)**: {{không làm thì mất gì · tăng theo quy mô ra sao}}
- **Bằng chứng**: {{câu chuyện thật / con số / hiện vật — không rỗng}}

<!-- §2: ≥3 giả thuyết TESTABLE (falsifiable + tín hiệu đo được + cách kiểm) + ≥2 phản-giả-thuyết (chặn scope-creep) + rủi ro chính. -->
## §2 Giả thuyết + rủi ro

**Giả thuyết (≥3, testable):**

| # | Giả thuyết (falsifiable) | Outcome đo được | Cách kiểm | Bằng chứng vì sao tin | Status |
|---|---|---|---|---|---|
| H1 | {{vd: nếu chặn đơn nhầm tự động thì tỉ lệ đơn sai giảm}} | {{vd: đơn sai < 2%}} | {{cách đo}} | {{quá khứ cụ thể}} | TESTABLE |
| H2 | {{…}} | {{…}} | {{…}} | {{…}} | TESTABLE |
| H3 | {{…}} | {{…}} | {{…}} | {{…}} | TESTABLE |

**Phản-giả-thuyết (≥2 — tường minh cái KHÔNG cược, chặn scope-creep):**
- {{vd: KHÔNG cược rằng user cần app mobile ở wave này}}
- {{…}}

**Rủi ro chính:**
- {{rủi ro · tác động · giảm thiểu}}

<!-- §3: NFR CÓ SỐ — không bịa, chưa rõ thì hỏi user. -->
## §3 NFR (phi chức năng — CÓ SỐ)
- **Perf**: {{vd: p95 < 300ms cho API lõi}}
- **Availability**: {{vd: 99.5% uptime tháng}}
- **Security / compliance**: {{vd: auth OAuth2 · PII mã hoá at-rest · tuân GDPR}}
- **Scale**: {{vd: 10k user đồng thời · 1M order/ngày}}

<!-- §4: tường minh cái KHÔNG làm — chống scope creep. -->
## §4 Out-of-scope
- {{…}}

<!-- §5: ≥1 metric CÓ SỐ. -->
## §5 Success metric
- {{vd: 80% order hoàn tất < 3 phút}}

<!-- §6: từ điển thuật ngữ nghiệp vụ + nguồn tham chiếu (intake / phỏng vấn / tài liệu). -->
## §6 Glossary + Nguồn

**Glossary:**
| Thuật ngữ | Nghĩa |
|---|---|
| {{term}} | {{định nghĩa nghiệp vụ}} |

**Nguồn:**
- {{vd: intake/brief.md · phỏng vấn Authority 2026-… · tài liệu X}}
