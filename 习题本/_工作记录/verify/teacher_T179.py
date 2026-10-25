# T179（2017江苏）满分120，前5名平均115分，得分为互不相同的整数，求第3名至少多少分。
from itertools import combinations

FULL, K, AVG = 120, 5, 115
OPTS = {'A': 112, 'B': 113, 'C': 115, 'D': 116}
total = K * AVG
best = None
for combo in combinations(range(0, FULL + 1), K):
    if sum(combo) != total:
        continue
    third = sorted(combo, reverse=True)[2]
    best = third if best is None else min(best, third)
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('min 3rd =', best)
print(hits[0])
