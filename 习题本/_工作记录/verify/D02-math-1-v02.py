# D02-math-1-v02  3大+2小=240亩/天，2大+5小=270亩/天；现有4大3小，3天内收完1500亩，至少再调几台小型
from fractions import Fraction as F
OPTS = {'A': 4, 'B': 5, 'C': 6, 'D': 9}
# 解单台效率（克拉默法则，精确分数）
a1, b1, c1 = 3, 2, 240
a2, b2, c2 = 2, 5, 270
det = a1 * b2 - a2 * b1
L = F(c1 * b2 - c2 * b1, det)
S = F(a1 * c2 - a2 * c1, det)
assert L > 0 and S > 0
assert a1 * L + b1 * S == c1 and a2 * L + b2 * S == c2
BIG, SMALL, DAYS, AREA = 4, 3, 3, 1500


def ok(n, L=L, S=S):
    """再调 n 台小型后，3 天能否收完。"""
    return DAYS * (BIG * L + (SMALL + n) * S) >= AREA


need = next(n for n in range(0, 1000) if ok(n))
assert need >= 1 and not ok(need - 1)
hits = [k for k, v in OPTS.items() if v == need]
assert len(hits) == 1, (need, hits)

# 干扰项来源核对
assert int((F(AREA, DAYS) - BIG * L - SMALL * S) / S) == OPTS['B']          # 向下取整
need_nosmall = next(n for n in range(0, 1000) if DAYS * (BIG * L + n * S) >= AREA)
assert need_nosmall == OPTS['D']                                            # 忘了现有3台小型
need_swap = next(n for n in range(0, 1000) if ok(n, L=S, S=L))
assert need_swap == OPTS['A']                                               # 大小型效率解反
print('L', L, 'S', S, 'need', need)
print(hits[0])
