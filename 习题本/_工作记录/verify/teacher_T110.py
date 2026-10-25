# T110 2024广东41：3男3女中选4人，女生不少于2名的选派方案数
from itertools import combinations

people = ['M1', 'M2', 'M3', 'F1', 'F2', 'F3']
OPTS = {'A': 4, 'B': 8, 'C': 12, 'D': 16}
cnt = sum(1 for g in combinations(people, 4) if sum(p[0] == 'F' for p in g) >= 2)
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('count =', cnt)
print(hits[0])
