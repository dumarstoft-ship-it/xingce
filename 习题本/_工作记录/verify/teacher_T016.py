# teacher_T016  三科室人数相等；甲党员=乙非党员；丙党员占全单位党员40%。党员比非党员多/少百分之几
from fractions import Fraction as F

OPTS = {'A': F(-1, 5), 'B': F(-1, 4), 'C': F(1, 5), 'D': F(1, 4)}   # (党员-非党员)/非党员
rel = set()
for N in range(1, 61):                    # 每个科室人数
    for x in range(0, N + 1):             # 甲党员
        y = N - x                         # 乙党员（乙非党员 = x）
        for z in range(0, N + 1):         # 丙党员
            P = x + y + z
            if P == 0 or 5 * z != 2 * P:
                continue
            nonP = 3 * N - P
            rel.add(F(P - nonP, nonP))
assert len(rel) == 1, rel
ans = rel.pop()
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('(党员-非党员)/非党员 =', ans)
print(hits[0])
