---
name: capability-mapping
description: Phương pháp map persona + capability cho /document — từ vision/problem sinh persona-pool (kèm MA TRẬN vai × hành động) + capability-map (persona × capability → outcome → candidate domain → wave giao). Capability TRƯỚC feature.
---

> Phương pháp cho /document (fork gộp discovery vào DOCUMENT). Không phải stage riêng.

# Capability Mapping Skill

## Khi load
Phương pháp **map persona + capability** cho `/document` (Business + Architecture co-author). Map **personas → capabilities → outcomes** và xác định **candidate domains** (input cho phương pháp event-storming). Load sau khi đã có bức tranh vision/problem (`docs/PRD.md`).

Input: `docs/PRD.md` (vision/problem/hypotheses).

## Hai chế độ hỏi (như khi khai thác ý tưởng — không đổi)

| Loại mục | Cách hỏi |
|---|---|
| **Khám phá** — persona là ai, họ làm gì hôm nay, ai được/không được làm gì, vì sao | **Hội thoại MỞ**. KHÔNG dùng AskUserQuestion — option mớm lời |
| **Quyết định** — gom capability nào vào domain nào, ưu tiên MVP hay Phase 2 | `AskUserQuestion` + đánh đổi cụ thể |

**Không giới hạn số câu.** Bốn luật đào sâu áp nguyên: hỏi quá khứ cụ thể · mỗi persona phải
dẫn được về người thật/vai thật · "thường/nhiều" quy ra số · đào theo mạch.

Lỗ hổng không giải được → ghi 1 dòng `docs/DECISIONS.md` (kèm giả định) rồi đi tiếp, đừng treo.

## Deliverable

1. **`docs/PERSONAS.md`** — giữ heading `## P1 — Name`, `## §2 Ma trận vai × hành động`, `## Anti-personas`:
   - **≥1 persona** `## P1 — <Name>` (role + goals + pains + workflow today + **năng lực được cấp** + **KHÔNG được làm** + anti-persona + active waves).
   - **≥2 anti-persona**.
   - **§2 Ma trận vai × hành động** — ≥1 hành động, **KHÔNG ô trống**.
   - **Gán persona cho vai dogfood** (6 lăng kính + cột Đợt).
2. **`docs/CAPABILITIES-MAP.md`** — giữ heading `## 1.` / `## 3.`:
   - **§1 Persona × Capability**: **≥5 capability row** (capability + persona cột + business outcome + candidate domain + MVP/Phase + **Wave giao** + **Trạng thái**).
   - **§3 Candidate domains**: **≥1 domain**. **Tên domain quyết định tên section event-storming** trong `docs/arch/OVERVIEW.md`.

## Ma trận vai × hành động — mục quan trọng nhất

Đây là artifact **duy nhất** trong toàn bộ vòng đời khai được *ai KHÔNG được làm gì*. Không có nó thì:
phân quyền lúc code là agent tự đoán · test không sinh được ca âm · dogfood không có gì để phá.

Cách dựng:
1. Liệt kê **hành động nghiệp vụ** (không phải endpoint, không phải màn hình) từ capability §1.
2. Mỗi persona một cột, cộng cột `chưa đăng nhập`.
3. Điền `có` / `cấm` — **mọi ô**. Ô có điều kiện ghi rõ: `có (chỉ bản ghi của mình)`.
4. Chỗ nào không chắc → **hỏi user**, đây vẫn là chỗ được hỏi. Vẫn không rõ → tự quyết theo hướng
   chặt hơn (`cấm`) + 1 dòng `docs/DECISIONS.md`. Mặc định chặt an toàn hơn mặc định mở.
5. Thêm **ca biên phân quyền** thứ ma trận không diễn tả được (A chạm dữ liệu của B; người submit
   tự duyệt bản của mình).

Ô trống là lỗi, không phải "chưa cần".

## Phương pháp map
1. **Persona seeding**: từ vision/problem + hỏi mở "Ai chạm vào việc này? Kể một ngày làm việc của họ".
2. **Capability**: mỗi persona "làm được gì?" (verb-noun: 'pay invoice', 'view order'). Tách capability rộng ("manage orders") thành atomic ("place order", "track order", "cancel order").
3. **Năng lực được cấp / KHÔNG được làm** per persona → nguồn của ma trận.
4. **Outcome + priority**: mỗi capability → outcome + vì sao persona muốn + gắn **MVP / Phase 2 / Phase N** (feed wave-sequencing khi chia wave).
5. **Candidate domain**: capability chia sẻ core entity → 1 domain (group theo data/event similarity, KHÔNG theo tech). Đây là input cho event-storming.
6. **Anti-capability**: nêu rõ cái NOT supported.

## Capability-map là bảng SỐNG, không chết sau khi map

Cột `Wave giao` để `_PLAN_` lúc map (chưa chốt được khi chưa chia wave), điền khi chia wave — cắt lát được
(`1 (scaffold), 3 (đầy đủ)`). Cột `Trạng thái` cập nhật ở `/next-wave`. Nhờ hai cột này trả lời được
"còn bao nhiêu năng lực chưa giao" từ MỘT file, không phải đọc lại mọi wave.

## Quy tắc
- KHÔNG assign capability cho boundary (việc của phương pháp boundary-charter).
- KHÔNG sửa `docs/PRD.md` (read-only ở bước này).
- Candidate domain dùng tên kebab rõ ràng (vd `payment`, `auth`) → khớp section event-storming trong `docs/arch/OVERVIEW.md`.
- **KHÔNG icon/checkmark** (`✓`/`✔`/emoji) ở bất kỳ đâu — dùng text (`x` / `có` / `cấm` / `-`). Convention no-icon toàn repo.

## Playback trước khi chốt
Đọc lại cho user: danh sách persona + ma trận quyền + danh sách capability. Ma trận là chỗ user hay
sửa nhất khi nghe đọc lại — vì nhìn bảng mới thấy mình vừa cấp nhầm quyền cho ai.

## Dấu hiệu hời hợt — dính ≥2 thì quay lại
- Persona bịa từ suy luận, không dẫn về được vai thật nào user kể
- Ma trận toàn `có`, không ô `cấm` nào — hệ thống nào cũng có ranh giới, không có nghĩa là chưa nghĩ tới
- Capability là tên màn hình / tên bảng chứ không phải động từ + đối tượng
- Mọi capability đều `MVP` — chưa cắt gì cả
- Không anti-capability nào

## Quality checklist
- [ ] ≥1 persona (`## P\d —`) + ≥2 anti-persona.
- [ ] Mỗi persona có `Năng lực được cấp` + `KHÔNG được làm`.
- [ ] §2 Ma trận vai × hành động: ≥1 hành động, KHÔNG ô trống, có ≥1 ca biên.
- [ ] Bảng gán 6 vai dogfood đã điền persona + đợt.
- [ ] ≥5 capability row THẬT (§1, không tính dòng mẫu/_TBD_).
- [ ] ≥1 candidate domain (§3) đặt tên rõ để event-storming dùng.
- [ ] Mỗi capability gắn MVP/Phase priority.
- [ ] Anti-capability listed.

## Done
- `docs/PERSONAS.md` + `docs/CAPABILITIES-MAP.md` đầy đủ; đã playback; user confirm → tiếp phương pháp event-storming.
