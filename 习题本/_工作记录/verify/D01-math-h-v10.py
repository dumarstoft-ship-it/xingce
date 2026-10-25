# D01-math-h-v10  建筑工地发劳保手套：
# 每人6副，剩50副；露天作业工人每人8副、其余工人每人5副，恰好发完；
# 露天作业工人比其余工人多1/3。求工人总数。
OPTS = {'A': 70, 'B': 100, 'C': 175, 'D': 470}

sols = []
for other in range(1, 3001):                    # 其余工人
    if (other * 4) % 3:                          # 露天 = 其余 × (1 + 1/3)
        continue
    outdoor = other * 4 // 3
    gloves1 = 6 * (outdoor + other) + 50
    gloves2 = 8 * outdoor + 5 * other
    if gloves1 == gloves2:
        sols.append((outdoor, other, gloves1))
assert len(sols) == 1, sols
outdoor, other, gloves = sols[0]
n = outdoor + other
hits = [k for k, v in OPTS.items() if v == n]
assert len(hits) == 1, hits

# 干扰项来源核对
from fractions import Fraction as F
assert F(50) / (F(8 + 5, 2) - 6) == OPTS['B']          # 简单平均 6.5 副
per_group_rev = 8 * 3 + 5 * 4                           # 人数比写反成 3:4
assert F(50) / (per_group_rev - 6 * 7) * 7 == OPTS['C']
assert gloves == OPTS['D']                              # 求成手套总数
print('outdoor, other, gloves =', sols[0])
print(hits[0])
