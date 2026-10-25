# D02-math-1-v13  8大4小可运行6天，大型日耗=2倍小型；运行2天后大-4、小+4；还能运行几天
from fractions import Fraction as F
OPTS = {'A': F(4), 'B': F(5), 'C': F(7), 'D': F(15, 2)}


def remain(big_w, small_w):
    """按每台日耗电 big_w、small_w 计算调整后还能运行的天数。"""
    total = 6 * (8 * big_w + 4 * small_w)
    left = total - 2 * (8 * big_w + 4 * small_w)
    return left / (4 * big_w + 8 * small_w)


ans = remain(F(2), F(1))
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)

# 干扰项来源核对
assert remain(F(1), F(1)) == OPTS['A']                       # 不折算，按台数算
assert 6 * (8 * 2 + 4) / F(4 * 2 + 8) == OPTS['D']           # 忘了已运行2天
assert 2 + ans == OPTS['C']                                  # 答成总天数
print('remain', ans)
print(hits[0])
