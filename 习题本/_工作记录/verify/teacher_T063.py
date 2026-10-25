# 验算 T063：每小时慢 2 分钟的表，11:50 校准，表走到次日 12:00 时的标准时间
import sys
from fractions import Fraction as F
watch_per_std_hour = 60 - 2           # 标准时间 60 分钟，表只走 58 分钟
start = 11 * 60 + 50
watch_end = 24 * 60 + 12 * 60         # 次日 12:00（从第一天 0:00 起）
watch_elapsed = watch_end - start
std_elapsed = watch_elapsed * F(60, watch_per_std_hour)
std_clock = start + std_elapsed - 24 * 60
options = {'A': 12 * 60 + 50, 'B': 13 * 60, 'C': 12 * 60 + 48, 'D': 13 * 60 + 2}
ans = [k for k, v in options.items() if v == std_clock]
assert len(ans) == 1
print(f'表走{watch_elapsed}分，标准走{std_elapsed}分，次日{std_clock // 60}:{std_clock % 60}', file=sys.stderr)
print(ans[0])
