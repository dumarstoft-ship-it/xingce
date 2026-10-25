# real 2026GD-38  蓄电池可供20台运行5天；运行12小时后新增5台；还可运行几天
from fractions import Fraction as F
OPTS = {'A': F(35, 10), 'B': F(36, 10), 'C': F(38, 10), 'D': F(4)}
TOTAL = 20 * 5 * 24                       # 以“台·小时”计的总电量
used = 20 * 12                            # 前12小时20台
ans = F(TOTAL - used, 25) / 24            # 25台还能运行的天数
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)

# 以6分钟（0.1小时）为步长逐段模拟复核
e, steps = F(TOTAL - used), 0
while e > 0:
    e -= 25 * F(1, 10)
    steps += 1
assert e == 0 and F(steps, 10) / 24 == ans

# 干扰项来源核对
assert F(20 * 5, 25) == OPTS['D']                    # 忘了已运行的12小时
assert F(20 * 5 - 25 * F(1, 2), 25) == OPTS['A']     # 前12小时也按25台计算
print('remaining days', ans)
print(hits[0])
