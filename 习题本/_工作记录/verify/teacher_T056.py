# 验算 T056：100 米水池两端相向往返，12 分钟内相遇次数（逐段精确模拟，含追及）
import sys
from fractions import Fraction as F
L = 100
v1, v2 = F(100, 72), F(100, 60)
T = 12 * 60
def pos(v, t, start):
    r = (v * t) % (2 * L)
    x = r if r <= L else 2 * L - r
    return x if start == 0 else L - x
bps = {F(0), F(T)}
for v in (v1, v2):
    k = 0
    while k * L / v <= T:
        bps.add(k * L / v)
        k += 1
bps = sorted(bps)
meets = set()
for a, b in zip(bps, bps[1:]):
    da = pos(v1, a, 0) - pos(v2, a, L)
    db = pos(v1, b, 0) - pos(v2, b, L)
    if da == 0:
        meets.add(a)
    if db == 0:
        meets.add(b)
    if da != db:
        tt = a + (b - a) * da / (da - db)
        if a < tt < b:
            meets.add(tt)
meets = sorted(t for t in meets if 0 < t <= T)
# 对照"迎面相遇时间比 1:3:5…"的结论
first = F(L) / (v1 + v2)
headon = [(2 * k - 1) * first for k in range(1, 100) if (2 * k - 1) * first <= T]
assert set(headon) <= set(meets)
options = {'A': 9, 'B': 10, 'C': 11, 'D': 12}
ans = [k for k, v in options.items() if v == len(meets)]
assert len(ans) == 1
print(f'相遇时刻={[str(t) for t in meets]}，共{len(meets)}次', file=sys.stderr)
print(ans[0])
