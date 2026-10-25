# D04-math-1-v04  会员价低于市场价25%，新会员首单再优惠10%，首单实付5400元，求少花多少
from fractions import Fraction as F

PAID = F(5400)
D1 = 1 - F(25, 100)   # 会员价 = 市场价 * 0.75
D2 = 1 - F(10, 100)   # 首单 = 会员价 * 0.9

# 在 1 元精度上穷举市场价
cands = [m for m in range(1, 100000) if m * D1 * D2 == PAID]
assert len(cands) == 1
market = cands[0]
saved = market - PAID

OPTS = {'A': 1890, 'B': 2025, 'C': 2600, 'D': 2800}
hits = [L for L, v in OPTS.items() if v == saved]
assert len(hits) == 1, hits

# 干扰项来源核对
assert PAID * F(35, 100) == OPTS['A']                      # 以实付为基数且折扣相加
assert PAID * F(125, 100) * F(11, 10) - PAID == OPTS['B']  # 反求误用乘法
assert market * F(35, 100) == OPTS['D']                    # 折扣相加

print('market', market, 'saved', saved)
print(hits[0])
