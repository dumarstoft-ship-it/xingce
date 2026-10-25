# 验算 T052：过隧道 33 秒、与对向列车错车 3 秒，减速一半过 600 米桥
import sys
from sympy import symbols, Eq, solve
s, v = symbols('s v', positive=True)
sol = solve([Eq((s + 1200) / v, 33), Eq((s + 150) / (v + 50), 3)], [s, v], dict=True)
assert len(sol) == 1
t = (sol[0][s] + 600) / (sol[0][v] / 2)
options = {'A': 18, 'B': 20, 'C': 30, 'D': 36}
ans = [k for k, val in options.items() if val == t]
assert len(ans) == 1
print(f'车长={sol[0][s]}，车速={sol[0][v]}，过桥={t}s', file=sys.stderr)
print(ans[0])
