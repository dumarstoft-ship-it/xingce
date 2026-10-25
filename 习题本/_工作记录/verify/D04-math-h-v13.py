# D04-math-h-v13：年需包装箱 8000 个。外购每个 30 元；自建车间：每年固定成本 9 万元，每个变动成本 18 元，
# 年产能最多 6000 个，不足部分仍需外购。问每年在包装箱上的支出最少为多少万元。
# 做法：列出全部可行方案——不建车间全部外购；建车间自制 q 个（0～6000）、其余外购——逐一计算总支出取最小。
from fractions import Fraction as F

OPTIONS = {'A': '19.8', 'B': '23.4', 'C': '24', 'D': '25.8'}   # 单位：万元
DEMAND, BUY, FIXED, VAR, CAP = 8000, 30, 90000, 18, 6000

plans = {('buy_all', 0): DEMAND * BUY}
for q in range(0, CAP + 1):
    plans[('build', q)] = FIXED + VAR * q + BUY * (DEMAND - q)
best = min(plans.values())
best_plans = [p for p, c in plans.items() if c == best]
best_wan = F(best, 10000)

hits = [k for k, v in OPTIONS.items() if F(v) == best_wan]
assert len(hits) == 1
print('best plan(s):', best_plans, 'cost =', best, 'yuan =', float(best_wan), '万元')
print(hits[0])
