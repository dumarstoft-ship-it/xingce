# 验算 T045：A→B 下坡，C 为中点，返程提速 1 米/秒，求 AB 距离范围
import sys
from sympy import symbols, Eq, solve, Rational
vd, vu = symbols('vd vu', positive=True)   # 千米/时
t_AC = 7 - 6                 # 6:00→7:00
t_CB = t_AC                  # 同速同距
arrive_B = 6 + t_AC + t_CB   # 8:00
t_BC = 10 - arrive_B         # 上坡 B→C
t_CA = Rational(23, 2) - 10  # 10:00→11:30，提速后 C→A
inc = Rational(36, 10)       # 1 米/秒 = 3.6 千米/时
sol = solve([Eq(vd * t_AC, vu * t_BC), Eq(vd * t_AC, (vu + inc) * t_CA)], [vd, vu], dict=True)
assert len(sol) == 1
AB = 2 * sol[0][vd] * t_AC
if AB < 30:
    letter = 'C'
elif AB <= 40:
    letter = 'D'
elif AB <= 50:
    letter = 'A'
else:
    letter = 'B'
print(f'下坡={sol[0][vd]}km/h，上坡={sol[0][vu]}km/h，AB={AB}km', file=sys.stderr)
print(letter)
