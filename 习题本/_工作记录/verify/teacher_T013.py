# teacher_T013  甲+丙=2乙；今年甲=3丙；9年后甲=2.4丙。几年后丙是乙的4/7
from fractions import Fraction as F

OPTS = {'A': 5, 'B': 6, 'C': 7, 'D': 8}
sols = []
for c in range(1, 120):                      # 丙今年年龄
    jia = 3 * c
    if F(jia + 9) != F(12, 5) * (c + 9):
        continue
    if (jia + c) % 2:
        continue
    yi = (jia + c) // 2
    for n in range(0, 120):
        if F(c + n, yi + n) == F(4, 7):
            sols.append((jia, yi, c, n))
assert len(sols) == 1, sols
jia, yi, c, n = sols[0]
hits = [k for k, v in OPTS.items() if v == n]
assert len(hits) == 1, (n, hits)
print('甲乙丙 =', jia, yi, c, ' n =', n)
print(hits[0])
