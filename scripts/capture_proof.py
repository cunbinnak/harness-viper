#!/usr/bin/env python3
"""capture_proof.py — HARNESS sinh bằng chứng RUNTIME → tracking/wave-N/proof.json.

Chạy `make check` + curl health endpoint. gate.py đọc proof (MÁY-sinh) thay vì tin checkbox STATE
→ chống fake tiến độ (State=running / tick tay chưa đủ; app phải thật xanh + trả 2xx).

proof.json CHỈ file này ghi (Python I/O, không qua Write tool); `guard_proof` chặn Write/Edit tool đụng
→ agent không giả được (retro: "test xanh nhờ H2" / "dev-done ≠ runnable").

Usage: python scripts/capture_proof.py [--wave N] [--health URL[,URL...]]   (mặc định health: http://localhost:8080/health)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def state_wave() -> str:
    try:
        m = re.search(r"Wave\s*:\s*(\d+)", (ROOT / "STATE.md").read_text(encoding="utf-8"))
        return m.group(1) if m else ""
    except OSError:
        return ""


def run_check() -> dict:
    try:
        p = subprocess.run(["make", "check"], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=1800)
        return {"ok": p.returncode == 0, "code": p.returncode, "tail": (p.stdout + p.stderr)[-400:]}
    except FileNotFoundError:
        return {"ok": False, "code": -1, "tail": "make không có — cài make hoặc chạy check thủ công"}
    except Exception as e:
        return {"ok": False, "code": -1, "tail": str(e)[:200]}


def curl(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return {"url": url, "status": r.status, "ok": 200 <= r.status < 300}
    except Exception as e:
        return {"url": url, "status": None, "ok": False, "err": str(e)[:120]}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", default=None)
    ap.add_argument("--health", default="http://localhost:8080/health")
    args = ap.parse_args(argv[1:])

    wave = args.wave or state_wave()
    if not wave.isdigit():
        print(f"Wave không rõ ({wave!r}) — cần đang mở wave. Không sinh proof.", file=sys.stderr)
        return 1

    check = run_check()
    health = [curl(u.strip()) for u in args.health.split(",") if u.strip()]
    proof = {
        "wave": int(wave),
        "check": check,
        "health": health,
        "note": "HARNESS capture_proof.py — agent KHÔNG được ghi (guard_proof chặn Write/Edit).",
    }
    out = ROOT / "tracking" / f"wave-{wave}" / "proof.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(proof, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = check["ok"] and all(h["ok"] for h in health)
    print(f"[proof wave {wave}] make check: {'✓' if check['ok'] else '✗ (' + str(check['code']) + ')'} · "
          f"health: {', '.join((h['url'].split('/')[-1] or h['url']) + ':' + str(h['status']) for h in health)}")
    print(f"→ {out.relative_to(ROOT)}  ({'SẴN SÀNG cho VERIFY' if ok else 'CHƯA xanh — gate BUILD sẽ đỏ'})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
