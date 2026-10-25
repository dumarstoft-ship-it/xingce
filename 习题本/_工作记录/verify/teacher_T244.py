# T244 圆锥(高10)尖朝下漂浮露出 2；尖朝上时露出高度范围
H = 10.0
sub = ((H - 2) / H) ** 3          # 水下体积占比（尖朝下时水下是相似小锥）
top = 1 - sub                     # 尖朝上：水上部分是相似小锥
x = H * top ** (1/3)
ranges = {"A": (0, 6), "B": (6, 7), "C": (7, 8), "D": (8, H)}
hits = [k for k, (lo, hi) in ranges.items() if lo < x < hi]
assert len(hits) == 1, (x, hits)
print(hits[0])
