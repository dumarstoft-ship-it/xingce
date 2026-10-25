# T203（2021江苏A）徒弟做6种剪纸用时2、6、10、12、15、25分钟，师傅效率是徒弟1.5倍，每件只由一人做。
# 最后一位游客至少等待多久（两人同时开工，取两人完工时间的较大者）。
from fractions import Fraction as F
from itertools import product

TIMES, RATIO = [2, 6, 10, 12, 15, 25], F(3, 2)
OPTS = {'A': 25, 'B': 27, 'C': 28, 'D': 30}
best = min(max(sum(t for t, w in zip(TIMES, who) if w == 0),
               sum(t for t, w in zip(TIMES, who) if w == 1) / RATIO)
           for who in product((0, 1), repeat=len(TIMES)))
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('min finish time =', best)
print(hits[0])
