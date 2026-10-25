# T092 2022国考副省级72：日产量降10%，能耗成本降50%，日利润增10%，出厂价=3×原单利，求原能耗/其他成本
from fractions import Fraction as F

QTY, ENERGY, DAILY = F(9, 10), F(1, 2), F(11, 10)
PRICE_MULT = 3

def classify(x):
    if x < F(1, 4):
        return 'A'
    if x < F(1, 3):
        return 'B'
    if x < F(1, 2):
        return 'C'
    return 'D'

# 枚举整数成本结构：出厂价P、能耗E、其他O（单利u=P-E-O），检验全部条件
ratios = set()
for u in range(1, 61):
    P = PRICE_MULT * u
    for E in range(1, P):
        O = P - u - E
        if O <= 0:
            continue
        u_new = P - E * ENERGY - O
        if QTY * u_new == DAILY * u:      # 日利润=日产量×单利
            ratios.add(F(E, O))
assert len(ratios) == 1, ratios
r = ratios.pop()
print('energy/other =', r, float(r))
print(classify(r))
