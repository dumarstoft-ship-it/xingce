# T180（2022上海B）满分100，5人平均90分，分数互不相同的整数，最低77分，求第2名至少多少分。
from itertools import combinations

FULL, K, AVG, LOW = 100, 5, 90, 77
OPTS = {'A': 90, 'B': 92, 'C': 94, 'D': 96}
best = None
for rest in combinations(range(LOW + 1, FULL + 1), K - 1):   # 其余4人都高于最低分
    if sum(rest) + LOW != K * AVG:
        continue
    second = sorted(rest, reverse=True)[1]
    best = second if best is None else min(best, second)
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('min 2nd =', best)
print(hits[0])
