# teacher_T033  牧草匀速生长：100头牛吃20天，150头牛吃10天，250头牛吃几天
from fractions import Fraction as F

(N1, D1), (N2, D2), N3 = (100, 20), (150, 10), 250
OPTS = {'A': 5, 'B': 6, 'C': 7, 'D': 8}
# 原有草量 G = (N - g) * D，两式相等解 g（每天新长草可供 g 头牛）
g = F(N1 * D1 - N2 * D2, D1 - D2)
G = (N1 - g) * D1
assert G == (N2 - g) * D2 and G > 0
days = G / (N3 - g)
hits = [k for k, v in OPTS.items() if v == days]
assert len(hits) == 1, (days, hits)
assert OPTS['D'] == F(N1 * D1, N3)       # 忘了草在生长
print('g =', g, ' G =', G, ' 天数 =', days)
print(hits[0])
