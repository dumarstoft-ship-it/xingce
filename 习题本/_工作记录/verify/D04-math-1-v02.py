# D04-math-1-v02  转手链：甲盈20%卖给乙，乙亏10%卖给丙，丙付540元，求甲乙合计盈亏
from fractions import Fraction as F

FINAL = F(540)
JIA_UP = F(20, 100)    # 甲按自己的买入价获利20%
YI_DOWN = F(10, 100)   # 乙按自己的买入价亏损10%

# 逐级还原
yi_cost = FINAL / (1 - YI_DOWN)        # 乙的买入价 = 甲的卖出价
jia_cost = yi_cost / (1 + JIA_UP)      # 甲的买入价
assert jia_cost * (1 + JIA_UP) == yi_cost and yi_cost * (1 - YI_DOWN) == FINAL
jia_pl = yi_cost - jia_cost
yi_pl = FINAL - yi_cost
total = jia_pl + yi_pl
assert total == FINAL - jia_cost       # 整体法

# 选项：(方向, 金额)；盈利记正、亏损记负
OPTS = {'A': ('盈利', 40), 'B': ('盈利', 45), 'C': ('盈利', 50), 'D': ('盈利', 60)}


def val(o):
    return F(o[1]) if o[0] == '盈利' else -F(o[1])


hits = [L for L, o in OPTS.items() if val(o) == total]
assert len(hits) == 1, hits

# 干扰项来源核对
w_yi = FINAL * (1 + YI_DOWN)                         # 反求乙成本误用乘法 594
assert FINAL - w_yi / (1 + JIA_UP) == val(OPTS['B'])  # 495 -> 盈利45
assert jia_cost * (JIA_UP - YI_DOWN) == val(OPTS['C'])  # 500*10% = 50
w_jia = yi_cost * (1 - JIA_UP)                       # 反求甲成本误用 600*0.8 = 480
assert FINAL - w_jia == val(OPTS['D'])               # 盈利60

print('jia_cost', jia_cost, 'yi_cost', yi_cost, 'jia', jia_pl, 'yi', yi_pl, 'total', total)
print(hits[0])
