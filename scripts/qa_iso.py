#!/usr/bin/env python3
"""qa_iso.py — bản sao hệ để QA kiểm ca phụ thuộc THỜI GIAN / JOB định kỳ trên hệ thật, không đụng hệ chính.

Mỗi bản sao = 1 DB clone (CREATE DATABASE … TEMPLATE từ DB mẫu) + 1 container backend thứ hai cùng image, cùng biến
môi trường, chỉ đổi DB và đồng hồ. Dùng thay cho restart hệ chính với APP_CLOCK_FIXED hay tự viết Dockerfile / clone DB.

  py -3 scripts/qa_iso.py snapshot --service <backend> [--sql "UPDATE …"]   # chụp DB chính làm DB mẫu
  py -3 scripts/qa_iso.py start <tag> --service <backend> --at 2026-11-01T00:00:50+07:00
        [--mode run|frozen] [--health /health/ready] [--sql "UPDATE …"] [--max 2]
  py -3 scripts/qa_iso.py move <tag> --at <giờ mới>     # đổi giờ: chạy lại container trên CÙNG DB clone
  py -3 scripts/qa_iso.py list | stop <tag> | clean --service <backend> [--image]

--mode run (mặc định): đồng hồ giả CHẠY TIẾP (libfaketime) → job @Scheduled tự chạy khi tới giờ; đặt --at vài giây
  TRƯỚC mốc job thay vì ngồi chờ; cần đi qua thời gian dài (thư trễ 15 phút) → `move` sang mốc sau.
--mode frozen: đồng hồ đứng yên qua biến APP_CLOCK_FIXED (ref-backend-test §3) — job không tự chạy.
DB mẫu là ảnh chụp lúc `snapshot` (lần `start` đầu tự chụp): dữ liệu nền đổi trên hệ chính → `snapshot` lại.
Tên riêng `<db>_iso_*` / `<service>-iso-*` — không đụng bản sao tự dựng theo cách khác.
Thoát: 0 ổn · 1 dùng sai / bản sao lỗi · 3 hạ tầng (docker không phản hồi) → ghi TC BLOCKED `hạ tầng: …`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

LABEL = "qa_iso"
FT_LIB = "/opt/faketime/libfaketimeMT.so.1"
JDBC = re.compile(r"(jdbc:postgresql://[^/\s]+/)([A-Za-z0-9_]+)")


class Infra(Exception):
    """docker không phản hồi / không có → exit 3."""


def die(msg: str, code: int = 1) -> None:
    print(f"qa_iso: {msg}", file=sys.stderr)
    sys.exit(code)


def docker(*args: str, timeout: int = 120, inp: str | None = None, check: bool = True) -> str:
    try:
        p = subprocess.run(["docker", *args], input=inp, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        raise Infra(f"docker {args[0]} quá {timeout}s không phản hồi")
    except FileNotFoundError:
        raise Infra("không thấy lệnh docker")
    if check and p.returncode != 0:
        raise RuntimeError(f"docker {' '.join(args[:3])}…: {(p.stderr or p.stdout).strip()[-400:]}")
    return p.stdout


# ---------- hàm thuần (selftest kiểm) ----------
def swap_db_env(env: list[str], db: str, new_db: str) -> list[str]:
    """Đổi tên DB trong mọi URL jdbc:postgresql trỏ tới `db` → `new_db`; bỏ APP_CLOCK_FIXED cũ."""
    out = []
    for kv in env:
        k, _, v = kv.partition("=")
        if k == "APP_CLOCK_FIXED":
            continue
        out.append(f"{k}={JDBC.sub(lambda m: m.group(1) + (new_db if m.group(2) == db else m.group(2)), v)}")
    return out


def faketime_value(at: dt.datetime, now: dt.datetime) -> str:
    """Độ lệch tương đối theo giây so với giờ thật — không phụ thuộc múi giờ của container."""
    return f"{int(round((at - now).total_seconds())):+d}"


def parse_at(s: str) -> dt.datetime:
    try:
        t = dt.datetime.fromisoformat(s)
    except ValueError:
        die(f"--at phải là ISO có múi giờ, vd 2026-11-01T00:00:50+07:00 (nhận: {s})")
    if t.tzinfo is None:
        die(f"--at thiếu múi giờ (+07:00): {s}")
    return t


def safe_tag(tag: str) -> str:
    if not re.fullmatch(r"[a-z0-9_]{1,30}", tag):
        die("tag chỉ gồm a-z, 0-9, _ (tối đa 30 ký tự)")
    return tag


# ---------- tìm hệ chính ----------
def find_container(service: str, project: str | None) -> dict:
    f = ["ps", "--filter", f"label=com.docker.compose.service={service}", "--format", "{{.ID}}"]
    if project:
        f[1:1] = ["--filter", f"label=com.docker.compose.project={project}"]
    # bản sao kế thừa nhãn com.docker.compose.* từ image → loại container mang nhãn bản sao, chỉ giữ hệ chính
    ids = [i for i in docker(*f).split()
           if docker("inspect", "--format", "{{index .Config.Labels \"" + LABEL + "\"}}", i).strip() != "1"]
    if not ids:
        die(f"không thấy container đang chạy của service `{service}`" + (f" (project {project})" if project else "")
            + " — hệ chính phải đang chạy")
    if len(ids) > 1:
        die(f"service `{service}` có {len(ids)} container — chỉ rõ --project")
    return json.loads(docker("inspect", ids[0]))[0]


def db_info(api: dict, db_service: str) -> dict:
    project = api["Config"]["Labels"].get("com.docker.compose.project")
    dbc = find_container(db_service, project)
    env = dict(kv.split("=", 1) for kv in dbc["Config"]["Env"] if "=" in kv)
    names = {m.group(2) for kv in api["Config"]["Env"] for m in JDBC.finditer(kv)}
    if len(names) != 1:
        die(f"không xác định được DB của backend từ biến jdbc:postgresql (thấy: {sorted(names) or 'không có'})")
    return {"container": dbc["Name"].lstrip("/"), "user": env.get("POSTGRES_USER", "postgres"), "db": names.pop(),
            "project": project}


def psql(d: dict, sql: str, db: str = "postgres", timeout: int = 120) -> str:
    return docker("exec", d["container"], "psql", "-U", d["user"], "-d", db, "-v", "ON_ERROR_STOP=1", "-tAc", sql,
                  timeout=timeout)


def db_exists(d: dict, name: str) -> bool:
    return psql(d, f"SELECT 1 FROM pg_database WHERE datname = '{name}'").strip() == "1"


def tpl_name(d: dict) -> str:
    return f"{d['db']}_iso_tpl"


def snapshot(d: dict, sqls: list[str]) -> None:
    tpl, u = tpl_name(d), d["user"]
    psql(d, f"DROP DATABASE IF EXISTS {tpl} WITH (FORCE)")
    psql(d, f"CREATE DATABASE {tpl}")
    docker("exec", d["container"], "sh", "-c",
           f"pg_dump -U {u} {d['db']} | psql -q -U {u} -d {tpl} -v ON_ERROR_STOP=1 >/dev/null", timeout=900)
    for s in sqls:
        psql(d, s, tpl)
    print(f"DB mẫu {tpl} = ảnh chụp {d['db']} lúc {dt.datetime.now():%H:%M:%S}")


# ---------- image faketime (build 1 lần cho mỗi image backend) ----------
def faketime_image(api: dict) -> str:
    base = api["Image"]
    short = base.split(":")[-1][:12]
    tag = f"qa-iso-faketime:{short}"
    if docker("images", "-q", tag).strip():
        return tag
    src = f"qa-iso-base:{short}"          # BuildKit không nhận FROM sha256:… → gắn tên tạm cho đúng image đang chạy
    docker("tag", base, src)
    kind = docker("run", "--rm", "--entrypoint", "sh", base, "-c",
                  "test -f /etc/alpine-release && echo alpine || echo glibc", check=False).strip()
    user = api["Config"].get("User") or "root"
    if kind == "alpine":
        df = (f"FROM {src}\nUSER root\nRUN apk add --no-cache libfaketime && mkdir -p /opt/faketime "
              f"&& ln -sf /usr/lib/faketime/libfaketimeMT.so.1 {FT_LIB}\nUSER {user}\n")
    elif kind == "glibc":
        df = ("FROM debian:bookworm-slim AS ft\nRUN apt-get update && apt-get install -y --no-install-recommends "
              "libfaketime && mkdir -p /opt/faketime && cp \"$(dpkg -L libfaketime | grep 'libfaketimeMT.so.1$')\" "
              f"/opt/faketime/\nFROM {src}\nCOPY --from=ft /opt/faketime/ /opt/faketime/\n")
    else:
        die("image backend không có shell (distroless?) → không gắn được libfaketime; dùng --mode frozen")
    print(f"build {tag} (1 lần cho image backend này)…")
    docker("build", "-t", tag, "-", inp=df, timeout=900)
    return tag


# ---------- chạy bản sao ----------
def free_port(start: int = 18080) -> int:
    for p in range(start, start + 200):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    die("không còn cổng trống 18080–18279")


def wait_ready(name: str, port: int, health: str | None, wait: int) -> None:
    url = f"http://localhost:{port}{health or '/'}"
    end = time.time() + wait
    while time.time() < end:
        st = json.loads(docker("inspect", name))[0]["State"]
        if not st["Running"]:
            print(docker("logs", "--tail", "30", name, check=False), file=sys.stderr)
            die(f"bản sao {name} đã dừng (exit {st.get('ExitCode')}) — xem log trên")
        try:
            code = urllib.request.urlopen(url, timeout=5).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception:
            code = 0
        if (code == 200) if health else (0 < code < 500):
            return
        time.sleep(3)
    die(f"bản sao {name} chưa sẵn sàng sau {wait}s ({url})")


def launch(api: dict, d: dict, tag: str, at: dt.datetime, mode: str, port: int, health: str | None, wait: int) -> None:
    service = api["Config"]["Labels"].get("com.docker.compose.service", "backend")
    name, clone = f"{service}-iso-{tag}", f"{d['db']}_iso_{tag}"
    env = swap_db_env(api["Config"]["Env"], d["db"], clone)
    image = api["Image"]
    if mode == "run":
        image = faketime_image(api)
        env += [f"LD_PRELOAD={FT_LIB}", f"FAKETIME={faketime_value(at, dt.datetime.now(dt.timezone.utc))}",
                "FAKETIME_NO_CACHE=1", "FAKETIME_DONT_FAKE_MONOTONIC=1"]
    else:
        env.append(f"APP_CLOCK_FIXED={at.isoformat()}")
    cport = next(iter(api["Config"].get("ExposedPorts") or {"8080/tcp": {}})).split("/")[0]
    net = next(iter(api["NetworkSettings"]["Networks"]))
    labels = {LABEL: "1", f"{LABEL}.tag": tag, f"{LABEL}.service": service, f"{LABEL}.project": d["project"] or "",
              f"{LABEL}.db": clone, f"{LABEL}.at": at.isoformat(), f"{LABEL}.mode": mode, f"{LABEL}.port": str(port),
              f"{LABEL}.health": health or ""}
    ep, cmd = api["Config"].get("Entrypoint") or [], api["Config"].get("Cmd") or []
    args = ["run", "-d", "--name", name, "--network", net, "-p", f"{port}:{cport}",
            "--entrypoint", ep[0] if ep else ""]          # chép entrypoint / command thật (compose có thể ghi đè)
    for k, v in labels.items():
        args += ["--label", f"{k}={v}"]
    for kv in env:
        args += ["-e", kv]
    docker(*args, image, *ep[1:], *cmd)
    try:
        wait_ready(name, port, health, wait)
    except SystemExit:
        docker("rm", "-f", name, check=False)       # không để rác: bản sao lỗi thì gỡ container
        raise
    print(f"bản sao `{tag}` sẵn sàng: http://localhost:{port} · DB {clone} · giờ {at.isoformat()} "
          f"({'chạy tiếp' if mode == 'run' else 'đứng yên'})")


def iso_containers(project: str | None = None, tag: str | None = None) -> list[dict]:
    f = ["ps", "-a", "--filter", f"label={LABEL}=1", "--format", "{{.ID}}"]
    if project:
        f[2:2] = ["--filter", f"label={LABEL}.project={project}"]
    if tag:
        f[2:2] = ["--filter", f"label={LABEL}.tag={tag}"]
    ids = docker(*f).split()
    return json.loads(docker("inspect", *ids)) if ids else []


def cmd_start(a) -> None:
    tag, at = safe_tag(a.tag), parse_at(a.at)
    api = find_container(a.service, a.project)
    d = db_info(api, a.db_service)
    if iso_containers(tag=tag):
        die(f"bản sao `{tag}` đã có — đổi giờ: move · bỏ: stop")
    running = [c for c in iso_containers(d["project"]) if c["State"]["Running"]]
    if len(running) >= a.max:
        die(f"đã có {len(running)} bản sao chạy (trần --max {a.max}): "
            + ", ".join(c["Config"]["Labels"][f"{LABEL}.tag"] for c in running)
            + " — stop bớt, hoặc gom các TC cùng mốc giờ vào một bản sao")
    if not db_exists(d, tpl_name(d)):
        snapshot(d, [])
    clone = f"{d['db']}_iso_{tag}"
    psql(d, f"DROP DATABASE IF EXISTS {clone} WITH (FORCE)")
    psql(d, f"CREATE DATABASE {clone} TEMPLATE {tpl_name(d)}", timeout=300)
    try:
        for s in a.sql:
            psql(d, s, clone)
        launch(api, d, tag, at, a.mode, free_port(), a.health, a.wait)
    except (SystemExit, RuntimeError):
        psql(d, f"DROP DATABASE IF EXISTS {clone} WITH (FORCE)")
        raise


def cmd_move(a) -> None:
    tag, at = safe_tag(a.tag), parse_at(a.at)
    cs = iso_containers(tag=tag)
    if not cs:
        die(f"không có bản sao `{tag}`")
    lb = cs[0]["Config"]["Labels"]
    api = find_container(lb[f"{LABEL}.service"], lb[f"{LABEL}.project"] or None)
    d = db_info(api, a.db_service)
    docker("rm", "-f", cs[0]["Name"].lstrip("/"))
    launch(api, d, tag, at, a.mode or lb[f"{LABEL}.mode"], int(lb[f"{LABEL}.port"]),
           lb[f"{LABEL}.health"] or None, a.wait)


def drop(c: dict, db_service: str) -> None:
    lb = c["Config"]["Labels"]
    docker("rm", "-f", c["Name"].lstrip("/"), check=False)
    try:
        api = find_container(lb[f"{LABEL}.service"], lb[f"{LABEL}.project"] or None)
        psql(db_info(api, db_service), f"DROP DATABASE IF EXISTS {lb[f'{LABEL}.db']} WITH (FORCE)")
    except SystemExit:
        print(f"  (hệ chính không chạy — chưa xoá được DB {lb[f'{LABEL}.db']})", file=sys.stderr)
    print(f"đã bỏ bản sao `{lb[f'{LABEL}.tag']}`")


def cmd_stop(a) -> None:
    cs = iso_containers(tag=safe_tag(a.tag))
    if not cs:
        die(f"không có bản sao `{a.tag}`")
    drop(cs[0], a.db_service)


def cmd_list(a) -> None:
    cs = iso_containers()
    for c in cs:
        lb = c["Config"]["Labels"]
        print(f"{lb[f'{LABEL}.tag']:<14} {'chạy' if c['State']['Running'] else 'dừng':<5} :{lb[f'{LABEL}.port']:<6} "
              f"{lb[f'{LABEL}.mode']:<6} {lb[f'{LABEL}.at']}  DB {lb[f'{LABEL}.db']}")
    print(f"{len(cs)} bản sao")


def cmd_clean(a) -> None:
    for c in iso_containers():
        drop(c, a.db_service)
    if a.service:
        d = db_info(find_container(a.service, a.project), a.db_service)
        for name in psql(d, f"SELECT datname FROM pg_database WHERE datname LIKE '{d['db']}\\_iso\\_%'").split():
            psql(d, f"DROP DATABASE IF EXISTS {name} WITH (FORCE)")
            print(f"đã xoá DB {name}")
    if a.image:
        for repo in ("qa-iso-faketime", "qa-iso-base"):
            for ref in docker("images", repo, "--format", "{{.Repository}}:{{.Tag}}").split():
                docker("rmi", ref, check=False)
        print("đã xoá image qa-iso-faketime / qa-iso-base")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, need_service: bool) -> None:
        sp.add_argument("--service", required=need_service, help="tên service backend trong docker compose")
        sp.add_argument("--project", help="compose project (khi nhiều project cùng tên service)")
        sp.add_argument("--db-service", default="db", help="service Postgres (mặc định db)")

    s = sub.add_parser("snapshot")
    common(s, True)
    s.add_argument("--sql", action="append", default=[])
    s = sub.add_parser("start")
    common(s, True)
    s.add_argument("tag")
    s.add_argument("--at", required=True)
    s.add_argument("--mode", choices=["run", "frozen"], default="run")
    s.add_argument("--health")
    s.add_argument("--sql", action="append", default=[])
    s.add_argument("--max", type=int, default=2)
    s.add_argument("--wait", type=int, default=240)
    s = sub.add_parser("move")
    s.add_argument("tag")
    s.add_argument("--at", required=True)
    s.add_argument("--mode", choices=["run", "frozen"])
    s.add_argument("--db-service", default="db")
    s.add_argument("--wait", type=int, default=240)
    s = sub.add_parser("stop")
    s.add_argument("tag")
    s.add_argument("--db-service", default="db")
    sub.add_parser("list")
    s = sub.add_parser("clean")
    common(s, False)
    s.add_argument("--image", action="store_true")
    a = p.parse_args()
    try:
        if a.cmd == "snapshot":
            snapshot(db_info(find_container(a.service, a.project), a.db_service), a.sql)
        else:
            {"start": cmd_start, "move": cmd_move, "stop": cmd_stop, "list": cmd_list, "clean": cmd_clean}[a.cmd](a)
    except Infra as e:
        die(f"hạ tầng: {e} — ghi TC là BLOCKED `hạ tầng: …`, báo MAIN; KHÔNG ngồi chờ", 3)
    except RuntimeError as e:
        die(str(e))


if __name__ == "__main__":
    main()
