# D02-math-1-v09  三网格同量N户同时开工；甲完成时乙剩18、丙剩30；乙完成时丙剩15；求N
from fractions import Fraction as F
OPTS = {'A': 60, 'B': 72, 'C': 75, 'D': 90}


def c_left_when_b_done(N):
    """同一时段完成量之比=效率比：乙做完N户时，丙还剩多少户。"""
    rb, rc = N - 18, N - 30
    return N - F(N * rc, rb)


sols = [N for N in range(31, 5000) if c_left_when_b_done(N) == 15]
assert len(sols) == 1, sols
N = sols[0]
hits = [k for k, v in OPTS.items() if v == N]
assert len(hits) == 1, hits
assert [k for k, v in OPTS.items() if c_left_when_b_done(v) == 15] == hits

# 干扰项来源核对
assert N - 18 == OPTS['B'] and N - 30 == OPTS['A'] and N - 15 == OPTS['C']
print('N', N)
print(hits[0])
