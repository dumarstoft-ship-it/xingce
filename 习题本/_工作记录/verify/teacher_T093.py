# T093 2009江苏A：按100%利润定价，售出70%后余下打折，总利润为期望的91%，求折扣
from fractions import Fraction as F

MARKUP, SOLD, TARGET = F(1), F(70, 100), F(91, 100)
OPTS = {'A': F(6, 10), 'B': F(7, 10), 'C': F(85, 100), 'D': F(9, 10)}

cost = F(1)
price = cost * (1 + MARKUP)
expected = (price - cost) * 1            # 全部按定价卖出的利润（按单位数量）
found = []
for k, d in OPTS.items():
    profit = SOLD * (price - cost) + (1 - SOLD) * (price * d - cost)
    if profit == TARGET * expected:
        found.append(k)
assert len(found) == 1, found
# 线段法核对：剩余部分利润率x满足 0.7*100% + 0.3*x = 91%
x = (TARGET - SOLD * MARKUP) / (1 - SOLD)
assert cost * (1 + x) / price == OPTS[found[0]]
print('remaining profit rate =', x)
print(found[0])
