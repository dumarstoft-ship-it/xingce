# T108 10名运动员平均分成两组（不分组名），有多少种分法
from itertools import combinations
from math import comb

N = 10
OPTS = {'A': 120, 'B': 126, 'C': 240, 'D': 252}
people = frozenset(range(N))
parts = set()
for g in combinations(range(N), N // 2):
    g = frozenset(g)
    parts.add(frozenset({g, people - g}))
cnt = len(parts)
assert comb(N, N // 2) == OPTS['D']        # 干扰项：未除序
print('partitions =', cnt)
print([k for k, v in OPTS.items() if v == cnt][0])
