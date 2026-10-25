# T097 2024国考副省级61：年龄比3:4:5，8年后甲+乙=1.5×丙，该年四人平均43岁，再过15年几人超过60岁
from fractions import Fraction as F

RATIO, YEARS1, MULT, AVG, YEARS2, LIMIT = (3, 4, 5), 8, F(3, 2), 43, 15, 60
OPTS = {'A': 4, 'B': 3, 'C': 2, 'D': 1}

sols = []
for k in range(1, 40):
    a, b, c = (r * k for r in RATIO)
    a8, b8, c8 = a + YEARS1, b + YEARS1, c + YEARS1
    if a8 + b8 == MULT * c8:
        d8 = 4 * AVG - (a8 + b8 + c8)
        if d8 > 0:
            sols.append((a8, b8, c8, d8))
assert len(sols) == 1, sols
ages = [x + YEARS2 for x in sols[0]]
n = sum(1 for x in ages if x > LIMIT)
hits = [k for k, v in OPTS.items() if v == n]
assert len(hits) == 1
print('ages 8 years later', sols[0], '-> +15:', ages)
print(hits[0])
