# 核对解析里写到的各条"错误路径"数值（与验算脚本分开）
from math import comb, perm, factorial as F
from itertools import permutations, combinations
ok = lambda name, got, exp: print(('OK  ' if got == exp else 'BAD ') + name, got, exp)

# v01 用排列列式无整数解
ok('v01 A式无解', [h for h in range(3, 30) if perm(h, 2) * perm(h - 2, 2) == 210], [])
ok('v01 荤6', comb(6, 2) * comb(4, 2), 90); ok('v01 荤8', comb(8, 2) * comb(6, 2), 420); ok('v01 荤4', comb(4, 2) * comb(2, 2), 6)
# v02
ok('v02 原题口径', comb(5, 2) * 3 * 4 * comb(3, 2), 360)
ok('v02 跳水也排', perm(5, 2) * 3 * 4 * perm(3, 2), 1440)
ok('v02 篮球男仍从5人选', perm(5, 2) * 5 * 4 * comb(3, 2), 1200)
# v03
ok('v03 忽略衔接', (3 + 2) * 2 + 2, 12); ok('v03 漏直达', 3 * 2 + 2 * 1, 8); ok('v03 漏乘口岸', 3 + 2 + 2, 7)
# v04
ok('v04 忘队长', comb(3, 2) * comb(3, 2) + comb(3, 3) * comb(3, 1), 12)
ok('v04 漏3女1男', comb(3, 2) * comb(3, 2) * 2, 18)
ok('v04 队长从3男选', 12 * 3, 36)
# v05 捆绑忘了甲乙互换
adj_no_order = 3 * 2                  # 3 个相邻道次对 × 另两人 2!
ok('v05 忘互换', (24 - adj_no_order) * 2 * 2, 72); ok('v05 忽略限制', 24 * 4, 96)
# v06
ok('v06 男女都有', comb(9, 3) - comb(6, 3) - comb(3, 3), 63); ok('v06 反面找成全女', comb(9, 3) - 1, 83)
ok('v06 只算2男1女', comb(6, 2) * 3, 45)
# v07
ok('v07 正面', 3 * 5**2 * 3 + 3 * 5 * 3**2, 360); ok('v07 只减全数字', 8**3 - 5**3, 387); ok('v07 只减全字母', 8**3 - 3**3, 485)
# v08
ok('v08 x=6', comb(6, 2) * 4 + 6 * comb(4, 2), 96)
ok('v08 方程', [x for x in range(1, 20) if x * (x + 2) == 35], [5])
ok('v08 只减全男无解', [x for x in range(1, 30) if comb(x + 4, 3) - comb(x, 3) == 70], [])
# v09
ok('v09 正面', comb(4, 2) * 3 * 2 + 4 * comb(3, 2) * 2 + 4 * 3 * 1, 72)
ok('v09 缺一地之和', comb(5, 4) + comb(6, 4) + comb(7, 4), 55)
ok('v09 忘加回', comb(9, 4) - 55, 71); ok('v09 保底法', 4 * 3 * 2 * 6, 144); ok('v09 只算粤2', comb(4, 2) * 3 * 2, 36)
# v10
ok('v10 忘加回', 720 - 240, 480); ok('v10 漏甲在最右', 4 * 4 * F(4), 384); ok('v10 比例', 720 * 25 / 36, 500)
ok('v10 分类合计', F(5) + 4 * 4 * F(4), 504)
# v11
ok('v11 不定位', F(3) * 2 * 6 * 6, 432); ok('v11 两端', 2 * 2 * 72, 288); ok('v11 忘排后两块', 72, 72)
# v12 把剩下4座当连续一排
ok('v12 连续一排', F(3) * F(2) * 2, 24); ok('v12 忘副职', 16 // 2, 8)
# v13
cars = ["动1", "动2", "餐", "客1", "客2", "客3"]
def train(front_only=False, two_bad=False):
    c = 0
    for p in permutations(cars):
        d1, d2, x = p.index("动1"), p.index("动2"), p.index("餐")
        if abs(d1 - d2) != 1: continue
        ends = ({0, 1},) if front_only else ({0, 1}, {4, 5})
        if {d1, d2} not in ends: continue
        bad = {min(d1, d2) - 1, max(d1, d2) + 1}
        if two_bad:  # 误以为两侧都有邻位：除紧挨的一节外再多排除一个位置
            bad = {2, 3} if {d1, d2} == {0, 1} else {2, 3}
        if x in bad: continue
        c += 1
    return c
ok('v13 只算车头', train(front_only=True), 36); ok('v13 餐车只剩2位', train(two_bad=True), 48)
# v14
p5 = list(permutations("甲乙丙丁戊"))
def pairs(p): 
    pos = sorted(p.index(x) for x in "甲乙丙")
    return sum(1 for a, b in combinations(pos, 2) if b - a == 1)
ok('v14 两两不相邻', sum(pairs(p) == 0 for p in p5), 12); ok('v14 三人连排', sum(pairs(p) == 2 for p in p5), 36)
ok('v14 只捆两人全排', comb(3, 2) * 2 * F(4), 144)
ok('v14 144=恰两+2*三连', 72 + 2 * 36, 144); ok('v14 减一次', 144 - 36, 108); ok('v14 漏减不相邻', 120 - 36, 84)
# v15
exact = sum(1 for s in combinations(range(7), 3) if all(s[i+1] - s[i] == 2 for i in range(2)))
ok('v15 恰好间隔', exact * 6, 18); ok('v15 只算日期', comb(5, 3), 10); ok('v15 4个空', comb(4, 3) * 6, 24)
# v16
ok('v16 忘排除周六', sum(1 for s in combinations(range(6), 2) if s[1] - s[0] >= 2), 10)
ok('v16 当成环形', sum(1 for s in combinations(range(1, 5), 2) if s[1] - s[0] >= 2), 3)   # 周二至周五选2
ok('v16 不管相邻', comb(6, 2), 15)
ok('v16 枚举', [s for s in combinations(range(1, 6), 2) if s[1] - s[0] >= 2],
   [(1, 3), (1, 4), (1, 5), (2, 4), (2, 5), (3, 5)])
# v17
ok('v17 首尾可关', sum(1 for s in combinations(range(10), 3) if all(b - a >= 2 for a, b in combinations(s, 2))), 56)
ok('v17 忽略不相邻', comb(8, 3), 56); ok('v17 无限制', comb(10, 3), 120)
# v18
ok('v18 忽略甲', F(4) * F(3), 144); ok('v18 乘2', 2 * 108, 216); ok('v18 两错', 2 * 144, 288)
# v19
ok('v19 当不相邻', sum(1 for s in combinations(range(1, 16), 4) if all(s[i+1] - s[i] >= 2 for i in range(3))), 495)
ok('v19 4次都锁', comb(7, 4), 35); ok('v19 公式', comb(15 - 3 * 2, 4), 126)
# v20
ok('v20 无序', sum(1 for s in combinations(range(1, 13), 3) if all(b - a >= 3 for a, b in combinations(s, 2))), 56)
ok('v20 当成隔3间(差>=4)', sum(1 for s in combinations(range(1, 13), 3) if all(b - a >= 4 for a, b in combinations(s, 2))), 20)
ok('v20 差>=4再排序', 20 * 6, 120)
# 2026GD-42
ok('real 恰好间隔', exact, 3)
ok('real 三种', [s for s in combinations(range(1, 8), 3) if all(s[i+1] - s[i] == 2 for i in range(2))], [(1, 3, 5), (2, 4, 6), (3, 5, 7)])
