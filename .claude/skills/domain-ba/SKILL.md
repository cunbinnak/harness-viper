---
name: domain-ba
description: "Phương pháp Business-Analyst cho /document Bước 3 — PHÂN TÍCH nghiệp vụ trước khi ai viết yêu cầu: dựng bảng luồng (Ai LÀM / Ai NHỜ / bằng chứng) → Authority ký → business-rule + persona + ma trận vai×hành động sinh TỪ bảng. Actor của mọi AC về sau lấy từ đây. Hỏi Authority chỗ CHƯA HỎI (đang DOCUMENT)."
---

> Phương pháp cho /document (fork gộp DOMAIN/DESIGN/PLAN vào DOCUMENT, 1 lớp doc). Không stage riêng, không translate.

# Business-Analyst Method (Luồng nghiệp vụ → Business-rule → Persona)

## Khi dùng
Bước 3 của `/document` — vai **Business Analyst**, chạy **sau khám phá (discovery = việc PO: vấn đề · đối tượng · cược) và TRƯỚC khi viết yêu cầu (Bước 5)**. Trình tự chuẩn PO → BA → yêu cầu: BA dựng quy trình *như thế nào, ai làm bước nào* rồi người viết AC mới có actor để dùng. Đảo thứ tự (viết AC trước, phân tích sau để rà) là chỗ model **suy diễn actor** — "bộ phận có nhu cầu" thành "Team Lead tạo yêu cầu" — và cả chuỗi FEAT/ma trận/API sai đồng bộ nên trace không bắt.

Viết **THẲNG** vào 1 lớp doc:
- **Bảng luồng nghiệp vụ** → `docs/INTERVIEW.md §Luồng nghiệp vụ đã xác nhận` (khung `templates/TEMPLATE.interview.md`).
- **Business-rule** → **FEAT `docs/feat/*` §3 Field kỹ thuật** (rule gắn 1-2 feature; ghi nháp, điền khi Bước 5 chạy) · rule nền/cross-cutting → **`docs/adr/`**.
- **Persona + ma trận vai × hành động** → **`docs/PERSONAS.md`**.

> Wireframe/UI KHÔNG thuộc method này — đó là UX: `docs/ux/` + `docs/DESIGN-SYSTEM.md`.

## Boot sequence (targeted — Bước 3: CAPABILITIES-MAP/FEAT CHƯA tồn tại, đừng tìm)
1. `STATE.md` + `PROTOCOL.md`.
2. `docs/INTERVIEW.md` (lời kể + bằng chứng — nguồn của bảng luồng) + `docs/PRD.md §1-2` (vấn đề · đối tượng).
3. Nếu có intake: `intake/*`.

## A. Dựng luồng nghiệp vụ thành BẢNG — Authority ký (việc lõi của BA, làm ĐẦU TIÊN)
Lời kể là văn xuôi ("bộ phận có nhu cầu liên hệ HR → HR đăng tin → …"); AC cần actor cụ thể. Khoảng trống giữa hai thứ đó là nơi sai actor sinh ra. Chặn bằng bảng:
1. **Đọc lại research của discovery** (PRD §6 — 4 loại: quy trình chuẩn từng nghiệp vụ · vai chuyên trách · menu sản phẩm cùng loại · ràng buộc ngoài). Nghiệp vụ nào Author kể mà PRD §6 **chưa có nguồn loại 1/2** → research bù ngay (cùng bảng 4 loại ở `discovery-hypothesis`), ghi link vào §6. KHÔNG dựng bảng luồng cho nghiệp vụ chưa có chuẩn ngành làm mốc — không có mốc thì không biết Author nói khác hay thiếu. KHÔNG bịa nguồn.
2. **Liệt kê actor** (role / system / external) từ INTERVIEW — chưa gán việc, chỉ liệt kê. Actor lộ ra ở đây là gợi ý bounded context (chốt ở `boundary-charter`).
3. **Mỗi nghiệp vụ Authority đã kể → 1 bảng** `# · Ai LÀM · Làm gì · Ai NHỜ/duyệt · Đầu vào → đầu ra · Bằng chứng`, 4-8 dòng, đi trọn vòng đời (ai tạo cái đầu tiên, cái cuối đi đâu, đường lùi/huỷ).
   - **Ai LÀM ≠ Ai NHỜ/duyệt** — hai cột riêng, bắt buộc. Người nêu nhu cầu / phê duyệt ngoài hệ thống KHÔNG phải actor; có thao tác riêng thì thành dòng riêng.
   - **Vai chuyên trách theo ngành là mặc định** (tuyển dụng = HR · tính lương = C&B · duyệt phép = quản lý trực tiếp). Giao cho vai khác phải có dòng bằng chứng.
   - **Cột Bằng chứng trỏ số dòng INTERVIEW §1.** Ô không trỏ được → ghi `CHƯA HỎI` — **đó là câu hỏi kế tiếp, hỏi Authority ngay** (đang DOCUMENT, hỏi hợp lệ và rẻ nhất). KHÔNG đoán, KHÔNG ghi DECISIONS thay cho việc hỏi.
4. **Use case per dòng bảng** (khi dòng có nhánh): precondition · main flow · alternate · postcondition — mỗi nhánh ngoại lệ sau này là 1 AC/ca biên ở Bước 5. Ghi gọn ngay dưới bảng hoặc để `domain-po` lấy.
5. **Playback đọc BẢNG, không đọc văn xuôi**: "bước 1: HR đăng tin, bộ phận chỉ nhờ — đúng không?". Sai actor lộ trên một dòng bảng trong 5 giây. Authority gật → ghi `chốt bởi Authority: <ngày ISO>` trên bảng. Gate DOCUMENT đòi: ≥1 bảng · đã ký · không ô `CHƯA HỎI`.

Bảng này là **nguồn duy nhất** cho: ô `có/cấm` ma trận PERSONAS §2 (mục C dưới) · actor của AC (`domain-po`) · hành trình persona `arch/<web>.md §2`. Không nơi nào được tự suy actor ngoài bảng.

## B. Business-rule (từ bảng luồng + INTERVIEW)
§Phát biểu (1 câu rõ) + §Lý do (**reference nguồn**: luật/policy/contract/quyết định — KHÔNG "best practice") + §Khi nào áp dụng + §Ngoại lệ + §Hệ quả + **≥2 ví dụ** (1 happy + 1 vi phạm, số liệu — QC seed test) + `severity` CORNERSTONE/NORMAL + **`related_features` ≥1** (rule chỉ 1 FEAT → đáng lẽ là AC, đưa thành AC trong FEAT đó). §**Enforce ở đâu** trỏ nơi CHẶN được (unique index · cột `version` · idempotency key · DB constraint · state machine) — viết chung file với contract (fork 1 lớp, không TODO-engineer để dịch sau).

## C. Persona + ma trận vai × hành động (sinh TỪ bảng luồng)
role/goals/pains/workflow narrative. **Anti-persona BẮT BUỘC.** Ma trận `docs/PERSONAS.md §2`: **ô `có` = có dòng bảng luồng mà vai đó ở cột Ai LÀM**; vai không có dòng nào cho hành động đó = `cấm`. KHÔNG suy từ FEAT (FEAT viết sau ma trận; suy ngược = sai đồng bộ, trace không bắt). Không ô trống.

## Hỏi hay không hỏi
Ô bảng luồng chưa có bằng chứng → xử theo **3 tầng** (PROTOCOL §2.3): có bằng chứng → làm · chuẩn ngành → research, ghi `[C]` + link · chỉ Author biết → hỏi. Ô chuẩn ngành ghi `[C] <link>` (vẫn đọc cho Authority ở playback); ô tầng 3 ghi `CHƯA HỎI` rồi hỏi ngay.

## Quy tắc
- ID `BR-<slug>` (nếu tách rule) / persona đặt trong `PERSONAS.md`. Cross-ref bằng ID canonical đầy đủ.
- Enforce viết chung file với contract (fork 1 lớp — KHÔNG `docs/domain/`, KHÔNG bước translate/TODO-engineer).
- Sửa doc đã chốt = **wave sau** (`ROADMAP §backlog` → `/next-wave` → `/document` top-up).

## Done
- Bảng luồng mọi nghiệp vụ đã kể: Authority ký, không ô `CHƯA HỎI` + Business-rule (≥2 ví dụ + nguồn + Enforce ở đâu) đặt đúng chỗ + Persona + ma trận (ô `có` trỏ được về dòng bảng) + mọi chỗ tự quyết có dòng `DECISIONS.md` → tiếp Bước 4 `capability-mapping` (đọc PERSONAS vừa viết).
