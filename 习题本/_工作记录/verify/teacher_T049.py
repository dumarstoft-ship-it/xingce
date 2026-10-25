# 验算 T049：流水行船，两人各从一端出发到某点后返回，返回起点用时相同，求该点距 A
import sys
from fractions import Fraction as F
L, water, t = 600, F(5, 2), 40
v_yi_up = F(L, t)          # 乙 A→B 逆水
v_jia_down = F(L, t)       # 甲 B→A 顺水
still_yi = v_yi_up + water
still_jia = v_jia_down - water
jia_up, jia_down = still_jia - water, still_jia + water   # 甲从 A 逆水出发，顺水返回
yi_down, yi_up = still_yi + water, still_yi - water       # 乙从 B 顺水出发，逆水返回
a = 1 / jia_up + 1 / jia_down
b = 1 / yi_down + 1 / yi_up
x = b * L / (a + b)        # x*a = (L-x)*b
assert x * a == (L - x) * b
options = {'A': 240, 'B': 247, 'C': 254, 'D': 260}
best = min(options, key=lambda k: abs(options[k] - x))
print(f'x={x}≈{float(x):.2f}', file=sys.stderr)
print(best)
