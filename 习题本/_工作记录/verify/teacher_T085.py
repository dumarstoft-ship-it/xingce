# T085 2017上海：50%溶液倒出1/4，用20%溶液补满，重复3次后浓度约为？
from fractions import Fraction as F

C0, C_ADD, POUR, TIMES = F(50, 100), F(20, 100), F(1, 4), 3
OPTS = {'A': F(327, 1000), 'B': F(303, 1000), 'C': F(270, 1000), 'D': F(294, 1000)}

V = F(1)                       # 容器容量
salt = C0 * V
for _ in range(TIMES):
    salt = salt * (1 - POUR)   # 倒出1/4，溶质按比例减少
    salt += C_ADD * POUR * V   # 补入1/4容量的20%溶液
c = salt / V
# 降维写法核对：与补入浓度的差距每次乘3/4
assert c == C_ADD + (C0 - C_ADD) * (1 - POUR) ** TIMES
best = min(OPTS, key=lambda k: abs(OPTS[k] - c))
assert abs(OPTS[best] - c) < F(1, 1000)
print('concentration =', float(c))
print(best)
