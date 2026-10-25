# T115 2020国考副省级：6户走访，甲乙相邻；丙在丁前；戊在丙前；己第一或最后
from itertools import permutations

OPTS = {'A': 24, 'B': 16, 'C': 48, 'D': 32}
cnt = 0
for p in permutations('甲乙丙丁戊己'):
    pos = {x: i for i, x in enumerate(p)}
    if abs(pos['甲'] - pos['乙']) != 1:
        continue
    if not (pos['戊'] < pos['丙'] < pos['丁']):
        continue
    if pos['己'] not in (0, 5):
        continue
    cnt += 1
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('orders =', cnt)
print(hits[0])
