# {{PROJECT_NAME}} — harness-viper

> Khung quy trình **ý tưởng → tài liệu → code → verify** cho phát triển bằng AI agent:
> **MAIN tự code · 1 lớp tài liệu · command inline-prompt · ít script + gate nhìn thấy được**.

---

## Ý tưởng cốt lõi
- **MAIN viết toàn bộ code sản phẩm.** Agent chỉ để **verification** (review + dogfood).
- **1 lớp `docs/`** — nguồn sự thật duy nhất.
- **Gate mỗi chốt** (`scripts/gate.py`) chỉ **BÁO thiếu gì**, không chặn; hook (`guard_*`) mới chặn cứng.
- **Loop engineering**: plan toàn dự án ở DOCUMENT → mỗi wave rà lại kế hoạch đối chiếu kết quả wave trước.

## Năm phase · bảy lệnh
```
DOCUMENT → BUILD → VERIFY → [SHIP?] → NEXT-WAVE          (SHIP opt-in theo wave)
```
| Lệnh | Việc |
|---|---|
| `/document` | phỏng vấn\|intake → doc set (PRD/PERSONAS/CAPABILITIES/FEAT/arch/UX) → **chia wave** → khoá scope |
| `/build [<wave>]` | MAIN code 1 wave: đọc KG → challenge → scaffold → walking skeleton → luồng nghiệp vụ → chạy thật |
| `/verify` | review 2 vai → test case (`test-writer` viết đề → `bug-hunter` rà đề → `test-writer` sửa đề + chạy) → dogfood 6 persona → vòng sửa tối đa 3 lượt: MAIN sửa, agent rà lại đúng phần bị lỗi, còn lại sang wave sau → kết luận QC |
| `/ship` | *(chỉ khi wave khai SHIP)* prod-ready → deploy → smoke → thử rollback |
| `/next-wave` | đóng wave (snapshot, KHÔNG reset) → rà lại + mở wave kế |
| `/status` | *(mọi lúc)* đang ở phase/wave nào · gate thiếu gì · chốt kế |
| `/dogfood [<vai>]` | chạy lại dogfood (6 vai / 1 vai) |

## Hai đường vào
- **interview** — ý tưởng mới → `/document` phỏng vấn Authority.
- **intake** — tài liệu phân tích sẵn thả vào `intake/` → `/document` dịch (marker `NGUỒN: INTAKE`).

## Yêu cầu máy
`make` (GNU make) + shell POSIX `sh` · Docker · Python 3 (PyYAML chỉ cần cho `selftest`: `pip install pyyaml`). Lệnh `make` gọi 6 lệnh của từng target, thân lệnh viết cho `sh`.
| Hệ điều hành | Cài |
|---|---|
| Windows | Git for Windows (Git Bash có `sh`, `find`) + `winget install ezwinports.make` (hoặc `choco install make` / `scoop install make`). **Chạy `make` trong Git Bash**, không từ PowerShell/cmd. Đường dẫn user có dấu cách (vd `C:\Users\Nguyen Van A`) vẫn chạy được: Makefile gốc đã bọc `"$(MAKE)"`; Makefile per-target cũng phải bọc ngoặc kép mọi đường dẫn. Đặt `git config core.autocrlf input` để script `gradlew`/`mvnw`/Makefile không bị đổi sang CRLF. |
| macOS | `xcode-select --install` (nếu chưa có `make`) |
| Linux | `sudo apt install make` (hoặc `build-essential`) |

**Lệnh Python:** tài liệu viết `python`, hook trong `.claude/settings.json` gọi `py -3` (Windows), Makefile dùng `python3`. Máy thiếu cái nào thì ghi đè mà không sửa file: `make gate PYTHON="py -3"`; trên Mac/Linux đổi `command` của hook về `python3`.

`python scripts/selftest.py` cảnh báo nếu thiếu công cụ. Ở BUILD, MAIN tự cài `make`/`sh` theo bảng trên khi thiếu (`/build` Bước 3).

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
| `services/{boundaries\|web\|bff\|mobile\|desktop}/{name}/` | code sản phẩm (MAIN scaffold; chia nhóm theo `kind`) |
| `.claude/commands/` · `agents/` · `skills/` | 7 lệnh · 10 agent (pre-mortem + verify + dogfood) · thư viện skill (stack/ref/review/method) |
| `scripts/` | `gate.py` (báo) · `capture_proof.py` (proof máy-sinh) · hooks (`guard_*`/`reanchor`) · `bootstrap`/`next_wave`/`compact`/`selftest` · `qa_iso` (bản sao hệ để QA kiểm ca theo thời gian / job định kỳ) |
| `intake/` · `deployment/` · `archive/` · `tracking/` · `Makefile` · `.mcp.json` | khay tài liệu intake · docker-compose local · snapshot wave đã đóng · bằng chứng wave đang chạy (3 file) · hợp đồng 6 lệnh make · slot trình duyệt cho dogfood |

## Đọc gì khi cần
- **Đang ở đâu / thiếu gì** → `/status` · `STATE.md`
- **Quy trình / gate / hook** → `PROTOCOL.md`
- **Mẫu tài liệu** → `templates/README.md`
