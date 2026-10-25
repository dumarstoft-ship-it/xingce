# D03-math-1-v10: 家→市场：先平路后上坡；平路20、上坡10、下坡30（千米/时）；去程36分、回程24分；求家到市场的路程
from fractions import Fraction as F

FLAT, UPH, DOWNH = 20, 10, 30
GO, BACK = F(36, 60), F(24, 60)
OPTS = {'A': F(6), 'B': F(15, 2), 'C': F(9), 'D': F(10)}

sols = set()
# 穷举平路长 a、坡路长 b（0.05千米步长，各至 30 千米）
for ia in range(1, 601):
    a = F(ia, 20)
    for ib in range(1, 601):
        b = F(ib, 20)
        if a / FLAT + b / UPH == GO and a / FLAT + b / DOWNH == BACK:   # 去程上坡，回程下坡
            sols.add((a, b))
assert len(sols) == 1, sols
a, b = sols.pop()
D = a + b
hit = [k for k, x in OPTS.items() if x == D]
assert len(hit) == 1, (D, hit)
# 干扰项来源
total = GO + BACK
assert F(UPH + DOWNH, 2) * total / 2 == OPTS['D']                # 坡路往返按算术平均20，与平路相同
H = F(2 * UPH * DOWNH, UPH + DOWNH)
assert H * total / 2 == OPTS['B']                                # 把坡路往返平均15当整段往返均速
assert a == OPTS['A']                                            # 只求出平路长就作答
print('平路', a, '坡路', b, '全程', D)
print(hit[0])
