# teacher T131（2021青海/河北联考）6座圆形旋转木马，2大人4孩子，两大人不相邻的概率
from fractions import Fraction as F
from itertools import permutations

OPTS = {'A': F(2, 5), 'B': F(3, 5), 'C': F(1, 3), 'D': F(2, 3)}
N = 6
people = ['大1', '大2', '孩1', '孩2', '孩3', '孩4']
good = tot = 0
for perm in permutations(people):          # perm[i] 坐环上第i个位置
    tot += 1
    i, j = perm.index('大1'), perm.index('大2')
    if (i - j) % N not in (1, N - 1):
        good += 1
P = F(good, tot)
print('P =', P)
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
