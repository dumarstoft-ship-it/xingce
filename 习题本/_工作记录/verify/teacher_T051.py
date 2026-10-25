# 验算 T051：货车、客车同向，车尾平齐到车头平齐 20 秒，求客车长
import sys
from fractions import Fraction as F
vf, vp = F(72 * 1000, 3600), F(108 * 1000, 3600)   # m/s
k, t = F(3, 2), 20      # 货车长 = 1.5 × 客车长
# 车尾平齐时：货车头在 k*Lp，客车头在 Lp；t 秒后车头平齐：k*Lp + vf*t = Lp + vp*t
Lp = (vp - vf) * t / (k - 1)
assert k * Lp + vf * t == Lp + vp * t
options = {'A': 160, 'B': 240, 'C': 400, 'D': 600}
ans = [kk for kk, v in options.items() if v == Lp]
assert len(ans) == 1
print(f'客车长={Lp}m，货车长={k*Lp}m', file=sys.stderr)
print(ans[0])
