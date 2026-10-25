# 验算 T061：4 点半之后时针与分针第一次成直线（180°；若含重合 0° 也一并比较）
import sys
from fractions import Fraction as F
start = 4 * 60 + 30
rel = lambda t: (F(11, 2) * t) % 360       # 分针领先时针的角度
r0 = rel(start)
cands = []
for target in (180, 0):
    need = (target - r0) % 360
    if need == 0:
        need = 360
    cands.append(start + need / F(11, 2))
t = min(cands)
options = {'A': 4 * 60 + 40, 'B': 4 * 60 + 45 + F(4, 11), 'C': 4 * 60 + 54 + F(6, 11), 'D': 4 * 60 + 57}
ans = [k for k, v in options.items() if v == t]
assert len(ans) == 1
print(f'起始领先{r0}°，时刻={t // 60}:{t % 60}', file=sys.stderr)
print(ans[0])
