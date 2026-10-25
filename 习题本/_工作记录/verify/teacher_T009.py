# teacher_T009  2023国考-61：八折卖2件利润 = 原价卖1件利润 = 降价120元卖3件利润，求定价
from fractions import Fraction as F

DISC, CUT = F(4, 5), 120
OPTS = {'A': 360, 'B': 450, 'C': 540, 'D': 720}

sols = []
for P in range(1, 5001):
    # 2(DISC*P - C) = P - C  →  C = 2*DISC*P - P
    C = 2 * DISC * P - P
    if C <= 0:
        continue
    if P - C == 3 * (P - CUT - C):
        sols.append((P, C))
assert len(sols) == 1, sols
P, C = sols[0]
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, (P, hits)
assert OPTS['A'] == DISC * P                 # 答成八折售价
print('定价, 成本 =', P, C)
print(hits[0])
