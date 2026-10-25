# T186（2014陕西/2020浙江选调）1~25号乒乓球，至少取多少个才能保证有两个标号之差为6的倍数。
# 穷举：找最小的k，使任意k个球中都存在两个标号之差为6的倍数（k<=8时组合数可接受）。
from itertools import combinations

BALLS, M = list(range(1, 26)), 6
OPTS = {'A': 6, 'B': 7, 'C': 9, 'D': 10}


def has_pair(sub):
    return any((x - y) % M == 0 for x, y in combinations(sub, 2))


ans = next(k for k in range(1, 9) if all(has_pair(s) for s in combinations(BALLS, k)))
hits = [kk for kk, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('min to guarantee =', ans)
print(hits[0])
