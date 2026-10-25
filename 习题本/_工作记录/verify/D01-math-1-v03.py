# D01-math-1-v03  港口外贸集装箱：进口箱量比出口箱量少37.5%，出口比进口多6000标箱。求进出口量共多少标箱。
from fractions import Fraction as F

LESS, DIFF = F(375, 1000), 6000
OPTS = {'A': 10000, 'B': 16000, 'C': 26000, 'D': 38000}

# 穷举出口箱量e（标箱，正整数），进口箱量i＝e×(1−37.5%)须为整数，且e−i＝6000
sols = []
for e in range(1, 300001):
    i = e * (1 - LESS)
    if i.denominator == 1 and e - i == DIFF:
        sols.append((e, int(i)))
assert len(sols) == 1, sols
e, i = sols[0]
total = e + i
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits

# 干扰项来源核对
i_bad = DIFF / LESS                       # 误读为“出口比进口多37.5%”：进口＝6000÷37.5%
e_bad = i_bad * (1 + LESS)
assert i_bad + e_bad == OPTS['D']         # 误读后的合计38000
assert e == OPTS['B'] and i == OPTS['A']  # 只求出口或只求进口
print('export', e, 'import', i, 'total', total)
print(hits[0])
