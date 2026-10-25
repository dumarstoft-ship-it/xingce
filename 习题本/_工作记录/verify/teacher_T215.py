# T215（2018广州）用全部156个单位小正方形，最多可拼成多少种形状不同的长方形。
AREA = 156
OPTS = {'A': 5, 'B': 6, 'C': 7, 'D': 8}
shapes = [(w, AREA // w) for w in range(1, AREA + 1) if AREA % w == 0 and w <= AREA // w]
hits = [k for k, v in OPTS.items() if v == len(shapes)]
assert len(hits) == 1, (shapes, hits)
print('shapes =', shapes)
print(hits[0])
