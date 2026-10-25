# D04-math-1-v14  单件成本=原材料(60%)+加工费(40%)；原材料+20%，加工费-25%，出厂价不变，
# 单件利润下降10%，求调整前的成本利润率
from fractions import Fraction as F

RAW_SHARE, RAW_UP, PROC_DOWN, PROFIT_DROP = F(60, 100), F(20, 100), F(25, 100), F(10, 100)

rates = set()
for c0 in (F(100), F(250), F(37)):                 # 赋值与结果无关
    c1 = c0 * RAW_SHARE * (1 + RAW_UP) + c0 * (1 - RAW_SHARE) * (1 - PROC_DOWN)
    # 在成本的万分之一精度上穷举出厂价
    ps = [c0 * F(t, 10000) for t in range(10001, 100000)
          if c0 * F(t, 10000) - c1 == (1 - PROFIT_DROP) * (c0 * F(t, 10000) - c0)]
    assert len(ps) == 1
    rates.add((ps[0] - c0) / c0)
assert len(rates) == 1
rate = rates.pop()

OPTS = {'A': ('', F(2)), 'B': ('约', F('16.7')), 'C': ('约', F('17.6')), 'D': ('', F(20))}


def match(opt, pct):
    approx, v = opt
    return abs(pct - v) < F(5, 100) if approx else pct == v


hits = [L for L, o in OPTS.items() if match(o, rate * 100)]
assert len(hits) == 1, hits

# 干扰项来源核对（赋值成本100）
c0 = F(100); c1 = 60 * (1 + RAW_UP) + 40 * (1 - PROC_DOWN); price = c0 * (1 + rate)
assert match(OPTS['A'], (c1 - c0) / c0 * 100)            # 成本变化率
assert match(OPTS['B'], (price - c0) / price * 100)      # 利润÷售价（口径错）
assert match(OPTS['C'], (price - c1) / c1 * 100)         # 调整后的成本利润率

print('rate', rate, 'new cost', c1, 'price', price)
print(hits[0])
