# 验算 T040：途中故障，骑车往返中点借工具 + 修车 30 分钟，求故障时刻
import sys
from sympy import symbols, Eq, solve, Rational
t = symbols('t')            # 故障时刻：8:00 后 t 分钟
v = 1                        # 汽车速度：每分钟 1 份路程
plan = 120                   # 8:00—10:00
mid = Rational(plan, 2) * v  # 中点位置
bike = Rational(1, 4) * v
repair = 30
arrive = (11 * 60 + 50) - 8 * 60   # 11:50 距 8:00 的分钟数
# 故障点在中点之前（不到1小时），骑车到中点再骑回，修好后继续开到 B
total = t + 2 * (mid - v * t) / bike + repair + (plan - t)
sol = solve(Eq(total, arrive), t)
assert len(sol) == 1 and 0 < sol[0] < 60
tt = sol[0]
hh, mm = 8 + int(tt) // 60, tt % 60
options = {'A': (8, 40), 'B': (8, 45), 'C': (8, 50), 'D': (8, 55)}
ans = [k for k, (h, m) in options.items() if h == hh and m == mm]
assert len(ans) == 1
print(f'故障时刻 {hh}:{mm}', file=sys.stderr)
print(ans[0])
