# teacher_T007  合作时各自效率提高20%；合作25天完工；甲先干15天、再合作15天、乙再单独10天完工。求甲效率是乙的几倍
from fractions import Fraction as F

BOOST = F(6, 5)                 # 合作时各自效率 ×1.2
T_ALL, T_JIA, T_CO, T_YI = 25, 15, 15, 10
OPTS = {'A': F(2, 5), 'B': F(2, 3), 'C': F(1), 'D': F(3, 2)}

def gap(a, b=F(1)):
    """方案一总量 - 方案二总量（a、b 为甲、乙单独效率）"""
    return T_ALL * BOOST * (a + b) - (T_JIA * a + T_CO * BOOST * (a + b) + T_YI * b)

# gap 关于 a 是一次函数，解 gap(a)=0
g0, g1 = gap(F(0)), gap(F(1))
a = -g0 / (g1 - g0)
assert gap(a) == 0 and a > 0
hits = [k for k, v in OPTS.items() if v == a]
assert len(hits) == 1, (a, hits)
assert OPTS['D'] == 1 / a                  # 比例颠倒
assert OPTS['A'] == a / (a + 1)            # 把"甲占两队效率和的比例"当倍数
# 把"效率高20%"错当"时间少20%"（效率×1.25）时得1
BOOST_WRONG = F(5, 4)
gw = lambda x: T_ALL * BOOST_WRONG * (x + 1) - (T_JIA * x + T_CO * BOOST_WRONG * (x + 1) + T_YI)
assert -gw(F(0)) / (gw(F(1)) - gw(F(0))) == OPTS['C']
print('甲/乙 =', a)
print(hits[0])
