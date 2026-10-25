# T099 2023国考副省级74：三企业2021年收入和增20%；甲+400，乙-100且为甲的一半；丙+30%且2020年=甲+乙
from fractions import Fraction as F

TOTAL_UP, A_UP, B_DOWN, C_UP = F(20, 100), 400, 100, F(30, 100)
OPTS = {'A': 900, 'B': 1100, 'C': 400, 'D': 600}

sols = []
for a in range(1, 10001):              # 2020年甲收入（万元）
    b2021 = F(a + A_UP, 2)              # 2021年乙是甲的一半
    b = b2021 + B_DOWN
    c = a + b
    if (a + A_UP) + b2021 + c * (1 + C_UP) == (a + b + c) * (1 + TOTAL_UP):
        sols.append((a, b))
assert len(sols) == 1, sols
a, b = sols[0]
diff = a - b
hits = [k for k, v in OPTS.items() if v == diff]
assert len(hits) == 1, (diff, hits)
assert (a + A_UP) - (b - B_DOWN) == OPTS['B']     # 干扰项：求成2021年的差
print('2020: A =', a, 'B =', b)
print(hits[0])
