# Makefile — HỢP ĐỒNG 6 LỆNH (mọi stack implement như nhau; command không cần biết stack).
# {{PROJECT_NAME}}
#
# HAI TẦNG:
#   • Root (file này) = ĐIỀU PHỐI, generic, viết 1 lần — quét mọi target trong services/ rồi gọi `make -C`.
#   • Per-target `services/<nhóm>/<tên>/Makefile` = THÂN THẬT, do stack skill điền lúc BUILD (Bước 3 scaffold).
# Giả định shell POSIX (git-bash / WSL / mac / linux). Hạ tầng dùng chung ở deployment/local/.
.PHONY: dev check test migrate deploy doctor infra-up infra-down

COMPOSE := deployment/local/docker-compose.yml
TARGETS := $(shell find services -mindepth 2 -maxdepth 2 -name Makefile -exec dirname {} \; 2>/dev/null)

infra-up:   ## db/redis/kafka local lên (nếu có compose)
	@if [ -f $(COMPOSE) ]; then docker compose -f $(COMPOSE) up -d; else echo "(chưa có $(COMPOSE))"; fi

infra-down: ## dừng hạ tầng (giữ volume)
	@[ -f $(COMPOSE) ] && docker compose -f $(COMPOSE) stop || true

dev: infra-up   ## hạ tầng + dev từng target — VERIFY đánh trên đây
	@for t in $(TARGETS); do echo ">> dev $$t"; $(MAKE) -s -C $$t dev || exit 1; done

check:   ## build + lint + typecheck MỌI target (phải xanh trước khi rời BUILD)
	@for t in $(TARGETS); do echo ">> check $$t"; $(MAKE) -s -C $$t check || exit 1; done

test:    ## test tự động unit/integration TRONG source (khác test-cases.md black-box)
	@for t in $(TARGETS); do echo ">> test $$t"; $(MAKE) -s -C $$t test || exit 1; done

migrate: ## chạy DB migration mọi target
	@for t in $(TARGETS); do echo ">> migrate $$t"; $(MAKE) -s -C $$t migrate || exit 1; done

deploy:  ## deploy production — guard_bc canh ở đây (BACKWARD-COMPAT §3)
	@for t in $(TARGETS); do echo ">> deploy $$t"; $(MAKE) -s -C $$t deploy || exit 1; done

doctor:  ## health check / smoke / rollback readiness mọi target
	@for t in $(TARGETS); do echo ">> doctor $$t"; $(MAKE) -s -C $$t doctor; done
