# 验算 T047：10:00 相向出发，10:30 相遇，10:54 甲到乙单位后原速返回；求甲回到单位时乙已到多久
import sys
from fractions import Fraction as F
D = F(1)
t_meet, t_jia_full = 30, 54
v_jia = D / t_jia_full
v_yi = D / t_meet - v_jia
t_yi_full = D / v_yi
diff = 2 * t_jia_full - t_yi_full     # 分钟
options = {'A': F(42), 'B': F(40) + F(30, 60), 'C': F(43) + F(30, 60), 'D': F(45)}
ans = [k for k, v in options.items() if v == diff]
assert len(ans) == 1
print(f'乙全程={t_yi_full}分，差={diff}分', file=sys.stderr)
print(ans[0])
