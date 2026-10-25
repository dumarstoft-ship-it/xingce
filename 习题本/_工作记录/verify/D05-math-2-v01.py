# D05-math-2-v01：6 名先进个人依次上台，要求甲先于乙、乙先于丙（不必相邻），其余不限。
# 暴力枚举 6 人的全部上台顺序，数出满足条件的个数，再对照选项。
from itertools import permutations

OPTIONS = {'A': 20, 'B': 120, 'C': 240, 'D': 720}

people = ['甲', '乙', '丙', '丁', '戊', '己']
count = 0
for order in permutations(people):
    if order.index('甲') < order.index('乙') < order.index('丙'):
        count += 1

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
