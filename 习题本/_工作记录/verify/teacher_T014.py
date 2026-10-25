# teacher_T014  甲路程比乙多1/3，乙时间比甲多1/4，求甲、乙速度比
from fractions import Fraction as F

OPTS = {'A': F(3, 5), 'B': F(16, 15), 'C': F(5, 3), 'D': F(16, 9)}
s_yi, t_jia = F(1), F(1)                 # 以乙的路程、甲的时间为基准
s_jia = s_yi * (1 + F(1, 3))
t_yi = t_jia * (1 + F(1, 4))
ans = (s_jia / t_jia) / (s_yi / t_yi)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert OPTS['B'] == (s_jia * t_jia) / (s_yi * t_yi)                   # 路程比×时间比
assert OPTS['D'] == (s_jia / (1 - F(1, 4))) / (s_yi / 1)              # 时间基准弄反：甲比乙少1/4
assert OPTS['A'] == 1 / ans
print('v甲:v乙 =', ans)
print(hits[0])
