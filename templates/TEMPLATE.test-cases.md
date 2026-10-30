<!-- Khung bảng đề test của MỘT wave. test-writer chép file này thành tracking/wave-N/test-cases.md (gate bỏ qua file TEMPLATE.*).
     Người ghi: CHỈ test-writer (QA độc lập). MAIN không sửa (hook guard_qa chặn), trừ dòng @thủ-công của mobile.
     Cách thiết kế TC: skill specialist-testing. Gate đọc bảng theo TÊN cột — đừng đổi tên cột.

     Ý nghĩa từng cột, ví dụ dùng chung một nghiệp vụ: "đăng ký làm từ xa, hạn chót 17h hôm trước".

     TC         Mã TC-<wave>-<số>. Ví dụ TC-2-014 = TC số 14 viết ở wave 2.
                TC cũ được chọn chạy lại (nguồn R) GIỮ NGUYÊN mã cũ: TC-1-007 vẫn là TC-1-007 khi nằm trong đề wave 2.
     loại       functional · security · contract · performance · e2e … (danh sách ở specialist-testing).
     nguồn      TC này sinh ra từ đâu — một trong bốn:
                AC  từ một AC trong FEAT. Ví dụ: AC-1 "gửi đơn trước 17h hôm trước thì được nhận"
                    → TC "gửi lúc 16:59 → đơn ở trạng thái CHỜ DUYỆT".
                CS  từ bảng chính sách từng hành động (INTERVIEW). Ví dụ: ô "hạn chót = 17:00 hôm trước"
                    → TC giá trị biên "gửi lúc 17:00:01 → bị chặn, không sinh đơn".
                TD  thăm dò chỗ tài liệu KHÔNG nói tới. Ví dụ: "đăng ký cho ngày cách 6 tháng" — không AC nào quy định
                    → chạy thử; hệ cho phép điều có hại thì kết quả là CHƯA CÓ QUY ĐỊNH, không phải FAIL.
                R   TC CŨ của wave trước, chép NGUYÊN VĂN sang wave này để chạy lại, vì code wave này sửa đúng logic mà
                    AC cũ dựa vào (dòng `B` ở đoạn Phạm vi ảnh hưởng). Ví dụ: wave 2 sửa cách tính số ngày phép khi huỷ
                    đơn → chép TC-1-007 "huỷ đơn đã duyệt → trả lại đúng số ngày phép" từ archive wave 1, giữ mã
                    TC-1-007, gắn tag @regression. Không sửa mô tả TC cũ; hành vi đã đổi thì ghi ĐÃ THAY và viết TC mới.
     AC         `FEAT-x AC-n` mà TC phục vụ. TC thăm dò (TD) không có AC → ghi `—`.
     tag        @smoke       1 TC đi trọn mỗi nghiệp vụ chính — luôn chạy lại.
                @trọng-yếu   FAIL nghĩa là sai tiền · lộ / sai quyền · hỏng dữ liệu người khác — hết 3 lượt sửa mà
                             còn FAIL thì KHÔNG được chuyển sang wave sau.
                @regression  CHỈ cho TC cũ nguồn R được chọn ở wave này — không gắn cho TC mới.
                @thủ-công    TC UI mobile do MAIN chạy tay (verify.md 3c).
                Không có tag nào thì để trống.
     mô tả      Tên nói HỎNG GÌ khi đỏ, rồi tiền đề → bước → kỳ vọng (gồm đọc lại dữ liệu đã lưu). 1–2 dòng.
     cách chạy  Lệnh / thao tác tái hiện được (curl · Playwright · k6).
     kết quả    PASS · FAIL · BLOCKED · CHƯA CHẠY · CHƯA CÓ QUY ĐỊNH · ĐÃ THAY.
                Lần chạy lại trong vòng sửa ghi kèm lượt: `PASS (lượt 2)`.
                ĐÃ THAY = TC cũ hết hợp lệ vì AC đã đổi qua top-up — ghi TC thay thế ở cột cuối.
                CHƯA CÓ QUY ĐỊNH = tài liệu không quy định ca này mà hệ đang cho phép một việc có thể gây hại → Authority
                quyết có thêm quy định không. KHÔNG phải bug. Ví dụ: đăng ký cho ngày cách 6 tháng vẫn được, dù kỳ
                chấm công tháng đó chưa mở.
     thực tế / bằng chứng
                1 dòng điều quan sát THẬT (status · body rút gọn · màn hình) — FAIL thì đây chính là báo cáo bug.
                BLOCKED → `hạ tầng: …` hoặc `spec: …`. CHƯA CÓ QUY ĐỊNH → hành vi + phép thử nào + hệ quả.
                Hết 3 lượt sửa, TC còn FAIL được chuyển sang wave sau → thêm `→ backlog wave N+1`. -->
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
