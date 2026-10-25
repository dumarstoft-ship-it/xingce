# 验算 T044：甲→乙下坡、乙→丙上坡，上坡速度为下坡 60%，甲乙段用时为去程一半；比较返程与去程用时
import sys
from fractions import Fraction as F
down = F(1)
up = F(60, 100) * down
t12 = t23 = F(1)          # 甲→乙用时 = 去程一半 → 两段用时相等
d12 = down * t12          # 甲乙段（去程下坡）
d23 = up * t23            # 乙丙段（去程上坡）
go = t12 + t23
back = d23 / down + d12 / up   # 返程：丙→乙下坡，乙→甲上坡
change = (back - go) / go
if change < 0:
    letter = 'A' if -change < F(1, 10) else 'B'
else:
    letter = 'C' if change < F(1, 10) else 'D'
print(f'去程={go}，返程={back}，变化={change}={float(change):.4f}', file=sys.stderr)
print(letter)
