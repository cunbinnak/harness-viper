<!-- gate bỏ qua TEMPLATE.* — test-writer copy thành tracking/wave-N/test-cases.md (1 bảng/wave). Cách thiết kế: skill specialist-testing.
     VAI: test-writer (QA độc lập) — MAIN không ghi file này.
     Gate đọc theo TÊN cột (không theo vị trí) — giữ nguyên tên cột:
     TC          : TC-<wave>-NNN · TC cũ được chọn chạy lại GIỮ mã gốc (vd TC-1-007)
     loại        : specialist-testing §taxonomy
     nguồn       : AC (FEAT · AC) · CS (bảng chính sách: hành động · cột) · TD (thăm dò ngoài tài liệu) · R (TC cũ của wave trước, được CHỌN chạy lại theo phạm vi ảnh hưởng của wave này)
     AC          : `FEAT-x AC-n` mà TC phục vụ (TD không có AC → `—`)
     tag         : @smoke (1 TC đi trọn mỗi luồng chính — luôn chạy lại) · @regression (CHỈ cho TC cũ nguồn R được chọn ở wave này — KHÔNG gắn cho TC mới) · @thủ-công (TC UI mobile do MAIN chạy tay — verify.md Bước 3c) · trống nếu không
     mô tả       : tên nói HỎNG GÌ khi đỏ — tiền đề → bước → kỳ vọng (gồm đọc lại dữ liệu đã lưu, theo chuẩn kiểm). 1-2 dòng
     cách chạy   : lệnh / thao tác tái hiện được (curl · Playwright · k6)
     kết quả     : PASS · FAIL · BLOCKED · CHƯA CHẠY · CHƯA CÓ QUY ĐỊNH · ĐÃ THAY
                   (ĐÃ THAY = TC cũ hết hợp lệ vì AC đổi qua top-up — ghi TC thay thế ở cột cuối)
                   (CHƯA CÓ QUY ĐỊNH = tài liệu — AC + bảng chính sách — không quy định ca này, hệ đang cho phép một việc
                    có thể gây hại → Authority quyết có thêm quy định không. KHÔNG phải bug. vd đăng ký làm từ xa lúc 18h vẫn được)
     thực tế / bằng chứng : 1 dòng điều quan sát THẬT (status · body rút gọn · màn hình). FAIL → chính là báo cáo bug.
                   BLOCKED → `hạ tầng: …` hoặc `spec: …`. CHƯA CÓ QUY ĐỊNH → hành vi + phép thử nào + hệ quả. -->
## Phạm vi ảnh hưởng
<!-- Wave ≥ 2: ĐIỀN TRƯỚC khi viết TC mới (specialist-testing §Regression theo phạm vi ảnh hưởng). Danh sách, KHÔNG phải bảng. Mỗi dòng mở đầu bằng loại:
     A = code chỉ đi qua luồng cũ → smoke là đủ · B = code sửa logic AC cũ dựa vào → TC trúng ca dễ vỡ · C = hành vi cũ đổi có chủ đích → ĐÃ THAY + TC mới.
     TC cũ chép NGUYÊN VĂN (gate so `mô tả` với archive). Wave 1: xoá mục này. -->
- B · {{FEAT-remote AC-2}} · {{đổi cách tính số ngày phép khi huỷ}} · ca dễ vỡ: {{huỷ đơn đã duyệt}} → TC chọn: {{TC-1-007}}
- A · {{xin nghỉ}} · {{màn đơn đọc thêm trường mới}} → smoke: {{TC-1-001}}
- C · {{FEAT-remote AC-3}} · {{hạn chót đổi 17h → 18h}} → ĐÃ THAY: {{TC-1-005}} → TC mới: {{TC-2-004}}
- Luôn chạy: @smoke mỗi nghiệp vụ chính ({{n}} TC)
- Không ảnh hưởng: {{FEAT / vùng cũ}} — {{vì sao}}

| TC | loại | nguồn | AC | tag | mô tả | cách chạy | kết quả | thực tế / bằng chứng |
|---|---|---|---|---|---|---|---|---|
| {{TC-1-001}} | {{functional}} | {{AC}} | {{FEAT-remote AC-1}} | {{@smoke}} | {{Không tạo được đơn remote hợp lệ — NV, ngày làm việc kế tiếp, trước 17h → gửi → 201; đọc lại: đơn CHỜ DUYỆT, có trong hàng chờ quản lý}} | {{curl -X POST /v1/remote …}} | {{PASS}} | {{201 · GET /v1/remote/12 → CHỜ DUYỆT · có trong /v1/approvals}} |
| {{TC-1-002}} | {{functional}} | {{CS}} | {{FEAT-remote AC-3}} | | {{Cho đăng ký sau hạn chót — đồng hồ 17:00:01 → gửi → 4xx REMOTE_DEADLINE, không sinh bản ghi}} | {{…}} | {{FAIL}} | {{201, tạo đơn #13 lúc 17:00:01}} |
| {{TC-1-020}} | {{functional}} | {{TD}} | {{—}} | | {{Đăng ký cho ngày cách 6 tháng — tài liệu không nói}} | {{…}} | {{CHƯA CÓ QUY ĐỊNH}} | {{201, hệ cho phép · phép thử hạ nguồn: kỳ chấm công đó chưa mở}} |
| {{TC-1-007}} | {{functional}} | {{R}} | {{FEAT-remote AC-2}} | {{@regression}} | {{Huỷ đơn đã duyệt → trả lại đúng số ngày phép}} | {{…}} | {{CHƯA CHẠY}} | |
