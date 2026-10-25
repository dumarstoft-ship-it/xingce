# T208（2019河北县乡）一位数×两位数×三位数=3930，三数之和最小为多少。
PRODUCT = 3930
OPTS = {'A': 144, 'B': 146, 'C': 148, 'D': 162}
sols = [(a, b, PRODUCT // (a * b)) for a in range(1, 10) for b in range(10, 100)
        if PRODUCT % (a * b) == 0 and 100 <= PRODUCT // (a * b) <= 999]
ans = min(sum(s) for s in sols)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('decompositions =', sols)
print(hits[0])
