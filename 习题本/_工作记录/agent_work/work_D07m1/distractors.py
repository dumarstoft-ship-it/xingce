# 核对每道题干扰项确实来自解析里写明的错误路径（工作文件，不参与 check_gen）
import math
from fractions import Fraction as F
pi, sq = math.pi, math.sqrt
def near(a, b, tol=1e-9): assert abs(a - b) <= tol, (a, b)
# v01 缩短 2 米、减少 44
near(2 * ((44 + 4) / 2), 48)          # 正解 2(l+w)-4=44
near(2 * ((44 - 4) / 2), 40)          # 照搬扩大时 +4
near(2 * (44 / 2), 44)                # 忽略角块
near((44 + 4) / 2, 24)                # 只求出 l+w
# v02
near(3.14 * 7 * 1.25, 27.475); near(2 * 3.14 * 6 * 1.25, 47.1); near(2 * 3.14 * 8 * 1.25, 62.8); near(2 * 3.14 * 7 * 1.25, 54.95)
# v03
near(2 * (8 + 0.6 + 5 + 0.6), 28.4); near(26 + 2 * pi * 0.6, 26 + 1.2 * pi)
# v04
V = pi * 36 * 9
near(V / (pi * 81), 4); near(V / (pi * 18 ** 2 / 3), 3); near(9 * 3, 27); near(V / (pi * 81 / 3), 12)
# v05 t=0.5, S=24
x = sq(24); near(x, 2 * sq(6))                         # 只少一个面
near(-1 + sq(1 + 24), 4)                               # x²+2x=24（忘了截面补回）
near(24 / 4, 6)                                        # 4x=24（漏乘厚度）
# v06
cone, ball = pi * 36 * 8 / 3, 4 / 3 * pi * 8
assert math.floor(cone * 0.9 / ball) == 8 and abs(cone / ball - 9) < 1e-9
assert math.floor(3 * cone * 0.9 / ball) == 24 and abs(3 * cone / ball - 27) < 1e-9
# v07
near(8000 / 1200, 20 / 3); near(400 * 8 / 1200, 8 / 3); near(1200 * 8 / 800, 12)
assert 8 + 20 / 3 < 20                                  # 完全浸没假设不成立
near(20 - 12, 8); assert 20 - 12 != 4                  # 露出高度 8 与正确答案 4 不同，不会“错路得对答案”
# v08
near(2 * sq(25 - 16), 6)
# v09
ex, ey = 25 / 13, 60 / 13
near(0.5 * 13 * ex, 12.5); near(0.5 * 13 * ey, 30); near(0.5 * 13 * (13 - ey), 54.5); near(0.5 * 13 * (13 - ex), 72)
# v10
near((1.5 ** 2 - 0.5 ** 2) / (2 * 0.5), 2); near(1.5 ** 2 / 1, 2.25)  # 漏 0.5²：2.25 = x
near(2 + 0.5, 2.5)
# 错误展开 (x+0.5)² = x²+0.5x+0.25 ⇒ 2.25 = 0.5x+0.25 ⇒ x=4
near((2.25 - 0.25) / 0.5, 4)
# v11 因数对
pairs = [(d, 144 // d) for d in range(1, 13) if 144 % d == 0 and d < 144 // d]
assert len(pairs) == 7
assert len([p for p in pairs if (p[0] - p[1]) % 2 == 0]) == 4
# v12
near(2 * 8 * math.sin(math.radians(60)) / 2, 4 * sq(3))   # 只算半个底边
# v13
near(sq(39 ** 2 - 15 ** 2), 36); near(sq(25 ** 2 - 15 ** 2), 20); near(39 - 25, 14); near(36 - 20, 16)
# v14
near(6 * 8 / 10, 4.8); near((6 + 8 - 10) / 2, 2); near(sq(36 + 64), 10)
# v15
near(140 / 70, 2); near(140 / 10, 14); near(140 / 40, 3.5); near(140 / sq(30 ** 2 + 40 ** 2), 2.8)
print('all distractor paths ok')
