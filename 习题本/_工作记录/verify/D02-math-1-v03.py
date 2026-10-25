# D02-math-1-v03  6000户，每天比原计划多核查20%可提前4天完成，求原计划每天核查户数
from fractions import Fraction as F
TOTAL, UP, EARLY = 6000, F(20, 100), 4
OPTS = {'A': 250, 'B': 300, 'C': 360, 'D': 375}

sols = []
for T in range(EARLY + 1, 2000):          # 原计划天数
    v = F(TOTAL, T)                        # 原计划每天户数
    if F(TOTAL) / (v * (1 + UP)) == T - EARLY:
        sols.append((T, v))
assert len(sols) == 1, sols
T, v = sols[0]
hits = [k for k, x in OPTS.items() if x == v]
assert len(hits) == 1, hits

# 干扰项来源核对
T_wrong = next(t for t in range(1, 2000) if F(t) * UP == EARLY)   # 误当“时间缩短20%”
assert F(TOTAL, T_wrong) == OPTS['B'] == v * (1 + UP)             # 也正是提效后的日核查量
assert OPTS['B'] * (1 + UP) == OPTS['C']                          # 由300反推时乘了1.2
assert F(TOTAL, EARLY * 4) == OPTS['D']                           # 误记“缩短1/(n-1)”→16天
print('T', T, 'v', v)
print(hits[0])
