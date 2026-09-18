---
description: STATUS — đang ở phase/wave nào, gate còn thiếu gì, chốt kế. Chạy mọi lúc, KHÔNG đổi state.
---
# /status

Chạy được **mọi lúc**. KHÔNG đổi phase, không tiêu gate.

## Đọc
1. `STATE.md` — dòng `Phase hiện tại` · `Wave` · `Phases wave này` + gate checklist đang mở (mục nào chưa tick).
2. `python scripts/gate.py` — chấm gate phase hiện tại (thiếu bằng chứng gì).

## Đọc thêm khi cần trả lời *"còn thiếu gì để đi tiếp"*
| Câu hỏi | Ở đâu |
|---|---|
| TC đang đỏ | `tracking/wave-N/test-cases.md` (dòng kết quả FAIL) |
| Finding chưa xử | `STATE §Findings` (BLOCKER/MAJOR open) |
| Amendment đang chờ | `docs/ROADMAP.md §backlog` |
| Ai được / KHÔNG làm gì | `docs/PERSONAS.md §ma trận vai×hành động` |
| Wave trước đã giao gì | `archive/wave-*/` (test-cases PASS + FEAT) |

## Báo cáo (3 dòng, KHÔNG đổ nguyên JSON)
```
Đang ở : <phase> · wave <N> · <target/kind>
Chốt kế: <lệnh cụ thể + arg>
Thiếu  : <gate đỏ / thiếu gì — hoặc "không thiếu, chạy được ngay">
```
Không đọc được `STATE.md` → nói thẳng là không đọc được, đừng đoán.
