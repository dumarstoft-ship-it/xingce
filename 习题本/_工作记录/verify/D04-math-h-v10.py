# D04-math-h-v10：地铁同月按原票价累计；累计不超过 100 元的部分原价，100～150 元的部分八折，超过 150 元的部分五折。
# 每次原票价 5 元，问当月至少乘车多少次，平均每次实付才不超过 4 元。
# 做法：两种口径分别模拟并确认一致——(1) 按累计金额"分部分"计价；(2) 逐次乘车，按该次乘车前已累计的金额所在档计价
# （票价 5 元整除各分界，两种口径应完全相同，说明题面无歧义）；再从 1 次起逐一检验平均实付。
from fractions import Fraction as F

OPTIONS = {'A': 21, 'B': 40, 'C': 43, 'D': 44}
FARE = 5
TIERS = [(0, 100, F(1)), (100, 150, F(8, 10)), (150, None, F(5, 10))]


def paid_by_portion(total_original):
    paid = F(0)
    for lo, hi, rate in TIERS:
        if total_original > lo:
            top = total_original if hi is None else min(total_original, hi)
            paid += (top - lo) * rate
    return paid


def paid_by_ride(n):
    paid, acc = F(0), 0
    for _ in range(n):
        if acc >= 150:
            rate = F(5, 10)
        elif acc >= 100:
            rate = F(8, 10)
        else:
            rate = F(1)
        paid += FARE * rate
        acc += FARE
    return paid


for n in range(1, 301):
    assert paid_by_portion(FARE * n) == paid_by_ride(n)

ok = [n for n in range(1, 301) if paid_by_portion(FARE * n) / n <= 4]
least = ok[0]
assert all(n in ok for n in range(least, 301))      # 达到之后一直满足
hits = [k for k, v in OPTIONS.items() if v == least]
assert len(hits) == 1
print('least rides =', least, 'avg =', float(paid_by_portion(FARE * least) / least))
print(hits[0])
