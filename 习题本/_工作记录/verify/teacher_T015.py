# teacher_T015  2022国考-63：500万预算买x台进口剩20万；国产单价为进口75%，可买x+3台剩5万。国产单价范围
from fractions import Fraction as F

BUDGET, LEFT1, LEFT2, RATE, MORE = 500, 20, 5, F(3, 4), 3
OPTS = {'A': (0, 30), 'B': (30, 40), 'C': (40, 50), 'D': (50, 10 ** 9)}   # 区间 [lo, hi)

sols = []
for x in range(1, 500):
    p_imp = F(BUDGET - LEFT1, x)
    p_dom = RATE * p_imp
    if (x + MORE) * p_dom == BUDGET - LEFT2:
        sols.append((x, p_dom))
assert len(sols) == 1, sols
x, p = sols[0]
hits = [k for k, (lo, hi) in OPTS.items() if lo <= p < hi]
assert len(hits) == 1, (p, hits)
print('x =', x, ' 国产单价 =', p)
print(hits[0])
