# T187（2020深圳）从01~10中选1~4个号码组成一注（不计顺序），至少投多少注才能保证至少有5注号码相同。
from itertools import combinations

NUMS, KMIN, KMAX, SAME = range(1, 11), 1, 4, 5
OPTS = {'A': 1255, 'B': 1361, 'C': 1401, 'D': 1541}
kinds = sum(1 for k in range(KMIN, KMAX + 1) for _ in combinations(NUMS, k))
ans = kinds * (SAME - 1) + 1
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('distinct bets =', kinds, 'answer =', ans)
print(hits[0])
