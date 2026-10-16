---
name: discovery-hypothesis
description: Phương pháp phỏng vấn khai thác cho /document Bước 1 (đường interview) — đào SÂU pain có bằng chứng (probe nghiệp vụ hóc búa) + 1 cược đo được (success metric + go/pivot/kill) + lỗ hổng. Bức tranh tổng quan TRƯỚC khi map capability/event-storming/boundary.
---

# Discovery Hypothesis Skill

> **Vai: PO** · **Viết**: `docs/INTERVIEW.md` (lời kể · bằng chứng · cược) · `docs/PRD.md` §1 vấn đề · §2 giả thuyết · §3 NFR có số · §4 out-of-scope · §5 metric · §6 glossary + nguồn research · §7 dữ liệu mẫu
> **KHÔNG viết**: bảng luồng / ai làm bước nào (BA — `domain-ba`) · giải pháp kỹ thuật cho NFR (SA — `system-design`)

## Khi load
Phương pháp **khai thác ý tưởng** cho `/document` (vai **PO khám phá**): biến ý tưởng/brief project thành **bức tranh tổng quan dạng giả thuyết** để đồng thuận vấn đề + đối tượng + cược gì, TRƯỚC khi map capability / event-storming / boundary. Load khi phỏng vấn Authority (đường interview) hoặc khi đọc `intake/`.

Input: mô tả project user truyền (`$ARGUMENTS`) hoặc tài liệu trong `intake/`. Không có → mở bằng câu hỏi mở, KHÔNG bằng option.

> **Đây là một trong những chỗ được hỏi nhiều nhất.** Mọi thứ không đào ra ở đây sẽ phải trả bằng
> một lần ngắt giữa lúc code, hoặc tệ hơn — bằng một quyết định agent tự đoán. Hỏi cho đủ và cho SÂU.

## Research xen vào phỏng vấn — chống hallucination + hỏi mù

**Trình tự (tránh research mù):** câu mở đầu nắm HẠT GIỐNG — Authority muốn làm gì + **liệt kê các nghiệp vụ họ vừa kể** (hoặc đọc `intake/`) → research NGAY theo bảng dưới → bám kết quả để **probe SÂU**. Authority chưa có kinh nghiệm (không kể được nghiệp vụ) → hạt giống = loại sản phẩm + bối cảnh (§Authority chưa có kinh nghiệm). Chưa có hạt giống thì research dễ trúng generic/nhầm hướng; research xong hỏi mới trúng. Giữ mạch LIỀN — research là bước **xen giữa**, không phải gate dừng lại. Authority mở nghiệp vụ mới giữa buổi → research bù cho nghiệp vụ đó.

**Search CÁI GÌ — 4 loại, từ khoá sinh từ LỜI AUTHOR, không từ tên ngành** (search "HRMS best practices" ra mảng nổi nhất là lương, bỏ trắng tuyển dụng/onboarding — đúng chỗ về sau sai):
| # | Search | Để làm gì | Ai dùng |
|---|---|---|---|
| 1 | **Quy trình chuẩn của TỪNG nghiệp vụ Authority kể** — "quy trình 〈nghiệp vụ〉 chuẩn" / "〈nghiệp vụ〉 workflow" — Authority nêu 5 module = **5 lượt**, không gộp | Biết bước mặc định → nhận ra Authority nói KHÁC (= đặc thù, đào) hoặc KHÔNG nói (= lỗ, hỏi) | probe · `domain-ba` A bảng luồng |
| 2 | **Vai chuyên trách trong ngành** — "〈ngành〉 ai chịu trách nhiệm 〈việc〉" / "HR vs line manager vs payroll responsibilities" | Mặc định cột **Ai LÀM** (tuyển dụng = HR, line manager chỉ phỏng vấn/duyệt); Authority giao khác mặc định → phải có bằng chứng | `domain-ba` A + ma trận |
| 3 | **Menu/module của 2-3 sản phẩm cùng loại** — "〈loại sản phẩm〉 features list", trang demo/tour (JS-heavy → skill `browse`) | Mục lục sản phẩm trưởng thành = danh sách nghiệp vụ ngành → bắt mảng Authority quên | `pre-mortem` · PRE-LOCK |
| 4 | **Ràng buộc bên ngoài của bối cảnh Authority** — luật/quy định địa phương, tích hợp bắt buộc (máy chấm công, ngân hàng, thuế, hoá đơn) | Thứ Authority coi là hiển nhiên nên không kể, sản phẩm vẫn phải theo | probe compliance · arch integrations |
**Nguồn cho "ai làm bước nào"**: hướng dẫn sử dụng / help center của sản phẩm · văn bản luật · quy trình mẫu. Trang giới thiệu sản phẩm (marketing) chỉ dùng cho loại 3, không làm nguồn vai trò.
Ghi PRD §6 **theo từng nghiệp vụ** (không một cụm link chung): mỗi nghiệp vụ Authority kể có ≥1 nguồn loại 1 (+ loại 2 nếu nhiều vai). Nghiệp vụ không có nguồn = chưa research, `domain-ba` A.1 sẽ research bù trước khi dựng bảng.

**Research = nguyên liệu, không phải đáp án — sau research LUÔN có bước suy luận** (PROTOCOL §2.3). Research cho *bước* (loại 1) · *vai* (loại 2) · *mảng* (loại 3) · *quy định* (loại 4) · và **dấu vết chiều chính sách** (help center / trang cấu hình sản phẩm cùng loại lộ ra họ cho chỉnh gì: hạn chót, hạn mức, ai duyệt…). Suy luận đem nguyên liệu đó áp vào bối cảnh của Authority để ra đề xuất. **Giá trị chính sách** (hạn chót bao giờ, mấy ngày/tuần, ai được ngoại lệ) do BA suy luận ở `domain-ba` A.6 — Authority không cần biết trước.

**Research bắt buộc, làm TRƯỚC, không "nếu có":** `WebSearch`/`WebFetch` luôn sẵn — bỏ research mà nói từ trí nhớ = **bịa có cấu trúc (hallucination)**. Research xong thì **kiến thức chuyên môn đã có** (từ huấn luyện) được dùng trong bước suy luận để lấp chỗ research không nói — ghi nhãn `suy luận`, trình đủ lập luận (PROTOCOL §2.3). Mọi kiến thức domain phải có nguồn: research (link vào PRD §6) · Authority trả lời · intake · suy luận có lập luận. **Quy định bên ngoài** (luật, nghị định, chuẩn bắt buộc) thì kiến thức có sẵn KHÔNG thay được văn bản: không tìm được → ghi `chưa xác minh — <điều nhớ được>`, Authority xác nhận. KHÔNG gọi suy luận là chuẩn ngành.

## Lời Authority = luồng chính (happy path) — MAIN đề xuất phần Authority chưa nói

Authority kể phần họ đang nghĩ tới; phần chưa nghĩ tới hoặc quên vẫn có thật. Đừng chỉ chép lời kể: sau MỖI nghiệp vụ Authority kể, chạy 2 phép thử rồi **chủ động đề xuất**, không chờ Authority tự nhớ:
1. **Dữ liệu/cấu hình Authority nhắc tới → luồng sinh ra và dùng nó.** Hỏi: ai/cái gì tạo ra nó · khi nào đổi · ai dùng · kết thúc thế nào. Ví dụ: Authority nói "cấu hình loại phép có số dư" nhưng chưa nói **cấp phát** → thiếu cả vòng: cấp đầu năm / theo tháng cho người vào giữa năm · cộng thâm niên · trừ khi duyệt, hoàn khi huỷ · chuyển/hết hạn cuối năm · thanh toán khi nghỉ việc · HR chỉnh tay.
2. **Bước của quy trình chuẩn (research loại 1) chưa có trong lời kể** → đề xuất. Gồm cả nhánh lỗi (từ chối · trả lại · huỷ · quá hạn · người duyệt vắng), nghiệp vụ liền kề (loại 3) và ràng buộc ngoài (loại 4).

Nói thành **đề xuất cụ thể, đủ 3 phần của PROTOCOL §2.3** (research cho thấy gì · áp vào bối cảnh ra sao · đề xuất + hệ quả lên sản phẩm): "Luật cho người vào giữa năm hưởng phép theo số tháng làm việc [link] — hệ thống tự cấp hay HR nhập tay? Tự cấp → job đầu năm + khi tạo hồ sơ; nhập tay → màn điều chỉnh số dư." Authority chọn: **cần** (ghi INTERVIEW) · **không cần** (PRD §4 out-of-scope) · **để sau** (backlog) — không để đề xuất treo. Đề xuất KHÔNG tự thành scope: chỉ vào doc khi Authority nhận.

## Vòng làm việc mỗi tầng — research → đề xuất → trả lời → lắp ráp

Áp cho MỌI tầng (bản đồ nghiệp vụ → từng mảng → chi tiết) và cho cả Authority có hay chưa có kinh nghiệm:
```
research → suy luận ra đề xuất → Authority chọn / trả lời → suy luận lắp ráp → đọc lại cho Authority → hỏi tiếp chỗ hở
```
**Suy luận lắp ráp** (định nghĩa ở PROTOCOL §2.3) — sau MỖI lượt trả lời, ghép các câu trả lời với nhau, ghi kết quả vào `docs/INTERVIEW.md` ngay:
| Phép thử | Câu tự hỏi | Ví dụ (HRMS) |
|---|---|---|
| **Kéo theo** | Câu trả lời này đòi thêm dữ liệu / chức năng / màn nào chưa ai nhắc? | "có 2 chi nhánh" → cần dữ liệu cơ cấu tổ chức (chi nhánh · phòng ban) |
| **Chọi nhau** | Hai câu trả lời có mâu thuẫn không? | "đi muộn bị trừ lương" + "bản đầu tính lương ngoài hệ thống" → dữ liệu chấm công xuất ra phải có số phút đi muộn |
| **Chỗ nối** | Đầu ra của phần này đi vào phần nào, bằng cách gì, lúc nào? | chấm công → lương: kỳ công chốt lúc nào để xuất |
| **Còn hở** | Thiếu mảnh nào thì luồng không chạy tròn? | dữ liệu nhân viên cũ đang nằm trong Excel — chưa ai nói đưa vào hệ thống bằng cách nào (mảng nhập dữ liệu ban đầu) |

Kết quả = bức tranh tổng (các mảng · dữ liệu chảy giữa các mảng) + danh sách câu hỏi mới → đọc lại cho Authority → hỏi tiếp. Dừng khi một lượt lắp ráp không sinh câu hỏi mới. **Ai làm bước nào** KHÔNG chốt ở đây — câu hỏi loại đó chuyển sang BA (`domain-ba` A, lắp ráp lần nữa ở A.7).

## Authority chưa có kinh nghiệm — MAIN dẫn đường từ bản đồ xuống chi tiết

**Nhận biết**: Authority nêu được loại sản phẩm ("muốn làm HRMS") nhưng không kể được nghiệp vụ, hoặc trả lời "không biết" cho câu khám phá (đang làm thế nào · lần gần nhất sai là khi nào). Khi đó KHÔNG hỏi tiếp câu khám phá — Authority không có gì để kể. MAIN dẫn theo 6 bước, mỗi bước chạy đúng vòng ở mục trên:
1. **Hỏi bối cảnh** — câu Authority luôn trả lời được vì nói về chính họ: làm cho đơn vị mình dùng hay để bán · bao nhiêu người dùng · ngành · hoạt động ở đâu (luật nước nào áp dụng) · vì sao muốn làm (mơ hồ cũng được) · thời gian và ngân sách.
2. **Dựng bản đồ nghiệp vụ** — research menu 3–5 sản phẩm cùng loại (loại 3) + quy định bên ngoài (loại 4) → danh sách mảng nghiệp vụ của loại sản phẩm đó, mỗi mảng giải thích bằng 1 câu dễ hiểu.
3. **Đề xuất phạm vi bản đầu** — suy luận ra đề xuất với **4 phép thử thứ tự**: **phụ thuộc dữ liệu** (mảng là đầu vào của mảng khác → làm trước) · **tần suất đau** (hằng ngày trước hằng năm) · **rủi ro pháp lý** (sai là bị phạt → làm kỹ hoặc lùi lại sau) · **độ khó**.
4. **Authority chọn** phạm vi bản đầu (`AskUserQuestion`, đề xuất đủ 3 phần); mảng để sau ghi PRD §4.
5. **Đi sâu VẤN ĐỀ của từng mảng đã chọn** (việc của PO — mức *cái gì · vì sao*): mảng này đang đau gì · đang xoay xở bằng gì · mỗi lần mất bao lâu / bao nhiêu · ai chịu · không làm thì mất gì → đủ để viết PRD §1 và chọn cược. CHỈ hỏi bằng **câu hỏi bối cảnh** (mục dưới). **Quy trình từng bước — ai làm bước nào · ai duyệt · điều kiện được làm — KHÔNG đào ở đây**: đó là phân tích quy trình của BA (`domain-ba` A, Bước 3); BA dùng lại research loại 1–2 và cùng kỹ thuật câu hỏi bối cảnh.
6. **Bằng chứng thay thế cho pain** — Authority không có câu chuyện thật thì sản phẩm đang là phỏng đoán: nói thẳng điều đó, rồi lấy bằng chứng từ (a) người làm nghề thật mà Authority hỏi hộ — MAIN soạn sẵn 5–7 câu hỏi quá khứ cụ thể theo 4 luật đào sâu · (b) than phiền của người dùng sản phẩm cùng loại (review, diễn đàn — research loại 3) · (c) cược đo được khi đơn vị tự dùng thử bản đầu. Ghi nguồn bằng chứng ở dòng `Bằng chứng:` + rủi ro "chưa có trải nghiệm thật" ở PRD §2.

## Câu hỏi bối cảnh — đổi câu cần chuyên môn thành câu Authority trả lời được

Kỹ thuật **dùng chung** cho PO (ở đây) và BA (`domain-ba` A.5) — mỗi vai chỉ hỏi phần việc của mình:

| Vai | Câu cần chuyên môn (KHÔNG hỏi) | Câu bối cảnh (hỏi thay) |
|---|---|---|
| **PO** — vấn đề · giá trị · quy mô | "Pain point của bạn là gì?" | "Cuối tháng HR mất bao lâu để tổng hợp công? Lần gần nhất sai là sai gì?" |
| **PO** | "Sản phẩm cần đạt chỉ số nào?" | "Làm xong, bạn muốn bớt được việc gì — bớt bao nhiêu thì đáng bỏ công?" |
| **BA** — quy trình · vai · luật | "Quy trình duyệt nghỉ phép thế nào?" | "Ở chỗ bạn, ai đồng ý cho một người nghỉ — trưởng nhóm hay giám đốc?" |
| **BA** | "Chính sách chấm công ra sao?" | "Mọi người vào làm mấy giờ? Đi muộn có bị trừ lương không?" |
| **BA** | "Cần phân quyền thế nào?" | "Ai được xem lương của người khác?" |

Quy tắc: câu bối cảnh hỏi **sự việc đang có** ở đơn vị của Authority (ai · mấy giờ · có hay không · bao nhiêu · mất bao lâu), KHÔNG hỏi **thiết kế** (quy trình · chính sách · phân quyền · chỉ số). Thiết kế là việc vai đó suy luận từ câu trả lời. Áp cho cả Authority có kinh nghiệm — câu bối cảnh luôn dễ trả lời đúng hơn.

## Ngân sách là THỜI GIAN, không phải số câu

**Không giới hạn số câu hỏi.** Một mục hỏi 3-4 lượt là bình thường. Xong trong 10 phút gần như
chắc chắn là hỏi hời hợt — dấu hiệu duy nhất đáng tin là *đã có bằng chứng cho từng pain hay chưa*,
không phải *đã hỏi đủ N câu hay chưa*.

## Hai chế độ hỏi — chọn đúng chế độ cho từng mục

| Loại mục | Cách hỏi |
|---|---|
| **Khám phá** — pain point, ai chịu, cách làm hiện tại, hệ quả, vì sao bây giờ · **câu hỏi bối cảnh** | **Hội thoại MỞ bằng lời**, đào theo mạch trả lời. **KHÔNG dùng AskUserQuestion** — option có sẵn mớm lời, user bấm cái nghe hợp lý thay vì kể thực tế của họ. Đây là nguồn hời hợt số một |
| **Quyết định** — chọn giữa các hướng đã đếm được (gồm phạm vi bản đầu · đề xuất lựa chọn thiết kế), ưu tiên cược nào trước | `AskUserQuestion` với option cụ thể **kèm đánh đổi** của từng cái |

## Bốn luật đào sâu (mất một luật là mất chiều sâu)

1. **Hỏi quá khứ cụ thể, không hỏi tương lai giả định.** "Lần gần nhất đơn bị nhầm là khi nào, kể lại?"
   chứ không phải "anh có muốn hệ thống chặn đơn nhầm không?". Ai cũng nói "có" với tương lai;
   chỉ quá khứ mới không nói dối.
2. **Mỗi pain point cần ≥1 bằng chứng**: câu chuyện thật đã xảy ra / con số / hiện vật (file Excel,
   ảnh sổ, tin nhắn đang dùng). Ghi vào dòng `Bằng chứng:`.
3. **"Thường", "nhiều", "hay bị" → quy ra số.** Bao nhiêu lần/tuần? Mỗi lần tốn bao nhiêu phút/tiền/khách?
4. **Đào theo mạch, đừng nhảy mục.** Sau mỗi câu trả lời tự hỏi: *"đã đủ để người khác quyết mà không
   phải quay lại hỏi chưa?"* — chưa thì hỏi tiếp cùng chủ đề.

## Probe đào sâu nghiệp vụ — dùng khi câu trả lời còn ở bề mặt

Bốn luật trên là CÁCH đào; đây là GÓC đào — bộ câu hỏi hóc búa của BA lão luyện. Không hỏi máy móc cả bộ —
chọn góc đang mờ mà xoáy; mỗi probe đào ra chi tiết → về đúng dòng `Bằng chứng:` của mục liên quan, KHÔNG mở mục mới:

- **Chỗ tiền/dữ liệu rơi**: "Trong cách làm hiện tại, chỗ nào tiền hoặc số liệu dễ sai/thất thoát nhất?"
- **Ai chịu + phát hiện muộn**: "Khi chỗ đó sai, ai gánh? Biết sau bao lâu — ngay, cuối ca, hay cuối tháng mới lòi?"
- **Root cause (5-whys)**: hỏi "vì sao" liên tiếp tới gốc, đừng dừng ở triệu chứng ("đơn nhầm" → vì sao? → "chép tay" → vì sao chép tay? → …).
- **Ngoại lệ xử tay**: "Trường hợp nào quy trình chuẩn không lo được, phải xử tay/linh động?" — ngoại lệ là nơi phần mềm hay bỏ sót nhất.
- **Scale-break**: "Lượng đơn/khách/giao dịch tăng gấp 10 thì chỗ nào vỡ trước?"
- **Xung đột vai**: "Vai [A] và [B] có chỗ nào mâu thuẫn lợi ích? (nhanh vs kiểm soát · doanh số vs rủi ro)"
- **Compliance/ràng buộc**: "Có quy định pháp lý / hợp đồng / SLA nào bắt buộc phải theo không?"
- **JTBD**: "Không có sản phẩm này thì họ đang 'thuê' cái gì để làm việc đó?" — lộ đối thủ thật + tiêu chí thắng.
- **Vòng đời trọn (probe DÒNG — các probe trên cắt ngang, cái này chạy DỌC)**: xác định **đơn vị nghiệp vụ trung tâm** ("thứ gì chảy qua hệ thống, mang giá trị, qua tay nhiều người, sai thì đau nhất?" — đơn hàng · nhân viên · kỳ lương · booking) rồi: "Kể lần gần nhất MỘT 〈đơn vị đó〉 đi TRỌN vòng đời, từ sinh ra đến kết thúc — từng bước, ai làm, bằng gì?" Luồng miss thường sống ở đoạn Authority coi là hiển nhiên. Đầu ra nuôi event-storming + state machine `arch §1`.
- **Ngày đầu / ngày cuối (per persona chính)**: "Người mới toanh, ngày ĐẦU TIÊN, từ chưa-có-gì đến dùng-được — diễn ra sao?" · "Ngày họ RỜI ĐI thì sao?" — nhà của cấp credential, bàn giao, thu hồi quyền (họ luồng Định danh phổ quát — `pre-mortem` sẽ đối chiếu).

**Ngôn ngữ**: user là người hiểu nghiệp vụ, không nhất thiết là kỹ sư. Hỏi bằng ngôn ngữ nghiệp vụ.
Term kỹ thuật bắt buộc phải dùng thì giảng giải theo hướng nghiệp vụ TRƯỚC khi hỏi — không hiểu câu
hỏi thì câu trả lời vô giá trị, và họ sẽ trả lời đại cho xong.

## Checklist đóng — đi tới khi đủ cả 7 mục

| # | Phải làm rõ | Đủ khi |
|---|---|---|
| 1 | Pain point + ai chịu | Câu chuyện thật + con số: ai chịu, tần suất, mỗi lần mất gì. KHÔNG phải "người dùng nói chung". Authority chưa có kinh nghiệm → bằng chứng thay thế (§Authority chưa có kinh nghiệm bước 6) + rủi ro ghi PRD §2 |
| 2 | Cách làm hiện tại (status quo) | Mô tả được họ đang xoay xở bằng gì — file/sổ/nhóm chat/phần mềm cũ. Sản phẩm mới hoàn toàn (Authority chưa có kinh nghiệm) → ghi `chưa có` + cách người làm nghề đang làm (bằng chứng thay thế bước 6) |
| 3 | Cost of inaction | Không làm thì mất gì, và cái mất đó tăng theo quy mô ra sao |
| 4 | Vì sao bây giờ | Bối cảnh/áp lực khiến việc này thành cấp thiết lúc này |
| 5 | Cược đo được (success metric) | **MỘT con số + ngưỡng go/pivot/kill** ghi TRƯỚC khi nhìn số liệu. Authority không biết đặt ngưỡng → MAIN đề xuất (lựa chọn thiết kế) bằng 3 phép thử: **mốc hiện trạng** (giờ đang mất bao lâu / bao nhiêu — đo, hoặc ước có nguồn) · **mức cải thiện đáng để đổi** (cải thiện bao nhiêu thì người dùng chịu bỏ cách cũ) · **thời gian đo** (dùng bao lâu thì đọc số). Giả thuyết phụ nếu nảy ra → ghi PRD §2 để verify sau, KHÔNG ép đủ ≥3/≥2. Out-of-scope tường minh → PRD §4 (chặn scope-creep) |
| 6 | Hướng tương lai (nguyên liệu Phase 2/N) | **MAIN suy luận ra đề xuất** (PROTOCOL §2.3) từ nghiệp vụ + research theo 3 câu: nhóm người dùng kế tiếp · nguồn thu kế tiếp · 2-3 việc chắc chắn cần khi quy mô lớn lên (đích 1-2 năm) → **đề xuất, rồi hỏi Authority xác nhận** ở playback/challenge — KHÔNG bắt Authority tự kể. Kết quả nuôi cột MVP/Phase 2/N của CAPABILITIES-MAP (Bước 4) |
| 7 | Dữ liệu mẫu (→ PRD §7) | Ưu tiên **dữ liệu THẬT Authority đang có** (ảnh sổ · file Excel · tin nhắn). KHÔNG có (dự án mới toanh) → **MAIN research domain + TỰ CHUẨN BỊ** bộ mẫu realistic (đúng thuật ngữ/giá trị thật ngoài đời — như QA chuẩn bị test-data), playback Authority gật. Ghi rõ nguồn (thật \| chuẩn bị). Bộ này nuôi 4 chỗ: mockup · seed `deployment/local/` · dogfood · test-cases |

Ngờ scope quá lớn → **nói thẳng ngay tại đây**, đề xuất cắt cái gì. Đây là lúc cắt rẻ nhất.

## Ghi sổ NGAY trong lúc hỏi

Điền `docs/PRD.md` (**§1 Vấn đề** + **§2 Giả thuyết + rủi ro**) dần theo `templates/TEMPLATE.prd.md`. Không đợi hỏi xong hết mới viết:
viết muộn là viết theo trí nhớ đã bị làm mượt.

## Playback trước khi chốt

Trước khi báo xong: tóm tắt lại từng mục, đọc cho user nghe — *"tôi hiểu là X, đúng chưa?"*.
Sai chỗ nào sửa tại chỗ. Hiểu sai bắt được ở đây tốn một phút; lọt tới BUILD tốn nửa ngày code sai.
**Đây là playback của khám phá (vấn đề · đối tượng · cược). Quy trình *ai làm bước nào* KHÔNG chốt ở đây** — đó là việc BA ở Bước 3 (`domain-ba` mục A: bảng luồng, Authority ký từng dòng). Discovery chỉ cần thu đủ lời kể + bằng chứng để BA dựng được bảng.

## Lỗ hổng → xử tại chỗ, không treo sang bước sau

Chỗ Authority không trả lời được hoặc chưa quyết → phân loại theo bảng chỗ chưa rõ PROTOCOL §2.3 (quy định bên ngoài → tra văn bản · lựa chọn thiết kế → đề xuất, Authority chọn · chỉ Authority biết → hỏi bằng câu bối cảnh).
Mọi lỗ hổng ghi lại kèm cách xử — bảng lỗ hổng trống = chưa đào đủ.

## Deliverable (ghi vào `docs/PRD.md`)

1. **PRD §1 Vấn đề (pain)** — ai đau + đau gì (status quo) + hệ quả (cost of inaction) + **dòng `Bằng chứng:` không rỗng**. Vision narrative (vấn đề gì, cho ai, vì sao bây giờ) mở đầu §1.
2. **PRD §2 Giả thuyết + rủi ro** — **1 giả thuyết chính = success metric** (con số + ngưỡng go/pivot/kill, ghi TRƯỚC khi nhìn số) + rủi ro chính. Giả thuyết phụ (nếu có) thêm dòng cùng bảng — tùy chọn, KHÔNG ép số lượng.
3. **Nguồn** — ghi vào **PRD §6 Glossary + Nguồn**: **≥1 link research** (không chỉ "phỏng vấn"/"intake") — dấu vết đã tra domain. §6 không có URL research = **chưa research**, quay lại làm. **Ghi THEO TỪNG NGHIỆP VỤ Authority kể** (mỗi nghiệp vụ: nguồn loại 1 quy trình chuẩn + loại 2 vai chuyên trách, kèm 3-5 bullet "chuẩn ngành làm thế nào / ai làm") + danh sách **luồng chuẩn ngành** (loại 3, "mọi 〈ngành〉 đều có: ...") — lưới cho `domain-ba` A (mặc định Ai LÀM) và `pre-mortem`/PRE-LOCK. Một cụm link chung cho cả ngành = chưa research (mảng nổi nhất che các mảng còn lại).
4. **PRD §3 NFR có số** — Authority không biết đặt số → đề xuất theo phép thử ở comment §3 của `templates/TEMPLATE.prd.md`, Authority chọn.
5. **Lỗ hổng & cách xử** (PRD §8) — ≥1 dòng, mỗi lỗ có cách xử + vết (trỏ `docs/DECISIONS.md`).

## Dấu hiệu hời hợt — dính ≥2 thì quay lại hỏi tiếp

- Mỗi mục chỉ hỏi đúng một câu, không mục nào phải hỏi lần hai
- Không có con số nào trong toàn bộ tài liệu
- Không có câu chuyện thật nào — toàn mô tả trừu tượng ("người dùng hay gặp khó khăn khi…")
- User chỉ bấm chọn option, chưa từng phải gõ mô tả thực tế của họ (đường Authority chưa có kinh nghiệm: chọn đề xuất là bình thường — dấu hiệu hời hợt ở đó là KHÔNG có câu trả lời bối cảnh nào bằng lời)
- Dòng `Bằng chứng:` chỉ là diễn đạt lại câu trả lời cho mượt hơn
- Bảng lỗ hổng trống — chưa buổi khai thác nào phủ hết mọi thứ ngay lần đầu
- Không lượt lắp ráp nào sinh câu hỏi mới — chưa lắp ráp thật
- Authority chưa có kinh nghiệm mà vẫn bị hỏi câu cần chuyên môn ("quy trình thế nào?") — Authority trả lời đại cho xong
- Câu hỏi đầy term kỹ thuật không giảng giải; user gật đại cho xong

## Quy tắc

- KHÔNG bịa số liệu/nguồn. Số nào là giả định thì ghi rõ ở PRD §2 Giả thuyết + rủi ro để verify sau.
- KHÔNG viết hypothesis không test được.
- Idempotent: re-run thì update file, không tạo file mới / blind-append.
- KHÔNG icon/emoji trong tài liệu.

## Done
- `docs/PRD.md` (§1 Vấn đề + §2 Giả thuyết + rủi ro) đầy đủ + **§6 Nguồn có ≥1 link research** + đã playback + user confirm → tiếp Bước 2 (PRD trọn §1-7) → Bước 3 `domain-ba` (bảng luồng → rule → persona + ma trận) → Bước 4 `capability-mapping`.
