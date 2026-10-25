# M06 排列组合：独立暴力验算所有真题（官方答案核对 + 3 道自解）
# 每题从题面数据出发枚举/计数，再映射到选项，断言恰好命中一个选项。
import itertools, json, math
from math import comb, perm, factorial
from fractions import Fraction as F

res = {}      # id -> (computed value, matched option)
def pick(val, opts):
    hits = [k for k, v in opts.items() if (v(val) if callable(v) else v == val)]
    assert len(hits) == 1, (val, opts, hits)
    return hits[0]
def rec(qid, val, opts):
    res[qid] = (val, pick(val, opts))

# ---------------- 自解 3 题 ----------------
# 2026GD-42 周一~周日选 3 天，任两次活动之间至少隔 1 天（不相邻）
v = sum(1 for s in itertools.combinations(range(7), 3) if all(s[i+1]-s[i] >= 2 for i in range(2)))
rec('2026GD-42', v, {'A':3,'B':5,'C':10,'D':15})

# 2026ZJA-51 2 行 3 列；张王前后相邻（同列不同行），李吴左右相邻（同行相邻列）
cells = [(r, c) for r in range(2) for c in range(3)]
cnt = 0
for p in itertools.permutations(cells):   # p[i] = 第 i 人的位置；0张 1王 2李 3吴 4,5 其他
    (r0,c0),(r1,c1),(r2,c2),(r3,c3) = p[0],p[1],p[2],p[3]
    if c0 == c1 and r0 != r1 and r2 == r3 and abs(c2-c3) == 1:
        cnt += 1
rec('2026ZJA-51', cnt, {'A':16,'B':32,'C':48,'D':96})

# 2026ZJA-61 先解部门人数：甲=(乙+丙)/2，乙=20%总，丙=甲+2；再每部门选 2~3 人共 8 人
sol = None
for a in range(1, 60):
    for b in range(1, 60):
        for c in range(1, 60):
            if 2*a == b+c and 5*b == a+b+c and c == a+2:
                assert sol is None; sol = (a, b, c)
a, b, c = sol
assert sol == (5, 3, 7)
v = sum(comb(a,x)*comb(b,y)*comb(c,z) for x in (2,3) for y in (2,3) for z in (2,3) if x+y+z == 8)
rec('2026ZJA-61', v, {'A':560,'B':780,'C':920,'D':1610})

# ---------------- 官方答案核对 ----------------
# 2022GD-34 甲乙丙共 12 份，每家 3~5 份（单位有区分 → 有序）
v = sum(1 for t in itertools.product(range(3,6), repeat=3) if sum(t) == 12)
v_unordered = sum(1 for t in itertools.combinations_with_replacement(range(3,6), 3) if sum(t) == 12)
rec('2022GD-34', v, {'A':2,'B':6,'C':7,'D':9})
res['2022GD-34'] += (f'无序理解={v_unordered}（=A项，题干"组合"一词有歧义）',)

# 2022HB-61 6 教师去 3 所学校，一所 1、一所 2、一所 3（名额固定 → 60；名额不固定 → 360）
fixed = sum(1 for f in itertools.product(range(3), repeat=6) if [f.count(k) for k in range(3)] == [1,2,3])
free = sum(1 for f in itertools.product(range(3), repeat=6) if sorted(f.count(k) for k in range(3)) == [1,2,3])
rec('2022HB-61', fixed, {'A':60,'B':120,'C':360,'D':720})
res['2022HB-61'] += (f'名额不固定理解={free}（=C项）',)

# 2022ZJA-56 6 滑雪 + 3 滑冰 选 6 项，每大项至少 1
items = ['S']*6 + ['K']*3
v = sum(1 for s in itertools.combinations(range(9), 6) if {items[i] for i in s} == {'S','K'})
rec('2022ZJA-56', v, {'A':83,'B':84,'C':92,'D':102})

# 2023GD-39 6 荤选 2、4 素选 2
v = sum(1 for _ in itertools.combinations(range(6), 2) for _ in itertools.combinations(range(4), 2))
rec('2023GD-39', v, {'A':42,'B':60,'C':72,'D':90})

# 2024GD-41 3 男 3 女选 4，女≥2
v = sum(1 for s in itertools.combinations(range(6), 4) if sum(1 for i in s if i >= 3) >= 2)
rec('2024GD-41', v, {'A':4,'B':8,'C':12,'D':16})

# 2024HB-68 部门人数 2,4,4，同部门连续 —— 用"部门块序列"枚举 10! 太慢，改为对部门标签序列枚举再乘组内全排
dept = [0]*2 + [1]*4 + [2]*4
labels = set(itertools.permutations(dept))
def contiguous(seq):
    seen, prev = set(), None
    for x in seq:
        if x != prev:
            if x in seen: return False
            seen.add(x); prev = x
    return True
v = sum(1 for L in labels if contiguous(L)) * factorial(2) * factorial(4) * factorial(4)
rec('2024HB-68', v, {'A':lambda x: x < 1000, 'B':lambda x: 1000 <= x <= 5000, 'C':lambda x: 5001 <= x <= 10000, 'D':lambda x: x > 10000})

# 2024SD-52 6 男 3 女选 3，男女都有
v = sum(1 for s in itertools.combinations(range(9), 3) if 0 < sum(1 for i in s if i >= 6) < 3)
rec('2024SD-52', v, {'A':63,'B':70,'C':73,'D':60})

# 2025SC-50 5 男 4 女：田径 2 男，篮球 1 男 1 女，跳水 2 女
sex = ['M']*5 + ['F']*4
v = 0
for f in itertools.product(range(4), repeat=9):  # 0 田径 1 篮球 2 跳水 3 不去
    g = [[sex[i] for i in range(9) if f[i] == k] for k in range(3)]
    if sorted(g[0]) == ['M','M'] and sorted(g[1]) == ['F','M'] and sorted(g[2]) == ['F','F']:
        v += 1
rec('2025SC-50', v, {'A':300,'B':320,'C':360,'D':400})

# 2025SD-54 8 人 8 道：名次 1-4 → 道 3-6，名次 5-6 → 道 7-8，名次 7-8 → 道 1-2
v = 0
for p in itertools.permutations(range(1, 9)):  # p[k] = 第 k+1 名的道次
    if set(p[:4]) == {3,4,5,6} and set(p[4:6]) == {7,8} and set(p[6:]) == {1,2}:
        v += 1
rec('2025SD-54', v, {'A':48,'B':72,'C':96,'D':120})

# 2026CQ-61 2 数学 + 4 英语，A、B 各 3 人，A 至少 1 数学
v = sum(1 for s in itertools.combinations(range(6), 3) if any(i < 2 for i in s))
rec('2026CQ-61', v, {'A':9,'B':12,'C':16,'D':20})

# 2026CQ-62 两侧各 3 个展位，6 家不同企业（数字 3 家、AI 3 家），数字企业不能都在同一侧
v = 0
for p in itertools.permutations(range(6)):  # p[企业] = 展位，展位 0-2 左侧 3-5 右侧
    sides = {p[i] // 3 for i in range(3)}
    if len(sides) == 2: v += 1
rec('2026CQ-62', v, {'A':244,'B':648,'C':684,'D':720})

# 2020HB-64 6 箱不同水果，A1 B2 C3，三个不同配送员各去一个仓储点
v = sum(1 for f in itertools.product(range(3), repeat=6) if [f.count(k) for k in range(3)] == [1,2,3]) * factorial(3)
rec('2020HB-64', v, {'A':60,'B':180,'C':360,'D':420})

# 2020SC1206-42 17 件相同产品分给 3 人，每人≥4；时长 = 最大份额；问时长有几种可能
maxes = {max(t) for t in itertools.product(range(4, 18), repeat=3) if sum(t) == 17}
rec('2020SC1206-42', len(maxes), {'A':9,'B':8,'C':4,'D':3})

# 2020SZS-19 1-12 号，夫妻各选一条（有序），号码差≥3
v = sum(1 for x in range(1,13) for y in range(1,13) if abs(x-y) >= 3)
rec('2020SZS-19', v, {'A':56,'B':72,'C':90,'D':111})

# 2021JSA-58 课程组合 af, df, ace, bcf；连续 6 天（7 天中选连续 6 天 → 2 个窗口），每人不连续两天考
groups = ['af','df','ace','bcf']
bad = set()
for g in groups:
    for x, y in itertools.combinations(g, 2):
        bad.add(frozenset((x, y)))
orders = [p for p in itertools.permutations('abcdef') if all(frozenset((p[i], p[i+1])) not in bad for i in range(5))]
windows = sum(1 for s in range(7) if s + 6 <= 7)
v = len(orders) * windows
rec('2021JSA-58', v, {'A':2,'B':4,'C':8,'D':12})

# 2021SC2-48 6 人：先容斥定技能；甲乙各 2 人需覆盖农牧渔，丙 2 人不能含渔且需覆盖农牧
# 技能：农 3、牧 3、渔 2；农牧双能 2 人；渔业者不精通农牧 → 枚举所有满足统计的技能分配，取唯一解
people_skills = None
opts_sets = [frozenset(s) for s in [{'N'},{'M'},{'Y'},{'N','M'},{'N','Y'},{'M','Y'},{'N','M','Y'}]]
sols = set()
for combo in itertools.combinations_with_replacement(range(len(opts_sets)), 6):
    ss = [opts_sets[i] for i in combo]
    if sum('N' in s for s in ss) == 3 and sum('M' in s for s in ss) == 3 and sum('Y' in s for s in ss) == 2 \
       and sum(s == {'N','M'} or s == {'N','M','Y'} for s in ss) >= 0 \
       and sum({'N','M'} <= s for s in ss) == 2 and all(not ('Y' in s and ({'N','M'} & s)) for s in ss):
        sols.add(tuple(sorted(tuple(sorted(s)) for s in ss)))
assert len(sols) == 1, sols
ss = [frozenset(s) for s in list(sols)[0]]
v = 0
for f in itertools.product(range(3), repeat=6):   # 0 甲 1 乙 2 丙
    if [f.count(k) for k in range(3)] != [2,2,2]: continue
    cov = [frozenset().union(*[ss[i] for i in range(6) if f[i] == k]) for k in range(3)]
    if cov[0] == {'N','M','Y'} and cov[1] == {'N','M','Y'} and cov[2] == {'N','M'}:
        v += 1
rec('2021SC2-48', v, {'A':4,'B':8,'C':15,'D':20})

# 2021ZJA-73 周长 260 面积 3600 → 长宽；10 米小方格；选 3 块两两不同行不同列
L = W = None
for l in range(1, 131):
    w = 130 - l
    if l * w == 3600 and l >= w: L, W = l, w
R, C = W // 10, L // 10
sq = [(r, c) for r in range(R) for c in range(C)]
v = sum(1 for s in itertools.combinations(sq, 3) if len({x[0] for x in s}) == 3 and len({x[1] for x in s}) == 3)
rec('2021ZJA-73', v, {'A':lambda x: x < 200, 'B':lambda x: 200 <= x <= 400, 'C':lambda x: 400 < x <= 800, 'D':lambda x: x > 800})

# 2022GK-69 6 专家平均分 2 组（无序），每组都要有环保、旅游、社媒
env, tour, soc = set('甲乙丙'), set('丁戊己'), set('甲丁戊')
allp = list('甲乙丙丁戊己')
v = 0
for g in itertools.combinations(allp, 3):
    if '甲' not in g: continue          # 固定甲所在组，消除两组顺序
    h = set(allp) - set(g)
    if all(set(x) & env and set(x) & tour and set(x) & soc for x in (g, h)):
        v += 1
rec('2022GK-69', v, {'A':12,'B':24,'C':4,'D':8})

# 2022SD-45 10:00:00~10:30:00 六个数字互不相同
v = 0
for t in range(10*3600, 10*3600 + 30*60 + 1):
    h, m, s = t // 3600, (t // 60) % 60, t % 60
    d = f'{h:02d}{m:02d}{s:02d}'
    if len(set(d)) == 6: v += 1
rec('2022SD-45', v, {'A':45,'B':90,'C':120,'D':210})

# 2022ZJA-64 两排各 4 车位，4 辆不同车；不能 4 车同排；甲乙同排
v = 0
for p in itertools.permutations(range(8), 4):   # p[0]甲 p[1]乙
    rows = [x // 4 for x in p]
    if rows[0] == rows[1] and len(set(rows)) == 2: v += 1
rec('2022ZJA-64', v, {'A':672,'B':480,'C':384,'D':288})

# 2023GK-68 5 个相邻铺位；餐厅 R1R2 各租 1 或 2 个相邻铺位，水果店 F1F2 各 1；铺位租完；同类不相邻
v = 0
tenants = ['R1','R2','F1','F2']
for order in itertools.permutations(tenants):
    for sizes in itertools.product((1,2), (1,2)):
        sz = {'R1': sizes[0], 'R2': sizes[1], 'F1': 1, 'F2': 1}
        if sum(sz.values()) != 5: continue
        # 同类型的两个租户之间至少隔 1 个铺位 ⇔ 两者在块序列中不相邻
        ok = all(order[i][0] != order[i+1][0] for i in range(3))
        if ok: v += 1
rec('2023GK-68', v, {'A':24,'B':48,'C':8,'D':16})

# 2023HB-65 10 国内 4 国外，选 3 家，国内外都有，且国内外交叉提问（相邻不同类）
kinds = ['D']*10 + ['F']*4
v = sum(1 for p in itertools.permutations(range(14), 3)
        if len({kinds[i] for i in p}) == 2 and all(kinds[p[i]] != kinds[p[i+1]] for i in range(2)))
rec('2023HB-65', v, {'A':240,'B':360,'C':480,'D':1440})

# 2023HB-68 七巧板 7 区面积：按图坐标计算（正方形边长 4）
def tri(a, b, c):
    return abs((b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])) / 2
def poly(pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i+1) % len(pts)]
        s += x1*y2 - x2*y1
    return abs(s) / 2
area = {
    1: tri((0,4),(4,4),(2,2)),
    2: tri((4,4),(4,0),(2,2)),
    3: tri((2,2),(2,0),(4,0)),
    4: tri((1,1),(2,2),(2,0)),
    5: tri((0,2),(0,0),(2,0)),
    6: poly([(0,2),(1,3),(2,2),(1,1)]),
    7: tri((0,4),(1,3),(0,2)),
}
assert abs(sum(area.values()) - 16) < 1e-9
v = sum(1 for p in itertools.permutations(area, 3) if len({area[i] for i in p}) == 3)
rec('2023HB-68', v, {'A':48,'B':72,'C':96,'D':192})

# 2023SC-55 A-B-C-D-A 四边形环（A 与 C、B 与 D 不相邻），4 色
adj = [('A','B'),('B','C'),('C','D'),('D','A')]
v = 0
for col in itertools.product(range(4), repeat=4):
    m = dict(zip('ABCD', col))
    if all(m[x] != m[y] for x, y in adj): v += 1
rec('2023SC-55', v, {'A':84,'B':64,'C':36,'D':24})

# 2024GK-68 团队 1-6 分到甲乙两课题，各≥2，各选一个负责团队且不是本课题最小编号
v = 0
for f in itertools.product(range(2), repeat=6):
    g = [[i+1 for i in range(6) if f[i] == k] for k in range(2)]
    if min(len(g[0]), len(g[1])) < 2: continue
    v += (len(g[0]) - 1) * (len(g[1]) - 1)
rec('2024GK-68', v, {'A':300,'B':340,'C':150,'D':170})

# 2024HB-66 4 人 4 基地，至少 3 人选不同基地 ⇔ 不同基地数≥3
v = sum(1 for f in itertools.product(range(4), repeat=4) if len(set(f)) >= 3)
rec('2024HB-66', v, {'A':24,'B':60,'C':144,'D':168})

# 2024HB-72 5 人 3 舱，每舱≥1，甲不去天和(0)
v = sum(1 for f in itertools.product(range(3), repeat=5) if len(set(f)) == 3 and f[0] != 0)
rec('2024HB-72', v, {'A':72,'B':88,'C':100,'D':144})

# 2024JSA-62 5 人去 4 城：一线 0,1 各≥1；二线 2,3 各恰 1
v = sum(1 for f in itertools.product(range(4), repeat=5) if f.count(0) >= 1 and f.count(1) >= 1 and f.count(2) == 1 and f.count(3) == 1)
rec('2024JSA-62', v, {'A':60,'B':72,'C':120,'D':144})

# 2024SZ-55 飞镖盘分值 30,25,20,15,10,5,4,1 及脱靶 0；三镖共 30 分，无序得分组合
scores = [30,25,20,15,10,5,4,1,0]
v = sum(1 for t in itertools.combinations_with_replacement(scores, 3) if sum(t) == 30)
rec('2024SZ-55', v, {'A':6,'B':7,'C':8,'D':9})

# 2024ZJA-70 共 10 串，每次 1~3 串（有序拿法）
def comps(n, parts):
    if n == 0: return 1
    return sum(comps(n-k, parts) for k in parts if k <= n)
rec('2024ZJA-70', comps(10, (1,2,3)), {'A':44,'B':81,'C':149,'D':274})

# 2025GK-72 5 题，对 +1 错 -1，每题后得分≥1
v = 0
for seq in itertools.product((1,-1), repeat=5):
    s, ok = 0, True
    for x in seq:
        s += x
        if s < 1: ok = False; break
    v += ok
rec('2025GK-72', v, {'A':7,'B':6,'C':4,'D':3})

# 2025HB-66 6 人去 A,B,C：A≥2，B≥1，C≥1
v = sum(1 for f in itertools.product(range(3), repeat=6) if f.count(0) >= 2 and f.count(1) >= 1 and f.count(2) >= 1)
rec('2025HB-66', v, {'A':180,'B':320,'C':345,'D':360})

# 2025HB-69 13 种蔬果分值 5×2,4×4,3×3,2×4；选 3 种总分≥13
sc = [5]*2 + [4]*4 + [3]*3 + [2]*4
v = sum(1 for s in itertools.combinations(range(13), 3) if sum(sc[i] for i in s) >= 13)
rec('2025HB-69', v, {'A':21,'B':19,'C':16,'D':13})

# 2025HB-70 5 景点门票 10,10,20,20,20；花 40 元依次游览不同景点（有序）
price = [10,10,20,20,20]
v = sum(1 for k in range(1,6) for p in itertools.permutations(range(5), k) if sum(price[i] for i in p) == 40)
rec('2025HB-70', v, {'A':6,'B':18,'C':24,'D':60})

# 2025JSA-64 舞蹈W 歌曲S1 S2 小品X 魔术M 杂技Z；歌曲开头结尾；W、Z 相邻；X、M 不相邻
v = 0
for p in itertools.permutations(['W','S1','S2','X','M','Z']):
    if {p[0], p[5]} != {'S1','S2'}: continue
    iw, iz, ix, im = p.index('W'), p.index('Z'), p.index('X'), p.index('M')
    if abs(iw-iz) == 1 and abs(ix-im) != 1: v += 1
rec('2025JSA-64', v, {'A':8,'B':12,'C':18,'D':24})

# 2020SD-44 3×3 白纸，2 红 1×1、3 黄 1×1、2 绿 1×2；图案轴对称；旋转重合视为同一种
cells9 = [(r, c) for r in range(3) for c in range(3)]
dominoes = []
for r in range(3):
    for c in range(3):
        if c + 1 < 3: dominoes.append(frozenset({(r,c),(r,c+1)}))
        if r + 1 < 3: dominoes.append(frozenset({(r,c),(r+1,c)}))
patterns = set()
for d1, d2 in itertools.combinations(dominoes, 2):
    if d1 & d2: continue
    rest = [x for x in cells9 if x not in d1 | d2]
    for reds in itertools.combinations(rest, 2):
        g = {}
        for x in d1 | d2: g[x] = 'G'
        for x in rest: g[x] = 'R' if x in reds else 'Y'
        # 图案按"颜色+纸片边界"记录（纸片拼缝可见与否不影响本题结果，下面两种口径都算）
        patterns.add((tuple(g[x] for x in cells9), frozenset({d1, d2})))
def tr(f, key):
    cols, doms = key
    m = dict(zip(cells9, cols))
    newm = {f(x): m[x] for x in cells9}
    return (tuple(newm[x] for x in cells9), frozenset(frozenset(f(x) for x in d) for d in doms))
rot = lambda x: (x[1], 2 - x[0])
refs = [lambda x: (x[0], 2 - x[1]), lambda x: (2 - x[0], x[1]), lambda x: (x[1], x[0]), lambda x: (2 - x[1], 2 - x[0])]
def canon(key, use_doms=True):
    ks = []
    k = key
    for _ in range(4):
        ks.append(k if use_doms else (k[0], None)); k = tr(rot, k)
    return min(ks, key=lambda z: (z[0], str(sorted(sorted(d) for d in z[1])) if z[1] else ''))
def symmetric(key, use_doms=True):
    for f in refs:
        k2 = tr(f, key)
        if (k2[0] == key[0]) and (not use_doms or k2[1] == key[1]): return True
    return False
cls_with = {canon(k) for k in patterns if symmetric(k)}
cls_color = {(canon(k)[0]) for k in patterns if symmetric(k, use_doms=False)}
# 颜色口径：只看颜色网格（同色纸拼缝不可见）
color_grids = {k[0] for k in patterns}
def ctr(f, cols):
    m = dict(zip(cells9, cols)); newm = {f(x): m[x] for x in cells9}
    return tuple(newm[x] for x in cells9)
def ccanon(cols):
    ks, k = [], cols
    for _ in range(4): ks.append(k); k = ctr(rot, k)
    return min(ks)
sym_color = {ccanon(cg) for cg in color_grids if any(ctr(f, cg) == cg for f in refs)}
rec('2020SD-44', len(sym_color), {'A':11,'B':10,'C':5,'D':4})
res['2020SD-44'] += (f'按纸片边界口径={len(cls_with)}',)

# 2020ZJB-16 1-9 中选 4 张排成四位数，能被 75 整除
v = sum(1 for p in itertools.permutations(range(1,10), 4) if int(''.join(map(str,p))) % 75 == 0)
rec('2020ZJB-16', v, {'A':lambda x: x < 15, 'B':lambda x: 15 <= x <= 20, 'C':lambda x: 21 <= x <= 25, 'D':lambda x: x > 25})

# 2022JSA-65 3 公司各 2 人，同公司不相邻
v = sum(1 for p in itertools.permutations(['A1','A2','B1','B2','C1','C2']) if all(p[i][0] != p[i+1][0] for i in range(5)))
rec('2022JSA-65', v, {'A':80,'B':120,'C':160,'D':240})

# 2022SC2-48 三个两位数，十位个位恰用 1-6 各一次；乙=平均数；甲最小
v = 0
for p in itertools.permutations(range(1,7)):
    nums = [10*p[0]+p[1], 10*p[2]+p[3], 10*p[4]+p[5]]   # 甲 乙 丙
    jia, yi, bing = nums
    if 3*yi == sum(nums) and jia == min(nums): v += 1
rec('2022SC2-48', v, {'A':3,'B':6,'C':8,'D':12})

# 2023GK-69 10 户各 1 份；100/150 元两种；总预算≤1250；150 元礼包优先给 3 户孤寡老人
v = 0
for x in range(0, 11):
    if 150*x + 100*(10-x) > 1250: continue
    # 发放对象：x 户拿 150 元。优先规则：若 x≤3，则 x 户全部来自孤寡 3 户；若 x>3，孤寡 3 户全拿且另 x-3 户来自其余 7 户
    for S in itertools.combinations(range(10), x):   # 0,1,2 为孤寡
        k = sum(1 for i in S if i < 3)
        if k == min(x, 3): v += 1
rec('2023GK-69', v, {'A':21,'B':28,'C':36,'D':55})

# 2023JSA-60 4 天，每天 2 类，5 类都要展出，同类不连续 2 天，玉器(2)国画(4)不在第 1 天
pairs = list(itertools.combinations(range(5), 2))   # 0 青铜 1 瓷 2 玉 3 书法 4 国画
v = 0
for seq in itertools.product(pairs, repeat=4):
    if 2 in seq[0] or 4 in seq[0]: continue
    if any(set(seq[i]) & set(seq[i+1]) for i in range(3)): continue
    if set().union(*map(set, seq)) != set(range(5)): continue
    v += 1
rec('2023JSA-60', v, {'A':72,'B':120,'C':216,'D':360})

# 2023ZJA-61 甲乙丙丁戊 5 门课排 4 个学期，每学期≥1；甲单独一学期；乙丙不在第 1、4 学期；丁在戊和甲之后
v = 0
for f in itertools.product(range(4), repeat=5):   # 0甲 1乙 2丙 3丁 4戊
    if len(set(f)) != 4: continue
    if any(f[i] == f[0] for i in range(1,5)): continue
    if f[1] in (0,3) or f[2] in (0,3): continue
    if not (f[3] > f[4] and f[3] > f[0]): continue
    v += 1
rec('2023ZJA-61', v, {'A':5,'B':6,'C':7,'D':8})

# 2023ZJA-70 12 人纵队重排，新号与原号相差≤1，且与原队不同
def count_perm(n):
    cnt = 0
    def bt(i, used):
        nonlocal cnt
        if i == n: cnt += 1; return
        for j in (i-1, i, i+1):
            if 0 <= j < n and not (used >> j) & 1:
                bt(i+1, used | (1 << j))
    bt(0, 0)
    return cnt
rec('2023ZJA-70', count_perm(12) - 1, {'A':155,'B':227,'C':232,'D':239})

# 2024ZJA-69 6 人一排：恰 2 人坐回原位；相邻且互换座位的恰好 1 对（其余 2 人坐错）
v = 0
for p in itertools.permutations(range(6)):
    fixed = sum(1 for i in range(6) if p[i] == i)
    adj_swaps = sum(1 for i in range(5) if p[i] == i+1 and p[i+1] == i)
    if fixed == 2 and adj_swaps == 1: v += 1
rec('2024ZJA-69', v, {'A':12,'B':18,'C':24,'D':36})

# 2025GD-42 3 软、2 硬、2 双能；甲乙两队，每队恰 2 人能软、恰 2 人能硬；不要求全派
cap = [('S',)]*3 + [('H',)]*2 + [('S','H')]*2
v = 0
for f in itertools.product(range(3), repeat=7):  # 0 甲 1 乙 2 不派
    ok = True
    for t in range(2):
        mem = [cap[i] for i in range(7) if f[i] == t]
        if sum('S' in m for m in mem) != 2 or sum('H' in m for m in mem) != 2: ok = False; break
    v += ok
rec('2025GD-42', v, {'A':30,'B':42,'C':70,'D':144})

# 2025GK-77 甲乙设备各 5 件分给 A,B,C；每车间两种各≥1；A 总数严格多于 B、C；B 的甲>乙
v = 0
for a in itertools.product(range(1,6), repeat=3):
    if sum(a) != 5: continue
    for b in itertools.product(range(1,6), repeat=3):
        if sum(b) != 5: continue
        tot = [a[i]+b[i] for i in range(3)]
        if tot[0] > tot[1] and tot[0] > tot[2] and a[1] > b[1]: v += 1
rec('2025GK-77', v, {'A':3,'B':6,'C':12,'D':24})

# 2021ZJA-73 等已覆盖；2021GK-61、2021SD-45 官方答案识别中，按任务要求不解

off = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/tasks_in/M06.json'))
offmap = {q['id']: q['answer_official'] for q in off['real']}
bad = []
for qid, r in res.items():
    o = offmap.get(qid)
    flag = '' if (o is None or o == r[1]) else '  <-- 与官方不符'
    if flag: bad.append(qid)
    print(f'{qid:15s} 计算={r[0]!s:>6}  选项={r[1]}  官方={o}{flag}  {" ".join(map(str, r[2:]))}')
print('checked', len(res), 'mismatch', bad)
