#!/usr/bin/env python3
"""gate.py — kiểm điều kiện rời phase. In ✓/✗ từng mục, exit 1 nếu còn thiếu.

KHÔNG chặn tool, KHÔNG sửa gì. Chỉ báo. Quyết định đi tiếp vẫn là của người.
Nguồn chuẩn của gate: PROTOCOL.md §6. Lệch nhau thì PROTOCOL thắng.

Usage:
    python scripts/gate.py                      # tự đọc phase từ STATE.md
    python scripts/gate.py DOCUMENT|BUILD|VERIFY|SHIP|NEXT-WAVE

Exit: 0 qua · 1 còn thiếu · 2 sai tham số.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "STATE.md"

# Windows console (cp1252) không in được Unicode — ép UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------- readers ----

def read(rel: str) -> str:
    p = ROOT / rel
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


def read_live(rel_or_text: str, *, is_text: bool = False) -> str:
    """Bỏ HTML comment <!-- --> trước khi đếm (guidance không tính)."""
    text = rel_or_text if is_text else read(rel_or_text)
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def filled(rel: str) -> bool:
    """File tồn tại, có nội dung, và không còn placeholder {{...}} (ngoài comment)."""
    live = read_live(rel).strip()
    return bool(live) and "{{" not in live


def count_rows(rel: str, pattern: str) -> int:
    return len(re.findall(pattern, read_live(rel), flags=re.MULTILINE))


def section(rel: str, header: str) -> str:
    """Cắt nội dung một `## header` (tới `## ` kế tiếp)."""
    text = read_live(rel)
    m = re.search(rf"^#{{1,4}}\s*{re.escape(header)}.*?$(.*?)(?=^#{{1,4}}\s|\Z)",
                  text, flags=re.MULTILINE | re.DOTALL)
    return m.group(1) if m else ""


def table_rows(text: str) -> list[list[str]]:
    """Parse các dòng bảng markdown → list ô (bỏ header + separator)."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= {"-", ":", " "} for c in cells):  # separator
            continue
        rows.append(cells)
    return rows[1:] if rows else []  # bỏ header


def state_field(name: str) -> str:
    m = re.search(rf"{re.escape(name)}\s*:\s*(.+)", read("STATE.md"))
    return m.group(1).strip() if m else ""


def phase_from_state() -> str:
    return state_field("Phase hiện tại").upper().replace(" ", "-") or ""


def state_wave() -> str:
    return state_field("Wave").strip()


def scope_locked() -> bool:
    return bool(re.search(r"- \[[xX]\].*Scope khoá", read("STATE.md")))


def challenge_pass(phase: str) -> bool:
    """§Challenge log có ≥1 dòng phase này = PASS."""
    for cells in table_rows(section("STATE.md", "Challenge log")):
        if len(cells) >= 4 and cells[1].upper().startswith(phase[:3]) and "PASS" in cells[3].upper():
            return True
    return False


def git_commit_count() -> int:
    try:
        out = subprocess.run(["git", "rev-list", "--count", "HEAD"],
                             cwd=ROOT, capture_output=True, text=True, timeout=10)
        return int(out.stdout.strip() or 0)
    except Exception:
        return 0


def roadmap_wave_row(wave: str) -> list[str]:
    for cells in table_rows(section("docs/ROADMAP.md", "§1")):
        if cells and cells[0].strip() == str(wave):
            return cells
    return []


def wave_declares_ship(wave: str) -> bool:
    row = roadmap_wave_row(wave)
    return any("SHIP" in c.upper() for c in row)


# ------------------------------------------------------------------ report ---

class Report:
    def __init__(self) -> None:
        self.ok = True

    def check(self, cond: bool, msg: str) -> None:
        mark = "✓" if cond else "✗"
        print(f"  {mark} {msg}")
        if not cond:
            self.ok = False

    def note(self, msg: str) -> None:
        print(f"  • {msg}")


# ------------------------------------------------------------------ gates ----

def gate_document(r: Report) -> None:
    for f in ("docs/PRD.md", "docs/PERSONAS.md", "docs/CAPABILITIES-MAP.md", "docs/TECHSTACK.md"):
        r.check(filled(f), f"{f} tồn tại + điền hết (không còn {{{{)")
    r.check(count_rows_glob("docs/feat", r"FEAT-.*\.md") >= 1, "≥1 docs/feat/FEAT-*.md")
    r.check(filled("docs/arch/OVERVIEW.md"), "docs/arch/OVERVIEW.md điền")
    # ma trận vai×hành động — không ô trống
    matrix = table_rows(section("docs/PERSONAS.md", "§2"))
    empty = [c for row in matrix for c in row[1:] if not c]
    r.check(bool(matrix) and not empty, "PERSONAS §2 ma trận không ô trống")
    # mọi dòng CAPABILITIES có CAP-
    caps = table_rows(section("docs/CAPABILITIES-MAP.md", "§1"))
    r.check(bool(caps) and all("CAP-" in row[0] for row in caps), "CAPABILITIES: mọi dòng có CAP-")
    # ROADMAP có wave + phases
    waves = roadmap_all_waves()
    r.check(bool(waves), "ROADMAP §1 có ≥1 wave")
    r.check(bool(waves) and all(any("BUILD" in c.upper() for c in row) for row in waves),
            "mỗi wave khai phases (≥ BUILD)")
    r.check(challenge_pass("DOCUMENT"), "Challenge DOCUMENT PASS (§Challenge log)")
    r.check(count_rows("docs/DECISIONS.md", r"^\| DEC-") >= 2, "≥2 dòng DECISIONS")
    r.check(scope_locked(), "Scope khoá (STATE tick)")


def gate_build(r: Report) -> None:
    wave = state_wave()
    if wave.isdigit() and int(wave) >= 2:
        row = roadmap_wave_row(wave)
        idx = _col_index("Rà lại")
        val = row[idx] if row and idx is not None and idx < len(row) else ""
        r.check(bool(val) and val not in ("—", "-"), f"ROADMAP wave {wave} có `Rà lại` (wave_reviewed)")
    else:
        r.note("wave 1 — miễn wave_reviewed (fresh từ DOCUMENT)")
    r.check(git_commit_count() >= 1, "đã có commit")
    _state_checkboxes(r, "BUILD")


def gate_verify(r: Report) -> None:
    wave = state_wave()
    tc = f"tracking/wave-{wave}/test-cases.md"
    rows = table_rows(section(tc, "2b")) or table_rows(read(tc))
    results = [row[4].upper() for row in rows if len(row) >= 5]
    has_fail = any("FAIL" in x for x in results)
    has_pass = any("PASS" in x for x in results)
    r.check(exists(tc) and has_pass and not has_fail, f"{tc}: có TC PASS, không TC FAIL")
    # §Findings không BLOCKER/MAJOR chưa xử
    open_major = [row for row in table_rows(section("STATE.md", "Findings"))
                  if len(row) >= 5 and any(s in row[2].upper() for s in ("BLOCKER", "MAJOR"))
                  and not row[4].strip()]
    r.check(not open_major, "§Findings: hết BLOCKER/MAJOR chưa xử")
    _state_checkboxes(r, "VERIFY")


def gate_ship(r: Report) -> None:
    wave = state_wave()
    if not wave_declares_ship(wave):
        r.note(f"wave {wave} không khai SHIP → bỏ qua, đi /next-wave")
        return
    unchecked = count_rows("docs/PRODUCTION-READY.md", r"^- \[ \]")
    # bỏ qua mục (sau deploy) khi tính P1
    after_deploy = count_rows("docs/PRODUCTION-READY.md", r"^- \[ \].*\(sau deploy\)")
    r.check(unchecked - after_deploy <= 0, "PRODUCTION-READY 4 nhóm xanh (trừ (sau deploy))")
    bc3 = count_rows("docs/BACKWARD-COMPAT.md", r"^- \[ \]")
    r.check(bc3 == 0, "BACKWARD-COMPAT §3 xanh (guard_bc)")


def gate_next_wave(r: Report) -> None:
    wave = state_wave()
    tc = f"tracking/wave-{wave}/test-cases.md"
    r.check(exists(tc), "wave đã qua VERIFY (test-cases.md tồn tại)")
    # backlog: mọi dòng có cột Xử
    backlog = table_rows(section("docs/ROADMAP.md", "§3"))
    undisposed = [row for row in backlog if len(row) >= 4 and not row[3].strip()]
    r.check(not undisposed, "ROADMAP §3 backlog: mọi item đã định đoạt (cột Xử không trống)")


# --------------------------------------------------------------- helpers -----

def count_rows_glob(dir_rel: str, pattern: str) -> int:
    d = ROOT / dir_rel
    if not d.exists():
        return 0
    return sum(1 for p in d.glob("*.md")
               if re.match(pattern, p.name) and not p.name.startswith("TEMPLATE"))


def roadmap_all_waves() -> list[list[str]]:
    return [row for row in table_rows(section("docs/ROADMAP.md", "§1"))
            if row and row[0].strip().isdigit()]


def _col_index(name: str) -> int | None:
    for line in section("docs/ROADMAP.md", "§1").splitlines():
        if line.strip().startswith("|") and name in line:
            headers = [c.strip() for c in line.strip("|").split("|")]
            for i, h in enumerate(headers):
                if name in h:
                    return i
    return None


def _state_checkboxes(r: Report, phase: str) -> None:
    sec = section("STATE.md", f"{phase} (wave") or section("STATE.md", phase)
    unchecked = re.findall(r"- \[ \] (.+)", sec)
    for item in unchecked:
        r.check(False, f"[STATE chưa tick] {item[:70]}")
    if not unchecked and sec:
        r.note(f"STATE gate {phase}: mọi mục đã tick")


GATES = {
    "DOCUMENT": gate_document, "BUILD": gate_build, "VERIFY": gate_verify,
    "SHIP": gate_ship, "NEXT-WAVE": gate_next_wave,
}


def main(argv: list[str]) -> int:
    phase = (argv[1].upper() if len(argv) > 1 else phase_from_state()).replace(" ", "-")
    if phase not in GATES:
        print(f"Phase không rõ: {phase!r}. Chọn: {', '.join(GATES)}", file=sys.stderr)
        return 2
    print(f"[gate {phase}]  (nguồn: PROTOCOL.md §6)")
    r = Report()
    GATES[phase](r)
    print(f"\n{'PASS — rời phase được' if r.ok else 'CÒN THIẾU — chưa rời phase'}")
    return 0 if r.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
