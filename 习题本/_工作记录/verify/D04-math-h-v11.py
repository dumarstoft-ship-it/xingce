# D04-math-h-v11：月应纳税所得额不超过 3000 元的部分 3%，3000～12000 元的部分 10%，12000～25000 元的部分 20%。
# 甲的应纳税所得额比乙少 6000 元，应纳税额比乙少 840 元，求甲的应纳税所得额。
# 做法：g(x)=tax(x+6000)-tax(x) 是分段一次函数，在每个分段上精确求解 g(x)=840；
# 再用整数元逐一枚举作交叉检查（乙不超过税率表给出的 25000 元）。
from fractions import Fraction as F

OPTIONS = {'A': 8400, 'B': 9600, 'C': 12000, 'D': 14400}
BRACKETS = [(0, 3000, F(3, 100)), (3000, 12000, F(10, 100)), (12000, 25000, F(20, 100))]
GAP_INCOME, GAP_TAX, TOP = 6000, 840, 25000


def tax(x):
    assert 0 <= x <= TOP
    t = F(0)
    for lo, hi, r in BRACKETS:
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def g(x):
    return tax(x + GAP_INCOME) - tax(x)


lo_x, hi_x = 0, TOP - GAP_INCOME
cuts = {lo_x, hi_x}
for _, hi, _ in BRACKETS[:-1]:
    for c in (hi, hi - GAP_INCOME):
        if lo_x < c < hi_x:
            cuts.add(c)
cuts = sorted(cuts)
exact = set()
for L, R in zip(cuts, cuts[1:]):
    gL, gR = g(F(L)), g(F(R))
    if gL == gR:
        assert gL != GAP_TAX, 'infinitely many solutions'
        continue
    x = L + (GAP_TAX - gL) * (R - L) / (gR - gL)
    if L <= x <= R:
        exact.add(x)
assert len(exact) == 1, exact
x = exact.pop()

grid = [v for v in range(lo_x, hi_x + 1) if g(v) == GAP_TAX]
assert grid == [x], grid

hits = [k for k, v in OPTIONS.items() if v == x]
assert len(hits) == 1
print('甲 =', x, '乙 =', x + GAP_INCOME, 'taxes =', tax(x), tax(x + GAP_INCOME))
print(hits[0])
