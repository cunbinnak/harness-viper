<!-- gate bỏ qua TEMPLATE.* — copy thành docs/DESIGN-SYSTEM.md. KHOÁ TRƯỚC prototype. Token = thứ DUY NHẤT chép nguyên sang code. -->
<!-- VAI: UX (ux-design). -->
# DESIGN-SYSTEM — {{PROJECT_NAME}}

## §1 Nguyên tắc
<!-- Gu giao diện (ux-design Phương pháp bước 0) — ghi TRƯỚC khi chọn token. Nguồn: Authority | MAIN đề xuất → Authority chọn | `Authority không yêu cầu`. -->
- **Gu giao diện**: {{Authority đưa: bộ nhận diện / template (tên + URL + license) / giao diện mẫu · hoặc hướng đã chọn (tên + URL) · hoặc `Authority không yêu cầu`}}
- **Ràng buộc cứng**: {{bắt buộc màu thương hiệu · cần chế độ tối · thiết bị chính · … hoặc `không`}}
- **Neutral-first**: nền trung tính, màu = nhấn ~10%, `danger` CHỈ cho lỗi. Ô trống im lặng, hover mới hiện affordance.

<!-- §2: token — tương phản AA · không token ngoài bảng · không hardcode màu. gate DOCUMENT tra token ở bảng này để tính tương phản · guard_ds chặn hex thô ngoài :root. -->
## §2 Token
| Token | Giá trị | Dùng cho |
|---|---|---|
| `--color-primary` | {{#…}} | {{nút chính}} |
| `--space-md` | {{16px}} | {{khoảng cách khối}} |

<!-- cặp tương phản: gate (_check_contrast) TỰ TÍNH tỉ số WCAG AA từ mã màu và CẢNH BÁO cặp dưới ngưỡng (không chặn — chuẩn cuối là file thiết kế/Figma).
     Mỗi cặp một dòng dạng `<chữ>` trên `<nền>` (hex hoặc token có trong §2 / :root). Chữ lớn (≥18px hoặc ≥14px đậm) → ghi `lớn` trong cùng vế → ngưỡng 3:1, còn lại 4.5:1.
     Khối chỉ chứa dòng cặp — ghi chú có chữ "trên" đặt ngoài khối (máy coi là cặp viết sai dạng). -->
- **cặp tương phản** (hex chữ / hex nền — WCAG AA): {{`#111827` trên `#ffffff` · body ≥ 4.5:1 · text lớn ≥ 3:1}}

<!-- §3: component — mỗi cái đủ trạng thái bắt buộc + có màn dùng. -->
## §3 Component
| Component | Trạng thái bắt buộc | Dùng ở màn |
|---|---|---|
| {{Button}} | {{default · hover · disabled · loading}} | {{…}} |

## §4 Trạng thái rỗng / lỗi / tải
- {{khuôn empty · error · loading}}
