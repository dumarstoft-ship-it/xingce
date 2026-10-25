# D02-math-1-v04  甲单独27天、合作18天；11月20日开工，甲先4天，合作x天，余下乙做，12月19日完工；求x
from fractions import Fraction as F
from datetime import date
OPTS = {'A': 8, 'B': 10, 'C': 12, 'D': 14}
jia = F(1, 27)
yi = F(1, 18) - jia
D = (date(2025, 12, 19) - date(2025, 11, 20)).days + 1   # 首尾都算
FIRST = 4


def solve(days_after, done_before):
    """剩余 days_after 天里先合作 x 天、再乙单独，恰好完成的整数 x。"""
    return [x for x in range(0, days_after + 1)
            if done_before + x * (jia + yi) + (days_after - x) * yi == 1]


sols = solve(D - FIRST, FIRST * jia)
assert D == 30 and len(sols) == 1, (D, sols)
x = sols[0]
assert D - FIRST - x > 0
hits = [k for k, v in OPTS.items() if v == x]
assert len(hits) == 1, hits

# 干扰项来源与日期误数检查
assert solve(D, FIRST * jia) == [OPTS['A']]          # 没扣甲单独的4天
assert solve(D - FIRST, 0) == [OPTS['D']]            # 忘减甲完成的量
assert solve(D, 0) == [OPTS['C']]                    # 两处都错
assert solve(D - 1 - FIRST, FIRST * jia) == [] and solve(D + 1 - FIRST, FIRST * jia) == []
print('days', D, 'x', x, 'yi alone', 1 / yi)
print(hits[0])
