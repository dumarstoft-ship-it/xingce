# D03-math-1-v07: 往返全程平均速度比去程快20%，返程比去程快百分之几
from fractions import Fraction as F

UP = F(20, 100)
OPTS = {'A': F(25), 'B': F(40), 'C': F(44), 'D': F(50)}

pcts = set()
# 穷举去程速度 v（1~120）与返程速度 w（0.5步长至360）、单程路程 s（1~50），用总路程÷总时间检验
for v in range(1, 121):
    for w2 in range(1, 721):
        w = F(w2, 2)
        for s in (1, 7, 30):                     # 平均速度与路程无关，抽几个路程复核
            avg = F(2 * s) / (F(s) / v + s / w)
            if avg != v * (1 + UP):
                break
        else:
            pcts.add((w - v) / v * 100)
assert len(pcts) == 1, pcts
ans = pcts.pop()
hit = [k for k, x in OPTS.items() if x == ans]
assert len(hit) == 1, (ans, hit)
# 干扰项来源（去程速度取 1）
assert (2 * (1 + UP) - 1 - 1) * 100 == OPTS['B']        # 算术平均
assert ((1 + UP) ** 2 - 1) * 100 == OPTS['C']           # 几何平均
assert (1 / (1 - UP) - 1) * 100 == OPTS['A']            # 当成返程用时少20%
print('return faster by', ans, '%')
print(hit[0])
