# T114 国庆7天安排6人值班，每天1人、每人至少1天；甲乙丙均只值1天且甲在乙之前
from itertools import product

PEOPLE = '甲乙丙丁戊己'
DAYS = 7
OPTS = {'A': 360, 'B': 758, 'C': 1680, 'D': 3780}
cnt = 0
for sched in product(range(6), repeat=DAYS):          # sched[d] = 第d天值班的人
    counts = [sched.count(p) for p in range(6)]
    if min(counts) < 1:
        continue
    if counts[0] != 1 or counts[1] != 1 or counts[2] != 1:
        continue
    if sched.index(0) < sched.index(1):
        cnt += 1
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('schedules =', cnt)
print(hits[0])
