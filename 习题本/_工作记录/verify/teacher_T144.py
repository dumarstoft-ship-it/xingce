# teacher T144（2015上海A）1~64擦去3的倍数，剩余数之和
OPTS = {'A': 2408, 'B': 1387, 'C': 1408, 'D': 1487}
N, K = 64, 3
s = sum(i for i in range(1, N + 1) if i % K)
print('剩余和 =', s)
hits = [k for k, v in OPTS.items() if v == s]
assert len(hits) == 1, hits
print(hits[0])
