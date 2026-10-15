---
name: system-design
description: "Vai SA — /document Bước 6, chạy giữa boundary-charter và technical-design: System design TỈ LỆ THUẬN quy mô — NFR (PRD §3) → ước lượng tải → sơ đồ thành phần → lưu trữ & mở rộng → nhất quán → chế độ lỗi → bảo mật (phân loại dữ liệu + mối đe dọa) → triển khai (số instance · proxy · môi trường) → ADR có số. Ghi docs/arch/OVERVIEW.md §5. KHÔNG viết contract chi tiết (technical-design), KHÔNG viết NFR (PO)."
---

# System Design (Bước 6 — giữa chia ranh giới và thiết kế contract)

> **Vai: SA** · **Viết**: `docs/arch/OVERVIEW.md §5 System design` (5.1–5.9) · ADR cho quyết định lớn (`docs/adr/`)
> **KHÔNG viết**: PRD §3 NFR (PO — thiếu số thì hỏi Authority, PO ghi vào PRD §3, SA không tự bịa số) · contract chi tiết `arch/{name}.md` §1–§6 (`technical-design`) · FEAT / bảng luồng (PO · BA)

## Khi dùng
Bước 6 của `/document`, **sau** `boundary-charter` (đã có danh sách service + dữ liệu mỗi service sở hữu ở OVERVIEW §1) và **trước** `technical-design`. DDD (event-storming → boundary) trả lời *chia thành mấy phần, phần nào sở hữu dữ liệu nào*; skill này trả lời *mỗi phần chạy trên hạ tầng nào, chịu tải ra sao, hỏng thì thế nào, bảo vệ dữ liệu gì*. `technical-design` đọc §5 để ghi xuống contract (phân trang, cache, outbox, mã hoá cột, lock job…).

Vì sao bắt buộc: thiếu lớp này thì code đúng nghiệp vụ nhưng gãy khi chạy thật — lọc cả bảng trong bộ nhớ (không ai khai bảng nào lớn) · PII lưu chữ thường dù PRD đòi mã hoá (không ai phân loại dữ liệu) · rate limit chung một bucket sau nginx (không ai khai đứng sau proxy) · job chạy trùng (không ai khai số instance).

## Boot sequence
1. `STATE.md` + `PROTOCOL.md`.
2. `docs/PRD.md` §3 NFR (+ §1 đối tượng · §7 dữ liệu mẫu để ước lượng) · `docs/arch/OVERVIEW.md` §1 (service) · §2 (tích hợp) · §4 (event storming) · `docs/INTERVIEW.md §Luồng nghiệp vụ đã xác nhận` (luồng + màn nháp) · `docs/feat/*` (AC).
3. `docs/SECURITY.md` (baseline chung — §5.7 chỉ ghi phần riêng dự án).

## Tỉ lệ thuận với quy mô — mục 5.2 quyết độ sâu
| Mức | Dấu hiệu (gợi ý — ghi số thật) | Độ sâu |
|---|---|---|
| **Nhỏ** | ≤ vài trăm người dùng · < ~10 req/s cao điểm · dữ liệu < vài chục GB/năm | 5.4/5.5/5.6 vài dòng, `n/a — <lý do>` hợp lệ. 1 instance + backup thường đủ |
| **Vừa** | nghìn–chục nghìn người dùng · ~10–200 req/s | cache có chủ đích · ≥2 instance (stateless, job có lock) · cân nhắc read replica |
| **Lớn** | > 200 req/s · dữ liệu TB · đa vùng | partition/shard · queue · tách đọc/ghi — mỗi quyết định có ADR + research |

**Luôn bắt buộc, kể cả mức nhỏ** (đã gây lỗi thật khi bỏ): số instance mỗi target · đứng sau reverse proxy/gateway hay không · môi trường (dev/sit/prod) · phân loại dữ liệu nhạy cảm · bảng nào sẽ lớn.

KHÔNG thiết kế thừa: không thêm Kafka/Redis/replica khi 5.2 không đòi. Mỗi thành phần hạ tầng phải trỏ được về một con số ở 5.1/5.2.

## Phương pháp — ghi vào `OVERVIEW §5`, đúng thứ tự
1. **5.1 NFR → quyết định**: mỗi NFR ở PRD §3 viết thành kịch bản đo được (*"500 người chấm công lúc 8h, p95 < 500ms"*) + quyết định thiết kế nó kéo theo. NFR không kéo theo quyết định nào → ghi "không đổi thiết kế". PRD §3 thiếu số → hỏi Authority (đang DOCUMENT), PO ghi vào PRD §3.
2. **5.2 Ước lượng tải** (ghi phép tính, không chỉ kết quả): người dùng × hành vi → req/s đọc/ghi lúc cao điểm · tỉ lệ đọc/ghi · dữ liệu 1–3 năm theo bảng lớn nhất · file. Kết luận mức Nhỏ/Vừa/Lớn.
3. **5.3 Sơ đồ thành phần** (mermaid, mức container của C4): client → proxy/gateway → service (theo §1) → DB/cache/queue/storage → hệ ngoài. Đánh dấu đường đi của luồng nghiệp vụ chính.
4. **5.4 Lưu trữ & mở rộng theo nhóm dữ liệu**: owner service · mẫu truy cập (đọc gì nhiều nhất) · kho · lớn tới đâu sau 3 năm · cache (TTL, invalidation) · index/partition · lưu giữ/xoá. Bảng đánh dấu **lớn** → `technical-design` bắt buộc phân trang ở DB + trần size, cấm nạp cả bảng.
5. **5.5 Nhất quán theo luồng**: luồng nào cần nhất quán ngay (1 transaction), luồng nào chấp nhận nhất quán sau (outbox · saga · bù). Ghi qua nhiều service → không dùng giao dịch phân tán.
6. **5.6 Chế độ lỗi & điểm chết đơn lẻ**: mỗi thành phần (DB · cache · broker · hệ ngoài · lưu file · IdP) chết hoặc chậm thì người dùng thấy gì · xử bằng gì (timeout/retry/circuit breaker/hàng đợi/suy giảm) · phục hồi (RTO/RPO, backup).
7. **5.7 Bảo mật riêng dự án**: (a) **phân loại dữ liệu** — dữ liệu · mức (công khai/nội bộ/nhạy cảm/PII/tài chính) · ai được xem · bảo vệ (mã hoá cột · che log · chỉ TLS); (b) **mối đe dọa chính** 3–7 dòng (STRIDE rút gọn): mối đe dọa · tài sản · chặn bằng gì; (c) **mô hình xác thực**: IdP, token, kiểm `iss`/`aud`, thu hồi khi khoá tài khoản. Baseline chung đã ở `SECURITY.md` — không chép lại.
8. **5.8 Triển khai & vận hành**: mỗi target — số instance prod · đứng sau gì (nginx/gateway/LB) · stateless? · job chạy ở đâu, có lock không · môi trường · observability (log JSON + `X-Request-ID`, metric, cảnh báo theo SLO 5.1) · backup.
9. **5.9 Quyết định lớn → ADR**: mỗi lựa chọn hạ tầng đáng kể có ADR, lý do **trích số** ở 5.1/5.2, phương án đã loại, khi nào phải xem lại.

## Giao cho `technical-design` (nó PHẢI phản ánh, rà ở chiều trace)
| §5 khai | `technical-design` ghi xuống |
|---|---|
| bảng lớn (5.4) | list/search phân trang ở DB, `size ≤ 100`, không `findAll` cả bảng — `arch §3` |
| cache (5.4) | key · TTL · invalidation — `arch §4` |
| nhất quán sau (5.5) | outbox/saga/bù — `arch §2` · `§5 Events` · `§6` E5 |
| dữ liệu nhạy cảm (5.7) | cột mã hoá / che log — `arch §1` data model |
| ≥ 2 instance (5.8) | job có lock, session stateless — `arch §4` |
| sau proxy (5.8) | lấy IP qua proxy tin cậy (`forward-headers-strategy`) — `arch §4` |

## Quality checklist
- [ ] §5 đủ 5.1–5.9; mục không áp dụng ghi `n/a — <lý do>`, không bỏ trắng.
- [ ] 5.2 có phép tính và kết luận mức; mọi thành phần ở 5.3 trỏ được về một số ở 5.1/5.2.
- [ ] Năm thứ "luôn bắt buộc" có giá trị thật (instance · proxy · môi trường · phân loại dữ liệu · bảng lớn).
- [ ] ADR ở 5.9 trích số làm lý do.
- [ ] Không chứa contract chi tiết (endpoint/field) — đó là `technical-design`.

## Done
- OVERVIEW §5 đủ và qua checklist → tiếp `technical-design` (đọc §5, ghi xuống contract theo bảng "Giao cho").
