# T121 2014北京：4辆车重新停入4个车位，都不得停在原车位
from itertools import permutations

N = 4
OPTS = {'A': 9, 'B': 12, 'C': 14, 'D': 16}
cnt = sum(1 for p in permutations(range(N)) if all(p[i] != i for i in range(N)))
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('derangements =', cnt)
print(hits[0])
