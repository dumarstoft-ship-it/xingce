# T096 2015江苏B：甲乙合作按期完成；甲效率+1/3、乙+1/2则用5/7工期；乙效率-1/4则推迟2天，求原工期
from fractions import Fraction as F

UP_A, UP_B, TIME_FR, DOWN_B, DELAY = F(1, 3), F(1, 2), F(5, 7), F(1, 4), 2
OPTS = {'A': 10, 'B': 12, 'C': 16, 'D': 18}

sols = set()
for a in range(1, 31):           # 甲、乙效率取小整数枚举（只有比值有意义）
    for b in range(1, 31):
        for T in range(1, 201):
            W = (a + b) * T
            ok2 = (a * (1 + UP_A) + b * (1 + UP_B)) * TIME_FR * T == W
            ok3 = (a + b * (1 - DOWN_B)) * (T + DELAY) == W
            if ok2 and ok3:
                sols.add((F(a, b), T))
Ts = {T for _, T in sols}
assert len(Ts) == 1, sols
T = Ts.pop()
print('A:B efficiency =', {r for r, _ in sols}, 'original days =', T)
print([k for k, v in OPTS.items() if v == T][0])
