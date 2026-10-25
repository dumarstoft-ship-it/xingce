# T122 2015山东：5个科室各抽调1人交流到其他科室，每科室只接收1人
from itertools import permutations

N = 5
OPTS = {'A': 120, 'B': 78, 'C': 44, 'D': 24}
cnt = sum(1 for p in permutations(range(N)) if all(p[i] != i for i in range(N)))
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('derangements =', cnt)
print(hits[0])
