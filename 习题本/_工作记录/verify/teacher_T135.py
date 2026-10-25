# teacher T135（2020山东）每月比上月高x万元，9月是1月的2倍，11月900万元，求全年销售额
from fractions import Fraction as F

OPTS = {'A': 7200, 'B': 7650, 'C': 8100, 'D': 8550}
# 未知数：1月a、月增量x。第m月 = a+(m-1)x
# 方程1：a+8x = 2a  ->  -a + 8x = 0
# 方程2：a+10x = 900
a11, a12, b1 = F(-1), F(8), F(0)
a21, a22, b2 = F(1), F(10), F(900)
det = a11 * a22 - a12 * a21
a = (b1 * a22 - a12 * b2) / det
x = (a11 * b2 - b1 * a21) / det
months = [a + (m - 1) * x for m in range(1, 13)]
total = sum(months)
print('a =', a, 'x =', x, '12月 =', months[-1], '全年 =', total)
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits
print(hits[0])
