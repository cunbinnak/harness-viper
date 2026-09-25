---
name: discovery-hypothesis
description: Phương pháp phỏng vấn khai thác cho /document Bước 1 (đường interview) — đào SÂU pain có bằng chứng (probe nghiệp vụ hóc búa) + 1 cược đo được (success metric + go/pivot/kill) + lỗ hổng. Bức tranh tổng quan TRƯỚC khi map capability/event-storming/boundary.
---

> Phương pháp cho /document (fork gộp discovery vào DOCUMENT). Không phải stage riêng.

# Discovery Hypothesis Skill

## Khi load
Phương pháp **khai thác ý tưởng** cho `/document` (vai **Business Authority**): biến ý tưởng/brief project thành **bức tranh tổng quan dạng giả thuyết** để đồng thuận vấn đề + đối tượng + cược gì, TRƯỚC khi map capability / event-storming / boundary. Load khi phỏng vấn Authority (đường interview) hoặc khi đọc `intake/`.

Input: mô tả project user truyền (`$ARGUMENTS`) hoặc tài liệu trong `intake/`. Không có → mở bằng câu hỏi mở, KHÔNG bằng option.

> **Đây là một trong những chỗ được hỏi nhiều nhất.** Mọi thứ không đào ra ở đây sẽ phải trả bằng
> một lần ngắt giữa lúc code, hoặc tệ hơn — bằng một quyết định agent tự đoán. Hỏi cho đủ và cho SÂU.

## Research xen vào phỏng vấn — chống hallucination + hỏi mù

**Trình tự (tránh research mù):** câu mở đầu nắm HẠT GIỐNG — Author muốn làm gì (hoặc đọc `intake/`) → **research domain đúng cái đó NGAY** (gọi `WebSearch`/`WebFetch`: pattern ngành + thuật ngữ + cách sản phẩm cùng loại giải) → bám kết quả research để **probe SÂU**. Chưa có hạt giống thì research dễ trúng generic/nhầm hướng; research xong hỏi mới trúng (probe hóc búa cần hiểu ngành để xoáy). Giữ mạch LIỀN — research là bước **xen giữa**, không phải gate dừng lại. Domain rộng → có thể research thêm giữa buổi khi mở mục mới.

**Bắt buộc, không "nếu có":** `WebSearch`/`WebFetch` luôn sẵn — domain mới mà không research = **trí nhớ mù → bịa có cấu trúc (hallucination)**. Mọi kiến thức domain phải có **NGUỒN**: research (ghi link vào PRD §6) / Authority trả lời / intake — KHÔNG từ "cảm giác".

## Ngân sách là THỜI GIAN, không phải số câu

**Không giới hạn số câu hỏi.** Một mục hỏi 3-4 lượt là bình thường. Xong trong 10 phút gần như
chắc chắn là hỏi hời hợt — dấu hiệu duy nhất đáng tin là *đã có bằng chứng cho từng pain hay chưa*,
không phải *đã hỏi đủ N câu hay chưa*.

## Hai chế độ hỏi — chọn đúng chế độ cho từng mục

| Loại mục | Cách hỏi |
|---|---|
| **Khám phá** — pain point, ai chịu, cách làm hiện tại, hệ quả, vì sao bây giờ | **Hội thoại MỞ bằng lời**, đào theo mạch trả lời. **KHÔNG dùng AskUserQuestion** — option có sẵn mớm lời, user bấm cái nghe hợp lý thay vì kể thực tế của họ. Đây là nguồn hời hợt số một |
| **Quyết định** — chọn giữa các hướng đã đếm được, ưu tiên cược nào trước | `AskUserQuestion` với option cụ thể **kèm đánh đổi** của từng cái |

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
| 1 | Pain point + ai chịu | Câu chuyện thật + con số: ai chịu, tần suất, mỗi lần mất gì. KHÔNG phải "người dùng nói chung" |
| 2 | Cách làm hiện tại (status quo) | Mô tả được họ đang xoay xở bằng gì — file/sổ/nhóm chat/phần mềm cũ |
| 3 | Cost of inaction | Không làm thì mất gì, và cái mất đó tăng theo quy mô ra sao |
| 4 | Vì sao bây giờ | Bối cảnh/áp lực khiến việc này thành cấp thiết lúc này |
| 5 | Cược đo được (success metric) | **MỘT con số + ngưỡng go/pivot/kill** ghi TRƯỚC khi nhìn số liệu. Giả thuyết phụ nếu nảy ra → ghi PRD §2 để verify sau, KHÔNG ép đủ ≥3/≥2. Out-of-scope tường minh → PRD §4 (chặn scope-creep) |
| 6 | Hướng tương lai (nguyên liệu Phase 2/N) | **MAIN tự suy** từ nghiệp vụ + research (đích 1-2 năm · nhóm user/nguồn thu kế tiếp · 2-3 việc "sau này chắc chắn cần") → **đề xuất, rồi hỏi Authority xác nhận** ở playback/challenge — KHÔNG bắt Authority tự kể. Kết quả nuôi cột MVP/Phase 2/N của CAPABILITIES-MAP (Bước 4) |
| 7 | Dữ liệu mẫu (→ PRD §7) | Ưu tiên **dữ liệu THẬT Authority đang có** (ảnh sổ · file Excel · tin nhắn). KHÔNG có (dự án mới toanh) → **MAIN research domain + TỰ CHUẨN BỊ** bộ mẫu realistic (đúng thuật ngữ/giá trị thật ngoài đời — như QA chuẩn bị test-data), playback Authority gật. Ghi rõ nguồn (thật \| chuẩn bị). Bộ này nuôi 4 chỗ: mockup · seed `deployment/local/` · dogfood · test-cases |

Ngờ scope quá lớn → **nói thẳng ngay tại đây**, đề xuất cắt cái gì. Đây là lúc cắt rẻ nhất.

## Ghi sổ NGAY trong lúc hỏi

Điền `docs/PRD.md` (**§1 Vấn đề** + **§2 Giả thuyết + rủi ro**) dần theo `templates/TEMPLATE.prd.md`. Không đợi hỏi xong hết mới viết:
viết muộn là viết theo trí nhớ đã bị làm mượt.

## Playback trước khi chốt

Trước khi báo xong: tóm tắt lại từng mục, đọc cho user nghe — *"tôi hiểu là X, đúng chưa?"*.
Sai chỗ nào sửa tại chỗ. Hiểu sai bắt được ở đây tốn một phút; lọt tới BUILD tốn nửa ngày code sai.

## Lỗ hổng → xử tại chỗ, không treo sang bước sau

Chỗ user không trả lời được, hoặc chưa quyết: (1) tìm trong tài liệu đã có → (2) hỏi user →
(3) vẫn chưa có → **tự quyết phương án hợp lý nhất + ghi 1 dòng `docs/DECISIONS.md`** (kèm giả định
đang mang) rồi đi tiếp. Mọi lỗ hổng ghi lại kèm cách xử — bảng lỗ hổng trống = chưa đào đủ.

## Deliverable (ghi vào `docs/PRD.md`)

1. **PRD §1 Vấn đề (pain)** — ai đau + đau gì (status quo) + hệ quả (cost of inaction) + **dòng `Bằng chứng:` không rỗng**. Vision narrative (vấn đề gì, cho ai, vì sao bây giờ) mở đầu §1.
2. **PRD §2 Giả thuyết + rủi ro** — **1 giả thuyết chính = success metric** (con số + ngưỡng go/pivot/kill, ghi TRƯỚC khi nhìn số) + rủi ro chính. Giả thuyết phụ (nếu có) thêm dòng cùng bảng — tùy chọn, KHÔNG ép số lượng.
3. **Nguồn** — ghi vào **PRD §6 Glossary + Nguồn**: **≥1 link research** (không chỉ "phỏng vấn"/"intake") — dấu vết đã tra domain. §6 không có URL research = **chưa research**, quay lại làm. **Kèm theo: danh sách LUỒNG CHUẨN NGÀNH** (5-10 bullet cạnh link — "mọi 〈ngành X〉 đều có: ...") — đây là lưới đối chiếu cho `pre-mortem` + PRE-LOCK dùng sau; research mà không đổ ra danh sách này = research để đó, không chống được miss luồng.
4. **Lỗ hổng & cách xử** — ≥1 dòng, mỗi lỗ có cách xử + vết (trỏ `docs/DECISIONS.md`).

## Dấu hiệu hời hợt — dính ≥2 thì quay lại hỏi tiếp

- Mỗi mục chỉ hỏi đúng một câu, không mục nào phải hỏi lần hai
- Không có con số nào trong toàn bộ tài liệu
- Không có câu chuyện thật nào — toàn mô tả trừu tượng ("người dùng hay gặp khó khăn khi…")
- User chỉ bấm chọn option, chưa từng phải gõ mô tả thực tế của họ
- Dòng `Bằng chứng:` chỉ là diễn đạt lại câu trả lời cho mượt hơn
- Bảng lỗ hổng trống — chưa buổi khai thác nào phủ hết mọi thứ ngay lần đầu
- Câu hỏi đầy term kỹ thuật không giảng giải; user gật đại cho xong

## Quy tắc

- KHÔNG bịa số liệu/nguồn. Số nào là giả định thì ghi rõ ở PRD §2 Giả thuyết + rủi ro để verify sau.
- KHÔNG viết hypothesis không test được.
- Idempotent: re-run thì update file, không tạo file mới / blind-append.
- KHÔNG icon/emoji trong tài liệu.

## Done
- `docs/PRD.md` (§1 Vấn đề + §2 Giả thuyết + rủi ro) đầy đủ + **§6 Nguồn có ≥1 link research** + đã playback + user confirm → tiếp Bước 2 (PRD trọn §1-6) → Bước 3 `domain-ba` (persona + ma trận) → Bước 4 `capability-mapping`.
