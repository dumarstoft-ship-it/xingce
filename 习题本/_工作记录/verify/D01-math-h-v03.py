# D01-math-h-v03  展会甲、乙、丙三个展区：甲是乙、丙之和的1/3，乙是甲、丙之和的1/4，
# 丙比乙多126家。求甲展区的参展企业数。
from fractions import Fraction as F

OPTS = {'A': 90, 'B': 198, 'C': 252, 'D': 360}
R_JIA = F(1, 3)    # 甲 ＝ (乙＋丙) × 1/3
R_YI = F(1, 4)     # 乙 ＝ (甲＋丙) × 1/4
DIFF = 126         # 丙 − 乙 ＝ 126
N = 2000

# 穷举甲、乙（正整数），丙由“丙比乙多126”给出，再检验两条倍数关系（交叉相乘，全用整数）
sols = []
for x in range(1, N + 1):          # 甲
    for y in range(1, N + 1):      # 乙
        z = y + DIFF               # 丙
        if (x * R_JIA.denominator == R_JIA.numerator * (y + z)
                and y * R_YI.denominator == R_YI.numerator * (x + z)):
            sols.append((x, y, z))
assert len(sols) == 1, sols
x, y, z = sols[0]
hits = [k for k, v in OPTS.items() if v == x]
assert len(hits) == 1, hits

# 干扰项来源核对
# (1) 把1/3、1/4直接当成甲、乙占总数的比例：丙占1−1/3−1/4，丙−乙对应126
naive = []
for t in range(1, 20001):
    a, b = R_JIA * t, R_YI * t
    c = t - a - b
    if a.denominator == 1 and b.denominator == 1 and c - b == DIFF:
        naive.append((t, int(a)))
assert len(naive) == 1 and naive[0][1] == OPTS['C'], naive
assert z == OPTS['B']              # 答成丙展区
assert x + y + z == OPTS['D']      # 答成总数
print('甲', x, '乙', y, '丙', z, 'total', x + y + z, '| naive total/甲', naive[0])
print(hits[0])
