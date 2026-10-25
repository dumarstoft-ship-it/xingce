# teacher T125（2016山东）6扇门，甲不经1号、乙不经2号、丙不经3号门进出的概率
from fractions import Fraction as F
from itertools import product

OPTS = {'A': F(125, 216), 'B': F(8, 27), 'C': F(27, 64), 'D': F(64, 125)}
DOORS = range(1, 7)
moves = [(i, o) for i in DOORS for o in DOORS if o != i]   # 进门任选，出门从剩下5扇中选
forbid = [1, 2, 3]                                           # 甲、乙、丙各自不能经过的门
good = tot = 0
for m in product(moves, repeat=3):
    tot += 1
    if all(f not in mv for f, mv in zip(forbid, m)):
        good += 1
P = F(good, tot)
print('P =', P, '| 只看进门的错误结果 =', F(5, 6) ** 3)
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
