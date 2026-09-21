<!-- gate bỏ qua TEMPLATE.* — copy thành docs/PRD.md. AC nằm ở docs/feat/FEAT-*, KHÔNG ở đây. -->
# PRD — {{PROJECT_NAME}}

<!-- §1: pain point + đối tượng cụ thể — ai đau, đau gì, hệ quả. Có bằng chứng (câu chuyện thật / con số / hiện vật). -->
## §1 Vấn đề (pain)
- **Ai đau**: {{đối tượng cụ thể · không phải "người dùng nói chung"}}
- **Đau gì**: {{pain point + status quo họ đang xoay xở bằng gì}}
- **Hệ quả (cost of inaction)**: {{không làm thì mất gì · tăng theo quy mô ra sao}}
- **Bằng chứng**: {{câu chuyện thật / con số / hiện vật — không rỗng}}

<!-- §2: 1 giả thuyết CHÍNH = success metric (con số + ngưỡng go/pivot/kill, ghi TRƯỚC khi nhìn số liệu) + rủi ro chính.
     Giả thuyết phụ (nếu phỏng vấn nảy ra) thêm dòng H2/H3… — tùy chọn, KHÔNG ép số lượng. Cái KHÔNG làm → §4 Out-of-scope. -->
## §2 Giả thuyết + rủi ro

**Giả thuyết chính (H1 = success metric của §5):**

| # | Giả thuyết (falsifiable) | Outcome đo được | Ngưỡng go/pivot/kill | Bằng chứng vì sao tin | Status |
|---|---|---|---|---|---|
| H1 | {{vd: nếu chặn đơn nhầm tự động thì tỉ lệ đơn sai giảm}} | {{vd: đơn sai < 2%}} | {{go ≥X · pivot X-Y · kill <Y}} | {{quá khứ cụ thể}} | TESTABLE |

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

<!-- §7: bộ dữ liệu mẫu — MỘT nguồn nuôi 4 chỗ: mockup (Bước 8) · seed deployment/local/ · dogfood · test-cases.
     Ưu tiên dữ liệu THẬT Authority đang có; không có → MAIN research domain + tự chuẩn bị bộ realistic
     (đúng thuật ngữ + giá trị thật ngoài đời — như QA chuẩn bị test-data), Authority gật ở playback.
     Vài bản ghi per entity chính là đủ — đủ dựng mockup không bịa + seed chạy dogfood. -->
## §7 Dữ liệu mẫu
Nguồn: {{thật (ảnh sổ/Excel/tin nhắn) | MAIN chuẩn bị từ research — Authority đã gật}}

| Entity | Bản ghi mẫu (giá trị THẬT ngoài đời, không "Nguyễn Văn A") |
|---|---|
| {{Món}} | {{Phở bò tái 45.000đ · Cơm tấm sườn 40.000đ · Trà đá 5.000đ}} |
| {{Bàn}} | {{B1-B12 (trệt) · L1-L6 (lầu, ghép được)}} |
