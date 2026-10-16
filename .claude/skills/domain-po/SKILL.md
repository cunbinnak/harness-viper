---
name: domain-po
description: "Vai PO — /document Bước 5 nhịp 1: cắt sản phẩm thành FEAT theo capability, tạo KHUNG FEAT (capability · has_ui · §1 Mục tiêu · §Ngoài phạm vi). KHÔNG viết AC/ca biên/ràng buộc (BA — domain-ba D), KHÔNG ghi chặn ở đâu hay contract (SA — technical-design)."
---

# Product-Owner Method (cắt FEAT)

> **Vai: PO** · **Viết**: danh sách FEAT · frontmatter `capability` / `has_ui` / `status` · FEAT §1 Mục tiêu · §Ngoài phạm vi · §References (dòng bảng luồng FEAT phủ)
> **KHÔNG viết**: §2 AC + §3 Ràng buộc nghiệp vụ (BA — `domain-ba` D) · chặn ở đâu, contract, `consumes` (SA — `technical-design`, `arch/{name}.md`)

## Khi dùng
Bước 5 **nhịp 1** của `/document`, sau CAPABILITIES-MAP (Bước 4). PO cắt từng capability thành FEAT đủ nhỏ để giao và nghiệm thu, rồi để **khung** cho BA viết AC ở nhịp 2 (`domain-ba` D). PO trả lời *cái gì và vì sao*; *ai làm bước nào* BA đã chốt ở Bước 3, *làm thế nào* là việc SA ở Bước 6.

## Output
| Đối tượng | Output |
|---|---|
| Khung FEAT | `docs/feat/FEAT-<slug>.md` theo `templates/TEMPLATE.feat.md` — điền frontmatter + §1 + §Ngoài phạm vi + §References; §2/§3 để BA điền |

## Boot sequence (targeted — đừng đọc sweeping)
1. `STATE.md` + `PROTOCOL.md`.
2. `docs/CAPABILITIES-MAP.md` (capability → outcome) · `docs/PRD.md` §1 vấn đề · §4 out-of-scope · §5 metric · `docs/INTERVIEW.md §Luồng nghiệp vụ đã xác nhận` (bảng luồng + màn nháp — để biết FEAT phủ dòng nào) · `docs/PERSONAS.md`.
3. Nếu có intake: `intake/*` (marker `NGUỒN: INTAKE` trong `docs/INTERVIEW.md`).
4. FEAT đã có trong `docs/feat/` (tránh trùng ID).

## Cách cắt
- **Mỗi capability → ≥1 FEAT.** 1 FEAT = một kết quả người dùng nhận được trọn vẹn (lát dọc qua mọi tầng), KHÔNG cắt theo module hay tầng kỹ thuật.
- **Phủ bảng luồng**: mỗi FEAT ghi ở §References các dòng bảng luồng nó phủ. Dòng bảng có thao tác trên hệ thống mà không FEAT nào phủ = thiếu FEAT.
- **Cỡ**: FEAT gồm nhiều luồng con độc lập → tách; đủ nhỏ để `implementation-plan` xếp ~3-4 FEAT/wave.
- **§1 Mục tiêu**: một đoạn góc nhìn người dùng — FEAT xong thì ai làm được gì mà trước đây chưa làm được.
- **§Ngoài phạm vi**: điều FEAT này KHÔNG làm — BA không viết AC ra ngoài ranh này, QC biết không test gì.
- **`has_ui`**: `true` khi FEAT có thao tác hoặc vùng dữ liệu trên màn (đối chiếu màn nháp của BA).
- `status: DRAFT` (PO đổi `APPROVED` ở bước cuối `/document` khi Authority chốt).
- **Điền ngược** (mục của PO): cột FEAT ở `CAPABILITIES-MAP §1` · dòng "gắn FEAT nó phục vụ" ở `INTERVIEW` · bảng truy vết `intake → FEAT` (đường intake).
- Không ghi tên class / bảng / công nghệ ở bất cứ mục nào — đó là việc SA.

## Chỗ chưa rõ
Không hỏi lại điều Authority đã trả lời (INTERVIEW · bảng luồng đã ký). Chỗ còn thiếu → phân loại theo bảng chỗ chưa rõ PROTOCOL §2.3.

## Quy tắc
- ID `FEAT-<slug>`. Cross-ref bằng ID canonical đầy đủ (không rút gọn).
- Sửa FEAT đã chốt (đã khoá scope) = **wave sau**: `ROADMAP §backlog` → `/next-wave` → `/document` top-up.

## Done
- Mọi capability có ≥1 FEAT · mọi dòng bảng luồng có thao tác hệ thống được ≥1 FEAT phủ · mỗi FEAT đủ frontmatter + §1 + §Ngoài phạm vi + §References → **nhịp 2**: `domain-ba` D viết §2 AC + §3 Ràng buộc nghiệp vụ vào khung.
