# T181（2017山东选调）8个城市共76家超市，数量两两不同，排名第4的城市有10家，求排名最后的城市最多几家。
from itertools import combinations

TOTAL, N, RANK, VAL = 76, 8, 4, 10
OPTS = {'A': 3, 'B': 4, 'C': 5, 'D': 6}
best = None
for low in combinations(range(1, VAL), N - RANK):          # 第5~8名：1~9中互不相同
    rest = TOTAL - VAL - sum(low)                            # 第1~3名之和
    ok = any(sum(top) == rest for top in combinations(range(VAL + 1, TOTAL + 1), RANK - 1))
    if ok:
        best = min(low) if best is None else max(best, min(low))
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('max of last =', best)
print(hits[0])
