# T260 甲在丙西 17，乙在丙北 8；张向东、李向南，整数速度；1 小时后距 13，4 小时时都过丙且距 5；李速=张速×60%
from fractions import Fraction as F
import math
sols = []
for vz in range(1, 60):
    for vl in range(1, 60):
        if F(vl) != F(3, 5) * vz:
            continue
        d1 = (17 - vz)**2 + (8 - vl)**2
        x4, y4 = 4 * vz - 17, 4 * vl - 8          # 4 小时后各自越过丙地的距离
        if d1 == 169 and x4 > 0 and y4 > 0 and x4**2 + y4**2 == 25:
            sols.append((vz, vl))
assert len(sols) == 1, sols
vz, vl = sols[0]
diff_min = (F(17, vz) - F(8, vl)) * 60          # 张到丙时刻 - 李到丙时刻（分钟）
# 选项：A 早不到10分钟 B 早10分钟以上 C 晚不到10分钟 D 晚10分钟以上
if diff_min < 0:
    ans = "A" if -diff_min < 10 else "B"
else:
    ans = "C" if diff_min < 10 else "D"
print(ans)
