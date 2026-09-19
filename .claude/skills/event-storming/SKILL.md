---
name: event-storming
description: Phương pháp event-storming cho /document — đọc candidate domains ở CAPABILITIES §2, facilitate event storming cho 1 domain → events ≥10 + commands + aggregates + hot-spots + external systems, ghi vào docs/arch/OVERVIEW.md §4. Làm từng domain một.
---

> Phương pháp cho /document (fork gộp discovery vào DOCUMENT). Không phải stage riêng.

# Event Storming Skill

## Khi load
Phương pháp **event-storming** cho `/document` (Architecture + Business). Facilitate event storming cho **MỘT domain mỗi lần**, theo candidate domains ở `docs/CAPABILITIES-MAP.md §2`. Interactive — dùng AskUserQuestion nhiều.

Input: `docs/CAPABILITIES-MAP.md §2` (candidate domains) + `docs/PERSONAS.md` (actors).

## Deliverable
Ghi vào `docs/arch/OVERVIEW.md §4 Event Storming` — **mỗi candidate domain (capability-map §2) một khối con** `### <domain>`. (Nếu domain phức tạp và tách file riêng thuận tiện hơn thì đặt tại `docs/arch/{domain}.md`; mặc định gom vào OVERVIEW §4.)

Mỗi khối con `### <domain>`:
- **Events**: **≥10 event** (numbered/list, past-tense, chronological).
- **Commands → event** (mỗi event có command + actor).
- **Aggregates** (≥1, state machine proto).
- **External systems** (≥1).
- **Hot-spots** (unresolved — output giá trị nhất).
- **Open questions** cho Architecture Authority (hand-off sang phương pháp boundary-charter).

## Phương pháp (4 phase)
1. **Events (past tense)**: "Sự kiện gì xảy ra trong domain? (OrderPlaced, RefundIssued...)". Thu 10-30, đừng over-constrain sớm.
2. **Commands + Actors**: mỗi event "command nào trigger? ai issue (persona/system)?".
3. **Aggregates**: group events mutate cùng entity → tên aggregate + state machine proto.
4. **Hot-spots + external + reactor**: cái chưa chắc/contentious, system ngoài, event→event chain.

## Quy tắc
- KHÔNG quyết boundary ownership (việc của phương pháp boundary-charter).
- 2 event cùng concept khác tên → push canonical naming (ubiquitous language seed).
- KHÔNG sửa `docs/CAPABILITIES-MAP.md` / `docs/PERSONAS.md` (read-only). Chỉ ghi vào `docs/arch/OVERVIEW.md §4`.
- REFINE mode: khối con đã có → đọc + tìm delta, KHÔNG rewrite from scratch.

## Flow
- 1 lượt = 1 domain. Nhiều domain → lặp phương pháp này (mỗi lần 1 domain) tới khi mọi candidate domain có khối con trong §4.
- Interactive (AskUserQuestion ≤5). Sau confirm: đủ mọi candidate domain thì tiếp phương pháp boundary-charter.

## Quality checklist
- [ ] Mỗi candidate domain (capability-map §2) có khối con `### <domain>` trong `docs/arch/OVERVIEW.md §4`.
- [ ] Events ≥10 (numbered, past-tense, chronological).
- [ ] Mỗi event có command + actor.
- [ ] ≥1 aggregate + ≥1 external + hot-spots flagged + open-questions cho Authority.

## Done
- Mọi candidate domain có section event-storming; user confirm → tiếp phương pháp boundary-charter.
