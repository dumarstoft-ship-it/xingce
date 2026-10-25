# real 2026GK-68  海外业务2023年亏损m、2024年盈利2m；国内每年利润不变；
# 2024年总利润是2023年的1.2倍，求国内每年利润（用m表示）
from fractions import Fraction as F

ratios = set()
for m in (F(1), F(7), F(5, 3)):
    # 在 m 的百分之一精度上穷举国内利润 D（-100m ~ 100m）
    sols = [F(t, 100) * m for t in range(-10000, 10001)
            if F(t, 100) * m + 2 * m == F(12, 10) * (F(t, 100) * m - m)]
    assert len(sols) == 1
    ratios.add(sols[0] / m)
assert len(ratios) == 1
k = ratios.pop()

OPTS = {'A': 13, 'B': 14, 'C': 15, 'D': 16}
hits = [L for L, v in OPTS.items() if v == k]
assert len(hits) == 1, hits

# 速算核对：总利润增加3m = 2023年总利润的20%
assert 3 / F(2, 10) == k - 1        # 2023年总利润15m，国内 = 15m + m
print('domestic =', k, 'm')
print(hits[0])
