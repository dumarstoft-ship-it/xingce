# D02-math-1-v10  两台盾构机各1200米；A完成一半时B完成40%；之后A提效20%、B提效50%；A完成时B剩多少
from fractions import Fraction as F
OPTS = {'A': 96, 'B': 120, 'C': 240, 'D': 320}
L = 1200
vA = F(1)                                # A 的原速度（任意单位）
t1 = (L / F(2)) / vA                     # A 完成一半的时刻
vB = (L * F(40, 100)) / t1               # B 在同一时段完成 40%


def b_left(upA, upB):
    t2 = (L / F(2)) / (vA * (1 + upA))   # A 完成后一半所需时间
    return L - vB * t1 - vB * (1 + upB) * t2


ans = b_left(F(20, 100), F(50, 100))
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)

# 干扰项来源核对
assert b_left(F(20, 100), 0) == OPTS['D']          # 只给 A 提效
assert b_left(0, 0) == OPTS['C']                   # 都不提效
assert L - vB * t1 - vB * t1 * (1 + F(50, 100) - F(20, 100)) == OPTS['A']   # 提效幅度直接相减
print('B left', ans)
print(hits[0])
