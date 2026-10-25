# T087 2019河北县级：300克95%酒精与若干60%酒精混合成75%，求60%酒精质量
from fractions import Fraction as F

M1, C1, C2, CM = F(300), F(95, 100), F(60, 100), F(75, 100)
OPTS = {'A': 225, 'B': 240, 'C': 380, 'D': 400}

sols = [x for x in range(0, 5001) if (M1 * C1 + x * C2) == CM * (M1 + x)]
assert len(sols) == 1
x = sols[0]
hits = [k for k, v in OPTS.items() if v == x]
assert len(hits) == 1, (x, hits)
assert M1 * (CM - C2) / (C1 - CM) == OPTS['A']   # 干扰项：比例对应反了
print('mass of 60% =', x)
print(hits[0])
