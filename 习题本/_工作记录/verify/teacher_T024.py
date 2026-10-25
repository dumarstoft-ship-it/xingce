# teacher_T024  四人年龄为相邻自然数，最年长者不超过30岁，乘积能被2700整除且不能被81整除。最年长者几岁
from math import prod

OPTS = {'A': 25, 'B': 26, 'C': 27, 'D': 28}
sols = [o for o in range(4, 31) if prod(range(o - 3, o + 1)) % 2700 == 0 and prod(range(o - 3, o + 1)) % 81 != 0]
assert len(sols) == 1, sols
ans = sols[0]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert prod(range(24, 28)) % 81 == 0                # 24~27 多一个3，被81整除
print('最年长 =', ans)
print(hits[0])
