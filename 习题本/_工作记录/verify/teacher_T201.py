# T201（2013江苏）依次与三人谈话10、12、8分钟，调整顺序使三人交谈和等待的总时间最少。
from itertools import permutations

TIMES = [10, 12, 8]
OPTS = {'A': 46, 'B': 48, 'C': 50, 'D': 56}


def total(order):
    t, s = 0, 0
    for x in order:
        t += x          # 此人谈完的时刻 = 等待 + 交谈
        s += t
    return s


best = min(total(p) for p in permutations(TIMES))
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('min total =', best)
print(hits[0])
