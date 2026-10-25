# D01-math-1-v09  环卫清运：大:中车数＝2:3，中:小＝4:5；每车每趟装载量5:3:2；每车趟数2:3:4；小型车共运180吨。求三种车共运多少吨。
from fractions import Fraction as F
from itertools import product

LOAD = (5, 3, 2)
TRIPS = (2, 3, 4)
SMALL_TOTAL = 180
OPTS = {'A': 336, 'B': 420, 'C': 462, 'D': 636}

# 穷举满足两个数量比的车队组合（各型号1~60辆），对每种组合按“小型车共运180吨”定出单位装载量，求总运量
totals = set()
fleets = 0
for L, M, S in product(range(1, 61), repeat=3):
    if L * 3 != M * 2 or M * 5 != S * 4:
        continue
    fleets += 1
    unit = F(SMALL_TOTAL, S * LOAD[2] * TRIPS[2])          # 单位装载量（吨）
    total = sum(n * w * t for n, w, t in zip((L, M, S), LOAD, TRIPS)) * unit
    totals.add(total)
assert fleets >= 1 and len(totals) == 1, totals            # 总运量与车队规模无关
total = totals.pop()
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits

# 干扰项来源核对（最小车队8:12:15）
cnt = (8, 12, 15)
def tot(weights):
    w = [c * x for c, x in zip(cnt, weights)]
    return F(SMALL_TOTAL, w[2]) * sum(w)
assert tot(LOAD) == OPTS['D']                               # 漏乘趟数
assert tot(TRIPS) == OPTS['A']                              # 漏乘装载量
assert tot((1, 1, 1)) == OPTS['B']                          # 只按车数之比分
print('fleets checked', fleets, 'total', total)
print(hits[0])
