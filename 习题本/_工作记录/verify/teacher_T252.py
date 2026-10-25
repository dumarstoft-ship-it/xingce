# T252 整数边直角三角形，一条直角边 7，随机点落在斜边上的概率范围
sols = []
for b in range(1, 1000):
    c2 = 49 + b * b
    c = int(round(c2 ** 0.5))
    if c * c == c2:
        sols.append((7, b, c))
assert len(sols) == 1, sols
a, b, c = sols[0]
p = c / (a + b + c)
ranges = {"A": (0, 0.35), "B": (0.35, 0.42), "C": (0.42, 0.50), "D": (0.50, 1)}
hits = [k for k, (lo, hi) in ranges.items() if lo < p < hi]
assert len(hits) == 1, (p, hits)
print(hits[0])
