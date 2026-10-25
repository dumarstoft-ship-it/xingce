# D04-math-2-v12 损耗定价
from fractions import Fraction as F
qty, cost, loss, rate = 200, 12, F(1, 10), F(35, 100)
sellable = qty * (1 - loss)
price = qty * cost * (1 + rate) / sellable
err = {'忽略损耗': cost * (1 + rate), '乘1.1代替除0.9': cost * (1 + rate) * F(11, 10), '损耗率加到利润率': cost * (1 + rate + loss)}
print('price =', price, {k: float(v) for k, v in err.items()})
options = {'A': F(162, 10), 'B': F(174, 10), 'C': F(1782, 100), 'D': F(18)}
hits = [k for k, v in options.items() if v == price]
assert len(hits) == 1, hits
print(hits[0])
