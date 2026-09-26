---
name: ux-design
description: UX/UI cho web target (bước 8 mockup của /document) — user flow, MOCKUP HTML tĩnh per screen (design bằng HTML, không ASCII), UI states đầy đủ, design tokens + Visual polish, a11y WCAG 2.1 AA, permission-based UI. Sinh docs/ux/SCREEN-MAP.md + docs/ux/mockups/{name}/*.html; token ở docs/DESIGN-SYSTEM.md §2.
---

# UX Design Skill

> Load ở /document (Bước 8 mockup) + persona-picky đối chiếu. Phương pháp: mockup HTML tĩnh · neutral-first · anti-pattern "demo đẹp chạy xấu" (vá E1).
Chạy SAU khi DOCUMENT đã chốt target + `docs/arch/{name}.md §3 API` (UX consume contract, không bịa endpoint).
Input: `PRD.md` (persona, platform, design system / ADR ui-kit + **§6 Glossary + §7 Dữ liệu mẫu**) + `feat/FEAT-*.md` (user story + AC) + `PERSONAS.md` + `docs/arch/{name}.md §3 API` (contract target phục vụ).

> **BÁM NGHIỆP VỤ — nội dung mockup phải có NGUỒN**: chữ/số trên màn lấy từ **PRD §7 Dữ liệu mẫu** (giá trị thật ngoài đời) + thuật ngữ đúng **PRD §6 Glossary** + ca thật trong INTERVIEW. **CẤM bịa placeholder generic** ("Nguyễn Văn A", "Sản phẩm 1", "Lorem") — mockup generic là mockup Authority không soi nổi nghiệp vụ, duyệt cũng vô nghĩa. Thiếu dữ liệu mẫu cho màn đang vẽ → bổ sung PRD §7 trước (research domain, không bịa tại chỗ).

## Deliverable
**Đơn vị thiết kế = MÀN (screen)** — boundary chỉ là nơi màn thuộc về. Sản phẩm gồm:
- **`docs/ux/SCREEN-MAP.md`** — MỤC LỤC MÀN, sinh TRƯỚC khi vẽ: **1 bảng đơn** `| Màn | Route | Target (web/mobile) | FEAT | Mockup | Ghi chú |` — mỗi màn 1 row, gắn rõ màn ↔ route ↔ web target ↔ FEAT:AC ↔ đường dẫn mockup, cột **Ghi chú** ghi behavior ngắn (empty→CTA, list realtime, validation…). **Luật gán màn → target** (quan trọng khi NHIỀU web target): (1) FEAT frontmatter `target_hint`; (2) không có hint → journey + persona của FEAT so với persona pool của target (`PERSONAS.md` + `CAPABILITIES-MAP.md`); (3) vẫn mơ hồ → **hỏi user**, KHÔNG đoán. Mỗi FEAT `has_ui_touchpoint=true` phải có ≥1 màn; màn dùng chung nhiều FEAT (list/detail) = 1 row ghi nhiều FEAT.
  **PHỦ Ở MỨC AC, KHÔNG PHẢI MỨC FEAT** (chống "FEAT có 1 màn list là đủ" — màn con form/detail/modal bị lười chính ở đây): **mọi AC `has_ui` in-scope wave phải xuất hiện ở ≥1 row**, và row đó nêu **PHẦN TỬ/KHUÔN xử nó** (nút nào · modal nào · form nào · khuôn lỗi nào). Mỗi *"Khi 〈thao tác〉"* trong AC → phần tử tương ứng phải **render trong mockup** (modal/confirm/form là section trong file màn cha hoặc màn con riêng — không được "màn chính có rồi" là xong). AC không có chỗ đứng trên màn nào = **màn con thiếu** — bổ sung TRƯỚC khi chốt; lỗ này lan chuỗi: picky không có mockup để so + arch §3 không ai đòi API cho nó.
- BEHAVIOR chi tiết per màn (API calls khớp `docs/arch/{name}.md §3 API` + validation FE map `error.code`→field + permission UI + a11y). **Khai API theo VÙNG DỮ LIỆU, không chỉ theo nút**: mọi vùng hiển thị dữ liệu trên mockup (bảng · tab lịch sử · panel · badge đếm — kể cả read-only không bấm được) → ghi API fetch nuôi nó; vùng cần API mà `arch §3` chưa có endpoint → **quay technical-design bổ sung §3 TRƯỚC khi chốt màn** (đang DOCUMENT, sửa được) — không ghi nợ. — state chính render TRONG mockup, chi tiết còn lại ghi gọn ở cột **Ghi chú** hoặc dev-handoff notes cuối file. **KHÔNG chép giá trị token vào .md** — `docs/DESIGN-SYSTEM.md §2` là SoT duy nhất về màu/spacing/chữ (chép = drift).
- **`docs/ux/mockups/{name}/{screen}.html`** — LOOK **per MÀN**: giao diện hoàn chỉnh bằng HTML (**ưu tiên nền từ template thật** — xem §Đường tắt template; không có template hợp → tự dựng app shell + screen theo §Visual polish, như trang web thật). Khi thiết kế 1 màn, đọc ĐÚNG tài liệu của màn đó: FEAT (AC) trong row SCREEN-MAP + `docs/arch/{name}.md §3 API` mà flow màn gọi — không đọc cả đống target khác. Luật: HTML TĨNH mở `file://` xem được (không JS/build/CDN) · style CHỈ `var(--...)` từ token ở `docs/DESIGN-SYSTEM.md §2` (thiếu token → thêm vào SoT, không bịa tại chỗ) · nội dung thật không lorem · state phụ (loading/empty/error) = section trong cùng file · responsive media query · đủ `:hover`/`:focus-visible`. **Mọi row mockup phải TỒN TẠI + dùng token; web target không có màn nào = chặn** (guard_ds). User duyệt "đẹp/xấu" TRÊN MOCKUP trước khi build; dev FE (stack-nextjs) bám mockup; reviewer đối chiếu.

## ĐƯỜNG TẮT TEMPLATE — ưu tiên khi có template hợp (nhanh + đẹp hơn tự vẽ)
Đừng tự vẽ từ đầu thứ đã có người làm đẹp sẵn. Trước khi vẽ tay, **tìm template/UI-kit hợp domain** (admin dashboard: Tabler/TailAdmin/AdminLTE · landing/app: HTML template MIT trên GitHub · **marketplace: ThemeForest** — demo free để neo phong cách; template **user đã mua license** → dùng luôn làm nền) và **LẤY LUÔN làm nền mockup**:
1. **Chọn** template license cho phép (MIT/Apache/CC, hoặc template trả phí **user đã sở hữu license** — ghi **tên + URL + license** vào `DESIGN-SYSTEM §1` làm neo). User đưa template có sẵn (file/link) → ưu tiên tuyệt đối cái đó. **Link → dùng `browse` skill (Playwright) mở xem trực tiếp** thay vì WebFetch — template cần JS/CSS render thật mới thấy đúng giao diện; WebFetch chỉ trả raw HTML, mất style. Xem xong **dọn ảnh/screenshot ngay** (luật #9) — không commit artifact tạm.
2. **Trích** đúng màn gần nhất với màn cần vẽ (đừng bê cả bộ) — giữ layout/component/CSS của nó.
3. **Token-hoá**: rút palette/spacing/radius của template vào **`:root` token §2** (SoT + qua `guard_ds` — hex chỉ được ở `:root`); class giữ nguyên, giá trị trỏ `var(--…)`. Đổi ý về màu sau này = sửa token, lan mọi màn.
4. **Thay nội dung** bằng dữ liệu mẫu `PRD §7` + thuật ngữ `§6 Glossary` (luật BÁM NGHIỆP VỤ ở trên) — template đẹp mà nội dung generic vẫn vô nghĩa.
5. Vẫn đủ chuẩn mockup: HTML tĩnh `file://` (gỡ JS/CDN của template) · 3 khuôn rỗng/lỗi/tải · `data-screen`/`data-ds` · responsive.
User đưa template cụ thể → **dùng đúng cái đó**. Không tìm được template hợp → mới tự vẽ theo archetype + §Visual polish bên dưới.

## Design system trước khi vẽ
- Project có design system / **ADR ui-kit** → TUÂN THEO (layout, color, component pattern, mobile nav).
- Chưa có → **đề xuất chốt 1 component library trưởng thành** (React → mặc định **Ant Design 5**; hoặc MUI/Chakra theo ý user) — báo user chốt để `/document` ghi **ADR ui-kit** (`docs/adr/`). KHÔNG tự chế design system từ số 0. Library đã chốt = visual language chuẩn cho CẢ mockup lẫn app.
- **Mockup mô phỏng đúng visual language của library đã chốt** (mockup là HTML tĩnh nên không nhúng antd thật — nhưng radius/màu/spacing/kiểu component phải nhìn NHƯ antd; dev sau đó dùng antd thật, token map qua `ConfigProvider`/theme → mockup và app hội tụ).
- KHÔNG hardcode color/spacing/typography → **reference design tokens** (token ở `docs/DESIGN-SYSTEM.md §2`, chỉnh theo palette của library đã chốt).
- **Shared design tokens:** `docs/DESIGN-SYSTEM.md §2` là SoT token dùng chung MỌI web target (`--color-*`/`--font-*`/`--space-*`/`--radius-*` + dark/hc theme). Mockup tham chiếu token NÀY (không bịa palette per-target). Web FE consume qua `var(--...)`; mobile map `ThemeData`/`ColorScheme`. Hook `guard_ds` ép plain-CSS phải dùng `var(--...)`.

## Chuẩn chuyên nghiệp + ANTI-PATTERNS (bắt buộc — mockup xấu = fail review)
**BƯỚC 0 — neo phong cách qua ARCHETYPE màn** (áp cho MỌI đề bài): 1 Dashboard · 2 Bảng danh sách · 3 Form · 4 Trang chi tiết · 5 Timeline/lịch tài nguyên · 6 Feedback states. Mỗi màn sắp vẽ: xác định thuộc archetype nào (hoặc ghép archetype nào) → đối chiếu về bố cục/mật độ/màu/states — đó là mức chất lượng TỐI THIỂU. **Research tham chiếu là OPTIONAL** (không có file mẫu bắt buộc mở): khi cần neo cụ thể hơn, tìm 2-3 sản phẩm tham chiếu THẬT qua WebSearch/trình duyệt (xem §Phương pháp bước 1) và ghi vào `docs/DESIGN-SYSTEM.md §1`. KHÔNG copy nội dung — chỉ neo phong cách. Vẽ xong tự so với archetype: thua chuẩn = làm lại trước khi trình user.

**LUẬT MÀU — neutral-first (lỗi hay phạm nhất):**
- NỀN luôn trung tính (`--color-surface`/`--color-surface-alt`). **CẤM sơn màu semantic (xanh lá/đỏ/vàng) lên mảng lớn** — màu chỉ để NHẤN (block/badge/button/status), chiếm ~10% màn hình.
- Vùng/ô trống = IM LẶNG: nền surface, không chữ, không màu; `:hover` mới hiện affordance.
- Sự kiện/booking bình thường = `--color-primary-soft` + viền primary. `--color-danger` CHỈ dành cho LỖI — "đã đặt" không phải lỗi, không được đỏ/hồng.

Benchmark: mockup phải trông như **sản phẩm SaaS thương mại** (chuẩn Ant Design/Linear-level) — người xem không phân biệt được với app thật đã style. Cấm các lỗi "bảng thô" hay gặp:
- **CẤM text-link lặp trong mọi ô** (vd chữ "Trống" gạch chân × 50 ô): ô trống phải IM LẶNG (nền nhạt), affordance chỉ hiện khi `:hover` (đổi nền + con trỏ/nhãn mờ). Trạng thái thể hiện bằng MÀU + BLOCK, không bằng chữ lặp.
- **CẤM link gạch chân thay button** — hành động dùng button/segment có nền, radius, hover.
- **Booking/sự kiện = BLOCK có chiều dài theo thời lượng** (span đúng số slot, tên + người + giờ trong block), KHÔNG phải 1 cell text.
- **CẤM bảng HTML mộc** (border đen mảnh, cell đều tăm tắp, không nhịp thở): dùng grid + separator mảnh màu `--color-border`, hàng có padding `--space-*`, header nhóm rõ.
- **Thông báo lỗi/toast đặt đúng chỗ** (banner trong luồng nội dung hoặc toast cố định có nền/đổ bóng chuẩn), không thả nổi lạc lõng góc màn.
- **Mật độ có nhịp**: mọi khoảng cách từ `--space-*`; không có vùng chữ dày đặc sát mép.
- **Responsive bắt buộc kiểm**: thu browser <768px phải ra layout mobile tử tế (card/stack), không phải bảng tràn ngang.

## Visual polish (spec CỤ THỂ để dev implement được "đẹp" — không chung chung)
Ghi vào `docs/DESIGN-SYSTEM.md §3` (kho component — dev implement + reviewer/verify đối chiếu được):
- **App shell**: layout khung chuẩn (header + nav + content + footer) dùng chung mọi screen — screen chỉ đổi content, KHÔNG mỗi trang một khung. **Shell là CANONICAL** (xem §Nhất quán cross-màn) — nav items/thứ tự/nhóm · logo · vị trí user-menu định NGHĨA MỘT LẦN, mọi màn copy nguyên văn.
- **Spacing rhythm**: MỌI padding/margin/gap từ `--space-*` (scale 4/8px) — cấm số lẻ tùy tiện; mật độ nhất quán (form row gap, card padding, section gap ghi rõ token nào).
- **Type scale**: heading/body/label dùng `--font-size-*` + `--font-weight-*`; mỗi screen có hierarchy rõ (1 h1, section h2, không nhảy cấp).
- **Component primitives**: Button (primary/secondary/danger + hover/focus/disabled), Input (+error state), Card, Table, Badge, Modal, Toast — định nghĩa 1 lần (style từ token), mọi screen compose lại; KHÔNG style ad-hoc per-page.
- **Interaction states**: element tương tác PHẢI có `:hover` + `:focus-visible` (outline token) + transition (`--motion-*`); loading = skeleton/spinner có style, empty = illustration/hint căn giữa (không text trần), error = màu `--color-danger` + hướng dẫn.
- **Elevation + depth**: card/modal dùng `--shadow-*` + `--radius-*` nhất quán — phân lớp rõ, không phẳng lì cũng không bóng đổ hỗn loạn.

## Phương pháp
1. **Research — BẮT BUỘC, không chỉ khi "chưa rõ"**: trước khi chốt token hay vẽ mockup đầu tiên, chủ động tìm THẬT sản phẩm/template cùng loại qua WebSearch/trình duyệt.
   - **Từ khoá tự suy TỪ CHÍNH dự án đang làm** (đọc `PRD.md` + loại màn sắp vẽ). KHÔNG dùng lại cụm từ/link cố định của lần trước hay của dự án khác — vd dự án quản lý kho thì tìm "warehouse/inventory dashboard UI", dự án đặt lịch thì tìm "booking/scheduling app UI".
   - Lấy **ít nhất 2-3 tham chiếu CỤ THỂ** (không mô tả chung chung "hiện đại, sạch sẽ"). Ghi **tên sản phẩm/template + URL + đặc điểm cụ thể định vay mượn** (bố cục thẻ số liệu, cách dùng màu xu hướng, kiểu bảng, spacing…) vào `docs/DESIGN-SYSTEM.md §1` làm **neo tham chiếu** — kể cả khi user chưa đưa ví dụ nào. **Tham chiếu là template mã nguồn mở dùng LUÔN được → đi §Đường tắt template** (lấy làm nền, không chỉ nhìn).
   - User đưa ví dụ/link cụ thể → **ưu tiên đúng cái đó**; dùng **`browse` skill (Playwright) mở link đó** (không WebFetch) để thấy giao diện render thật trước khi neo phong cách; **dọn ảnh/screenshot ngay sau khi xem xong** (luật #9); agent tìm THÊM để bổ sung góc nhìn, không thay thế link user đã cho.
   - Trang chặn bot (Cloudflare/403…) → thử nguồn khác (blog tổng hợp, ảnh chụp trên trang review, Dribbble, tìm ảnh). KHÔNG bỏ bước này, KHÔNG ghi nguồn chưa thật sự xem qua.
   - Tham khảo cùng lúc: UX pattern cho loại sản phẩm (form/table/dashboard), WCAG 2.1 AA, design system doanh nghiệp (Ant/Material/Atlassian), mobile-first.
   - Vì sao bắt buộc: không có mẫu thật thì giao diện ra theo gu của agent, và người vận hành phải tự đi tìm mẫu rồi bắt làm lại. Ô neo §1 phải có ít nhất một URL.
2. **SCREEN-MAP trước** (mục lục màn): từ FEAT `has_ui_touchpoint` + journeys derive danh sách MÀN → gán target theo luật (hint → persona → hỏi) → ghi bảng SCREEN-MAP.md. Đây là kế hoạch thiết kế — user thấy được toàn cảnh màn nào thuộc đâu trước khi vẽ.
3. **Thiết kế TỪNG MÀN** (đơn vị công việc — đi theo SCREEN-MAP, ưu tiên màn trong flow FEAT Must):
   - Đọc đúng tài liệu của màn: FEAT:AC trong row + `docs/arch/{name}.md §3 API` mà flow gọi + journey liên quan.
   - **Mockup HTML** (`docs/ux/mockups/{name}/{screen}.html`): THIẾT KẾ giao diện hoàn chỉnh — app shell + nội dung screen thật, compose từ token ở `docs/DESIGN-SYSTEM.md §2`. Mockup là SoT về look — làm "đẹp" ở ĐÂY theo §Visual polish, không tả suông, không skeleton chờ điền.
   - **Component states đầy đủ**: default / hover / disabled / loading / error / empty — state chính render trong mockup, bảng behavior ở ux-*.md.
   - **Bản kê trong mockup (BẮT BUỘC)**: `data-screen="<mã cột Màn của SCREEN-MAP>"` trên khung gốc · `data-ds="<mã #, vd C3>"` trên MỖI khối, chỉ lấy từ `docs/DESIGN-SYSTEM.md §3` · `data-state="empty|loading|error"` trên section trạng thái phụ. Vẽ xong màn thì cập nhật cột "Dùng ở màn" của §3 cho khớp — đối chiếu hai chiều. Đây là thứ biến mockup từ ảnh để nhìn thành bản code FE lắp theo được.
   - **API calls**: trigger → endpoint → method → loading state, khớp `docs/arch/{name}.md §3 API`.
   - **Validation FE-side**: field · required · rule · error message.
   - Mobile layout riêng nếu khác desktop đáng kể.
4. **Permission-based UI**: ẩn/hiện element theo role (`roles[]` từ JWT) — ghi rõ phần tử nào cần quyền gì.
5. **Responsive**: breakpoint desktop / tablet / mobile + hành vi (sidebar collapse, table → card…).
6. **Accessibility (WCAG 2.1 AA)**: label/`aria-label`, focus visible, contrast ≥ 4.5:1, keyboard nav (Tab/Enter/Esc), `role`/`aria-live` cho modal/toast, error gắn input qua `aria-describedby`.
7. **Dev handoff notes**: animation/transition, edge case (empty / long text / overflow), breakpoint, a11y.
8. **Rà nhất quán cross-màn** (sau khi vẽ HẾT màn của wave): đối chiếu app shell mọi mockup vs `_shell.html` — nav/logo/user-menu khớp hết chưa (xem §Nhất quán cross-màn). Lệch → sửa khớp canonical trước khi trình chốt.

## Nhất quán cross-màn — app shell dùng chung (vá lỗi shell trôi mỗi màn một kiểu)
Mỗi mockup vẽ ĐỘC LẬP (đọc đúng tài liệu màn đó) → **app shell dễ trôi**: màn này có nhóm "QUẢN LÝ" màn kia không · mục đầu "Dashboard" vs "Tổng quan" · user-menu góc dưới sidebar vs góc trên · logo trơn vs có subtitle · thứ tự/số mục nav lệch. Người dùng thật thấy NGAY — cùng một app mà mỗi trang một khung = mockup chưa đạt.

**Chặn tại nguồn — shell là CANONICAL, không tái phát minh per màn:**
- Định nghĩa app shell **MỘT LẦN**: 1 file `docs/ux/mockups/{name}/_shell.html` (sidebar: logo + **nav items + ICON mỗi mục** + user-menu · top-bar chrome) — **danh sách mục nav + thứ tự + nhóm heading + icon từng mục + vị trí logo/user cố định TẠI ĐÂY**. Đây là nguồn sự thật của shell target đó.
- Bọc phần **BẤT BIẾN** của shell trong marker `<!-- SHELL:START -->` … `<!-- SHELL:END -->` (ở cả `_shell.html` lẫn mọi màn) — `guard_shell` so đúng khối này. **Breadcrumb + vùng content per màn nằm NGOÀI khối** (chúng được phép khác nhau).
- Mỗi màn cần shell: **Read `_shell.html` trước** → trích đúng khối `<!-- SHELL:START -->…<!-- SHELL:END -->` → paste nguyên vào màn → CHỈ đổi **1 chỗ**: đánh `aria-current="page"` lên mục nav đang đứng. **KHÔNG** gõ lại từ trí nhớ — phải lấy từ file, không thì sai. **KHÔNG** thêm/bớt/đổi thứ tự mục nav · **KHÔNG** đổi icon · **KHÔNG** dời chỗ user-menu/logo.
- HTML tĩnh không `include` được → Read + copy tay mỗi màn; `guard_shell` **cảnh báo** (không chặn) nếu lệch — lệch sẽ bị bắt ở bước rà cuối wave.

**Bước rà nhất quán (BẮT BUỘC — SAU khi vẽ hết màn của wave, TRƯỚC khi trình chốt):**
Mở tất cả mockup của target cạnh nhau, đối chiếu vùng shell — mọi màn phải KHỚP `_shell.html` (`guard_shell` cảnh báo khi Write nhưng không chặn — đây là lượt rà chính thức bắt drift):
- [ ] Danh sách mục nav + **thứ tự** + **nhóm heading** + **ICON mỗi mục** giống hệt mọi màn
- [ ] Logo (+ subtitle) + **vị trí user-menu** giống hệt mọi màn
- [ ] Cùng cấu trúc header + cùng token (guard_ds lo màu). Breadcrumb/content được phép khác (ngoài khối SHELL)
Lệch → **sửa màn lệch cho khớp canonical** (KHÔNG sửa canonical theo 1 màn lẻ, trừ khi chính canonical sai). Ghi phát hiện + cách xử vào `SCREEN-MAP.md §Chốt`.

## Quality checklist
- [ ] **SCREEN-MAP đủ**: mọi FEAT `has_ui_touchpoint` có ≥1 màn; mọi màn gán đúng target (mơ hồ đã hỏi user); mọi web target có ≥1 màn.
- [ ] Mọi FEAT Must có user flow.
- [ ] Mọi màn trong SCREEN-MAP có **mockup HTML tồn tại** mở browser xem được (responsive trong cùng file; đủ section state phụ).
- [ ] **Shell nhất quán cross-màn** (§Nhất quán cross-màn): mọi mockup của target dùng CÙNG app shell — nav items/thứ tự/nhóm · logo · vị trí user-menu giống hệt, chỉ khác active-state + content. Đã rà cạnh nhau, lệch đã sửa khớp `_shell.html`.
- [ ] Mọi mockup có **bản kê**: `data-screen` khớp SCREEN-MAP · mọi khối có `data-ds` thuộc §3 · cột "Dùng ở màn" của §3 khớp hai chiều với mockup · đủ `data-state` theo **§4 (ba khuôn rỗng/lỗi/tải)** của component trên màn.
- [ ] Mockup CHỈ dùng `var(--...)` — không hardcode hex/px (hook `guard_ds` check reference token).
- [ ] Mọi component có đủ states (default/hover/disabled/loading/error/empty).
- [ ] API call mỗi screen khớp `docs/arch/{name}.md §3 API` (op name, method, loading state).
- [ ] Design tokens referenced — KHÔNG hardcode màu/spacing/typography; `docs/DESIGN-SYSTEM.md §2` tồn tại + §3 (kho component) trỏ tới nó.
- [ ] Permission-based UI documented (ẩn/hiện theo quyền).
- [ ] A11y WCAG 2.1 AA checklist pass.
- [ ] Handoff notes có edge case dev dễ sót.

## Thứ tự BẮT BUỘC: design system TRƯỚC, mockup SAU

Đảo thứ tự là mất tác dụng — token rút ra từ mockup đã vẽ chỉ là bản mô tả những màu đã lỡ chọn, không phải quyết định. Và phản hồi "chữ nhỏ quá" lẽ ra sửa MỘT token rồi lan ra mọi màn, nay thành đi sửa tay từng file.

`docs/DESIGN-SYSTEM.md` (chép từ `templates/TEMPLATE.design-system.md`) khai phần **máy không suy được từ token (§2)**:

| § | Khai gì | Ai dùng về sau |
|---|---|---|
| §1 | **Ba tính từ + neo tham chiếu THẬT** — ưu tiên user chỉ ra ("nhìn như app X"); KHÔNG có thì agent tự tìm (bước Research) và ghi tên + URL + đặc điểm vay mượn, không để trống | chỗ đối chiếu khi cãi nhau đẹp/xấu — không có neo thì tranh luận không có đáy |
| §2 | Token + **cặp tương phản** (hex chữ / hex nền — WCAG AA) | gate **tự tính tỉ số WCAG**, không tin lời khai |
| §3 | **Kho component ĐÓNG** — mỗi khối: dùng ở màn nào + **trạng thái bắt buộc** | vai `picky` ở `/verify` đi kiểm đúng cột này trên app đã render |
| §4 | **Ba khuôn** rỗng / lỗi / đang tải | năm màn không được đẻ ra năm kiểu báo lỗi |

**§3 là mục dễ bỏ nhất và đắt nhất khi bỏ.** Thiếu trạng thái "đang gửi (khoá lại)" chính là cái bấm-hai-lần mà vai `rushed` sẽ tìm thấy — và lúc đó đã code xong. Component không dùng ở màn nào → **xoá dòng**, đừng giữ cho đủ bộ.

Mockup chỉ được **lắp từ kho §3** và dùng `var(--…)` từ token §2. Cần khối mới → thêm dòng ở §3 trước, không vẽ khối lạ tại chỗ. Thiếu token → thêm vào `docs/DESIGN-SYSTEM.md §2`, không gõ thẳng hex.

Bốn mục §1/§2/§3/§4 phải đầy đủ trước khi khoá scope @ `/document`.

## Chốt mockup — KHÔNG dừng ở đây

Vẽ xong toàn bộ màn trong SCREEN-MAP thì **đi tiếp luôn** sang chốt kế. Việc user xem và chốt
giao diện xảy ra **một lần duy nhất, ở khoá scope `/document`** — nơi họ vốn đang đọc cả bộ tài liệu.
Dừng thêm một lần giữa bước UX là hỏi cùng một câu hai lần ở hai chỗ.

Việc của chốt này là **để lại thứ đáng xem**:

1. Ghi vào `SCREEN-MAP.md` §Chốt: danh sách đường dẫn mockup + **mở thẳng bằng trình duyệt**
   (`file://`, không cần server) + màn nên xem trước (màn đầu của luồng FEAT Must) + đi thử theo
   persona nào.
2. Mỗi màn phải bấm được và thấy đủ ba khuôn (rỗng · lỗi · đang tải) — không có thì không có gì
   để user đánh giá, và họ sẽ chốt một thứ chưa tồn tại.
3. Để trống dòng `Chốt bởi user:` — khoá scope `/document` điền.

Khi user phản hồi ở khoá scope `/document`: **hình thức** ("chữ nhỏ quá", "màu chìm quá") → sửa
**TOKEN** ở `docs/DESIGN-SYSTEM.md §2` rồi để nó lan ra mọi màn. **KHÔNG sửa tay từng file mockup** —
sửa tay là mất đúng tác dụng của design token, và pha code thừa hưởng nguyên mớ lệch đó.

Khoá scope `/document` đòi dòng `Chốt bởi user: <ISO>` khi có target
web/mobile. Chưa chốt = chưa mở cổng wave.

Khuôn ghi ở cuối `SCREEN-MAP.md`:

```markdown
## Chốt

| Ngày | Phản hồi | Xử (token nào đổi / màn nào sửa) |
|---|---|---|
| 2026-08-22 | chữ trong bảng nhỏ, khó đọc ngoài sáng | `--font-size-sm` 12px → 14px |

Chốt bởi user: 2026-08-22
```

## Done
- `docs/ux/SCREEN-MAP.md` đủ user flow + screens + states + a11y + permission UI cho mọi FEAT Must của web target.
