# T109 2019河南选调：6个年级各从6个科技馆（含A馆）中任选一个，恰有两个年级选A馆的方案数
from itertools import product

GRADES, HALLS, K = 6, 6, 2
OPTS = {'A': 1800, 'B': 18750, 'C': 3800, 'D': 9375}
cnt = sum(1 for choice in product(range(HALLS), repeat=GRADES) if choice.count(0) == K)
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('count =', cnt)
print(hits[0])
