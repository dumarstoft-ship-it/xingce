# 验算 T041：60km/h 起匀加速，50 秒行驶 1 公里，求加速到 120km/h 的时间
import sys
from fractions import Fraction as F
v0 = F(60 * 1000, 3600)     # m/s
vmax = F(120 * 1000, 3600)
t, s = 50, 1000
a = (s - v0 * t) * 2 / (t * t)   # s = v0 t + a t^2 / 2
need = (vmax - v0) / a
options = {'A': 100, 'B': 125, 'C': 150, 'D': 180}
ans = [k for k, v in options.items() if v == need]
assert len(ans) == 1
print(f'a={a} m/s^2, 用时={need} 秒', file=sys.stderr)
print(ans[0])
