# D02-math-1-v14  27头6天吃完、23头9天吃完；草量保持不减最多放几头
from fractions import Fraction as F
OPTS = {'A': 12, 'B': 14, 'C': 15, 'D': 35}

# 每头牛每天吃1份，每天生长x份，原有Y份：穷举x（0.1步长）
sols = [(x, (27 - x) * 6) for x in [F(k, 10) for k in range(0, 270)]
        if (27 - x) * 6 == (23 - x) * 9]
assert len(sols) == 1, sols
x, Y = sols[0]


def never_decrease(n):
    """逐日模拟：放牧 n 头时草量是否始终不减少。"""
    grass = Y
    for _ in range(1000):
        new = grass + x - n
        if new < grass:
            return False
        grass = new
    return True


best = max(n for n in range(0, 100) if never_decrease(n))
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)

# 干扰项来源核对
assert 27 - x == OPTS['A']                       # 放27头时吃原有草的牛数
assert best - 1 == OPTS['B']                     # 误以为必须严格小于生长量
swapped = [z for z in [F(k, 10) for k in range(0, 1000)] if (27 - z) * 9 == (23 - z) * 6]
assert swapped == [OPTS['D']]                    # 两组天数对调列式
print('growth', x, 'stock', Y, 'max', best)
print(hits[0])
