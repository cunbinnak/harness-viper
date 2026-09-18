<!-- gate bỏ qua TEMPLATE.* — copy thành docs/ROADMAP.md. KẾ HOẠCH WAVE (loop engineering) + backlog. -->
# ROADMAP — {{PROJECT_NAME}}

<!-- §1: bảng wave, 1 dòng/wave.
     `phases`     — gate đọc để biết wave chạy pha nào. BUILD,VERIFY bắt buộc; thêm SHIP nếu deploy (opt-in).
     `Rà lại`     — để trống tới khi /next-wave MỞ wave đó → stamp ngày (gate wave_reviewed, wave ≥2; wave 1 miễn).
     `Legacy phá` — mặc định `—` (không phá); khai rõ nếu wave này được phá surface cũ (guard_bc so với đây).
     `Wave giao` ở CAPABILITIES-MAP phải khớp cột Wave dưới đây. -->
## §1 Wave plan
| Wave | Target (kind) | AC in-scope | phases | Phụ thuộc wave trước | Legacy được phép phá | Rà lại | Trạng thái |
|---|---|---|---|---|---|---|---|
| 1 | {{order-service (backend), customer-web (web)}} | {{FEAT-order-create AC-1..3}} | BUILD,VERIFY | — | — | (wave 1 miễn) | {{chưa mở}} |
| 2 | {{payment (backend)}} | {{FEAT-pay AC-1..2}} | BUILD,VERIFY,SHIP | {{order-service.api}} | — | {{—}} | {{chưa mở}} |

<!-- §2: RÀ LẠI thấy kế hoạch lệch thực tế thì thêm 1 dòng (không sửa lén §1). -->
## §2 Điều chỉnh khi mở wave
| Ngày | Wave | Đổi gì | Vì sao |
|---|---|---|---|

<!-- §3: BACKLOG — amendment (miss luồng / scope mới phát hiện khi BUILD/VERIFY, hoặc finding minor/blocker treo).
     /next-wave RÀ LẠI ĐỊNH ĐOẠT từng dòng ở cột `Xử`: `wave N` | `hoãn: lý do` | `bỏ: lý do`.
     KHÔNG để trống cột Xử (chống backlog trôi — retro D1). -->
## §3 Backlog (amendment → wave sau)
| Ngày | Phát hiện (miss gì · đụng FEAT nào) | Wave phát hiện | Xử |
|---|---|---|---|
