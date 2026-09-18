---
name: discovery-hypothesis
description: Phương pháp khai thác ý tưởng cho /document — KHAI THÁC SÂU ý tưởng project thành vision + problem có bằng chứng + ≥3 hypothesis testable + ≥2 anti-hypothesis + lỗ hổng. Bức tranh tổng quan TRƯỚC khi map capability/event-storming/boundary.
---

> Phương pháp cho /document (fork gộp discovery vào DOCUMENT). Không phải stage riêng.

# Discovery Hypothesis Skill

## Khi load
Phương pháp **khai thác ý tưởng** cho `/document` (vai **Business Authority**): biến ý tưởng/brief project thành **bức tranh tổng quan dạng giả thuyết** để đồng thuận vấn đề + đối tượng + cược gì, TRƯỚC khi map capability / event-storming / boundary. Load khi phỏng vấn Authority (đường interview) hoặc khi đọc `intake/`.

Input: mô tả project user truyền (`$ARGUMENTS`) hoặc tài liệu trong `intake/`. Không có → mở bằng câu hỏi mở, KHÔNG bằng option.

> **Đây là một trong những chỗ được hỏi nhiều nhất.** Mọi thứ không đào ra ở đây sẽ phải trả bằng
> một lần ngắt giữa lúc code, hoặc tệ hơn — bằng một quyết định agent tự đoán. Hỏi cho đủ và cho SÂU.

## Ngân sách là THỜI GIAN, không phải số câu

**Không giới hạn số câu hỏi.** Một mục hỏi 3-4 lượt là bình thường. Xong trong 10 phút gần như
chắc chắn là hỏi hời hợt — dấu hiệu duy nhất đáng tin là *đã có bằng chứng cho từng pain hay chưa*,
không phải *đã hỏi đủ N câu hay chưa*.

## Hai chế độ hỏi — chọn đúng chế độ cho từng mục

| Loại mục | Cách hỏi |
|---|---|
| **Khám phá** — pain point, ai chịu, cách làm hiện tại, hệ quả, vì sao bây giờ | **Hội thoại MỞ bằng lời**, đào theo mạch trả lời. **KHÔNG dùng AskUserQuestion** — option có sẵn mớm lời, user bấm cái nghe hợp lý thay vì kể thực tế của họ. Đây là nguồn hời hợt số một |
| **Quyết định** — chọn giữa các hướng đã đếm được, ưu tiên cược nào trước | **Hỏi bằng lời**: nêu option cụ thể **kèm đánh đổi** từng cái (KHÔNG dùng AskUserQuestion) |

## Bốn luật đào sâu (mất một luật là mất chiều sâu)

1. **Hỏi quá khứ cụ thể, không hỏi tương lai giả định.** "Lần gần nhất đơn bị nhầm là khi nào, kể lại?"
   chứ không phải "anh có muốn hệ thống chặn đơn nhầm không?". Ai cũng nói "có" với tương lai;
   chỉ quá khứ mới không nói dối.
2. **Mỗi pain point cần ≥1 bằng chứng**: câu chuyện thật đã xảy ra / con số / hiện vật (file Excel,
   ảnh sổ, tin nhắn đang dùng). Ghi vào dòng `Bằng chứng:`.
3. **"Thường", "nhiều", "hay bị" → quy ra số.** Bao nhiêu lần/tuần? Mỗi lần tốn bao nhiêu phút/tiền/khách?
4. **Đào theo mạch, đừng nhảy mục.** Sau mỗi câu trả lời tự hỏi: *"đã đủ để người khác quyết mà không
   phải quay lại hỏi chưa?"* — chưa thì hỏi tiếp cùng chủ đề.

**Ngôn ngữ**: user là người hiểu nghiệp vụ, không nhất thiết là kỹ sư. Hỏi bằng ngôn ngữ nghiệp vụ.
Term kỹ thuật bắt buộc phải dùng thì giảng giải theo hướng nghiệp vụ TRƯỚC khi hỏi — không hiểu câu
hỏi thì câu trả lời vô giá trị, và họ sẽ trả lời đại cho xong.

## Checklist đóng — đi tới khi đủ cả 6 mục

| # | Phải làm rõ | Đủ khi |
|---|---|---|
| 1 | Pain point + ai chịu | Câu chuyện thật + con số: ai chịu, tần suất, mỗi lần mất gì. KHÔNG phải "người dùng nói chung" |
| 2 | Cách làm hiện tại (status quo) | Mô tả được họ đang xoay xở bằng gì — file/sổ/nhóm chat/phần mềm cũ |
| 3 | Cost of inaction | Không làm thì mất gì, và cái mất đó tăng theo quy mô ra sao |
| 4 | Vì sao bây giờ | Bối cảnh/áp lực khiến việc này thành cấp thiết lúc này |
| 5 | Cược gì (≥3 hypothesis) | Mỗi cược falsifiable + tín hiệu đo được + cách kiểm + **bằng chứng vì sao tin** |
| 6 | KHÔNG cược gì (≥2 anti-hypothesis) | Nêu tường minh cái ngoài scope, để chặn scope-creep về sau |

Ngờ scope quá lớn → **nói thẳng ngay tại đây**, đề xuất cắt cái gì. Đây là lúc cắt rẻ nhất.

## Ghi sổ NGAY trong lúc hỏi

Điền `docs/PRD.md` (§Vision / §Problem) dần theo `docs/TEMPLATE.prd.md`. Không đợi hỏi xong hết mới viết:
viết muộn là viết theo trí nhớ đã bị làm mượt.

## Playback trước khi chốt

Trước khi báo xong: tóm tắt lại từng mục, đọc cho user nghe — *"tôi hiểu là X, đúng chưa?"*.
Sai chỗ nào sửa tại chỗ. Hiểu sai bắt được ở đây tốn một phút; lọt tới BUILD tốn nửa ngày code sai.

## Lỗ hổng → xử tại chỗ, không treo sang bước sau

Chỗ user không trả lời được, hoặc chưa quyết: (1) tìm trong tài liệu đã có → (2) hỏi user →
(3) vẫn chưa có → **tự quyết phương án hợp lý nhất + ghi 1 dòng `docs/DECISIONS.md`** (kèm giả định
đang mang) rồi đi tiếp. Mọi lỗ hổng ghi lại kèm cách xử — bảng lỗ hổng trống = chưa đào đủ.

## Deliverable (ghi vào `docs/PRD.md`)

1. **§Vision narrative** — 1-2 đoạn: vấn đề gì, cho ai, vì sao bây giờ.
2. **§Problem statement** — mỗi pain point + status quo + cost of inaction + **dòng `Bằng chứng:` không rỗng**.
3. **§Hypotheses** — ≥3 row: statement falsifiable + outcome đo được + test method + **cột Bằng chứng** + status TESTABLE.
4. **§Anti-hypotheses** — ≥2 item.
5. **§Lỗ hổng & cách xử** — ≥1 dòng, mỗi lỗ có cách xử + vết (trỏ `docs/DECISIONS.md`).

## Dấu hiệu hời hợt — dính ≥2 thì quay lại hỏi tiếp

- Mỗi mục chỉ hỏi đúng một câu, không mục nào phải hỏi lần hai
- Không có con số nào trong toàn bộ tài liệu
- Không có câu chuyện thật nào — toàn mô tả trừu tượng ("người dùng hay gặp khó khăn khi…")
- User chỉ bấm chọn option, chưa từng phải gõ mô tả thực tế của họ
- Dòng `Bằng chứng:` chỉ là diễn đạt lại câu trả lời cho mượt hơn
- Bảng lỗ hổng trống — chưa buổi khai thác nào phủ hết mọi thứ ngay lần đầu
- Câu hỏi đầy term kỹ thuật không giảng giải; user gật đại cho xong

## Quy tắc

- KHÔNG bịa số liệu/nguồn. Số nào là giả định thì ghi rõ ở §Hypotheses để verify sau.
- KHÔNG viết hypothesis không test được.
- Idempotent: re-run thì update file, không tạo file mới / blind-append.
- KHÔNG icon/emoji trong tài liệu.

## Done
- `docs/PRD.md` (§Vision/§Problem/§Hypotheses) đầy đủ + đã playback + user confirm → tiếp phương pháp capability-mapping.
