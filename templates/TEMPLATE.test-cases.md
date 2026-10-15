<!-- gate bỏ qua TEMPLATE.* — test-writer copy thành tracking/wave-N/test-cases.md (1 bảng/wave). Cách thiết kế: skill specialist-testing.
     VAI: test-writer (QA độc lập) — MAIN không ghi file này.
     Gate đọc theo TÊN cột (không theo vị trí) — giữ nguyên tên cột:
     TC          : TC-<wave>-NNN · TC regression chạy lại GIỮ mã gốc (vd TC-1-007)
     loại        : specialist-testing §taxonomy
     nguồn       : AC (FEAT · AC) · CS (bảng chính sách: hành động · cột) · TD (thăm dò ngoài tài liệu) · R (regression từ wave trước)
     AC          : `FEAT-x AC-n` mà TC phục vụ (TD không có AC → `—`)
     tag         : @smoke · @regression (có thể cả hai · trống nếu không)
     mô tả       : tên nói HỎNG GÌ khi đỏ — tiền đề → bước → kỳ vọng (gồm đọc lại dữ liệu đã lưu, theo chuẩn kiểm). 1-2 dòng
     cách chạy   : lệnh / thao tác tái hiện được (curl · Playwright · k6)
     kết quả     : PASS · FAIL · BLOCKED · CHƯA CHẠY · CHƯA CÓ QUY ĐỊNH · ĐÃ THAY
                   (ĐÃ THAY = TC regression wave trước hết hợp lệ vì AC đổi qua top-up — ghi TC thay thế ở cột cuối)
                   (CHƯA CÓ QUY ĐỊNH = tài liệu — AC + bảng chính sách — không quy định ca này, hệ đang cho phép một việc
                    có thể gây hại → Author quyết có thêm quy định không. KHÔNG phải bug. vd đăng ký làm từ xa lúc 18h vẫn được)
     thực tế / bằng chứng : 1 dòng điều quan sát THẬT (status · body rút gọn · màn hình). FAIL → chính là báo cáo bug.
                   BLOCKED → `hạ tầng: …` hoặc `spec: …`. CHƯA CÓ QUY ĐỊNH → hành vi + phép thử nào + hệ quả. -->
| TC | loại | nguồn | AC | tag | mô tả | cách chạy | kết quả | thực tế / bằng chứng |
|---|---|---|---|---|---|---|---|---|
| {{TC-1-001}} | {{functional}} | {{AC}} | {{FEAT-remote AC-1}} | {{@smoke @regression}} | {{Không tạo được đơn remote hợp lệ — NV, ngày làm việc kế tiếp, trước 17h → gửi → 201; đọc lại: đơn CHỜ DUYỆT, có trong hàng chờ quản lý}} | {{curl -X POST /v1/remote …}} | {{PASS}} | {{201 · GET /v1/remote/12 → CHỜ DUYỆT · có trong /v1/approvals}} |
| {{TC-1-002}} | {{functional}} | {{CS}} | {{FEAT-remote AC-3}} | {{@regression}} | {{Cho đăng ký sau hạn chót — đồng hồ 17:00:01 → gửi → 4xx REMOTE_DEADLINE, không sinh bản ghi}} | {{…}} | {{FAIL}} | {{201, tạo đơn #13 lúc 17:00:01}} |
| {{TC-1-020}} | {{functional}} | {{TD}} | {{—}} | | {{Đăng ký cho ngày cách 6 tháng — tài liệu không nói}} | {{…}} | {{CHƯA CÓ QUY ĐỊNH}} | {{201, hệ cho phép · phép thử hạ nguồn: kỳ chấm công đó chưa mở}} |
