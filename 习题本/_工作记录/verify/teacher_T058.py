# 验算 T058：12 时 30 分时针与分针夹角
import sys
from fractions import Fraction as F
h, m = 12, 30
t = (h % 12) * 60 + m          # 距 12:00 的分钟数
hour = (F(1, 2) * t) % 360     # 时针 0.5°/分
minute = (6 * t) % 360         # 分针 6°/分
ang = abs(minute - hour)
ang = min(ang, 360 - ang)
options = {'A': 165, 'B': 155, 'C': 150, 'D': 145}
ans = [k for k, v in options.items() if v == ang]
assert len(ans) == 1
print(f'时针={hour}°，分针={minute}°，夹角={ang}°', file=sys.stderr)
print(ans[0])
