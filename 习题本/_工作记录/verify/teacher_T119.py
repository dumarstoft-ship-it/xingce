# T119 2014四川下：8个协管员名额分到4个路口，每个路口至少1个
from itertools import product

SLOTS, CROSS = 8, 4
OPTS = {'A': 35, 'B': 70, 'C': 96, 'D': 114}
cnt = sum(1 for x in product(range(1, SLOTS + 1), repeat=CROSS) if sum(x) == SLOTS)
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('ways =', cnt)
print(hits[0])
