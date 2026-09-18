#!/usr/bin/env python3
"""guard_ask — chặn tool AskUserQuestion ở MỌI phase (VIPER-style: tool không phải cơ chế hỏi).

Tương tác Authority CHỈ qua HỘI THOẠI thường, và chỉ ở: DOCUMENT (phỏng vấn) · NEXT-WAVE (go/pivot/kill).
Tool AskUserQuestion (multiple-choice) bị chặn: option có sẵn **mớm lời** — phỏng vấn mở đào sâu hơn,
quyết định thì nêu option + đánh đổi bằng lời. Sau khoá scope (BUILD+): tự quyết (DECISIONS.md),
tắc cứng → STATE §Blocker. Hành động ra-ngoài/không-đảo-ngược vẫn xác nhận được bằng LỜI (lớp permission `ask`).

PreToolUse(AskUserQuestion): exit 2 + stderr = deny (luôn). Fail-open nếu lỗi hook infra.
"""
import sys

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    try:
        sys.stdin.read()
    except Exception:
        return 0  # fail-open: lỗi hạ tầng hook thì không chặn cứng
    sys.stderr.write(
        "[guard_ask] KHÔNG dùng tool AskUserQuestion (VIPER-style — option mớm lời).\n"
        "Hỏi Authority bằng LỜI, chỉ ở DOCUMENT (phỏng vấn mở) / NEXT-WAVE (go/pivot/kill). "
        "Sau khoá scope → tự quyết + docs/DECISIONS.md; tắc cứng → STATE.md §Blocker.\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
