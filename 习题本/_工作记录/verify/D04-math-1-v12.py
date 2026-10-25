# D04-math-1-v12  富硒稻：亩产-10%、单价+50%、每亩成本+20%；普通稻每亩利润=成本的50%；
# 富硒稻每亩利润比普通稻高百分之几
from fractions import Fraction as F

Y, P, C = F(-10, 100), F(50, 100), F(20, 100)
PROFIT_SHARE = F(50, 100)

incs = set()
for cost0, yield0 in ((F(100), F(1000)), (F(800), F(1250)), (F(37), F(3))):   # 赋值与结果无关
    profit0 = cost0 * PROFIT_SHARE
    rev0 = cost0 + profit0
    price0 = rev0 / yield0
    rev1 = yield0 * (1 + Y) * price0 * (1 + P)
    cost1 = cost0 * (1 + C)
    incs.add(((rev1 - cost1) - profit0) / profit0)
assert len(incs) == 1
inc = incs.pop()

OPTS = {'A': F(15), 'B': F('32.5'), 'C': F(35), 'D': F(65)}   # 百分数
hits = [L for L, v in OPTS.items() if v == inc * 100]
assert len(hits) == 1, hits

# 干扰项来源核对（赋值普通稻成本100）
rev_growth = (1 + Y) * (1 + P) - 1
assert (rev_growth - C) * 100 == OPTS['A']                        # 收入增幅-成本增幅
assert ((150 * (1 + Y) * (1 + P) - 120) - 50) / 100 * 100 == OPTS['B']   # 增加额误以成本为基数
assert rev_growth * 100 == OPTS['C']                              # 只看收入增幅

print('inc', inc)
print(hits[0])
