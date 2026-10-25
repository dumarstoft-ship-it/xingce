# 验算 T059：24 小时内时针分针成直角的次数（逐个求出时刻并复核夹角）
import sys
from fractions import Fraction as F
def angle(t):
    hour = (F(1, 2) * t) % 360
    minute = (6 * t) % 360
    d = abs(minute - hour)
    return min(d, 360 - d)
times = set()
for target in (90, 270):            # 分针相对时针转过的角度 ≡ 90 或 270 (mod 360)
    k = 0
    while True:
        t = (target + 360 * k) / F(11, 2)
        if t >= 24 * 60:
            break
        assert angle(t) == 90
        times.add(t)
        k += 1
n = len(times)
options = {'A': 28, 'B': 36, 'C': 44, 'D': 48}
ans = [k for k, v in options.items() if v == n]
assert len(ans) == 1
print(f'直角次数={n}', file=sys.stderr)
print(ans[0])
