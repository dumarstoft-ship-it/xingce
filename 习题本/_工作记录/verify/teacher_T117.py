# T117 圆桌6个编号座位（1-6，两两相对），6人就座，张的正对面必须是吴
from itertools import permutations

NAMES = '张王李赵周吴'
OPTS = {'A': 24, 'B': 36, 'C': 72, 'D': 144}
cnt = 0
for seat_of in permutations(range(6)):           # seat_of[i] = 第i人的座位号
    s = dict(zip(NAMES, seat_of))
    if (s['张'] + 3) % 6 == s['吴']:
        cnt += 1
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('ways =', cnt)
print(hits[0])
