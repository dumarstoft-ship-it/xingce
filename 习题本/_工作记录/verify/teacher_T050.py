# 验算 T050：自动人行道传包裹，小明逆行取包再返回终点，求总时间
import sys
from fractions import Fraction as F
L, belt, walk = 42, F(3, 4), 1
v_against = walk - belt          # 逆行地速
t_meet = F(L) / (belt + v_against)
meet_from_end = v_against * t_meet
t_back = meet_from_end / (walk + belt)
total = t_meet + t_back
options = {'A': 24, 'B': 42, 'C': 48, 'D': 56}
ans = [k for k, v in options.items() if v == total]
assert len(ans) == 1
print(f'取包={t_meet}s，返回={t_back}s，共{total}s', file=sys.stderr)
print(ans[0])
