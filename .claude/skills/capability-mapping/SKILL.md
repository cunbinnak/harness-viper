---
name: capability-mapping
description: Phương pháp map capability cho /document — ĐỌC persona (domain-ba đã viết) rồi map capability-map (persona × capability → outcome → candidate domain → wave giao). Capability TRƯỚC feature. KHÔNG tự viết persona/ma trận.
---

> Phương pháp cho /document (fork gộp discovery vào DOCUMENT). Không phải stage riêng.

# Capability Mapping Skill

## Khi load
Phương pháp **map capability** cho `/document`. Map **personas → capabilities → outcomes** và xác định **candidate domains** (input cho phương pháp event-storming). Load sau khi đã có bức tranh vision/problem (`docs/PRD.md`) VÀ danh sách persona (`docs/PERSONAS.md`, do domain-ba viết).

Input: `docs/PRD.md` (vision/problem/hypotheses) + `docs/PERSONAS.md` (persona + ma trận vai × hành động — **read-only**, để map capability về persona).

## Hai chế độ hỏi (như khi khai thác ý tưởng — không đổi)

| Loại mục | Cách hỏi |
|---|---|
| **Khám phá** — persona này làm được gì, capability nào còn thiếu, vì sao | **Hội thoại MỞ**. KHÔNG dùng AskUserQuestion — option mớm lời |
| **Quyết định** — gom capability nào vào domain nào, ưu tiên MVP hay Phase 2 | `AskUserQuestion` + đánh đổi cụ thể |

**Không giới hạn số câu.** Bốn luật đào sâu áp nguyên: hỏi quá khứ cụ thể · mỗi capability phải
dẫn được về persona thật (đã có trong PERSONAS) · "thường/nhiều" quy ra số · đào theo mạch.

Lỗ hổng không giải được → ghi 1 dòng `docs/DECISIONS.md` (kèm giả định) rồi đi tiếp, đừng treo.

## Deliverable

**`docs/CAPABILITIES-MAP.md`** — giữ heading `## §1` / `## §2`:
- **§1 Capability → FEAT**: **≥5 capability row** (capability + persona cột + business outcome + FEAT + **Wave giao** + **Trạng thái**). Mỗi capability truy về ≥1 persona **đã có trong `docs/PERSONAS.md`**.
- **§2 Candidate domains**: **≥1 domain** (gom capability §1 theo core entity). **Tên domain quyết định tên section event-storming** trong `docs/arch/OVERVIEW.md §4`.

> **Ma trận vai × hành động KHÔNG thuộc skill này.** Nó do domain-ba viết ở `docs/PERSONAS.md §2`. Skill này **ĐỌC** ma trận đó (danh sách persona + ai được/cấm) để map capability về đúng persona — KHÔNG tự tạo persona/ma trận.

## Phương pháp map
1. **ĐỌC persona**: lấy danh sách persona + ma trận vai × hành động từ `docs/PERSONAS.md` (đã có, read-only). Không phát minh persona mới; capability không dẫn được về persona nào → 1 dòng `docs/DECISIONS.md`.
2. **Capability**: mỗi persona "làm được gì?" (verb-noun: 'pay invoice', 'view order'). Tách capability rộng ("manage orders") thành atomic ("place order", "track order", "cancel order").
3. **Outcome + priority**: mỗi capability → outcome + vì sao persona muốn + gắn **MVP / Phase 2 / Phase N** (feed wave-sequencing khi chia wave).
4. **Candidate domain** (§2): capability chia sẻ core entity → 1 domain (group theo data/event similarity, KHÔNG theo tech). Đây là input cho event-storming.
5. **Anti-capability**: nêu rõ cái NOT supported.

## Capability-map là bảng SỐNG, không chết sau khi map

Cột `Wave giao` để `_PLAN_` lúc map (chưa chốt được khi chưa chia wave), điền khi chia wave — cắt lát được
(`1 (scaffold), 3 (đầy đủ)`). Cột `Trạng thái` cập nhật ở `/next-wave`. Nhờ hai cột này trả lời được
"còn bao nhiêu năng lực chưa giao" từ MỘT file, không phải đọc lại mọi wave.

## Quy tắc
- KHÔNG assign capability cho boundary (việc của phương pháp boundary-charter).
- KHÔNG sửa `docs/PRD.md` / `docs/PERSONAS.md` (read-only ở bước này — persona + ma trận do domain-ba sở hữu).
- Candidate domain (§2) dùng tên kebab rõ ràng (vd `payment`, `auth`) → khớp section event-storming trong `docs/arch/OVERVIEW.md §4`.
- **KHÔNG icon/checkmark** (`✓`/`✔`/emoji) ở bất kỳ đâu — dùng text (`x` / `có` / `cấm` / `-`). Convention no-icon toàn repo.

## Playback trước khi chốt
Đọc lại cho user: danh sách capability + candidate domain (§2). (Persona + ma trận đã chốt ở bước domain-ba —
không lặp lại ở đây; chỉ chỉ ra capability nào chưa dẫn được về persona nào.)

## Dấu hiệu hời hợt — dính ≥2 thì quay lại
- Capability không dẫn về được persona nào trong `docs/PERSONAS.md`
- Capability là tên màn hình / tên bảng chứ không phải động từ + đối tượng
- Mọi capability đều `MVP` — chưa cắt gì cả
- Không candidate domain nào (§2) — event-storming không có input
- Không anti-capability nào

## Quality checklist
- [ ] ≥5 capability row THẬT (§1, không tính dòng mẫu/_TBD_).
- [ ] Mỗi capability truy về ≥1 persona có trong `docs/PERSONAS.md`.
- [ ] ≥1 candidate domain (§2) đặt tên rõ để event-storming dùng.
- [ ] Mỗi capability gắn MVP/Phase priority.
- [ ] Anti-capability listed.

## Done
- `docs/CAPABILITIES-MAP.md` §1 + §2 đầy đủ; đã playback; user confirm → tiếp Bước 5 `domain-po` (viết FEAT từ capability §1); §2 Candidate domains để dành cho `event-storming` ở Bước 6.
