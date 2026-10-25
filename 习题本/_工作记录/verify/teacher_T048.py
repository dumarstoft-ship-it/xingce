# 验算 T048：出租车往返 100 分钟；小明 8:00 步行，出租 9:00 出发，接到后回乙地 10:20 到；求车速/步速
import sys
from sympy import symbols, Eq, solve, Rational
w, c, tm = symbols('w c tm', positive=True)   # 步速、车速、相遇时刻（8:00 后分钟）
D = Rational(100, 2) * c   # 往返 100 分钟 → 单程 50 分钟车程
taxi_start, arrive = 60, 140
sol = solve([Eq(w * tm + c * (tm - taxi_start), D),
             Eq(tm + (tm - taxi_start), arrive)], [w, tm], dict=True)
assert len(sol) == 1
ratio = (c / sol[0][w]).simplify()
options = {'A': 4, 'B': 6, 'C': 8, 'D': 10}
ans = [k for k, v in options.items() if v == ratio]
assert len(ans) == 1
print(f'相遇时刻=8:00后{sol[0][tm]}分，倍数={ratio}', file=sys.stderr)
print(ans[0])
