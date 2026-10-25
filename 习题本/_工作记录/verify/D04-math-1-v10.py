# D04-math-1-v10  上月售价是进价的1.6倍，销售300台；本月进价上涨25%，售价不变；
# 本月利润不低于上月的90%，本月至少要销售多少台（台数为整数）
from fractions import Fraction as F

MULT, UP, KEEP, N0 = F(16, 10), F(25, 100), F(90, 100), 300

res = set()
for c in (F(20), F(7), F(123, 4)):          # 任取几个进价，结果应与赋值无关
    price = c * MULT
    old_profit = (price - c) * N0
    unit = price - c * (1 + UP)
    n = next(n for n in range(0, 100000) if unit * n >= KEEP * old_profit)   # 最小整数台数
    res.add(n)
assert len(res) == 1
n = res.pop()

OPTS = {'A': 360, 'B': 462, 'C': 463, 'D': 515}
hits = [L for L, v in OPTS.items() if v == n]
assert len(hits) == 1, hits

# 干扰项来源核对（赋值进价20元：单件利润12元→7元，上月总利润3600元）
c = F(20); price = c * MULT; old_profit = (price - c) * N0; unit = price - c * (1 + UP)
assert (price - c, unit, old_profit) == (12, 7, 3600)
assert int(KEEP * old_profit / unit) == OPTS['B']                     # 舍去小数 462
assert unit * OPTS['B'] < KEEP * old_profit <= unit * OPTS['C']       # 462台不够、463台够
assert -(-old_profit // unit) == OPTS['D']                            # 漏乘90%：3600÷7进一
assert KEEP * old_profit / ((price - c) * (1 - UP)) == OPTS['A']      # 单件利润误作只降25%

print('n', n)
print(hits[0])
