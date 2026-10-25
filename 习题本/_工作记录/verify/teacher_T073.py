# 验算 T073：甲 200 天、乙 300 天，合作 60 天后甲调离，乙完成剩余，共需多少天
import sys
from fractions import Fraction as F
a, b = F(1, 200), F(1, 300)
together = 60
N = (1 - a * together) / b          # 乙从头干到尾，乙的天数 = 总天数
assert N > together
options = {'A': 120, 'B': 150, 'C': 180, 'D': 210}
ans = [k for k, v in options.items() if v == N]
assert len(ans) == 1
print(f'总天数={N}', file=sys.stderr)
print(ans[0])
