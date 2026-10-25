# teacher T149（2022浙江/河北）105架无人机依次升空n、n-1、…、1架，第10次升空几架
OPTS = {'A': 3, 'B': 5, 'C': 8, 'D': 10}
TOTAL, K = 105, 10
ns = [n for n in range(1, 1000) if n * (n + 1) // 2 == TOTAL]
assert len(ns) == 1
ans = ns[0] - (K - 1)
print('n =', ns[0], '第10次', ans)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits
print(hits[0])
