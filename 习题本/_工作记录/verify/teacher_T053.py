# 验算 T053：环湖相向，19:25 相遇，19:45 甲到 B，20:05 再相遇，求乙一圈用时
import sys
from fractions import Fraction as F
t1, tB, t2 = 25, 45, 65          # 以 19:00 为 0
vj = F(1)                        # 甲速取 1
d_AB = vj * tB                   # 甲从 A 到 B（相向这一侧）的路程
vy = d_AB / t1 - vj              # 第一次相遇：t1*(vj+vy) = d_AB
lap = t2 * (vj + vy) - d_AB      # 第二次相遇：合走 d_AB + 一圈
assert lap > d_AB
T_yi = lap / vy
options = {'A': 72, 'B': 81, 'C': 90, 'D': 100}
ans = [k for k, v in options.items() if v == T_yi]
assert len(ans) == 1
print(f'乙速={vy}，一圈={lap}，乙一圈用时={T_yi}', file=sys.stderr)
print(ans[0])
