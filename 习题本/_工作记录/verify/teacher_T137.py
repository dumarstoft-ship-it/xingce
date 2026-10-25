# teacher T137（2012浙江）四个连续奇数和为32，求积
OPTS = {'A': 945, 'B': 1875, 'C': 2745, 'D': 3465}
SUM, K = 32, 4
sols = [[n + 2 * i for i in range(K)] for n in range(-101, 102, 2) if sum(n + 2 * i for i in range(K)) == SUM]
assert len(sols) == 1, sols
prod = 1
for v in sols[0]:
    prod *= v
print(sols[0], prod)
hits = [k for k, v in OPTS.items() if v == prod]
assert len(hits) == 1, hits
print(hits[0])
