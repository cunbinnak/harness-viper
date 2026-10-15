---
name: ref-bff-test
description: Pattern test cho MAIN viết ở BUILD — BFF GraphQL (Apollo/NestJS, Node/TS). Vitest; executeOperation với context giả; mock backend tại datasource bằng MSW/nock (khớp arch §3 backend); ma trận ánh xạ lỗi HTTP → extensions.code; DataLoader gộp lô (không N+1); schema chỉ thêm; auth context; coverage 70%. Load khi BUILD target kind=bff.
---

# Reference: BFF Test (MAIN viết ở BUILD)

> **Lưới an toàn của người làm** (`make test`) — không thay TC nghiệm thu của `test-writer`. Convention: `stack-bff`. Viết CÙNG LÚC code.

## 1. Viết test cho gì (ưu tiên)
1. **Mỗi resolver ≥ 3 ca**: thành công · backend trả lỗi · không có quyền.
2. **Ma trận ánh xạ lỗi** backend → GraphQL `extensions.code` (bảng dưới).
3. **DataLoader** gộp lô: N phần tử → backend được gọi **1 lần**.
4. **Auth context**: token hợp lệ → `userId/tenantId/roles`; thiếu/sai/hết hạn → `UNAUTHENTICATED`; resolver KHÔNG đọc identity từ args.
5. **Schema chỉ thêm**: `npm run schema:check` (`stack-bff §4`) trong `make check`.

## 2. Chạy operation — không cần HTTP server
```ts
const res = await server.executeOperation(
  { query: REMOTE_REQUESTS, variables: { first: 10 } },
  { contextValue: makeContext({ userId: 'u-a', tenantId: 't-1', roles: ['EMPLOYEE'] }) });
assert(res.body.kind === 'single');
expect(res.body.singleResult.errors).toBeUndefined();
```
`makeContext` dựng DataLoader **mới mỗi lần** (đúng như runtime: per-request).

## 3. Mock backend tại datasource — khớp contract
MSW (`msw/node`) hoặc `nock` chặn HTTP tới base-url backend. Path/method/envelope **copy đúng `arch/{backend}.md §3`**, dữ liệu có kiểu từ type contract; `onUnhandledRequest: 'error'`. Không mock resolver/datasource nội bộ.

## 4. Ma trận lỗi (mỗi dòng 1 test)
| Backend trả | `extensions.code` |
|---|---|
| 400 / 422 (lỗi nhập, mã nghiệp vụ) | `BAD_USER_INPUT` hoặc mã nghiệp vụ theo `arch §3` (KHÔNG gộp INTERNAL) |
| 401 | `UNAUTHENTICATED` |
| 403 | `FORBIDDEN` |
| 404 | `NOT_FOUND` (hoặc null theo schema) |
| 409 | mã nghiệp vụ (trùng / xung đột) |
| 5xx · timeout | `INTERNAL` — message đã che, không lộ stack |

## 5. DataLoader — chứng minh không N+1
```ts
const spy = vi.fn(); server.use(http.post(`${EMP}/employees/batch`, async ({ request }) => { spy(await request.json()); return HttpResponse.json(...) }));
await exec(LIST_WITH_EMPLOYEE /* 20 dòng */);
expect(spy).toHaveBeenCalledTimes(1);
```

## 6. Coverage + chạy
`vitest run --coverage` ≥ 70% (`src/auth/**` nên ≥ 90%). Test `src/config` đọc env bằng `vi.stubEnv`, không sửa `process.env` trực tiếp.

## 7. Cấm
Test qua HTTP server thật khi `executeOperation` đủ · DataLoader/cache dùng chung giữa test · mock datasource nội bộ thay vì chặn HTTP · response mock không kiểu / path tự đặt · bỏ ca lỗi chỉ test thành công.
