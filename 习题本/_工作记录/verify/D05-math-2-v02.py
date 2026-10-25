# D05-math-2-v02：原 5 个节目顺序已定，再加入 2 个不同的新节目（位置不限），原节目先后顺序不变。
# 暴力枚举 7 个节目的全部排列，保留"原 5 个节目仍按原顺序出现"的排列。
from itertools import permutations

OPTIONS = {'A': 21, 'B': 30, 'C': 36, 'D': 42}

old = ['旧1', '旧2', '旧3', '旧4', '旧5']   # 原节目单顺序
new = ['新1', '新2']                        # 两个不同的新节目
count = 0
for order in permutations(old + new):
    if [x for x in order if x in old] == old:
        count += 1

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
