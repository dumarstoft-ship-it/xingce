# 验算 T062：7 点多成 90° 出门、12 点多成 90° 回家，外出期间成 180° 至多几次
import sys
from fractions import Fraction as F
def times_with(target, lo, hi):
    res, k = [], 0
    while True:
        t = (target + 360 * k) / F(11, 2)    # 分针领先时针 target 度（mod 360）
        if t >= hi:
            return res
        if t >= lo:
            res.append(t)
        k += 1
dep = times_with(90, 420, 480) + times_with(270, 420, 480)    # 7 点多（分钟，从 0:00 起）
ret = times_with(90, 720, 780) + times_with(270, 720, 780)    # 12 点多
opp = times_with(180, 0, 24 * 60)
best = max(sum(1 for t in opp if d < t < r) for d in dep for r in ret)
options = {'A': 4, 'B': 5, 'C': 6, 'D': 7}
ans = [k for k, v in options.items() if v == best]
assert len(ans) == 1
print(f'出门候选={[str(x) for x in dep]}，回家候选={[str(x) for x in ret]}，至多{best}次', file=sys.stderr)
print(ans[0])
