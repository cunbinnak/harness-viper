---
name: domain-ba
description: "Vai BA — /document Bước 3 PHÂN TÍCH (A bảng luồng Ai LÀM/Ai NHỜ/bằng chứng → Authority ký · B business-rule · C persona + ma trận sinh TỪ bảng) + Bước 5 nhịp 2 ĐẶC TẢ (D viết §2 AC + ca biên + §3 Ràng buộc nghiệp vụ vào khung FEAT của PO). Actor mọi AC lấy từ bảng. KHÔNG ghi chặn ở đâu (SA)."
---

# Business-Analyst Method (Luồng nghiệp vụ → Business-rule → Persona → AC)

> **Vai: BA** · **Viết**: `INTERVIEW §Luồng nghiệp vụ đã xác nhận` (bảng luồng + màn nháp + bảng chính sách + câu hỏi còn mở) · business-rule · `PERSONAS.md` (persona + ma trận) · FEAT §2 AC + ca biên · FEAT §3 Ràng buộc nghiệp vụ
> **KHÔNG viết**: PRD (PO — `discovery-hypothesis`; cần thêm nguồn thì trích ở cột Bằng chứng của bảng luồng) · khung FEAT: capability / mục tiêu / phạm vi (PO — `domain-po`) · chặn Ở ĐÂU, contract, data model (SA — `technical-design`)

## Khi dùng
Bước 3 của `/document` — vai **Business Analyst**, chạy **sau khám phá (discovery = việc PO: vấn đề · đối tượng · cược) và TRƯỚC khi viết yêu cầu (Bước 5)**. Trình tự chuẩn PO → BA → yêu cầu: BA dựng quy trình *như thế nào, ai làm bước nào* rồi người viết AC mới có actor để dùng. Đảo thứ tự (viết AC trước, phân tích sau để rà) là chỗ model **suy diễn actor** — "bộ phận có nhu cầu" thành "Team Lead tạo yêu cầu" — và cả chuỗi FEAT/ma trận/API sai đồng bộ nên trace không bắt.

Viết **THẲNG** vào 1 lớp doc:
- **Bảng luồng nghiệp vụ** → `docs/INTERVIEW.md §Luồng nghiệp vụ đã xác nhận` (khung `templates/TEMPLATE.interview.md`).
- **Business-rule** (đặc tả đầy đủ) → **`docs/INTERVIEW.md §Business rules`** (ngay sau bảng luồng; rule gắn ≥2 feature — rule chỉ 1 FEAT thì viết thành AC của FEAT đó; rule nền/cross-cutting cũng ghi ở đây, đánh dấu `nền`). FEAT §3 chỉ trỏ `BR-<slug>`. Rule cần quyết định kỹ thuật → SA ra ADR, BA KHÔNG ghi `docs/adr/`.
- **Persona + ma trận vai × hành động** → **`docs/PERSONAS.md`**.
- **AC + ca biên + ràng buộc** (phần D, Bước 5) → FEAT §2 + §3, vào khung PO đã tạo.

> Mockup/visual KHÔNG thuộc method này (UX: `docs/ux/` + `docs/DESIGN-SYSTEM.md`). Nhưng **danh sách màn nháp** (A.5) thì có — UX dựng SCREEN-MAP từ nó, không suy lại.

## Boot sequence (targeted — Bước 3: CAPABILITIES-MAP/FEAT CHƯA tồn tại, đừng tìm)
1. `STATE.md` + `PROTOCOL.md`.
2. `docs/INTERVIEW.md` (lời kể + bằng chứng — nguồn của bảng luồng) + `docs/PRD.md §1-2` (vấn đề · đối tượng).
3. Nếu có intake: `intake/*`.

## A. Dựng luồng nghiệp vụ thành BẢNG — Authority ký (việc lõi của BA, làm ĐẦU TIÊN)
Lời kể là văn xuôi ("bộ phận có nhu cầu liên hệ HR → HR đăng tin → …"); AC cần actor cụ thể. Khoảng trống giữa hai thứ đó là nơi sai actor sinh ra. Chặn bằng bảng:
1. **Đọc lại research của discovery** (PRD §6 — 4 loại: quy trình chuẩn từng nghiệp vụ · vai chuyên trách · menu sản phẩm cùng loại · ràng buộc ngoài). Nghiệp vụ nào Authority kể mà PRD §6 **chưa có nguồn loại 1/2** → research bù ngay (cùng bảng 4 loại ở `discovery-hypothesis`), **trích link ở cột Bằng chứng của bảng luồng (nhãn `research <link> + suy luận`) — KHÔNG ghi vào PRD §6** (PRD là mục PO sở hữu). KHÔNG dựng bảng luồng cho nghiệp vụ chưa có chuẩn ngành làm mốc — không có mốc thì không biết Authority nói khác hay thiếu. KHÔNG bịa nguồn.
2. **Liệt kê actor** (role / system / external) từ INTERVIEW — chưa gán việc, chỉ liệt kê. Actor lộ ra ở đây là gợi ý bounded context (chốt ở `boundary-charter`).
3. **Mỗi nghiệp vụ Authority đã kể → 1 bảng** `# · Ai LÀM · Làm gì · Ai NHỜ/duyệt · Đầu vào → đầu ra · Bằng chứng`, 4-8 dòng, đi trọn vòng đời (ai tạo cái đầu tiên, cái cuối đi đâu, đường lùi/huỷ).
   - **Bảng không chỉ là lời kể**: mỗi dữ liệu xuất hiện trong bảng/màn nháp (vd "xem số dư phép") phải có dòng sinh ra nó; mỗi bước quy trình chuẩn (PRD §6) phải có dòng tương ứng hoặc đã được Authority loại. Thiếu → đề xuất ngay theo `discovery-hypothesis` §Lời Authority = luồng chính.
   - **Ai LÀM ≠ Ai NHỜ/duyệt** — hai cột riêng, bắt buộc. Người nêu nhu cầu / phê duyệt ngoài hệ thống KHÔNG phải actor; có thao tác riêng thì thành dòng riêng.
   - **Vai chuyên trách theo ngành là mặc định** (tuyển dụng = HR · tính lương = C&B · duyệt phép = quản lý trực tiếp). Giao cho vai khác phải có dòng bằng chứng.
   - **Cột Bằng chứng** — nhãn chung PROTOCOL §2.3, 1 trong 3: `§1 dòng N` (Authority nói) · `research <link> + suy luận` (quy trình chuẩn / vai chuyên trách đem áp vào bối cảnh Authority — nguồn ưu tiên hướng dẫn sử dụng sản phẩm, văn bản luật, quy trình mẫu; trang marketing không tính) · `intake/<file>`. Ô không có cả 3 → ghi `CHƯA HỎI` — **đó là câu hỏi kế tiếp, hỏi Authority ngay** (đang DOCUMENT, hỏi hợp lệ và rẻ nhất). KHÔNG đoán, KHÔNG ghi DECISIONS thay cho việc hỏi.
4. **Use case per dòng bảng** (khi dòng có nhánh): precondition · main flow · alternate · postcondition — mỗi nhánh ngoại lệ sau này là 1 AC/ca biên ở Bước 5. Ghi gọn ngay dưới bảng — phần D lấy làm AC.
5. **Màn nháp + câu hỏi có hệ quả** — ngay dưới bảng luồng: (a) **theo vai**: mỗi vai làm gì, làm thế nào (nguồn cho ma trận ở mục C); (b) **màn nháp** `Mã màn · Module · Vai dùng · Hành động phải có trên màn · Dữ liệu hiển thị` — mỗi dòng bảng luồng có thao tác trên hệ thống phải có màn đứng; cột **Dữ liệu hiển thị** liệt kê MỌI vùng dữ liệu người dùng thấy trên màn, kể cả chỉ xem (bảng · tab lịch sử · panel · badge đếm · danh mục nguồn của ô chọn), bằng lời nghiệp vụ — đây là đặc tả chức năng của màn, SA thiết kế API từ nó (không ghi tên API/bảng); (c) mỗi ô `CHƯA HỎI` viết thành **câu hỏi bối cảnh** (`discovery-hypothesis` §Câu hỏi bối cảnh) **kèm hệ quả A/B lên màn** ("HR lập tờ trình → nút ở EMP-DETAIL chỉ HR thấy · Quản lý lập → thêm lối vào + bước HR tiếp nhận"). Authority trả lời theo hệ quả, không trả lời mơ hồ.
6. **Bảng chính sách từng hành động — research + suy luận, Authority chọn.** Bảng luồng nói *ai làm gì theo thứ tự nào*; bảng này nói *mỗi việc được làm trong điều kiện nào* — chỗ Authority hay thiếu chuyên môn nhất, cũng là nơi sinh bug "tài liệu im lặng" (vd đăng ký làm từ xa lúc 18h vẫn được vì không ai đặt hạn chót). **Authority không cần biết trước luật — BA mang chuyên môn, Authority chỉ chọn.**
   Mỗi dòng bảng luồng có thao tác trên hệ thống → 1 dòng `Hành động · Khi nào được làm · Ai · Giới hạn · Trạng thái tiền đề · Trùng/xung đột · Vi phạm thì · Ngoại lệ · Nguồn` (khung `TEMPLATE.interview.md`). Ô không áp dụng ghi `n/a — <lý do>`, **không ô trống**. Cách lấp:
   - **Research = nguyên liệu, không phải đáp án**: không ai công bố cách làm sản phẩm của họ. Research cho *luật/quy định* (số liệu bắt buộc) + *dấu vết chiều chính sách* — help center / hướng dẫn cấu hình của sản phẩm cùng loại lộ ra **họ cho chỉnh những gì** (có mục "hạn chót đăng ký" = chiều cần quyết), hiếm khi cho giá trị mặc định.
   - **Suy luận ra đề xuất** (PROTOCOL §2.3) — nguyên liệu research + kiến thức chuyên môn đã có, qua 4 phép thử chính sách cho MỖI hành động:
     (1) **Lạm dụng** — để tự do hoàn toàn thì ai lợi dụng được? (đăng ký làm từ xa lùi ngày để hợp thức hoá ngày vắng)
     (2) **Hạ nguồn** — dữ liệu của hành động này ai dùng, **chốt lúc nào** (chấm công cuối ngày · lương cuối tháng · báo cáo cuối kỳ)? Làm sau mốc chốt thì dữ liệu hạ nguồn sai thế nào? → **hạn chót suy ra từ mốc chốt hạ nguồn** — phép thử mạnh nhất, không cần nguồn ngoài.
     (3) **Xung đột** — cùng người / cùng thời gian / cùng tài nguyên còn nghiệp vụ nào? (ngày đã có phép duyệt · ngày lễ · đi công tác · trùng lịch)
     (4) **Vòng đời** — sửa/huỷ sau khi duyệt, hoặc sau khi dữ liệu đã bị hạ nguồn dùng, thì sao?
   - **Nguồn** — nhãn chung PROTOCOL §2.3: `Authority` · `[quy định] <link>` (luật / nghị định bắt buộc — phải có văn bản) · `research <link> + suy luận → Authority chọn` · `suy luận → Authority chọn` (research không ra gì). KHÔNG gắn link chung chung rồi gọi "chuẩn ngành".
   - Ô cần Authority chọn → gom **một lượt hỏi Authority dạng quyết định** (`AskUserQuestion`), mỗi câu trình **đủ 3 phần** (PROTOCOL §2.3): research cho thấy gì · áp vào hành động này ra sao (trích phép thử, nói hệ quả nếu không có luật) · **đề xuất mặc định** + 1-2 phương án khác. Authority không rành → chọn đề xuất; có chính sách riêng → sửa. Chưa chọn = `CHƯA HỎI`.
   - Bảng này là **nguồn của business-rule (mục B) và AC luật (phần D)**: mỗi ô có giá trị (không `n/a`) → ≥1 rule/AC; mỗi giới hạn số/thời gian → ca biên **giá trị biên** (hạn chót 17h → 16:59 · 17:00 · 17:01).
7. **Lắp ráp rồi playback.** Trước khi đọc cho Authority, chạy **suy luận lắp ráp** (PROTOCOL §2.3) giữa các bảng luồng + bảng chính sách vừa dựng — kéo theo · chọi nhau · chỗ nối · còn hở → câu hỏi mới hỏi luôn lượt này. Playback **đọc BẢNG, không đọc văn xuôi**: "bước 1: HR đăng tin, bộ phận chỉ nhờ — đúng không?". Sai actor lộ trên một dòng bảng trong 5 giây. Authority gật → ghi `chốt bởi Authority: <ngày ISO>` trên bảng. Gate DOCUMENT đòi: ≥1 bảng · đã ký · không ô `CHƯA HỎI` · bảng chính sách có dòng, không ô trống.

Bảng + màn nháp là **nguồn duy nhất** cho: ô `có/cấm` ma trận PERSONAS §2 (mục C dưới) · actor của AC (phần D) · actor của event-storming · SCREEN-MAP (`ux-design`) · luồng nghiệp vụ mà build/verify/dogfood đi theo. Không nơi nào được tự suy actor ngoài bảng. Bảng chính sách là **nguồn duy nhất** của luật hành động (khi nào · bao nhiêu · trùng gì · ngoại lệ).

## B. Business-rule (từ bảng luồng + bảng chính sách A.6 + INTERVIEW)
§Phát biểu (1 câu rõ) + §Lý do (**reference nguồn**: luật/policy/contract/quyết định — "best practice" chung chung không tính; chuẩn ngành phải kèm link; rule từ bảng chính sách → nguồn = cột Nguồn của ô, `suy luận → Authority chọn` hợp lệ kèm lập luận) + §Khi nào áp dụng + §Ngoại lệ + §Hệ quả + **≥2 ví dụ** (1 happy + 1 vi phạm, số liệu — QC seed test) + `severity` CORNERSTONE/NORMAL + **`related_features` ≥1** (rule chỉ 1 FEAT → đáng lẽ là AC, đưa thành AC trong FEAT đó) + §**Phải chặn gì** (điều không bao giờ được xảy ra, nói bằng lời nghiệp vụ). Chặn **Ở ĐÂU** (unique index · cột `version` · state machine…) là việc SA — ghi ở `arch/{name}.md §6`, cột AC/BR trỏ về rule này.

## C. Persona + ma trận vai × hành động (sinh TỪ bảng luồng)
role/goals/pains/workflow narrative. **Anti-persona BẮT BUỘC.** Ma trận `docs/PERSONAS.md §2`: **ô `có` = có dòng bảng luồng mà vai đó ở cột Ai LÀM**; vai không có dòng nào cho hành động đó = `cấm`. KHÔNG suy từ FEAT (FEAT viết sau ma trận; suy ngược = sai đồng bộ, trace không bắt). Không ô trống. **`PERSONAS §3` Gán vai dogfood**: mỗi vai dogfood (edge · newbie · picky · rushed · breaker · mobile) đóng persona nào — dogfood đọc mục này (đợt chạy do `dogfood.md` quyết, không ghi ở đây).

## Hỏi hay không hỏi
Ô bảng luồng chưa có bằng chứng → phân loại theo bảng PROTOCOL §2.3: research được quy trình chuẩn / vai chuyên trách → ghi `research <link> + suy luận` (vẫn đọc cho Authority ở playback để xác nhận) · chỉ Authority biết (cách đơn vị họ đang làm, chính sách riêng) → ghi `CHƯA HỎI` rồi hỏi ngay bằng câu bối cảnh.

## Quy tắc
- ID `BR-<slug>` (nếu tách rule) / persona đặt trong `PERSONAS.md`. Cross-ref bằng ID canonical đầy đủ.
- Một lớp doc — KHÔNG `docs/domain/`, KHÔNG bước translate. Mọi thứ BA viết là **cái gì / ai / khi nào**, không ghi tên class, bảng hay công nghệ.

## D. Viết AC + ràng buộc vào khung FEAT (Bước 5 nhịp 2)
PO đã tạo khung FEAT (capability · has_ui · §1 Mục tiêu · §Ngoài phạm vi · §References dòng bảng luồng phủ) ở nhịp 1 (`domain-po`). BA điền **§2 AC** + **§3 Ràng buộc nghiệp vụ**, không sửa phần của PO — thấy khung sai (thiếu FEAT, phạm vi lệch) thì báo PO sửa.

**Boot**: `docs/INTERVIEW.md §Luồng nghiệp vụ đã xác nhận` (bảng + use case A.4 + màn nháp) · `docs/PERSONAS.md §2` · business-rule đã ghi nháp (mục B) · khung FEAT trong `docs/feat/`.

**Cách viết AC BDD tốt**
- **Cho/Khi/Thì (Given/When/Then)** — mỗi AC 1 hành vi kiểm được, có kết quả quan sát được (không "hệ thống hoạt động đúng").
- **Actor của AC = cột Ai LÀM trong bảng luồng đã ký** — CẤM lấy từ cột Ai NHỜ/duyệt, CẤM suy từ "ai có nhu cầu". AC cần actor mà bảng không có dòng → quay mục A hỏi Authority (còn DOCUMENT), không tự gán rồi ghi DECISIONS.
- Mỗi nhánh use case (A.4) → 1 AC hoặc ca biên. KHÔNG viết AC cho điều PO đã ghi ở §Ngoài phạm vi.
- **AC có hành vi cảnh báo / xác nhận / giữ dữ liệu khi rời màn** → nêu **người dùng chọn được gì và chuyện gì xảy ra với từng lựa chọn** (vd "Ở lại → dữ liệu còn nguyên · Rời đi → bỏ dữ liệu đã nhập"), không viết "có cảnh báo" chung chung. Hộp cụ thể do UX vẽ (kho `DESIGN-SYSTEM §3`) — BA không ghi tên component.
- Phủ **4 loại nền tối thiểu**: happy path · validation (input sai) · error/failure · a11y (bàn phím/screen-reader/tương phản khi là UI). **≥4 AC/FEAT.**
- **TAXONOMY CA BIÊN — quét MỖI FEAT qua TỪNG trục.** Trục nào FEAT chạm → **phải có AC**; không chạm → ghi `n/a`, **KHÔNG bỏ trắng** (bỏ trắng = điểm mù Authority lọt thẳng tới code):
  - **rỗng/đầy/biên**: 0 bản ghi · đúng 1 · rất nhiều (phân trang) · min/max/tràn độ dài
  - **lỗi/timeout**: input sai · downstream chết/chậm · validate fail → hiện thông báo gì
  - **quyền/tenant**: vai bị `cấm` (ma trận) · chạm dữ liệu tenant khác · thu hồi quyền giữa chừng
  - **đồng thời**: gửi 2 lần · 2 người sửa 1 bản ghi · race tạo trùng
  - **thời gian/kỳ**: **cửa sổ được phép hành động** (hạn chót · làm lùi ngày · ngoài giờ · ngày lễ — lấy từ bảng chính sách A.6) · hết hạn giữa chừng · ranh giới kỳ (cuối tháng/năm/ca) · timezone · job chạy nền
  - **tiền/số**: làm tròn · số âm · đơn vị · cộng dồn lệch
  - **idempotency**: retry · webhook/callback lặp · job chạy 2 lần
  - **partial-failure**: ghi xong nhưng thông báo/email fail → bù/hoàn thế nào
  - **thứ tự**: sự kiện tới lệch thứ tự · phụ thuộc bước trước chưa xong
  > Danh sách này còn là **danh sách săn** cho `pre-mortem` audit (cuối DOCUMENT).
- **LƯỚI LUỒNG — cạnh-có-chủ + seam** (chống miss luồng; cùng idiom n/a tường minh):
  - **Cạnh-có-chủ**: FEAT đụng entity có trạng thái → mọi **cạnh chuyển trạng thái** (vòng đời trong bảng luồng, kể cả cạnh ngoài-hạnh-phúc: chưa-kích-hoạt · bị-khoá · thu hồi · rời đi) phải có AC phủ **hoặc** 1 dòng `n/a`/out-of-scope. Cạnh không chủ = luồng miss.
  - **Seam**: FEAT nối FEAT khác (dữ liệu chảy qua) → trả lời được *"output của FEAT này đến tay ACTOR của FEAT kia bằng CƠ CHẾ gì?"* (email · SMS · notification · in giấy · admin đưa tay). Cơ chế chưa viết ở đâu = luồng thiếu — viết thành AC.

**§3 Ràng buộc nghiệp vụ**: mỗi AC/BR có điều "không bao giờ được xảy ra" (không trùng · chỉ vai X · không vượt hạn mức…) → 1 dòng, nói bằng lời nghiệp vụ + nguồn. KHÔNG ghi chặn ở đâu (SA ghi ở `arch §6`, trỏ ngược về dòng này).

**Chỗ chưa rõ**: không hỏi lại điều Authority đã trả lời; còn thiếu → phân loại theo bảng PROTOCOL §2.3.

## Done
- **Bước 3**: bảng luồng mọi nghiệp vụ đã kể: Authority ký, không ô `CHƯA HỎI` + bảng chính sách (mọi hành động có dòng · không ô trống · ô cần chọn có đề xuất đủ 3 phần + Authority đã chọn) + business-rule (≥2 ví dụ + nguồn + Phải chặn gì) + persona + ma trận (ô `có` trỏ được về dòng bảng) + mọi chỗ tự quyết có dòng `DECISIONS.md` → tiếp Bước 4 `capability-mapping`.
- **Bước 5 (D)**: mọi FEAT có ≥4 AC BDD (happy/validation/error/a11y) + taxonomy quét đủ trục (AC hoặc `n/a`) + cạnh trạng thái/seam có chủ + §3 Ràng buộc nghiệp vụ → tự rà bằng checklist `business-analysis` → tiếp Bước 6.
