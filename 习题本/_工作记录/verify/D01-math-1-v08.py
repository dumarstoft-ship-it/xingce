# D01-math-1-v08  义诊两天：第二天接诊总人次是第一天的1.4倍，第二天人均是第一天的70%；共30名医生（每人只去一天）、480人次。
# 求第一天平均每名医生接诊人次。
from fractions import Fraction as F

DOCS, VISITS = 30, 480
TOTAL_RATIO, AVG_RATIO = F(14, 10), F(7, 10)
OPTS = {'A': 10, 'B': 14, 'C': 16, 'D': 20}

# 穷举两天的医生数与接诊人次
sols = []
for d1 in range(1, DOCS):
    d2 = DOCS - d1
    for p1 in range(1, VISITS):
        p2 = VISITS - p1
        if p2 == TOTAL_RATIO * p1 and F(p2, d2) == AVG_RATIO * F(p1, d1):
            sols.append((d1, d2, p1, p2))
assert len(sols) == 1, sols
d1, d2, p1, p2 = sols[0]
avg1 = F(p1, d1)
hits = [k for k, v in OPTS.items() if v == avg1]
assert len(hits) == 1, hits

# 干扰项来源核对
assert F(p2, d2) == OPTS['B']                    # 答成第二天的人均
assert F(VISITS, DOCS) == OPTS['C']              # 两天合在一起平均
ratio_bad = AVG_RATIO / TOTAL_RATIO              # 除法做反：第二天:第一天医生数＝1:2
d1_bad = DOCS / (1 + ratio_bad)                  # 第一天20名
assert F(p1) / d1_bad == OPTS['A']
print('doctors', d1, d2, 'visits', p1, p2, 'day1 avg', avg1)
print(hits[0])
