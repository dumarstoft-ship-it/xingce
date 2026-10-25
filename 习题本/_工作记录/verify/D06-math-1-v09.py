# D06-math-1-v09: 10 盏灯全亮，每次随机选 2 盏各按一下，共 3 次；任一盏灯最后仍亮的概率（精确枚举）
from fractions import Fraction as F
from itertools import combinations, product
pairs = list(combinations(range(10), 2))
total = on_lamp0 = on_count = 0
for ops in product(pairs, repeat=3):
    total += 1
    state = [1] * 10
    for p in ops:
        for i in p:
            state[i] ^= 1
    on_lamp0 += state[0]
    on_count += sum(state)
p0 = F(on_lamp0, total)
assert p0 == F(on_count, total * 10)          # 每盏灯对称，与"任意一盏"一致
opts = {'A': F(392, 1000), 'B': F(512, 1000), 'C': F(544, 1000), 'D': F(608, 1000)}
hit = [L for L, v in opts.items() if v == p0]
assert len(hit) == 1, (p0, hit)
print('P =', p0, float(p0))
print(hit[0])
