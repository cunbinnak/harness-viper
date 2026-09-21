# {{PROJECT_NAME}} — harness-viper

> Khung quy trình **ý tưởng → tài liệu → code → verify** cho phát triển bằng AI agent, học phương pháp **VIPER**:
> **MAIN tự code · 1 lớp tài liệu · command inline-prompt · ít script + gate nhìn thấy được**.
> Bản refactor tinh gọn (thay harness cũ: nhiều state · ~58 gate · build_prompt · 2 lớp doc).

---

## Ý tưởng cốt lõi
- **MAIN viết toàn bộ code sản phẩm.** Agent chỉ để **verification** (review + dogfood), không dev-agent.
- **1 lớp `docs/`** — nguồn sự thật duy nhất, không dịch 2 lớp business↔eng.
- **Gate mỗi chốt** (`scripts/gate.py`) chỉ **BÁO thiếu gì**, không chặn; hook (`guard_*`) mới chặn cứng.
- **Loop engineering**: plan toàn dự án ở DOCUMENT → mỗi wave rà lại kế hoạch đối chiếu kết quả wave trước.

## Năm phase · bảy lệnh
```
DOCUMENT → BUILD → VERIFY → [SHIP?] → NEXT-WAVE          (SHIP opt-in theo wave)
```
| Lệnh | Việc |
|---|---|
| `/document` | phỏng vấn\|intake → doc set (PRD/PERSONAS/CAPABILITIES/FEAT/arch/UX) → **chia wave** → khoá scope |
| `/build [<wave>]` | MAIN code 1 wave: đọc KG → challenge → scaffold → walking skeleton → luồng lõi → chạy thật |
| `/verify` | review 2 vai + `test-writer` thiết kế/chạy test-cases + dogfood 6 persona → MAIN sửa tới sạch |
| `/ship` | *(chỉ khi wave khai SHIP)* prod-ready → deploy → smoke → thử rollback |
| `/next-wave` | đóng wave (snapshot, KHÔNG reset) → rà lại + mở wave kế |
| `/status` | *(mọi lúc)* đang ở phase/wave nào · gate thiếu gì · chốt kế |
| `/dogfood [<vai>]` | chạy lại dogfood (6 vai / 1 vai) |

## Hai đường vào
- **interview** — ý tưởng mới → `/document` phỏng vấn Authority.
- **intake** — tài liệu phân tích sẵn thả vào `intake/` → `/document` dịch (marker `NGUỒN: INTAKE`).

## Bắt đầu
```bash
python scripts/bootstrap.py --name "Tên dự án" --authority "Tên <email>"   # thay {{PROJECT_NAME}}…
# rồi trong phiên agent:
/document        # dựng tài liệu + chia wave (SỐ WAVE = số dòng docs/ROADMAP.md §1)
/build 1         # code wave 1
/verify          # test + review + dogfood
/next-wave       # mở wave kế
python scripts/selftest.py   # smoke bộ khung
```
Wave chia theo `feat_cap_per_wave` (~3-4 FEAT/wave) — xem `docs/ROADMAP.md §1`.

## Cấu trúc repo
| Đường dẫn | Vai |
|---|---|
| `CLAUDE.md` | **router** — đọc mỗi phiên (luật nền, đọc gì khi nào) |
| `PROTOCOL.md` | **định nghĩa CHUẨN** quy trình (phase · gate · hook · failure modes) |
| `STATE.md` | **trạng thái sống** (phase/wave/gate đang mở) |
| `templates/` | mẫu tài liệu (copy → `docs/`; xem `templates/README.md`) |
| `docs/` | tài liệu THẬT (PRD/PERSONAS/FEAT/arch/ROADMAP…) + `CONVENTIONS`·`SECURITY` (framework) |
| `knowledge-base/{name}.md` | KG per-target — bộ nhớ va vấp, MAIN đọc TRƯỚC khi code |
| `services/{boundaries\|web\|bff\|mobile}/{name}/` | code sản phẩm (MAIN scaffold; chia nhóm theo `kind`) |
| `.claude/commands/` · `agents/` · `skills/` | 7 lệnh · 9 agent verify+dogfood · thư viện skill (stack/ref/review/method) |
| `scripts/` | `gate.py` (báo) · `capture_proof.py` (proof máy-sinh) · hooks (`guard_*`/`reanchor`) · `bootstrap`/`next_wave`/`compact`/`selftest` |

## Đọc gì khi cần
- **Đang ở đâu / thiếu gì** → `/status` · `STATE.md`
- **Quy trình / gate / hook** → `PROTOCOL.md`
- **Mẫu tài liệu** → `templates/README.md`
