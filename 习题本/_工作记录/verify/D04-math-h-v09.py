# D04-math-h-v09：停车按小时收费，不足 1 小时按 1 小时计；前 a 小时每小时 3 元，超过 a 小时的部分每小时 b 元（a 为正整数）。
# 甲停 4 小时 20 分钟付 19 元，乙停 7 小时 35 分钟付 34 元；丙付 24 元，问丙的停车时长最多为几小时。
# 做法：枚举 a，由甲、乙两组数据解出所有一致的 (a, b)；再找出使费用恰为 24 元的计费小时数 h，
# 计费 h 小时对应实际时长 t 满足 h-1 < t <= h，故最长为 h 小时。
import math
from fractions import Fraction as F

OPTIONS = {'A': 6, 'B': 7, 'C': 8, 'D': 5}   # 单位：小时（升序轮转排列）
P1 = 3
DATA = [(4 * 60 + 20, 19), (7 * 60 + 35, 34)]  # (实际停车分钟数, 费用)


def billed_hours(minutes):
    return math.ceil(F(minutes, 60))


def fee(h, a, b):
    return P1 * min(h, a) + b * max(h - a, 0)


solutions = []
for a in range(1, 500):
    hs = [billed_hours(m) for m, _ in DATA]
    # 只要有一组数据超过 a 小时，就能由它解出 b，再用另一组检验
    over = [(h, c) for h, (_, c) in zip(hs, DATA) if h > a]
    if not over:
        if all(fee(h, a, 0) == c for h, (_, c) in zip(hs, DATA)):
            solutions.append((a, None))
        continue
    h0, c0 = over[0]
    b = F(c0 - P1 * a, h0 - a)
    if b <= 0:
        continue
    if all(fee(h, a, b) == c for h, (_, c) in zip(hs, DATA)):
        solutions.append((a, b))

assert len(solutions) == 1, solutions
a, b = solutions[0]
assert b is not None

hours_for_24 = [h for h in range(1, 2000) if fee(h, a, b) == 24]
assert len(hours_for_24) == 1, hours_for_24
max_time = hours_for_24[0]                     # 实际时长 t ∈ (h-1, h]，最长 h 小时

hits = [k for k, v in OPTIONS.items() if v == max_time]
assert len(hits) == 1
print('a =', a, 'b =', b, 'billed hours for 24 yuan =', max_time)
print(hits[0])
