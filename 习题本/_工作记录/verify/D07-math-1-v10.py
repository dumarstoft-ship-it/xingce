# D07-math-1-v10: 荷花高出水面 0.5 米，吹斜后花朵贴水面、水平移动 1.5 米，求水深
from fractions import Fraction as F

ABOVE, SHIFT = F(1, 2), F(3, 2)
roots = []
for k in range(1, 5001):                  # 水深以 0.01 米为步长穷举
    x = F(k, 100)
    stem = x + ABOVE                      # 花茎长度不变
    if x * x + SHIFT * SHIFT == stem * stem:
        roots.append(x)
assert len(roots) == 1, roots
depth = roots[0]
opts = {'A': 2, 'B': 2.25, 'C': 2.5, 'D': 4}
hit = [k for k, v in opts.items() if v == depth]
assert len(hit) == 1, (depth, hit)
print('水深 =', depth)
print(hit[0])
