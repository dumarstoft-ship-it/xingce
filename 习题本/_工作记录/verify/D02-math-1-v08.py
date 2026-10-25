# D02-math-1-v08  A=3B，甲效率=2乙；甲做A、乙做B同时开始，乙完成后协助甲，又2小时A完成；求甲单独做A的时间
from fractions import Fraction as F
OPTS = {'A': 3, 'B': 6, 'C': 8, 'D': 9}
YI, JIA = F(1), F(2)
GRID = [F(k, 100) for k in range(1, 4001)]     # B 的工作量以 0.01 为步长穷举

sols = []
for B in GRID:
    A = 3 * B
    t = B / YI                    # 乙完成 B 的时刻
    rest = A - JIA * t            # 此时 A 剩余
    if rest > 0 and rest / (JIA + YI) == 2:
        sols.append((B, A, t))
assert len(sols) == 1, sols
B, A, t = sols[0]
ans = A / JIA
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits

# 干扰项来源核对
assert t + 2 == OPTS['C'] and t == OPTS['B']
B2 = next(b for b in GRID if (3 * b - JIA * b) / YI == 2)        # 协助阶段只算乙的效率
assert 3 * B2 / JIA == OPTS['A']
B3 = next(b for b in GRID if 3 * b / (JIA + YI) == 2)            # 忘了甲前一段的进度
assert 3 * B3 / JIA == OPTS['A']
print('B', B, 'A', A, 't', t, 'ans', ans)
print(hits[0])
