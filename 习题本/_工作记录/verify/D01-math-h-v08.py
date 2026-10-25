# D01-math-h-v08  医院本院与分院：
# 本院:分院=3:1；本院抽调部分医生到分院后变为7:3；此后分院招聘20名医生，变为3:2；期间无其他人员变动。
# 求最初分院医生人数。
OPTS = {'A': 20, 'B': 30, 'C': 36, 'D': 50}
RECRUIT = 20

sols = []
for b0 in range(1, 1001):                 # 最初分院人数
    a0 = 3 * b0                           # 本院:分院 = 3:1
    for x in range(1, a0):                # 本院抽调到分院的人数
        a1, b1 = a0 - x, b0 + x
        if 3 * a1 != 7 * b1:              # 抽调后 7:3
            continue
        a2, b2 = a1, b1 + RECRUIT         # 分院招聘，本院不变
        if 2 * a2 != 3 * b2:              # 招聘后 3:2
            continue
        sols.append((a0, b0, x, a1, b1, b2))
assert len(sols) == 1, sols
a0, b0, x, a1, b1, b2 = sols[0]
hits = [k for k, v in OPTS.items() if v == b0]
assert len(hits) == 1, hits

# 干扰项来源核对
# 招聘一步仍按“总数不变”通分：7:3 与 3:2 都化成10份，分院 3→4 份 = 20人
from fractions import Fraction as F
part = F(RECRUIT, 4 - 3)
assert 10 * part / 4 == OPTS['D']                 # 总数200，分院占1/4
# 首尾 3:1 与 3:2 直接比、当本院始终不变：分院 1→2 份 = 20人
assert RECRUIT // (2 - 1) == OPTS['A']
assert b1 == OPTS['C']                            # 答成抽调后的分院人数
print('a0,b0,x,a1,b1,b2 =', sols[0])
print(hits[0])
