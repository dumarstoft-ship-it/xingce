# D01-math-h-v05  甲、乙两个合作社合并：种植户:养殖户 甲社2:1、乙社1:2，合并后5:4；
# 开设网店的比例：甲社种植户1/4、养殖户1/3，乙社种植户1/2、养殖户2/3。
# 求合并后开设网店的社员中种植户与养殖户的人数之比。
from fractions import Fraction as F
from math import gcd

OPTS = {'A': (1, 2), 'B': (3, 5), 'C': (3, 4), 'D': (4, 3)}
JIA, YI, MERGED = (2, 1), (1, 2), (5, 4)        # 种植户:养殖户
F_JIA = (F(1, 4), F(1, 3))                      # 甲社：种植户、养殖户中开网店的比例
F_YI = (F(1, 2), F(2, 3))                       # 乙社：种植户、养殖户中开网店的比例
N = 400


def split(n, r):
    zh = F(n * r[0], r[0] + r[1])
    return zh, n - zh


def shop_ratio(nj, ny):
    jz, jy = split(nj, JIA)
    yz, yy = split(ny, YI)
    a = jz * F_JIA[0] + yz * F_YI[0]
    b = jy * F_JIA[1] + yy * F_YI[1]
    r = a / b
    return (r.numerator, r.denominator)


# 穷举两社人数（各类人数、开网店人数都须为整数），只保留满足“合并后5:4”的组合
found = set()
for nj in range(1, N + 1):
    for ny in range(1, N + 1):
        jz, jy = split(nj, JIA)
        yz, yy = split(ny, YI)
        if any(v.denominator != 1 for v in (jz, jy, yz, yy)):
            continue
        if (jz + yz) * MERGED[1] != (jy + yy) * MERGED[0]:
            continue
        shops = [jz * F_JIA[0], jy * F_JIA[1], yz * F_YI[0], yy * F_YI[1]]
        if any(v.denominator != 1 for v in shops):
            continue
        a, b = int(shops[0] + shops[2]), int(shops[1] + shops[3])
        g = gcd(a, b)
        found.add((a // g, b // g))
assert len(found) == 1, found          # 无论两社具体人数是多少，答案唯一
ans = found.pop()
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits
vals = [F(*OPTS[k]) for k in 'ABCD']
assert vals == sorted(vals)            # 选项按数值从小到大

# 干扰项来源核对
assert shop_ratio(1, 1) == OPTS['B']   # 默认两社人数相等
assert shop_ratio(1, 2) == OPTS['A']   # 规模比对应反了（甲:乙误作1:2）
assert (ans[1], ans[0]) == OPTS['D']   # 比例颠倒
print('ratio', ans, '| equal-size', shop_ratio(1, 1), '| swapped-size', shop_ratio(1, 2))
print(hits[0])
