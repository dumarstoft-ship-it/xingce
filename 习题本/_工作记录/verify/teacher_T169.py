# teacher T169（2021江苏）从1号起每隔6个号得A，从最后一号往前每隔8个号得B，无人同时得A、B，人数最多多少
OPTS = {'A': 46, 'B': 48, 'C': 52, 'D': 54}
GA, GB = 6, 8                                      # 每隔6个 -> 步长7；每隔8个 -> 步长9

def clash(n):
    a = set(range(1, n + 1, GA + 1))
    b = set(range(n, 0, -(GB + 1)))
    return bool(a & b)

LIMIT = 2000
ok = [n for n in range(1, LIMIT) if not clash(n)]
best = max(ok)
assert all(clash(n) for n in range(best + 1, LIMIT))
print('不重合的最大人数', best, '| 选项是否重合', {v: clash(v) for v in OPTS.values()})
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, hits
print(hits[0])
