# teacher_T021  A、B、C三校共招三百多人；A=(B+C)的80%，B比C多60%。至少再招多少人能平分到7个部门
from fractions import Fraction as F

OPTS = {'A': 6, 'B': 5, 'C': 4, 'D': 3}
totals = set()
for c in range(1, 400):
    b = F(8, 5) * c
    if b.denominator != 1:
        continue
    a = F(4, 5) * (b + c)
    if a.denominator != 1:
        continue
    t = int(a + b + c)
    if 300 <= t <= 399:
        totals.add(t)
assert len(totals) == 1, totals
T = totals.pop()
m = next(m for m in range(0, 7) if (T + m) % 7 == 0)
hits = [k for k, v in OPTS.items() if v == m]
assert len(hits) == 1, (m, hits)
# 误把"B比C多60%"当"C是B的60%"（B:C=5:3）时得4
wrong = set()
for c in range(1, 400):
    b = F(5, 3) * c
    a = F(4, 5) * (b + c)
    if b.denominator == 1 and a.denominator == 1 and 300 <= a + b + c <= 399:
        wrong.add(int(a + b + c))
assert len(wrong) == 1, wrong
tw = wrong.pop()
assert next(m for m in range(0, 7) if (tw + m) % 7 == 0) == OPTS['C']
print('总人数 =', T, ' 再招 =', m)
print(hits[0])
