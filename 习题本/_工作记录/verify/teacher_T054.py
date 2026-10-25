# 验算 T054：400 米环道同起点反向跑，求再次在起点相遇的时间
import sys
from fractions import Fraction as F
L, va, vb = 400, 5, 3
t_meet = F(L, va + vb)
k = 1
while True:
    t = k * t_meet
    pa, pb = (va * t) % L, (-vb * t) % L
    assert pa == pb                     # 确为相遇
    if pa == 0:
        break
    k += 1
options = {'A': 4 * 60 + 10, 'B': 5 * 60 + 50, 'C': 6 * 60 + 40, 'D': 7 * 60 + 30}
ans = [kk for kk, v in options.items() if v == t]
assert len(ans) == 1
print(f'第{k}次相遇，t={t}s', file=sys.stderr)
print(ans[0])
