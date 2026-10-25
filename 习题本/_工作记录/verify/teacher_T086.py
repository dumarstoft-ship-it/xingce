# T086 2024四川：70%盐水100克，倒出40克再加40克20%盐水，共操作5次后浓度范围
from fractions import Fraction as F

TOTAL, C0, OUT, C_ADD, TIMES = F(100), F(70, 100), F(40), F(20, 100), 5
RANGES = {'A': (F(0), F(23, 100)), 'B': (F(23, 100), F(25, 100)),
          'C': (F(25, 100), F(27, 100)), 'D': (F(27, 100), F(1))}

salt = TOTAL * C0
trace = []
for _ in range(TIMES):
    salt -= salt * OUT / TOTAL      # 倒出40克（按浓度带走溶质）
    salt += OUT * C_ADD             # 加入40克20%盐水
    trace.append(salt / TOTAL)
c = trace[-1]
hits = [k for k, (lo, hi) in RANGES.items() if lo < c < hi]
assert len(hits) == 1, (c, hits)
assert RANGES['C'][0] < trace[3] < RANGES['C'][1]   # 只做4次会落入C
print('trace %:', [round(float(x) * 100, 3) for x in trace])
print(hits[0])
