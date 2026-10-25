# D07-math-1-v11: 三边都是整数、有一条直角边长 12 的直角三角形有多少种（按三边长度区分）
LEG = 12
triples = set()
for b in range(1, 10000):                 # c−b ≥ 1 ⇒ c+b ≤ 144，b 远小于此上限
    c2 = LEG * LEG + b * b
    c = int(round(c2 ** 0.5))
    for cc in (c - 1, c, c + 1):
        if cc > 0 and cc * cc == c2:
            triples.add(tuple(sorted((LEG, b, cc))))
n = len(triples)
opts = {'A': 2, 'B': 3, 'C': 4, 'D': 7}
hit = [k for k, v in opts.items() if v == n]
assert len(hit) == 1, (n, hit)
print(sorted(triples))
print(hit[0])
