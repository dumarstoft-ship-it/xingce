# 验算 T064：一块每天快 30 分、一块每天慢 20 分，再次同时显示标准时间的最少天数
import sys
from fractions import Fraction as F
fast, slow, dial = 30, 20, 12 * 60
# 误差随时间连续累计，只有误差为 720 分钟整数倍时显示标准时间；t 以天为单位
cands = sorted({F(dial * i, fast) for i in range(1, 50)} & {F(dial * j, slow) for j in range(1, 50)})
n = cands[0]
options = {'A': 24, 'B': 36, 'C': 72, 'D': 114}
ans = [k for k, v in options.items() if v == n]
assert len(ans) == 1
print(f'最少天数={n}', file=sys.stderr)
print(ans[0])
