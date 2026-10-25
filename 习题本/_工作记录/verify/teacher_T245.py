# T245 圆锥尖朝下在密度1液体中露出 0.1x；尖朝上放入密度1.5液体，露出高度范围
rho1, rho2 = 1.0, 1.5
sub1 = 0.9 ** 3                   # 尖朝下：液面下为高 0.9x 的相似锥
sub2 = sub1 * rho1 / rho2         # 浮力=重力不变：ρ·V排 不变
exposed = 1 - sub2                # 尖朝上：露出的是顶部相似小锥
k = exposed ** (1/3)              # 露出高度 / x
ranges = {"A": (0.8, 1.0), "B": (0.7, 0.8), "C": (0.6, 0.7), "D": (0.0, 0.6)}
hits = [key for key, (lo, hi) in ranges.items() if lo < k < hi]
assert len(hits) == 1, (k, hits)
print(hits[0])
