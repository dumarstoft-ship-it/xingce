# D02-math-1-v11  柴油可供16台运行7天；运行h小时后停4台，余油恰好供12台运行9天；求h
from fractions import Fraction as F
OPTS = {'A': 4, 'B': 6, 'C': 8, 'D': 24}
N, D, K, E = 16, 7, 4, 9
TOTAL = N * D * 24                        # 以“台·小时”计的总油量

sols = [F(m, 60) for m in range(0, D * 24 * 60 + 1)       # 以分钟为步长穷举 h
        if N * F(m, 60) + (N - K) * E * 24 == TOTAL]
assert len(sols) == 1, sols
h = sols[0]
hits = [k for k, v in OPTS.items() if v == h]
assert len(hits) == 1, hits

# 干扰项来源核对
diff_taitian = N * D - (N - K) * E
assert diff_taitian == OPTS['A']                          # 把台·天当小时
assert F(diff_taitian, N - K) * 24 == OPTS['C']           # 误除以剩下的12台
assert F(diff_taitian, K) * 24 == OPTS['D']               # 误除以停机的4台
print('h', h)
print(hits[0])
