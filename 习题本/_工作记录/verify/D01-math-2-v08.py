# D01-math-2-v08 4篮+3足=960，3篮+4足=1000，求1篮+1足
from fractions import Fraction as Fr

opts = {'A': 40, 'B': 140, 'C': 160, 'D': 280}
e1 = (4, 3, 960)    # 第一次：4个篮球、3个足球，960元
e2 = (3, 4, 1000)   # 第二次：3个篮球、4个足球，1000元

# 克莱姆法则精确求解（单价不必是整数）
a1, b1, c1 = e1
a2, b2, c2 = e2
det = a1 * b2 - a2 * b1
assert det != 0
B = Fr(c1 * b2 - c2 * b1, det)
F = Fr(a1 * c2 - a2 * c1, det)
assert B > 0 and F > 0
ans = B + F

# 再用整数单价穷举交叉核对唯一性
grid = [(x, y) for x in range(1, 1001) for y in range(1, 1001)
        if a1 * x + b1 * y == c1 and a2 * x + b2 * y == c2]
assert grid == [(B, F)], grid

# 干扰项的错误路径
assert c2 - c1 == opts['A']                 # 两式相减得到的是差价
assert Fr(c1 + c2, 14) == opts['B']         # 除以球的总个数14
assert F == opts['C']                       # 只求出足球单价

hits = [k for k, v in opts.items() if v == ans]
assert len(hits) == 1, hits
print('basketball', B, 'football', F, 'sum', ans)
print(hits[0])
