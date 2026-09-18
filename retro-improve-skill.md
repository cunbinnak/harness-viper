---
type: retro
scope: xuyên suốt dự án (mọi wave) — dùng để cải thiện skill agent, KHÔNG phải sổ bug
---

# Retro — vấn đề khi phát triển, để cải thiện skill agent

> **Tài liệu sống, cộng dồn theo thời gian** — KHÔNG riêng cho 1 wave. Mỗi mục là một **lỗ trong
> QUY TRÌNH/SKILL** (không phải một bug đơn lẻ đã sửa) — bug cụ thể đã nằm ở
> `tracking/wave-{N}/review-findings.md`/`dogfood-report.md`. File này hỏi *"skill nào lẽ ra phải
> bắt được cái này, và vì sao không bắt được"*, để sửa skill chứ không chỉ sửa code. Mỗi mục ghi rõ
> **wave phát hiện** — khi sửa skill thật, tick vào cột cuối, KHÔNG xoá mục (giữ lịch sử).

| Wave phát hiện | # | Tóm tắt | Đã sửa skill? |
|---|---|---|---|
| wave-001 | A1 | Quyết định discovery không lan tới AC ("lý do nghỉ phép") | Chưa |
| wave-001 | A2 | Quyết định UI đặc thù mất khi rebuild-from-scratch (org-chart) | Chưa |
| wave-001 | A3 | Token spacing đúng ở mock nhưng code không áp (nút Duyệt/Từ chối) | Chưa |
| wave-001 | B1 | 2 agent ghi file chung đồng thời → đè mất nội dung | Chưa |
| wave-001 | B2 | Code xong quên `git add`/commit | Chưa |
| wave-001 | B3 | Rebuild-from-scratch không áp lại gotcha/quyết định cũ trong KG | Chưa |
| wave-001 | B4 | Biến env thiếu đồng bộ giữa `application.yml`/`docker-compose.yml`/`.env.example` | Chưa |
| wave-001 | B5 | Rescope giữa wave không cập nhật ngay bảng Deferred của wave plan | Chưa |
| wave-001 | C1 | **Mockup KHÔNG được rà lại khi FEAT đổi version — lệch diện rộng** | Chưa |
| wave-001 | D1 | **NGUYÊN NHÂN GỐC: gap-audit không có completion-tracking — 13 mục "làm" bị bỏ sót** | Chưa |
| wave-001 | F1 | **Back-edge domain mở (sửa nội dung) nhưng không bao giờ đóng (ký lại) — 110+ file business kẹt DRAFT 2 ngày** | Chưa |
| wave-001 | F2 | Amendment nội dung hợp lệ ở docs/domain/ không hề được `git commit` — chỉ tồn tại trong working tree | Chưa |

---

## A. Phát hiện từ UAT (`/next-wave` — user đọc trực tiếp trước khi ký) — wave-001, 2026-09-17

### A1. Quyết định discovery không lan tới AC — "lý do nộp đơn nghỉ phép"

- **Chuyện gì xảy ra**: User hỏi trực tiếp ngày 2026-09-16 "xin nghỉ phép có lý do chưa?" → quyết
  định đổi ngay, ghi rõ ở `ES-leave-management.md` (change log §15, dòng 239) + field-level ở event
  4 (dòng 26/86): `lý_do` bắt buộc cho UNPAID/OTHER_PAID, `ngày_dự_sinh` cho MATERNITY, `giấy_khám`
  tuỳ chọn cho SICK. Quyết định **dừng lại ở discovery** — không bao giờ được dịch vào
  `FEAT-hrm-007.md` (business + eng), không vào `BR-hrm-055.md`, không vào mockup, không vào code.
- **Skill nào lẽ ra bắt được**: `domain-ba`/`domain-po` (chốt dịch business→eng của `/domain`) —
  hai skill này đọc `capability-map`/`persona-pool`/`ES-*` để BIẾT viết gì, nhưng KHÔNG có bước đối
  chiếu ngược: "mọi dòng REVISION trong ES change-log đã có FEAT/BR nào tương ứng chưa?".
- **Vì sao lọt lưới đến cả review-document (chốt 9 rà chéo) và dogfood**: rà chéo chỉ đối chiếu
  capability↔FEAT↔AC ở mức tồn tại (có FEAT chưa), không đối chiếu ES change-log dòng REVISION↔AC.
  Dogfood/`breaker`/`picky` chỉ soi hệ ĐANG CHẠY so với AC hiện có — AC hiện có vốn đã thiếu thì
  dogfood không có gì để so.
- **Đề xuất sửa skill**: thêm bước cho `domain-ba`/`domain-po` (hoặc riêng `review-document`):
  grep mọi dòng `REVISION` trong `docs/discovery/event-storming/ES-*.md` change-log → xác nhận mỗi
  dòng đã có ít nhất 1 FEAT/BR tham chiếu (`§References` hoặc nội dung AC nhắc tới). Dòng REVISION
  không có FEAT/BR nào trỏ tới = finding BLOCKER ở chốt rà chéo.

### A2. Quyết định UI đặc thù bị mất khi rebuild-from-scratch — org-chart dùng sai component

- **Chuyện gì xảy ra**: `tracking/decisions.md` (2026-09-15, wave-003) quyết định RÕ: `OrgChartPage`
  dùng "box+line diagram" tự vẽ (`DepartmentTree.tsx`, `<ul>/<li>` lồng), KHÁC `DepartmentManagePage`
  (giữ AntD `Tree`) — hai màn tuy cùng dữ liệu nhưng khác mục đích hiển thị. Sau khi code mất và
  rebuild lại (2026-09-17), agent dựng cả 2 màn dùng CHUNG AntD `Tree` — quyết định tách biệt bị mất.
- **Skill nào lẽ ra bắt được**: `dev-{prefix}-{boundary}-agent` lúc rebuild-from-scratch — DOCS TO
  READ của chốt `start-dev` chỉ liệt kê FEAT/HLD/API/UX hiện hành, KHÔNG có bước đọc
  `tracking/decisions.md` lọc theo tên MÀN/COMPONENT cụ thể đang dựng.
- **Vì sao lọt lưới đến review-dev**: `review-web-agent` so sánh code với AC/BR/design-tokens (màu,
  spacing chung) — không có trục "đối chiếu quyết định UI đặc thù theo tên màn cụ thể trong
  decisions.md", vì decisions.md không phải nguồn review-agent được giao đọc.
- **Đề xuất sửa skill**: (1) `build_prompt.py` khi sinh prompt `start-dev`/review cho 1 boundary có
  UI, tự grep `tracking/decisions.md` theo tên file mockup/màn liên quan (`grep -i "<screen-name>"`)
  và chèn kết quả thẳng vào DOCS TO READ — không để agent tự nhớ tìm. (2) Khi rebuild sau mất code
  (tình huống đặc biệt), thêm bước bắt buộc: đọc TOÀN BỘ `learnings.decisions` trong KG cũ của
  boundary đó (nếu còn — KG không phase-locked, sống sót qua mất code) làm checklist "phải áp dụng
  lại", không chỉ đọc FEAT/HLD như dựng mới hoàn toàn.

### A3. Token spacing đúng nhưng không được áp cho cụm nút hành động cụ thể

- **Chuyện gì xảy ra**: mock (`shared.css` dòng 125) định nghĩa `.rowacts { gap: var(--space-xs) }`
  (4px) cho cụm nút hành động trong 1 dòng bảng. Code (`LeaveApprovalsPage.tsx` dòng 75) dùng antd
  `<Space>` không set `size` → rơi về default 8px — gấp đôi mock.
- **Vì sao lọt lưới**: agent + review đều verify "màu/token áp dụng đúng chưa" ở mức match màu (dễ
  đo bằng `getComputedStyle().color`), nhưng KHÔNG có bước đo `gap`/`margin` giữa các phần tử con
  trong 1 cụm — spacing tinh vi hơn màu, dễ bị bỏ qua khi chỉ đọc token bảng màu chung.
- **Đề xuất sửa skill**: `rules-web`/`review-web` thêm mục kiểm tường minh: với MỌI cụm nút hành
  động lặp lại nhiều dòng (table row actions), đo `getBoundingClientRect()` của 2 nút liền kề, so
  khoảng cách với giá trị mock đo cùng cách — không chỉ tin "dùng đúng class antd là xong".

---

## B. Vấn đề phát hiện xuyên suốt phiên rebuild wave-001 (không phải riêng UAT) — 2026-09-17

### B1. Hai agent ghi file mới gần đồng thời → đè mất nội dung nhau

- **Chuyện gì xảy ra**: xảy ra ≥2 lần trong phiên này — (1) `review-findings.md` giữa 2 agent
  review-dev vòng 1 (core/web) tưởng đã append an toàn nhưng thực ra file được TẠO đồng thời; (2)
  `dogfood-report.md` — agent `newbie` và `picky` (đợt 1) đều "tạo file mới theo template" gần cùng
  lúc, agent ghi SAU đè sạch nội dung agent ghi TRƯỚC (mất hoàn toàn phần `newbie`, phải khôi phục
  tay từ RETURN SCHEMA).
- **Đề xuất sửa skill**: mọi skill có bước "ghi vào 1 file CHUNG nhiều agent cùng đợt sẽ đụng" (
  `dogfood-*-agent`, `review-{kind}-agent` vòng 1 không-có-mốc) phải đổi hướng dẫn từ "tạo file theo
  template nếu chưa có" → "**kiểm `Read` trước — nếu đã tồn tại (dù trống/template) thì DÙNG `Edit`
  nối vào, KHÔNG `Write` đè**". Cân nhắc thêm: MAIN chạy 1 agent "khởi tạo file" tuần tự TRƯỚC khi
  spawn song song các lăng kính cùng đợt, để không ai phải tự quyết "tạo mới hay nối".

### B2. Code xong nhưng quên `git add`/commit — coi như chưa tồn tại

- **Chuyện gì xảy ra**: agent `dev-hrm-core-agent` (rebuild wave-001) báo `build: pass, test: pass`
  đầy đủ nhưng KHÔNG hề `git add`/commit — 588 file nằm hoàn toàn ngoài git. Review vòng 2 mới phát
  hiện (`RF-013`). Agent web tương tự cho 4 fix RF-001..004 (`RF-014`) — dù build/test pass thật.
- **Đề xuất sửa skill**: mọi task list của `dev-*-agent`/`fix-*-agent` phải có bước CUỐI CÙNG tường
  minh bằng chữ **"git add + git commit — build/test pass mà không commit = coi như CHƯA làm gì,
  đây chính là nguyên nhân dự án từng mất code (xem CLAUDE.md IDENTITY)"**, không để ẩn trong "Run
  scoped build/test" rồi ngầm hiểu commit theo sau.

### B3. Rebuild-from-scratch không tự động áp lại các gotcha/quyết định đã ghi trong KG cũ

- **Chuyện gì xảy ra**: `national_id` mã hoá (RF-006), reassign approver khi đổi manager (RF-008),
  CORS wiring (RF-001 gốc) — TẤT CẢ đã từng được fix + ghi vào `knowledge-base/core.knowledge-graph.
  yaml`/`web.knowledge-graph.yaml` ở implementation CŨ (trước khi mất code), nhưng agent rebuild
  KHÔNG đọc lại các mục này trước khi viết code mới → tự lặp lại đúng các lỗi đã từng vá.
- **Đề xuất sửa skill**: khi `start-dev` phát hiện `services/{boundary}/` trống NHƯNG
  `knowledge-base/{boundary}.knowledge-graph.yaml` đã có `learnings.decisions`/`gotchas`/
  `failure_modes` không rỗng (dấu hiệu rebuild-sau-mất-code, không phải dựng mới lần đầu) → BẮT
  BUỘC đọc hết các mục đó làm checklist áp dụng lại, ghi rõ trong RETURN SCHEMA mục nào đã áp/mục
  nào cố ý bỏ + lý do.

### B4. Biến môi trường có trong `application.yml` nhưng thiếu ở `docker-compose.yml`/`.env.example`

- **Chuyện gì xảy ra**: `HRM_NATIONAL_ID_KEY` (khoá AES mã hoá `national_id`) đọc được ở
  `application.yml` nhưng không được khai ở `docker-compose.yml` hay `.env.example` — chỉ phát hiện
  ở audit `production_ready` cuối wave, không phải lúc code hay review.
- **Đề xuất sửa skill**: `dev-handoff`/`infra-local-dev` thêm bước máy-móc: `grep -oE '\$\{[A-Z_]+' 
  application*.yml` đối chiếu 1-1 với biến khai trong `docker-compose.yml` + `.env.example` — thiếu
  1 biến ở 1 trong 3 nơi = finding, không chờ tới `production_ready` mới lộ.

### B5. Rescope giữa wave (rewind sau sự cố) không cập nhật ngay bảng "Deferred" của wave plan

- **Chuyện gì xảy ra**: quyết định rewind 2026-09-17 (loại 10 AC ra khỏi baseline wave-001) được ghi
  đầy đủ ở `tracking/decisions.md` NGAY LÚC rewind, nhưng KHÔNG được phản ánh vào bảng "Deferred to
  later waves" của `docs/plans/wave-001.md` cùng lúc — vì file đó phase-locked ngoài PLAN/REVIEW.
  Hậu quả: 3 gate khác nhau (`test_evidence`, `check_test_passed`, gián tiếp `dogfood_done`) đều vướng
  cùng 1 nguyên nhân, phải xử lý 3 lần bằng `force:true` trước khi tìm ra cách sửa gốc (back-edge hẹp
  MANUAL_TEST↔PLAN).
- **Đề xuất sửa skill/harness**: khi `decide.py` ghi một quyết định loại AC ra khỏi scope wave đang
  chạy (`--reversible` bất kỳ, `--why` trỏ tới FEAT/AC cụ thể), tự động nhắc (in ra màn hình, không
  chặn) "AC vừa loại cần khai thêm vào bảng Deferred của docs/plans/wave-N.md — hiện đang ở stage
  X, cần back-edge PLAN mới sửa được, làm ngay trong lượt này để tránh vướng gate nhiều lần về sau".

---

## C. Phát hiện diện rộng — mockup không đồng bộ với FEAT/AC khi FEAT đổi version

### C1. Mockup KHÔNG được rà lại có hệ thống mỗi khi FEAT liên quan đổi version

- **Chuyện gì xảy ra**: quét toàn bộ 10 mockup của wave-001 đối chiếu với các FEAT đã đổi version
  gần nhất (2026-09-15/16/17), chỉ ~2/9 điểm kiểm khớp đúng. Cụ thể:
  - `leave-approvals.html` (dòng 92) còn nguyên câu **"Chờ HR Admin khác duyệt hộ"** — đúng hành vi
    ĐÃ BỊ HUỶ BỎ hoàn toàn từ FEAT-hrm-008 v2 (NP-11/NS-08, 2026-09-16: HR không còn tham gia duyệt
    nghỉ phép dưới bất kỳ hình thức nào). Đây là mockup — TÀI LIỆU THIẾT KẾ NGUỒN — chứ không phải
    code, mức độ nghiêm trọng cao hơn 1 bug code thường vì mọi lượt code/review sau này đều tin
    mockup là đúng.
  - `onboarding.html` — dev-note vẫn viết AC-7 (rehire) "chưa giải quyết" trong khi DESIGN đã chốt
    xong từ 2026-09-13 (`ux-web.md` tự đánh dấu "ĐÃ GIẢI QUYẾT") — **bug thật** (ghi chú lỗi thời).
  - **KHÔNG phải bug** (đã xác nhận lại với user 2026-09-17, để KHÔNG lặp lại nhầm lẫn): `onboarding.
    html`/`profile-view.html`/`profile-edit.html` thiếu 3 field `employment_type`/`hire_date`/
    `tax_id` (FEAT-hrm-001 AC-8/9/10) và `leave-request.html` chỉ 3/5 loại phép (FEAT-hrm-007 AC-9)
    — cả hai đã có quyết định hoãn sang wave sau TỪ TRƯỚC (`docs/plans/wave-001.md` Sec Deferred).
    Mockup/code không vẽ/code phần deferred là ĐÚNG, không phải lệch. Nhãn "HR Admin" còn ở 10/10
    mockup cũng vậy — cố ý hoãn (`ux-web.md` Q10), không phải phát hiện mới.
- **Vì sao lọt lưới**: không có skill/gate nào đối chiếu "mockup ↔ version hiện tại của FEAT liên
  quan". `design-ux` (chốt vẽ mockup của `/domain`) chỉ vẽ MỘT LẦN theo FEAT lúc đó — khi FEAT được
  sửa SAU (qua back-edge `domain-po`/`domain-ba`), không có bước tự động nhắc "mockup nào tham chiếu
  FEAT này cần vẽ lại". `review-web-agent`/dogfood đều lấy MOCKUP làm chuẩn để so — nếu mockup sai
  thì cả review lẫn dogfood đều không phát hiện được (chuẩn so sánh chính nó đã sai).
- **Đề xuất sửa skill/harness**: (1) Thêm gate/kiểm mới ở chốt đóng-domain hoặc rà chéo: mỗi khi
  `domain-po`/`domain-ba` sửa 1 FEAT có `has_ui_touchpoint=true` (bump version), tự động in ra danh
  sách mockup tham chiếu FEAT đó (từ `SCREEN-MAP.md` cột `feat`) kèm nhắc "cần `design-ux` vẽ lại
  trước khi FEAT này coi là sẵn sàng cho dev". (2) `SCREEN-MAP.md` thêm cột "FEAT version lúc vẽ" —
  lệch với version hiện tại của FEAT = cảnh báo tự động, không cần người nhớ tay.

---

## D. NGUYÊN NHÂN GỐC — `gap-audit-2026-09-15.md` không có completion-tracking

> User tự đặt câu hỏi đúng trọng tâm: "vẫn chưa phải nguyên nhân chính gây tài liệu discovery chưa
> viết sang AC/FEAT". A1 (mục "lý do nghỉ phép") chỉ là MỘT trường hợp của một lỗ LỚN HƠN nhiều.

### D1. `gap-audit-2026-09-15.md` là ảnh chụp quyết định 1 lần, không phải checklist sống

- **Chuyện gì xảy ra**: file `tracking/gap-audit-2026-09-15.md` (80+ mục, rà độ phủ nghiệp vụ toàn
  hệ thống) có cột "Quyết định" ghi "làm"/"không làm"/"để sau" — nhưng **không có cột trạng thái
  hoàn thành**. Rà lại toàn bộ 10 FEAT wave-001 (2026-09-17, theo yêu cầu user) phát hiện **13 mục
  khác** (ngoài NP-15 đã biết) cùng bị bỏ sót: NS-01 (đổi vai trò không reassign đơn), NP-09 (không
  chặn chồng ngày nghỉ), NP-16 (không nghỉ nửa ngày), NP-06 (HR không điều chỉnh số dư), NP-08
  (không huỷ đơn đã duyệt), NP-12 (HR không tra cứu đơn nghỉ toàn công ty), NP-19 (field riêng theo
  loại phép, chi tiết hơn NP-15), NP-20 (duyệt đa cấp cho đơn >3 ngày), NS-05 (offboard thiếu ngày
  hiệu lực/lý do/loại chấm dứt), NS-13 (chưa đảo quyết định liên kết hồ sơ tái tuyển), NS-11 (hồ sơ
  thiếu tài khoản NH/mã BHXH), NP-17 (không có lịch nghỉ team). **TẤT CẢ 13 mục đều thuộc FEAT đã bị
  `domain-po`/`domain-ba` sửa lại SAU ngày quyết (2026-09-16, vì lý do KHÁC — đổi nhãn persona hoặc
  vá NP-11/TD-01)** — tức agent CÓ CHẠM vào đúng file đó, đúng lúc đó, nhưng không có gì nhắc "file
  này còn nợ gì từ gap-audit chưa". Đã đánh dấu `⚠ CHƯA VÀO AC (UAT 2026-09-17)` trực tiếp vào từng
  dòng ở `gap-audit-2026-09-15.md`. (Ngoại lệ: NP-10 hoá ra ĐÃ được vá thật trong lúc sửa concurrency
  ở test-execute hôm nay — chỉ `BR-hrm-002.md` mô tả bằng chữ còn lệch, không phải AC thiếu.)
- **Vì sao đây mới là nguyên nhân GỐC, không phải A1 riêng lẻ**: A1 hỏi "domain-po/domain-ba thiếu
  bước gì" — câu trả lời đúng hơn là "toàn bộ quy trình không có nơi nào bắt buộc phải ĐÓNG một mục
  gap-audit trước khi coi FEAT liên quan là ổn định". Một agent sửa FEAT vì lý do A (đổi nhãn) hoàn
  toàn hợp lý không nghĩ tới lý do B, C, D (12 mục khác) nếu không có gì buộc nó phải kiểm.
- **Đề xuất sửa skill/harness (mạnh hơn đề xuất ở A1)**:
  1. Thêm cột **"Trạng thái"** vào `gap-audit-2026-09-15.md` (và mọi gap-audit tương lai) —
     `open`/`resolved`/`wontfix`, cập nhật MỖI LẦN FEAT liên quan được sửa, không chỉ lúc quyết định
     ban đầu.
  2. `domain-po`/`domain-ba` (chốt sửa FEAT qua back-edge) — TRƯỚC khi sửa 1 FEAT vì lý do X, BẮT
     BUỘC `grep` toàn bộ `tracking/gap-audit-*.md` cho tên FEAT đó → nếu có dòng "làm" trạng thái
     còn `open`, phải xử lý CÙNG LƯỢT (hoặc quyết định dời + ghi rõ lý do dời, không im lặng bỏ qua).
  3. Gate mới (rà chéo `/domain` chốt 9, hoặc riêng): mọi dòng gap-audit "làm" mà FEAT liên quan đã
     `last_reviewed` SAU ngày gap-audit nhưng trạng thái vẫn `open` → finding BLOCKER (bằng chứng rõ
     ràng "có cơ hội sửa mà không sửa", khác với "chưa tới lượt sửa FEAT đó lần nào").

---

## E. Giao diện THẬT lệch mockup vì mọi cơ chế kiểm chỉ soi TOKEN MÀU, không soi CẤU TRÚC COMPONENT — 2026-09-17

> User gửi link tham khảo thật (SmartHR demo) + tự nhận xét app thật chưa giống mockup. Câu hỏi đúng
> trọng tâm của user: "trước hết phải xem lỗ hổng ở đâu mà chệch so với design?" — tức đòi xác định
> ĐÚNG chỗ hổng trong tiến trình, không phải chỉ vá code cho giống rồi thôi.

### E1. `web_styling` gate + dogfood lăng kính `picky` chỉ đo GIÁ TRỊ token (màu/spacing), không đo CẤU TRÚC component

- **Chuyện gì xảy ra**: đối chiếu app thật (`services/hrm-web`, chạy tại `localhost:5173`) với mockup
  (`docs/architecture/ux/mockups/web/*.html`) — lệch rất nặng. Mockup có **311 class component**
  trong `shared.css` (avatar tròn+tên `.cell-person`, nhãn trạng thái có màu `.status-pill`, card,
  stat-card dẫn icon...); `services/hrm-web/src/styles/global.css` chỉ có **36 class**, KHÔNG class
  nào cùng tên/cùng vai trò. Chụp ảnh thật: bảng "Duyệt đơn" chỉ là `<Table>`/`<Tag>` mặc định Ant
  Design, hiện cả UUID thô thay tên; Dashboard không có stat-card nào. Đợt "redesign" 2026-09-14 chỉ
  đồng bộ GIÁ TRỊ màu token vào `services/hrm-web` (xanh dương → cam), KHÔNG đồng bộ phần component.
- **Vì sao lọt lưới suốt nhiều wave — soát lại từng lớp enforcement THẬT đang có**:
  1. Gate `web_styling` (`scripts/gates.py`) chỉ scan CSS xem có dùng `var(--...)` hay không — KHÔNG
     đọc JSX/HTML để biết component nào được chọn. Dùng đúng token cho một `<Tag>` trần vẫn PASS.
  2. Dogfood lăng kính `picky` — `tracking/wave-001/dogfood-report.md` dòng 65 tự ghi rõ: **"5/5 cặp
     màu đo được khớp đúng design-tokens.css"** — chỉ so 5 cặp MÀU bằng computed style, không so cấu
     trúc DOM/component. Đây CHÍNH LÀ điểm soi mockup duy nhất ở `/dogfood`, và nó chỉ soi màu.
  3. Skill `ux-design` (`.claude/skills/ux-design/SKILL.md`) tự mô tả cơ chế hội tụ mockup↔app DUY
     NHẤT là "token map qua `ConfigProvider`/theme → mockup và app hội tụ" — không có bước nào yêu
     cầu so cấu trúc HTML thật với mockup, chỉ so màu/spacing.
  4. `dev-hrm-web-agent` — mục **DOCS TO READ** do `build_prompt.py` sinh ra (danh sách file agent
     CHẮC CHẮN mở) chỉ liệt `ux-web.md`, KHÔNG liệt trực tiếp file mockup HTML tương ứng. Mockup chỉ
     được nhắc ở TASKS §6, lẫn giữa nhiều bullet convention khác — mức ưu tiên đọc thấp hơn hẳn so
     với việc mở FEAT.md/api-core.md (mục riêng, tên riêng trong DOCS TO READ).
  5. `review-web-agent` không có bước screenshot-diff hay đối chiếu cấu trúc với mockup.
  - **Kết luận**: một trang có thể dùng ĐÚNG 100% token màu (pass `web_styling`, pass `picky`) mà vẫn
    KHÔNG giống mockup một chút nào về cấu trúc/component — vì không có bất kỳ bước nào trong toàn bộ
    pipeline đo chuyện đó. Đây là lỗ hổng Ở CẢ 3 TẦNG (gate tự động + dogfood + skill hướng dẫn agent),
    không phải lỗi 1 agent quên đọc kỹ.
- **Đề xuất sửa skill/harness**:
  1. `dev-hrm-web-agent`/`dev-{fe}-agent` — DOCS TO READ (`build_prompt.py`) thêm dòng liệt RÕ file
     mockup HTML tương ứng của từng FEAT đang code (tra qua `SCREEN-MAP.md`), nâng từ "1 bullet nhắc
     trong TASKS" lên "file bắt buộc mở", đồng cấp với FEAT.md/api-core.md.
  2. Thêm 1 bước bắt buộc ở `review-dev` (hoặc dogfood `picky`) cho boundary web: chụp ảnh page thật
     (Playwright) đặt CẠNH mockup cùng route — không cần pixel-perfect, nhưng phải xác nhận cùng dùng
     đúng "khối" component (avatar-cell/status-pill/card) chứ không chỉ đúng màu.
  3. Gate mới (nhẹ, tương tự `web_styling` nhưng soi cấu trúc): parse mockup `shared.css` lấy danh
     sách class "public" lặp lại ≥3 mockup (status-pill/cell-person/stat-card...) → grep
     `services/{web}/src` xem có tối thiểu N% các class/React-component cùng vai trò được dùng —
     không cần khớp tuyệt đối, chỉ cần bắt được ca "0% dùng" như lần này.

---

## F. Back-edge nghiệp vụ mở nhưng không đóng — 110+ file `docs/domain/` kẹt `DRAFT` 2 ngày, chưa commit — 2026-09-18

> User yêu cầu trực tiếp: "kiểm tra tài liệu như thế nào có đúng luồng tôi mô tả và từ discover ra
> không, sau đó ghi chép lại vấn đề vào retro" — phát sinh khi chạy `/domain` để sửa 1 dòng AC-11
> (field `reason` cho nghỉ phép năm) và bị chặn ở chốt `domain-translate` vì gate đòi TOÀN BỘ
> `docs/domain/**` phải ký, không chỉ file vừa sửa.

### F1. Back-edge `domain-po`/`domain-ba` mở để sửa nội dung, nhưng KHÔNG có gì bắt buộc phải đóng lại (`domain-approve` → `domain-translate` → `domain-end`) cùng lượt

- **Chuyện gì xảy ra**: `git diff` xác nhận content của ~110 file `docs/domain/**` (BR/FEAT/PERSONA...)
  đã được sửa ĐÚNG và CÓ CĂN CỨ — ví dụ `BR-hrm-001.md` version 1→2, nội dung cập nhật khớp hoàn
  toàn với quyết định NP-11/NS-08 ("HR không còn duyệt hộ đơn nghỉ phép") đã ghi ở
  `tracking/decisions.md` 2026-09-17 và `tracking/gap-audit-2026-09-15.md`. Đây KHÔNG phải nội dung
  sai hay bịa — là một back-edge `domain-po`/`domain-ba` hợp lệ, đúng quy trình, đúng cách: sửa xong
  thì `status` tự động lùi về `DRAFT` chờ ký lại (đúng thiết kế `domain_approve.py`). Vấn đề là **sau
  khi sửa xong, không ai (agent lẫn MAIN) chạy tiếp `domain-approve` (ký lại) → `domain-translate`
  (dịch lại eng) → `domain-end` (đóng lớp, quay về DESIGN)** — back-edge bị bỏ dở giữa chừng, và vì
  gate `domain-translate`/`domain-approve` soi TOÀN BỘ cây `docs/domain/` (không phải riêng file vừa
  sửa), việc bỏ dở này khoá luôn MỌI back-edge domain khác sau đó — kể cả việc chỉ sửa 1 dòng AC như
  lượt hôm nay.
- **Vì sao lọt lưới suốt 2 ngày** (`last_reviewed` của các file này = 2026-09-16, hôm nay 2026-09-18):
  không có gate/hook nào tự cảnh báo "còn back-edge domain đang mở dở" ở các stage SAU đó (DEV,
  TEST_PLAN, MANUAL_TEST đều chạy được bình thường suốt 2 ngày mà không ai biết lớp business phía
  dưới đang ở trạng thái nửa-vời) — vì owned_paths/phase-lock chỉ chặn EDIT ngoài đúng stage, không
  có gì chủ động nhắc "bạn rời DOMAIN_AUTHORING mà chưa ký hết".
- **Đề xuất sửa skill/harness**:
  1. `domain-po`/`domain-ba` — RETURN SCHEMA (đã có field `completed`) nên tự thêm bước nhắc MAIN
     ngay cuối lượt: "Còn N file `docs/domain/**` status=DRAFT sau khi sửa — chạy `domain-approve` +
     `domain-translate` + `domain-end` để đóng back-edge trước khi rời DOMAIN_AUTHORING, nếu không
     mọi back-edge domain sau này (kể cả không liên quan) sẽ bị chặn."
  2. Gate mới (nhẹ) ở MỌI stage sau `DOMAIN_AUTHORING`: nếu `docs/domain/**` có file `status=DRAFT`
     mà `stage` hiện tại KHÔNG phải `DOMAIN_AUTHORING`/`REVIEW` → cảnh báo (không chặn) "back-edge
     domain có thể đang bị bỏ dở — kiểm tra trước khi tiếp tục", in kèm số file + đường dẫn.
  3. Cân nhắc: gate `domain-translate`/`domain-approve` khi gọi KHÔNG-ARG nên có chế độ phạm vi hẹp
     (`--scope <file>`) để đóng back-edge CHỈ cho (các) file vừa sửa trong lượt này, thay vì bắt buộc
     xử lý toàn bộ backlog không liên quan mới đi tiếp được — tách rõ "ký cái tôi vừa sửa" khỏi "dọn
     nợ cũ của người khác" (2 quyết định khác nhau, không nên bị ép làm chung).

### F2. Nội dung đã sửa hợp lệ nhưng CHƯA `git commit` — chỉ tồn tại trong working tree ~2 ngày

- **Chuyện gì xảy ra**: `git log -- docs/domain/business-rules/BR-hrm-001.md` chỉ có 1 commit
  (`7c590b4`, nội dung version 1/APPROVED/2026-09-13) — bản sửa version 2 (2026-09-16, nội dung
  NP-11/NS-08) CHƯA từng được commit, tồn tại 2 ngày chỉ ở working tree. Cùng tình trạng: hàng chục
  file `BR-hrm-056.md` trở lên (business rule MỚI hoàn toàn) là `??` (untracked) — chưa từng `git
  add`. Đây là ĐÚNG loại sự cố `retro-skill-improvements.md` mục B2 đã cảnh báo ("Code xong nhưng
  quên `git add`/commit") — nhưng B2 chỉ nói về code (`services/`), lần này xảy ra ở TÀI LIỆU
  (`docs/domain/`), cho thấy B2 chưa đủ rộng.
- **Rủi ro thật**: repo này từng MẤT CODE THẬT một lần (lý do đổi Polyrepo→Monorepo ghi ở
  `CLAUDE.md` IDENTITY) — vì `services/` từng bị gitignore. Tài liệu domain không bị gitignore,
  nhưng nếu working tree bị mất (máy hỏng, `git clean -fd`/`checkout` sai tay, crash giữa chừng)
  thì 2 ngày phân tích NP-11/NS-08 + toàn bộ business rule mới sẽ mất y hệt cách code đã từng mất.
- **Đề xuất sửa skill/harness**: mở rộng đúng đề xuất B2 sang MỌI lớp tài liệu, không chỉ code —
  bất kỳ chốt nào return `files_changed` không rỗng (không riêng `dev-*-agent`) nên có dòng nhắc rõ
  "đã `git add`+commit các file này chưa?" trong RETURN SCHEMA hoặc TASKS, và cân nhắc gate cuối mỗi
  chốt lớn (`domain-end`, `design-end`, `plan`) kiểm `git status --porcelain` cho đúng owned_paths
  của layer đó — còn thay đổi chưa commit ở layer VỪA ĐÓNG = cảnh báo, không chặn cứng (tài liệu
  chưa phase-lock lại `services`/`tracking` nên vẫn có thể có lý do hợp lệ để chưa commit).

---

## Tóm tắt ưu tiên sửa skill (nếu chỉ chọn 3, tính tới wave-001)

0. **F2 — khẩn nhất vì là rủi ro MẤT DỮ LIỆU thật, không chỉ quy trình**: 2 ngày phân tích nghiệp vụ
   (~110 file sửa + hàng chục BR mới) đang NẰM NGOÀI git hoàn toàn. Trước khi làm bất cứ ưu tiên nào
   dưới đây ở wave sau: `git add` + commit ngay phần này (sau khi user soát qua), rồi mới tính chuyện
   sửa skill dài hạn.
1. **D1** — nguyên nhân gốc: thêm cột "Trạng thái" sống cho gap-audit + bắt buộc `domain-po`/
   `domain-ba` grep gap-audit theo tên FEAT trước khi sửa — nếu sửa cái này thì A1 và phần lớn danh
   sách 13 mục D1 tự động không tái diễn ở wave sau.
2. **E1** — cơ chế kiểm mockup-fidelity hiện tại (gate + dogfood + skill) chỉ soi TOKEN MÀU, không
   soi CẤU TRÚC component — sửa 1 lần ở `build_prompt.py`/gate mới thì áp dụng cho MỌI wave/boundary
   web sau này, không riêng wave-001.
2. **C1** — thêm cơ chế tự động cảnh báo "mockup lệch version FEAT" — mockup là CHUẨN mà cả
   review-dev và dogfood dùng để so sánh; mockup sai thì không lượt kiểm nào bắt được.
3. **A2/B3** — rebuild-from-scratch PHẢI đọc lại KG cũ + `tracking/decisions.md` lọc theo tên màn/
   component cụ thể, không chỉ đọc FEAT/HLD như dựng mới hoàn toàn.
4. **F1** — tách "ký cái vừa sửa" khỏi "dọn nợ ký cũ của người khác" ở gate `domain-approve`/
   `domain-translate` (chế độ phạm vi hẹp theo file) — nếu không, một sửa nhỏ 1 dòng AC sẽ luôn bị
   kẹt sau lưng một backlog không liên quan, đúng như đã xảy ra hôm nay.
