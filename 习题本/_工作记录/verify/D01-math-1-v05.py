# D01-math-1-v05  四市新增充电桩：深圳是广州的1.25倍、东莞的2倍、佛山的2.5倍；广州比佛山多200个。求四市共新增多少个。
from fractions import Fraction as F

M_GZ, M_DG, M_FS, DIFF = F(5, 4), F(2), F(5, 2), 200
OPTS = {'A': 850, 'B': 900, 'C': 1350, 'D': 1800}

# 穷举深圳新增数s，其余三市由倍数关系确定且须为正整数
sols = []
for s in range(1, 200001):
    gz, dg, fs = F(s) / M_GZ, F(s) / M_DG, F(s) / M_FS
    if any(v.denominator != 1 for v in (gz, dg, fs)):
        continue
    if gz - fs == DIFF:
        sols.append((s, int(gz), int(dg), int(fs)))
assert len(sols) == 1, sols
total = sum(sols[0])
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits

# 干扰项来源核对（以深圳为1，其余城市所占比例）
share = 1 + 1 / M_GZ + 1 / M_DG + 1 / M_FS                        # 共2.7
s_swap = DIFF / (1 / M_GZ - 1 / M_DG)                              # 东莞、佛山的倍数对调：广州−佛山变成0.8−0.5
assert s_swap * share == OPTS['D']
s_pair = DIFF / (1 - 1 / M_FS)                                     # 把200当成深圳与佛山之差
assert s_pair * share == OPTS['B']
assert total - sols[0][0] == OPTS['A']                              # 漏加深圳
print('SZ GZ DG FS', sols[0], 'total', total)
print(hits[0])
