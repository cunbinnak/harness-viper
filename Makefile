# Makefile — HỢP ĐỒNG 6 LỆNH (mọi stack implement như nhau; command/gate không cần biết stack).
# {{PROJECT_NAME}}
#
# HỢP ĐỒNG CỐ ĐỊNH — **KHÔNG sửa file này** (guard_makefile chặn Write/Edit). Root chỉ ĐIỀU PHỐI,
# viết 1 lần. MAIN điền THÂN THẬT ở per-target `services/<nhóm>/<tên>/Makefile` (stack skill §4, lúc BUILD).
# Hạ tầng dùng chung ở deployment/local/. Shell POSIX (git-bash / WSL / mac / linux).
.PHONY: help dev check test migrate deploy doctor gate infra-up infra-down

COMPOSE := deployment/local/docker-compose.yml
PYTHON  ?= python3
TARGETS := $(shell find services -mindepth 2 -maxdepth 2 -name Makefile -exec dirname {} \; 2>/dev/null)

# Chưa scaffold target nào → BÁO LỖI. KHÔNG để `make check` xanh-giả khi TARGETS rỗng
# (vòng lặp rỗng exit 0 → capture_proof ghi check.ok=true dù chưa có code → gate BUILD qua oan).
GUARD = @[ -n "$(TARGETS)" ] || { echo ""; echo "  ✗ make $@ — chưa scaffold target nào (services/<nhóm>/<tên>/Makefile)."; echo "  BUILD Bước 3: tạo target bằng CLI + điền thân 6 lệnh theo stack-<tên>/SKILL.md §4."; echo ""; exit 1; }

help:    ## liệt kê lệnh
	@echo "{{PROJECT_NAME}} — 6 lệnh: dev check test migrate deploy doctor (+ gate)"
	@echo "  dev/check/test/migrate/deploy/doctor → điều phối make -C tới MỌI target"
	@echo "  gate  → python scripts/gate.py (P=<phase> tuỳ chọn)"
	@echo "Targets: $(TARGETS)"

infra-up:   ## db/redis/kafka local lên (nếu có compose)
	@if [ -f $(COMPOSE) ]; then docker compose -f $(COMPOSE) up -d; else echo "(chưa có $(COMPOSE))"; fi

infra-down: ## dừng hạ tầng (giữ volume)
	@[ -f $(COMPOSE) ] && docker compose -f $(COMPOSE) stop || true

dev: infra-up   ## hạ tầng + dev từng target — VERIFY đánh trên đây
	$(GUARD)
	@for t in $(TARGETS); do echo ">> dev $$t"; $(MAKE) -s -C $$t dev || exit 1; done

check:   ## build + lint + typecheck MỌI target (phải xanh trước khi rời BUILD)
	$(GUARD)
	@for t in $(TARGETS); do echo ">> check $$t"; $(MAKE) -s -C $$t check || exit 1; done

test:    ## test tự động unit/integration TRONG source (khác test-cases.md black-box)
	$(GUARD)
	@for t in $(TARGETS); do echo ">> test $$t"; $(MAKE) -s -C $$t test || exit 1; done

migrate: ## chạy DB migration mọi target
	$(GUARD)
	@for t in $(TARGETS); do echo ">> migrate $$t"; $(MAKE) -s -C $$t migrate || exit 1; done

deploy:  ## deploy production — guard_bc canh ở đây (BACKWARD-COMPAT §3)
	$(GUARD)
	@for t in $(TARGETS); do echo ">> deploy $$t"; $(MAKE) -s -C $$t deploy || exit 1; done

doctor:  ## health check / smoke / rollback readiness mọi target
	$(GUARD)
	@for t in $(TARGETS); do echo ">> doctor $$t"; $(MAKE) -s -C $$t doctor; done

gate:    ## kiểm gate phase hiện tại (make gate  hoặc  make gate P=BUILD)
	@$(PYTHON) scripts/gate.py $(P)
