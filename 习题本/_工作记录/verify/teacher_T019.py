# teacher_T019  连续5天年假，日期相乘为7893600，最后一天是几日
from math import prod

PRODUCT = 7893600
OPTS = {'A': 25, 'B': 26, 'C': 27, 'D': 28}
sols = [d + 4 for d in range(1, 28) if prod(range(d, d + 5)) == PRODUCT]
assert len(sols) == 1, sols
ans = sols[0]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('最后一天 =', ans)
print(hits[0])
