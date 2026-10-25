# D02-math-1-v15  积水+雨水匀速流入：5台6小时、8台3小时；4小时内排完至少几台
from fractions import Fraction as F
OPTS = {'A': 4, 'B': 5, 'C': 6, 'D': 7}

# 每台泵每小时排1份，每小时流入x份：穷举x（0.1步长）
sols = [x for x in [F(k, 10) for k in range(0, 50)] if (5 - x) * 6 == (8 - x) * 3]
assert len(sols) == 1
x = sols[0]
Y = (5 - x) * 6


def can(n, T=4):
    """逐分钟模拟积水量，T 小时内能否排完。"""
    water = Y
    for _ in range(T * 60):
        water += (x - n) / 60
        if water <= 0:
            return True
    return water <= 0


need = next(n for n in range(1, 100) if can(n))
hits = [k for k, v in OPTS.items() if v == need]
assert len(hits) == 1, (need, hits)

# 干扰项来源核对
assert int(x + Y / 4) == OPTS['C']                    # 向下取整
assert -(-Y // 4) == OPTS['B']                        # 漏了抵消流入的泵
assert int(Y / 4) == OPTS['A']                        # 漏了流入且向下取整
assert int(F(8 * 3, 4)) == OPTS['C']                  # 忽略流入、按8台3小时算存量
print('inflow', x, 'stock', Y, 'need', need)
print(hits[0])
