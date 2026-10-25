# D04-math-h-v16：杨梅进价 10.53 元/斤，运输 2 天，每天损耗当天开始时所剩量的同一个百分比 x；
# 运到后可售部分 80% 按 18 元/斤售出，其余按 12.5 元/斤清仓；这批杨梅的利润率恰好为 30%。求 x。
# 独立求解：对任意 x，按一批 10000 斤逐日模拟损耗，成本按进货量计，算出利润率；
# 利润率随 x 单调递减，用二分法在 [0, 1) 内求出使利润率等于 30% 的 x，再逐个选项代回检验，确认恰好一个选项成立。
from fractions import Fraction as Fr

COST = Fr('10.53')
DAYS = 2
FULL_SHARE, FULL_PRICE, CLEAR_PRICE = Fr(80, 100), Fr(18), Fr('12.5')
TARGET = Fr(30, 100)

OPTIONS = {'A': '2.5', 'B': '9.5', 'C': '10', 'D': '19'}   # 百分数


def profit_rate(x):
    batch = Fr(10000)
    left = batch
    for _ in range(DAYS):
        left -= left * x                  # 每天损耗当天开始时所剩量的 x
    revenue = left * FULL_SHARE * FULL_PRICE + left * (1 - FULL_SHARE) * CLEAR_PRICE
    cost = COST * batch
    return (revenue - cost) / cost


lo, hi = Fr(0), Fr(99, 100)
assert profit_rate(lo) > TARGET > profit_rate(hi)
for _ in range(60):
    mid = (lo + hi) / 2
    if profit_rate(mid) > TARGET:
        lo = mid
    else:
        hi = mid
print('二分求得每天损耗率约', float(lo) * 100, '%')
for k, v in OPTIONS.items():
    print(k, v + '%', '利润率', float(profit_rate(Fr(v) / 100)))

hits = [k for k, v in OPTIONS.items() if profit_rate(Fr(v) / 100) == TARGET]
assert len(hits) == 1 and abs(Fr(OPTIONS[hits[0]]) / 100 - lo) < Fr(1, 10 ** 9), hits
print(hits[0])
