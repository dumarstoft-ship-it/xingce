# real 2026GD-36  风电占40%，光伏占35%，其余为生物质能；光伏比生物质能多120兆瓦。求新能源总装机容量。
from fractions import Fraction as F
OPTS = {'A': 600, 'B': 800, 'C': 1000, 'D': 1200}
WIND, PV, DIFF = F(40, 100), F(35, 100), 120
bio = 1 - WIND - PV
# 以1兆瓦为步长穷举总装机容量
sols = [T for T in range(1, 100001) if (PV - bio) * T == DIFF]
assert len(sols) == 1, sols
T = sols[0]
hits = [k for k, v in OPTS.items() if v == T]
assert len(hits) == 1, hits
assert DIFF / (WIND - bio) == OPTS['B']   # 把120兆瓦错配到风电与生物质能之差
print('bio share', bio, 'total', T)
print(hits[0])
