# 验算 T079：前轮 3 万公里、后轮 4 万公里报废，中途前后交换使四胎同时报废，求交换里程
import sys
from sympy import symbols, Eq, solve, Rational
x, D = symbols('x D', positive=True)   # 交换时里程、总里程（万公里）
front, rear = 3, 4
sol = solve([Eq(x / front + (D - x) / rear, 1),     # 先前后后的轮胎
             Eq(x / rear + (D - x) / front, 1)],    # 先后后前的轮胎
            [x, D], dict=True)
assert len(sol) == 1
xv = sol[0][x]
options = {'A': Rational(15, 10), 'B': Rational(17, 10), 'C': 2, 'D': Rational(22, 10)}
best = min(options, key=lambda k: abs(options[k] - xv))
print(f'交换里程={xv}≈{float(xv):.3f}万公里，总里程={sol[0][D]}', file=sys.stderr)
print(best)
