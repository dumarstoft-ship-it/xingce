# D04-math-2-v08 阶梯电价：两月合计电费与用电差，求7月用电量
from fractions import Fraction as F
tiers = [(200, F(60, 100)), (400, F(65, 100)), (None, F(90, 100))]
def fee(u):
    u = F(u); total = F(0); lo = 0
    for hi, pr in tiers:
        if hi is None or u <= hi:
            total += (u - lo) * pr
            return total
        total += (hi - lo) * pr
        lo = hi
S, D = 453, 120
sols = [u for u in range(0, 2001) if fee(u) + fee(u + D) == S]
assert len(sols) == 1, sols
# 严格单调 => 实数解唯一
assert all(fee(u + 1) + fee(u + 1 + D) > fee(u) + fee(u + D) for u in range(0, 2000))
july = sols[0]
both_mid = (S + 20 - F(65, 100) * D) / F(130, 100)   # 误设两月都在第二档
print('july =', july, 'aug =', july + D, 'both-tier2 july ~', float(both_mid))
options = {'A': 280, 'B': 300, 'C': 304, 'D': 420}
hits = [k for k, v in options.items() if v == july]
assert len(hits) == 1, hits
print(hits[0])
