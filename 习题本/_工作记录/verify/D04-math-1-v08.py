# D04-math-1-v08  A比B贵4元，B是A的80%；同一笔经费全买B比全买A多15份（都恰好用完）；
# 两款买相同份数，最多各买多少份？
from fractions import Fraction as F

DIFF, RATIO, MORE = 4, F(80, 100), 15

# 1) 单价：在0.01元精度上穷举A的单价
prices = [(F(c, 100), F(c, 100) - DIFF) for c in range(1, 100000)
          if F(c, 100) - DIFF > 0 and F(c, 100) - DIFF == RATIO * F(c, 100)]
assert len(prices) == 1
A, B = prices[0]
# 2) 经费：全买A x份、全买B x+15份，花费相同
xs = [x for x in range(1, 100000) if A * x == B * (x + MORE)]
assert len(xs) == 1
budget = A * xs[0]
# 3) 两款各买n份，总价不超过经费
n = max(n for n in range(0, 100000) if n * (A + B) <= budget)

OPTS = {'A': 30, 'B': 33, 'C': 34, 'D': 40}
hits = [L for L, v in OPTS.items() if v == n]
assert len(hits) == 1, hits

# 干扰项来源核对
assert min(int((budget / 2) // A), int((budget / 2) // B)) == OPTS['A']   # 经费平分
assert -(-budget // (A + B)) == OPTS['C']                                 # 进一
wB = F(DIFF) / F(20, 100)          # 误读为"A比B贵20%"：B=20、A=24
wA = wB + DIFF
wx = [x for x in range(1, 100000) if wA * x == wB * (x + MORE)][0]
assert int((wA * wx) // (wA + wB)) == OPTS['D']

print('A', A, 'B', B, 'x', xs[0], 'budget', budget, 'n', n)
print(hits[0])
