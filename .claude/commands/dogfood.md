---
description: DOGFOOD — dùng thử hệ ĐANG CHẠY bằng 6 lăng kính persona, 2 đợt theo trạng thái DB. Ghi §Findings, KHÔNG fix.
---
# /dogfood [<vai>] — tự dùng trước khi bảo là xong

Là **bước dogfood của VERIFY** (Bước 4). Không arg = chạy đủ **6 vai 2 đợt**. Có arg (`/dogfood breaker`) = **chạy lại 1 vai**.
KHÔNG đổi phase — chạy lại tuỳ ý.

## Vì sao có
auto-test chỉ chạy **TC đã viết** → chỉ tìm thứ ai đó đã nghĩ ra trước. Dogfood bù đúng khoảng đó:
cảnh rỗng không nói gì · lỗi nuốt im lặng · bấm 2 lần ra 2 bản ghi · vai A chạm dữ liệu vai B · nút chính tràn màn nhỏ.

## Điều kiện vào
Hệ **đang chạy thật** (từ BUILD Bước 6: docker / dev server / emulator theo kind). Chết → STOP, quay `/build`.
**Không dogfood ảo** — 1 lượt trên hệ chết còn tệ hơn không chạy (để lại vết "đã kiểm"). Cần `docs/PERSONAS.md` có
**ma trận vai×hành động** (phép thử của `breaker`) + persona cho mỗi vai.

## Workflow
1. Lấy URL/endpoint thật của hệ đang chạy — **không đoán**.
2. Đọc `docs/PERSONAS.md` (persona · ma trận quyền · gán vai↔persona) + luồng lõi/AC của wave + mockup đã chốt.
3. **MAIN TỰ DÙNG TRƯỚC — bắt buộc, TRƯỚC khi spawn vai nào.** Đích thân mở trình duyệt (Playwright), đóng **persona chính**, vào **từ trang đầu** (không nhảy URL trong), đi hết luồng lõi đầu→cuối: kiểm **từng AC** làm được THẬT không · đối chiếu từng màn với **mockup đã chốt** (lệch = phát hiện, không phải thẩm mỹ) · soi token/trạng thái (nút gửi có khoá, lỗi đúng khuôn). Ghi mọi thứ vướng kể cả nhỏ. → *"Eat your own shit" gốc ở đây: MAIN nếm TRƯỚC, rồi mới giao 6 lăng kính.*
4. **Đợt 1 (DB SẠCH)** — spawn 3 vai 1 lượt: `edge` (rỗng/lỗi) · `newbie` · `picky`.
5. Đợi **đủ 3 vai** trả kết quả → **seed lại** `deployment/local/`.
6. **Đợt 2 (DB CÓ DỮ LIỆU)** — spawn 3 vai 1 lượt: `rushed` · `breaker` (chạy đủ ma trận) · `mobile`.
7. Gộp phát hiện (**MAIN Bước 3 + 6 vai**) → soi **dấu hiệu dogfood giả** → vai nào dính thì chạy lại vai đó.
8. Agent **TRẢ VỀ** phát hiện → **MAIN ghi `STATE §Findings`** (chống retro B1 hai agent đè file).
9. Báo Authority theo **mẫu tổng kết** (dưới). Còn finding `sửa ngay` → `/verify` fix-loop. Sạch → quay `/verify` Bước cuối (gate VERIFY xanh) rồi mới `/ship`|`/next-wave`.

## Vì sao 2 đợt (KHÔNG phải dàn tải)
Các vai dùng chung **1 hệ + 1 DB**: `breaker` đổ dữ liệu bậy, `rushed` tạo bản ghi trùng NGAY giữa lúc `newbie` nhìn màn →
người này thấy cảnh người kia. Nặng nhất: **trạng thái rỗng (thứ `edge` coi trọng nhất) chết ngay khi vai nào tạo bản ghi đầu**.
Ba ràng buộc **CỨNG**: ≤ **3 vai/đợt** · **không mở đợt 2 khi đợt 1 chưa xong** · **seed lại giữa 2 đợt**.

## Mỗi vai phải nhận gì
| # | Nội dung | Thiếu thì |
|---|---|---|
| 1 | URL/endpoint thật | vai không thử được |
| 2 | **Persona được giao** (chân dung + năng lực + luồng) | thử như "người dùng nói chung" |
| 3 | Luồng lõi + AC của wave | không biết đúng/sai theo gì |
| 4 | `breaker`: ma trận đầy đủ + tài khoản từng vai | không có danh sách phép thử |
| 5 | `picky`: màn liên quan + `docs/DESIGN-SYSTEM.md` token + **mockup** | không có gì đối chiếu |

> **`picky` đo CẢ CẤU TRÚC component vs mockup (screenshot-diff), KHÔNG chỉ màu token** — vá retro E1 (app dùng đúng màu mà cấu trúc lệch mockup).

## Bằng chứng bộ ba (không có = không tính)
```
Tôi đã làm   : <thao tác chính xác — URL, dữ liệu đã gõ, nút đã bấm>
Tôi thấy     : <thứ hiện ra / mã lỗi / response thật>
Tôi mong đợi : <thứ lẽ ra phải xảy ra + dẫn về AC/FEAT/ô ma trận>
```
Thiếu vế đầu = suy từ code chứ chưa chạy. Vế cuối không dẫn được về tài liệu = ý kiến cá nhân, không phải finding.

## Mẫu báo cáo tổng kết (cuối dogfood → Authority)
```
Đã dùng thử ở <local|prod>, MAIN đóng <persona chính> + 6 vai × 2 đợt

Luồng lõi:     đi hết được / gãy ở bước <n>
AC:            <x>/<y> làm được thật
Phân quyền:    <x>/<y> ô ✗ ma trận đã thử, chặn đúng hết / thủng ở <đâu>
Mockup:        khớp bản đã chốt / lệch ở <màn> (n/a nếu KHÔNG CÓ UI)
Design system: <x> màu lạ · <y>/<z> cặp tương phản đạt · <a>/<b> component đủ trạng thái
Ghi §Findings: <n> (BLOCKER <> · MAJOR <> · MINOR <>)
Đẩy backlog:   <danh sách>
```

## Forbidden
- **KHÔNG tự fix** — trả finding, MAIN điều phối lượt sửa (nhân quả rõ ràng).
- **KHÔNG sửa `test-cases.md`** cho khớp thứ vừa thấy.
- **KHÔNG sửa doc spec** cho khớp code — đúng anti-pattern harness sinh ra để chống.
- **KHÔNG teardown hệ** — giữ chạy cho fix-loop (teardown ở `/next-wave` khi hết wave).
- Vai dogfood **KHÔNG hỏi Authority** — trả phát hiện + đề xuất, quyền quyết ở phiên chính.
