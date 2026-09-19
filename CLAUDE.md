# {{PROJECT_NAME}} — CLAUDE.md  (fork VIPER-style · feat/viper-adlc)

> **Router. Đọc top-to-bottom mỗi phiên.** Chi tiết → [PROTOCOL.md](PROTOCOL.md). Trạng thái sống → [STATE.md](STATE.md).

---

## NON-NEGOTIABLES
1. **Đọc `STATE.md` trước khi làm** (phase · wave · gate đang mở). Không rõ đang ở đâu → `/status`.
2. **Chuyển phase qua slash command**; **gate mỗi chốt** chặn "đi tiếp khi chưa đủ" — **chốt đỏ thì DỪNG**, báo thiếu gì, KHÔNG `force`.
3. **Sau khoá scope (DOCUMENT): KHÔNG hỏi Authority** (BUILD trở đi) — mơ hồ → `docs/DECISIONS.md` · tắc cứng → `STATE §Blocker` · ngoài scope → `ROADMAP §backlog`. (Ngoại lệ: hành động ra-ngoài / không-đảo-ngược thì hỏi thật.)
4. **Quyết định non-trivial → artifact NGAY** (DECISIONS/ADR/FEAT), không để trong chat.
5. **Sửa doc đã chốt = wave sau**: `ROADMAP §backlog` → `/next-wave` → `/document` top-up. Doc wave đã ship (`archive/`) **bất biến**; đổi surface đã giao = **additive** (BACKWARD-COMPAT).
6. **Không bypass test · không hardcode secret · code xong → git commit · artifact tạm → dọn** (luật #9).

> Vi phạm → hook chặn (`guard_ask`/`guard_bc`/`guard_ds`). `gate.py` chỉ BÁO thiếu gì (không chặn). Chi tiết PROTOCOL §6/§8.

## MAIN TỰ CODE
MAIN viết **toàn bộ code sản phẩm**. Agent CHỈ để **verification** (`reviewer`/`bug-hunter`/`test-writer` — chỉ trả finding, MAIN ghi §Findings) + **dogfood** (6 persona). **Không dev-agent, không build_prompt** — spawn bằng Task tool + prompt ngắn tay.

## HAI ĐƯỜNG VÀO
- **interview** — ý tưởng mới → `/document` phỏng vấn Authority.
- **intake** — tài liệu phân tích sẵn thả vào `intake/` → `/document` dịch (marker `NGUỒN: INTAKE` trong `docs/INTERVIEW.md`).

## NĂM PHASE · BẢY LỆNH
```
DOCUMENT → BUILD → VERIFY → [SHIP?] → NEXT-WAVE        (SHIP opt-in theo wave)
```
| Lệnh | Việc |
|---|---|
| `/document` | interview\|intake → PRD/PERSONAS/CAPABILITIES/FEAT/arch/UX → chia wave → **khoá scope** (1 lần cho dự án) |
| `/build [<wave>]` | **MAIN code** 1 wave: đọc KG/context → challenge → scaffold → walking skeleton → luồng lõi → chạy thật |
| `/verify` | auto-test (`test-cases.md`) + review 2 vai + **dogfood 6 persona** → MAIN sửa tới sạch |
| `/ship` | *(chỉ khi wave khai SHIP)* prod-ready → deploy → smoke → thử rollback |
| `/next-wave` | đóng wave (snapshot, **KHÔNG reset**) → **RÀ LẠI** + mở wave kế (loop engineering) |
| `/status` | *(mọi lúc)* đang ở đâu · gate thiếu gì · chốt kế |
| `/dogfood [<vai>]` | chạy lại dogfood (đủ 6 vai / 1 vai) |

## DOC SET (1 lớp `docs/` — chia per-target cho doc code)
| File | Vai |
|---|---|
| `PRD` · `PERSONAS`(+ma trận vai×hành động) · `CAPABILITIES-MAP` · `TECHSTACK` | nền dự án |
| `feat/FEAT-*` | AC (BDD) + ca biên + field kỹ thuật · `arch/OVERVIEW` + `arch/{target}` (frontmatter `kind/stack/consumes` + data/API/ranh giới) |
| `DESIGN-SYSTEM` + `ux/` (SCREEN-MAP + mockups) · `ROADMAP` (wave plan + §backlog) | UX · kế hoạch |
| `DECISIONS` · `BACKWARD-COMPAT` · `PRODUCTION-READY` · `adr/` | quyết định · hợp đồng · prod · ADR |
| `CONVENTIONS` · `SECURITY` **(framework, cố định)** | quy ước code cross-stack + bảo mật baseline |
| `knowledge-base/{target}.md` | **KG** — bộ nhớ va vấp, MAIN đọc TRƯỚC khi code target |

## ĐỌC GÌ KHI NÀO (chống lost-in-middle — targeted load)
- **Luôn**: `STATE.md` + `PROTOCOL.md`.
- **BUILD target X**: CHỈ slice của X — `ROADMAP wave-N` · `feat/FEAT-*` in-scope · `arch/X.md` · `knowledge-base/X.md` · mockup X · `CONVENTIONS`/`SECURITY`. KHÔNG đọc target khác.
- **Grep khi cần**: `DECISIONS` · `archive/`.
- **KHÔNG** đọc cả `docs/` rồi mới làm.

## HOOKS (awareness — chi tiết PROTOCOL §8)
`guard_ask` (AskUserQuestion chỉ ở DOCUMENT; Scope khoá ✓ / ngoài DOCUMENT → chặn) · `guard_bc` (deploy khi BC §3 xanh) · `guard_ds` (mockup dùng token, không hex thô) · `reanchor` (nhồi lại luật sau compact). `gate.py` chỉ BÁO.

## ROUTING
| Câu hỏi | Ở đâu |
|---|---|
| Đang ở đâu / thiếu gì | `/status` · `STATE.md` |
| Quy trình / gate / failure mode | `PROTOCOL.md` |
| FEAT/AC · thiết kế target | `docs/feat/` · `docs/arch/{target}.md` |
| Ai được / cấm làm gì | `docs/PERSONAS.md §2` |
| Quy ước code · bảo mật | `docs/CONVENTIONS.md` · `docs/SECURITY.md` |
| Va vấp / bất biến của target | `knowledge-base/{target}.md` |
