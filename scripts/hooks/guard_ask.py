#!/usr/bin/env python3
"""guard_ask — hook PreToolUse chặn AskUserQuestion ngoài pha DOCUMENT (port VIPER: pha V).

Luật #2 (sau khoá scope KHÔNG hỏi Authority) chỉ dặn bằng văn xuôi thì sau compact trôi mất — agent
lại hỏi. Hook biến thành cơ chế: **CHỈ pha DOCUMENT** (trước khoá scope, chỗ phỏng vấn/quyết định) được
dùng AskUserQuestion; BUILD/VERIFY/SHIP/NEXT-WAVE bị chặn. Ô "Scope khoá" đã tick = chữ ký kết thúc
DOCUMENT → chặn LUÔN, kể cả khi dòng phase còn ghi DOCUMENT (bắt lỗi quên đổi phase).

Exit 0 = cho qua (DOCUMENT chưa khoá scope, hoặc không đọc được STATE — fail-open).
Exit 2 = CHẶN; stderr đưa lại cho model. Ngoại lệ (hành động không-đảo-ngược / ra-ngoài) hỏi bằng LỜI
trong chat (lớp permission `ask` lo), KHÔNG qua tool này.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

REMINDER = (
    "Mơ hồ → tự quyết theo doc + 1 dòng docs/DECISIONS.md, đi tiếp.\n"
    "Ngoài scope → docs/ROADMAP.md §backlog. Tắc cứng (đã thử hết) → STATE.md §Blocker.\n"
    "Ngoại lệ (hành động không đảo ngược / ra ngoài): hỏi bằng LỜI trong chat, không qua tool này.\n"
)


def main() -> int:
    try:
        sys.stdin.read()
        text = (ROOT / "STATE.md").read_text(encoding="utf-8")
    except Exception:
        return 0  # fail-open: lỗi hạ tầng / không có STATE thì không chặn cứng

    # Ô "Scope khoá" tick = kết thúc DOCUMENT → chặn dù dòng phase còn ghi gì (bắt lỗi quên đổi phase).
    if re.search(r"- \[[xX]\]\s*\*\*Scope khoá\*\*", text):
        sys.stderr.write(
            "[guard_ask] Scope ĐÃ KHOÁ (STATE §Gate) — không hỏi Authority qua AskUserQuestion nữa.\n"
            "Vừa rời DOCUMENT? Cập nhật `Phase hiện tại` cho đúng.\n" + REMINDER)
        return 2

    m = re.search(r"Phase hiện tại\s*:\s*([A-Za-z-]+)", text)
    if m is None:
        return 0  # STATE không theo khung — fail-open
    phase = m.group(1).upper().replace(" ", "-")
    if phase == "DOCUMENT":
        return 0  # pha V — chỗ DUY NHẤT được hỏi Authority (phỏng vấn + quyết định)
    sys.stderr.write(
        f"[guard_ask] Pha {phase}: không hỏi Authority qua AskUserQuestion (chỉ DOCUMENT được hỏi).\n" + REMINDER)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
