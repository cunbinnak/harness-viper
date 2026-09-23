#!/usr/bin/env python3
"""capture_proof.py — HARNESS sinh bằng chứng RUNTIME → tracking/wave-N/proof.json.

Chạy `make check` + curl health endpoint. gate.py đọc proof (MÁY-sinh) thay vì tin checkbox STATE
→ chống fake tiến độ (State=running / tick tay chưa đủ; app phải thật xanh + trả 2xx).

proof.json CHỈ file này ghi (Python I/O, không qua Write tool); `guard_proof` chặn Write/Edit tool đụng
→ agent không giả được (retro: "test xanh nhờ H2" / "dev-done ≠ runnable").

Health PER-TARGET tự suy: đọc ROADMAP §1 cột Target (name+kind) + `docker compose ps` (health Docker tự chấm
per service; service-name = target-name theo convention infra-local-dev/ref-*-config) → không cần gõ URL/port.
Thiếu/không-healthy target container hoá (backend/bff/web) nào = proof đỏ. Mobile (emulator) không proof qua docker.

Usage: python scripts/capture_proof.py [--wave N] [--compose deployment/local/docker-compose.yml]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
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


def _find_bash() -> str | None:
    """Tìm bash.exe trên Windows (Git for Windows)."""
    import os, platform
    if platform.system() != "Windows":
        return None
    candidates = [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def run_check() -> dict:
    try:
        p = subprocess.run(["make", "check"], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=1800)
        return {"ok": p.returncode == 0, "code": p.returncode, "tail": (p.stdout + p.stderr)[-400:]}
    except FileNotFoundError:
        # make không có trên Windows — chạy fallback: mvnw verify trên mỗi backend service
        bash = _find_bash()
        if not bash:
            return {"ok": False, "code": -1, "tail": "make và bash đều không có — cài make hoặc chạy check thủ công"}
        import glob as _glob
        makefiles = _glob.glob(str(ROOT / "services" / "*" / "*" / "Makefile"))
        if not makefiles:
            return {"ok": False, "code": -1, "tail": "make không có và không tìm thấy service nào trong services/*/*/"}
        all_ok = True
        combined = ""
        for mf in makefiles:
            svc = Path(mf).parent
            svc_dir = str(svc)
            if (svc / "mvnw").exists():
                cmd = f'cd "{svc_dir}" && SPRING_DATASOURCE_PASSWORD=${{SPRING_DATASOURCE_PASSWORD:-hrms_dev_secret}} ./mvnw verify -q'
            elif (svc / "package.json").exists():
                # npm check — always succeeds (|| true in Makefile)
                cmd = f'cd "{svc_dir}" && npm run build 2>&1 | grep -E "error|warning" || true'
            else:
                combined += f"\n--- {svc.name} SKIP (unknown project type) ---\n"
                continue
            p = subprocess.run([bash, "-c", cmd], cwd=ROOT, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=1800)
            combined += f"\n--- {svc.name} rc={p.returncode} ---\n" + (p.stdout + p.stderr)[-300:]
            if p.returncode != 0:
                all_ok = False
        return {"ok": all_ok, "code": 0 if all_ok else 1, "tail": combined[-400:]}
    except Exception as e:
        return {"ok": False, "code": -1, "tail": str(e)[:200]}


def _read(rel: str) -> str:
    try:
        return (ROOT / rel).read_text(encoding="utf-8")
    except OSError:
        return ""


def wave_targets(wave: str) -> list[tuple[str, str]]:
    """ROADMAP §1 cột Target của dòng `wave` → [(name, kind)]. Ô: `name (kind), name (kind)`."""
    text = re.sub(r"<!--.*?-->", "", _read("docs/ROADMAP.md"), flags=re.DOTALL)
    m = re.search(r"§1(.*?)(?=\n##\s|\Z)", text, flags=re.DOTALL)
    block = m.group(1) if m else ""
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= {"-", ":", " "} for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return []
    tcol = next((i for i, h in enumerate(rows[0]) if "Target" in h), None)
    if tcol is None:
        return []
    for cells in rows[1:]:
        if cells and cells[0] == str(wave) and tcol < len(cells):
            return [(n, k.lower()) for n, k in re.findall(r"([\w.\-]+)\s*\(\s*(\w+)\s*\)", cells[tcol])]
    return []


def docker_health(compose: str) -> tuple[dict, str | None]:
    """{service: {'state','health'}} từ `docker compose ps --format json` (NDJSON hoặc mảng)."""
    cf = ROOT / compose
    if not cf.exists():
        return {}, f"không thấy {compose}"
    try:
        p = subprocess.run(["docker", "compose", "-f", str(cf), "ps", "--format", "json"],
                           cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=60)
    except FileNotFoundError:
        return {}, "docker không có trên PATH — bật Docker Desktop / cài docker"
    except Exception as e:
        return {}, str(e)[:150]
    if p.returncode != 0:
        return {}, (p.stderr or p.stdout)[-200:] or f"docker compose ps rc={p.returncode}"
    out = p.stdout.strip()
    entries = []
    if out.startswith("["):
        try:
            entries = json.loads(out)
        except ValueError:
            entries = []
    else:
        for line in out.splitlines():
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except ValueError:
                    continue
    m = {}
    for e in entries:
        svc = e.get("Service") or e.get("Name") or ""
        if svc:
            m[svc] = {"state": e.get("State", ""), "health": e.get("Health", "")}
    return m, None


def build_targets(wave: str, compose: str) -> tuple[list[dict], str | None]:
    """Mỗi target ROADMAP → entry tagged {target, kind, state, health, healthy}."""
    targets = wave_targets(wave)
    hmap, err = docker_health(compose)
    out = []
    for name, kind in targets:
        if kind == "mobile":
            out.append({"target": name, "kind": kind, "healthy": None,
                        "note": "emulator — không proof qua docker (dựa ô tick STATE)"})
            continue
        info = hmap.get(name)
        if info is None:
            out.append({"target": name, "kind": kind, "state": "missing", "health": "", "healthy": False,
                        "note": err or "service không thấy trong `docker compose ps` (chưa up? hoặc tên service ≠ tên target)"})
        else:
            out.append({"target": name, "kind": kind, "state": info["state"],
                        "health": info["health"] or "(no healthcheck)",
                        "healthy": info["health"].lower() == "healthy"})
    return out, err


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", default=None)
    ap.add_argument("--compose", default="deployment/local/docker-compose.yml")
    args = ap.parse_args(argv[1:])

    wave = args.wave or state_wave()
    if not wave.isdigit():
        print(f"Wave không rõ ({wave!r}) — cần đang mở wave. Không sinh proof.", file=sys.stderr)
        return 1

    check = run_check()
    targets, derr = build_targets(wave, args.compose)
    proof = {
        "wave": int(wave),
        "check": check,
        "targets": targets,   # per-target tagged: {target, kind, health, healthy} — gate đối chiếu ROADMAP
        "note": "HARNESS capture_proof.py — agent KHÔNG được ghi (guard_proof chặn Write/Edit).",
    }
    out = ROOT / "tracking" / f"wave-{wave}" / "proof.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(proof, ensure_ascii=False, indent=2), encoding="utf-8")

    cont = [t for t in targets if t["kind"] in ("backend", "bff", "web")]
    ok = check["ok"] and bool(targets) and all(t["healthy"] for t in cont)
    tsum = ", ".join(f"{t['target']}:{'✓' if t.get('healthy') else ('n/a' if t.get('healthy') is None else '✗')}" for t in targets) or "(không đọc được target từ ROADMAP)"
    print(f"[proof wave {wave}] make check: {'✓' if check['ok'] else '✗ (' + str(check['code']) + ')'} · targets: {tsum}")
    if derr:
        print(f"  ! docker: {derr}")
    print(f"→ {out.relative_to(ROOT)}  ({'SẴN SÀNG cho VERIFY' if ok else 'CHƯA xanh — gate BUILD sẽ đỏ'})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
