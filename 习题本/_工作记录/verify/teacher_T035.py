# teacher_T035  草地5、15、24亩，每亩草量与长速相同；5亩供10头牛30天，15亩供28头牛45天。24亩供多少头牛吃80天
from fractions import Fraction as F

(A1, N1, D1), (A2, N2, D2), (A3, D3) = (5, 10, 30), (15, 28, 45), (24, 80)
OPTS = {'A': 38, 'B': 42, 'C': 45, 'D': 48}
# 每亩原有草量 G、每亩每天长草 g（单位：头牛·天），A*G + A*g*D = N*D
# 两式联立：G + g*D1 = N1*D1/A1 ， G + g*D2 = N2*D2/A2
e1, e2 = F(N1 * D1, A1), F(N2 * D2, A2)
g = (e2 - e1) / (D2 - D1)
G = e1 - g * D1
assert G > 0 and g > 0
cows = (A3 * G + A3 * g * D3) / D3
hits = [k for k, v in OPTS.items() if v == cows]
assert len(hits) == 1, (cows, hits)
assert int(A3 * g) == OPTS['A']                       # 只算吃新草的38.4头
assert F(N1 * A3, A1) == OPTS['D']                   # 按面积直接放大第一块
assert round(F(N2 * A3, A2)) == OPTS['C']            # 按面积直接放大第二块（44.8）
print('每亩原草 =', G, ' 每亩日长 =', g, ' 牛数 =', cows)
print(hits[0])
