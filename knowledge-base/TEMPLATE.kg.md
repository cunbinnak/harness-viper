<!-- gate bỏ qua TEMPLATE.* — copy thành knowledge-base/<name>.md. Viết DẦN ở BUILD/VERIFY, không điền 1 lần. -->
# KG — {{name}}

> Bộ nhớ va vấp per-target. **MAIN ĐỌC file này TRƯỚC khi code/rebuild target này** (áp lại invariants/gotchas).
> KHÔNG phase-lock · sống sót qua mất code · viết dần ở BUILD/VERIFY (MAIN + review agent append learnings).

<!-- bất biến không được phạm — phạm là bug nghiêm trọng. -->
## §Invariants
- {{vd: mọi query scope theo (tenantId, outletId) — không query xuyên tenant}}

<!-- đã va — cách tránh. -->
## §Gotchas
- {{vd: docker-compose YAML anchor merge nông → khai env tường minh REDIS_HOST/PORT per-service}}

<!-- lỗi từng xảy ra — nguyên nhân gốc — cách vá. -->
## §Failure-modes
- {{lỗi · nguyên nhân gốc · cách vá}}

<!-- quyết định kỹ thuật per-target (link docs/DECISIONS.md). -->
## §Key-decisions
- {{vd: soft-delete thay hard-delete (DEC-0012)}}
