# T209（2012江苏A）一位数×两位数×三位数=2004，三数之和是多少。
PRODUCT = 2004
OPTS = {'A': 100, 'B': 180, 'C': 179, 'D': 178}
sols = [(a, b, PRODUCT // (a * b)) for a in range(1, 10) for b in range(10, 100)
        if PRODUCT % (a * b) == 0 and 100 <= PRODUCT // (a * b) <= 999]
sums = {sum(s) for s in sols}
assert len(sums) == 1, sols
ans = sums.pop()
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('decompositions =', sols)
print(hits[0])
