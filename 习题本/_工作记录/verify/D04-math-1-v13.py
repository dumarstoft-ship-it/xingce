# D04-math-1-v13  营业收入+20%、营业支出+12%、营业利润(=收入-支出)+50%，
# 求去年营业支出是营业利润的多少倍
from fractions import Fraction as F

GR, GE, GP = F(20, 100), F(12, 100), F(50, 100)

ratios = set()
for P in (F(100), F(800), F(37, 3)):        # 任取去年利润，结果应与赋值无关
    # 在 P 的百分之一精度上穷举去年支出 E（0~100P）
    sols = [F(t, 100) * P for t in range(1, 10001)
            if (1 + GR) * (F(t, 100) * P + P) - (1 + GE) * (F(t, 100) * P) == (1 + GP) * P]
    assert len(sols) == 1
    ratios.add(sols[0] / P)
assert len(ratios) == 1
k = ratios.pop()

OPTS = {'A': ('约', F('0.27')), 'B': ('', F('3.75')), 'C': ('', F('4.75')), 'D': ('', F('6.25'))}


def match(opt, v):
    approx, x = opt
    return abs(v - x) < F(5, 1000) if approx else v == x


hits = [L for L, o in OPTS.items() if match(o, k)]
assert len(hits) == 1, hits

# 线段法核对：支出∶利润 = (50%-20%)∶(20%-12%)
assert (GP - GR) / (GR - GE) == k
# 干扰项来源核对
assert match(OPTS['A'], (GR - GE) / (GP - GR))     # 比例放反
assert match(OPTS['C'], k + 1)                     # 收入∶利润（答非所问）
assert match(OPTS['D'], GP / (GR - GE))            # 代入时漏掉0.2P：0.08E=0.5P

print('E/P =', k)
print(hits[0])
