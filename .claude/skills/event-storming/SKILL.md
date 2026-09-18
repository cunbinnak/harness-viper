---
name: event-storming
description: Phương pháp event-storming cho /document — facilitate event storming cho 1 domain → events ≥10 + commands + aggregates + hot-spots + external systems, ghi vào docs/arch/OVERVIEW.md. Làm từng domain một.
---

> Phương pháp cho /document (fork gộp discovery vào DOCUMENT). Không phải stage riêng.

# Event Storming Skill

## Khi load
Phương pháp **event-storming** cho `/document` (Architecture + Business). Facilitate event storming cho **MỘT domain mỗi lần**, theo candidate domains ở `docs/CAPABILITIES-MAP.md §3`. Interactive — dùng AskUserQuestion nhiều.

Input: `docs/CAPABILITIES-MAP.md §3` (candidate domains) + `docs/PERSONAS.md` (actors).

## Deliverable
Ghi một **section event-storming cho mỗi candidate domain** (§3 capability-map) vào `docs/arch/OVERVIEW.md` — mỗi domain một mục `## Event Storming — <domain>`. (Nếu domain phức tạp và tách file riêng thuận tiện hơn thì đặt tại `docs/arch/{domain}.md`; mặc định gom vào OVERVIEW.)

Mỗi section domain:
- **§1 Events**: **≥10 event** (numbered list, past-tense, chronological).
- §4 Commands → events (mỗi event có command + actor).
- §5 Aggregates (≥1, state machine proto).
- §6 External systems (≥1).
- §7 Hot-spots (unresolved — output giá trị nhất).
- §9 Open questions cho Architecture Authority (hand-off sang phương pháp boundary-charter).

## Phương pháp (4 phase)
1. **Events (past tense)**: "Sự kiện gì xảy ra trong domain? (OrderPlaced, RefundIssued...)". Thu 10-30, đừng over-constrain sớm. → §1.
2. **Commands + Actors**: mỗi event "command nào trigger? ai issue (persona/system)?" → §4.
3. **Aggregates**: group events mutate cùng entity → tên aggregate + state machine proto → §5.
4. **Hot-spots + external + reactor**: cái chưa chắc/contentious (§7), system ngoài (§6), event→event chain (§8).

## Quy tắc
- KHÔNG quyết boundary ownership (việc của phương pháp boundary-charter).
- 2 event cùng concept khác tên → push canonical naming (ubiquitous language seed §10).
- KHÔNG sửa `docs/CAPABILITIES-MAP.md` / `docs/PERSONAS.md` (read-only). Chỉ ghi vào `docs/arch/OVERVIEW.md`.
- REFINE mode: section đã có → đọc + tìm delta, KHÔNG rewrite from scratch.

## Flow
- 1 lượt = 1 domain. Nhiều domain → lặp phương pháp này (mỗi lần 1 domain) tới khi mọi candidate domain có section event-storming.
- Interactive (AskUserQuestion ≤5). Sau confirm: đủ mọi candidate domain thì tiếp phương pháp boundary-charter.

## Quality checklist
- [ ] Mỗi candidate domain (capability-map §3) có section `## Event Storming — <domain>` trong `docs/arch/OVERVIEW.md`.
- [ ] §1 Events ≥10 (numbered, past-tense, chronological).
- [ ] Mỗi event có command + actor (§4).
- [ ] ≥1 aggregate (§5) + ≥1 external (§6) + hot-spots flagged (§7) + open-questions cho Authority (§9).

## Done
- Mọi candidate domain có section event-storming; user confirm → tiếp phương pháp boundary-charter.
