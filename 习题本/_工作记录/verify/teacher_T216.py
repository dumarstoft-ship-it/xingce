# T216（2014山东）三个办公室人均植树4、5、6棵，三室植树总数相等，三室总共至少多少人。
RATES = [4, 5, 6]
OPTS = {'A': 37, 'B': 53, 'C': 74, 'D': 106}
T = next(t for t in range(1, 10 ** 4) if all(t % r == 0 for r in RATES))
ans = sum(T // r for r in RATES)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('trees per office =', T, 'people =', [T // r for r in RATES])
print(hits[0])
