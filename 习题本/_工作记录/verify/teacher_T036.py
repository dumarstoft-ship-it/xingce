# teacher_T036  两村共9600头牛，各卖出本村40%，甲再送乙120头后相等。甲村原有多少头
from fractions import Fraction as F

TOTAL, SELL, GIFT = 9600, F(2, 5), 120
OPTS = {'A': 5200, 'B': 5400, 'C': 5600, 'D': 5000}
sols = [x for x in range(0, TOTAL + 1)
        if (1 - SELL) * x - GIFT == (1 - SELL) * (TOTAL - x) + GIFT]
assert len(sols) == 1, sols
ans = sols[0]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('甲村原有 =', ans)
print(hits[0])
