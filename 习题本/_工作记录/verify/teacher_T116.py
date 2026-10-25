# T116（老师改编T115）：甲乙相邻；丁在丙前；戊在丙前；己第一或最后
from itertools import permutations

OPTS = {'A': 16, 'B': 24, 'C': 32, 'D': 48}       # 补设选项
cnt = 0
for p in permutations('甲乙丙丁戊己'):
    pos = {x: i for i, x in enumerate(p)}
    if abs(pos['甲'] - pos['乙']) != 1:
        continue
    if not (pos['丁'] < pos['丙'] and pos['戊'] < pos['丙']):
        continue
    if pos['己'] not in (0, 5):
        continue
    cnt += 1
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
# 干扰项来源：照搬上题除以3!（16）；把两个条件各当"一半"除以4（24）；只考虑一个条件除以2（48）
assert 2 * 2 * 24 // 6 == OPTS['A'] and 2 * 2 * 24 // 4 == OPTS['B'] and 2 * 2 * 24 // 2 == OPTS['D']
print('orders =', cnt)
print(hits[0])
