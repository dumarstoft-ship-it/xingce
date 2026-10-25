# teacher T132（2021江苏A/青海）8座圆桌，4部门各2人且同部门相邻，不同部门的小李、小王相邻的概率
from fractions import Fraction as F
from itertools import permutations

OPTS = {'A': F(1, 48), 'B': F(1, 24), 'C': F(1, 12), 'D': F(1, 6)}
N = 8
dept = {'李': 0, '李同事': 0, '王': 1, '王同事': 1, '丙1': 2, '丙2': 2, '丁1': 3, '丁2': 3}
people = list(dept)
same_pairs = [(a, b) for i, a in enumerate(people) for b in people[i + 1:] if dept[a] == dept[b]]
adj = lambda i, j: (i - j) % N in (1, N - 1)
good = tot = 0
for perm in permutations(people):
    pos = {p: i for i, p in enumerate(perm)}
    if not all(adj(pos[a], pos[b]) for a, b in same_pairs):
        continue
    tot += 1
    good += adj(pos['李'], pos['王'])
P = F(good, tot)
print('合法坐法', tot, '| 李王相邻', good, '| P =', P)
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
