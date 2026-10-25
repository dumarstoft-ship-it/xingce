# T112 2022江苏A65：3个分公司各2人共6人出场，同一分公司的两人不能相邻，求出场顺序数
from itertools import permutations

people = [(c, i) for c in 'abc' for i in (1, 2)]
OPTS = {'A': 80, 'B': 120, 'C': 160, 'D': 240}
cnt = 0
for p in permutations(people):
    if all(p[i][0] != p[i + 1][0] for i in range(len(p) - 1)):
        cnt += 1
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
# 老师的整除筛选：内部交换2^3、公司换名3!，答案必为48的倍数，选项中唯一
assert [k for k, v in OPTS.items() if v % 48 == 0] == hits
print('orders =', cnt)
print(hits[0])
