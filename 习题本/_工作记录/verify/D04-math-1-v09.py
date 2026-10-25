# D04-math-1-v09  利润率26%，进货价下降、售价不变后利润率变为40%，求进货价降幅
from fractions import Fraction as F

R0, R1 = F(26, 100), F(40, 100)

drops = set()
for c0 in (F(100), F(37), F(253, 7)):           # 任取几个原进价，结果应与赋值无关
    price = c0 * (1 + R0)
    # 在原进价的万分之一精度上穷举新进价
    news = [c0 * F(k, 10000) for k in range(1, 10000) if (price - c0 * F(k, 10000)) / (c0 * F(k, 10000)) == R1]
    assert len(news) == 1
    drops.add(1 - news[0] / c0)
assert len(drops) == 1
drop = drops.pop()

# 选项（百分数；"约"表示保留一位小数）
OPTS = {'A': ('', F(10)), 'B': ('约', F('11.1')), 'C': ('', F(14)), 'D': ('约', F('18.9'))}


def match(opt, true_pct):
    approx, v = opt
    return abs(true_pct - v) < F(5, 100) if approx else true_pct == v


hits = [L for L, o in OPTS.items() if match(o, drop * 100)]
assert len(hits) == 1, hits

# 干扰项来源核对
assert match(OPTS['B'], ((1 + R1) / (1 + R0) - 1) * 100)     # 比值倒过来
assert match(OPTS['C'], (R1 - R0) * 100)                      # 百分点直接相减
assert match(OPTS['D'], ((1 - R0) - (1 - R1)) / (1 - R0) * 100)  # 利润率误作"利润占售价"

print('drop', drop)
print(hits[0])
