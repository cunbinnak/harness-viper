<!-- gate bỏ qua TEMPLATE.* — copy thành docs/DESIGN-SYSTEM.md. KHOÁ TRƯỚC prototype. Token = thứ DUY NHẤT chép nguyên sang code. -->
# DESIGN-SYSTEM — {{PROJECT_NAME}}

## §1 Nguyên tắc
- **Neutral-first**: nền trung tính, màu = nhấn ~10%, `danger` CHỈ cho lỗi. Ô trống im lặng, hover mới hiện affordance.

<!-- §2: token — tương phản AA · không token ngoài bảng · không hardcode màu. gate ds_token_rows đọc bảng này. -->
## §2 Token
| Token | Giá trị | Dùng cho |
|---|---|---|
| `--color-primary` | {{#…}} | {{nút chính}} |
| `--space-md` | {{16px}} | {{khoảng cách khối}} |

<!-- §3: component — mỗi cái đủ trạng thái bắt buộc + có màn dùng. -->
## §3 Component
| Component | Trạng thái bắt buộc | Dùng ở màn |
|---|---|---|
| {{Button}} | {{default · hover · disabled · loading}} | {{…}} |

## §4 Trạng thái rỗng / lỗi / tải
- {{khuôn empty · error · loading}}
