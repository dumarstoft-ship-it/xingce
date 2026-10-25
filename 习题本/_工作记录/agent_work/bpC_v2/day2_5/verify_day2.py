# -*- coding: utf-8 -*-
"""第2天（C02 首次）改编骨架验算。"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bpC_v2')
from lib import *
from itertools import permutations, product, combinations

# ---------- G1-a 2023SZ-39 变式：不能推出（2 解）
P = ['甲', '乙', '丙']
S = []
for o in permutations(['广州', '汕头', '湛江']):
    O = dict(zip(P, o))
    for r in permutations([1, 2, 3]):
        R = dict(zip(P, r)); byO = {O[x]: R[x] for x in P}
        if O['乙'] == '湛江' or byO['湛江'] != 1 or R['丙'] == 1 or byO['广州'] == 3: continue
        S.append((O, R))
print('G1-a 解', S)
judge('D2-G1a', S, {'A': lambda x: x[0]['甲'] == '湛江',
                    'B': lambda x: {x[0][p]: x[1][p] for p in P}['广州'] == 2,
                    'C': lambda x: {x[0][p]: x[1][p] for p in P}['汕头'] == 3,
                    'D': lambda x: x[1]['乙'] == 2}, 'notmust', 'D')

# ---------- G1-b 熟悉表：能确定几人
tab = {'小林': {'采集'}, '小许': {'采集', '调解'}, '老郑': {'代办', '巡查'},
       '小冯': {'代办', '巡查', '调解'}, '老何': {'采集', '代办', '巡查', '宣传'}}
T = ['采集', '代办', '调解', '巡查', '宣传']
M = [dict(zip(tab, p)) for p in permutations(T) if all(p[i] in tab[k] for i, k in enumerate(tab))]
print('G1-b 方案', M)
fixed = [k for k in tab if len({m[k] for m in M}) == 1]
count_options('D2-G1b', len(fixed), {'A': 2, 'B': 3, 'C': 4, 'D': 5}, 'B')

# ---------- G1-c 二选一成环 + 条件句
tab = {'甲': {'非遗', '侨批'}, '乙': {'侨批', '海丝'}, '丙': {'海丝', '科技'}, '丁': {'科技', '湾区'}, '戊': {'湾区', '非遗'}}
T = ['非遗', '侨批', '海丝', '科技', '湾区']
M0 = [dict(zip(tab, p)) for p in permutations(T) if all(p[i] in tab[k] for i, k in enumerate(tab))]
M = [m for m in M0 if (m['乙'] != '侨批') or (m['丁'] == '湾区')]
print('G1-c 基础方案', M0, '加条件后', M)
judge('D2-G1c', M, {'A': lambda m: m['甲'] == '非遗', 'B': lambda m: m['丙'] == '科技',
                    'C': lambda m: m['戊'] == '湾区', 'D': lambda m: m['乙'] == '侨批'}, 'must', 'B')

# ---------- G1-d 补哪条信息可唯一确定
tab = {'甲': {'登记', '审核'}, '乙': {'登记', '回访', '发证'}, '丙': {'登记', '回访'}, '丁': {'回访', '审核'}, '戊': {'咨询', '审核'}}
T = ['登记', '咨询', '审核', '发证', '回访']
def mats(tb):
    return [dict(zip(tb, p)) for p in permutations(T) if all(p[i] in tb[k] for i, k in enumerate(tb))]
print('G1-d 基础方案数', len(mats(tab)))
def drop(x, y):
    t2 = {k: set(v) for k, v in tab.items()}; t2[x].discard(y); return len(mats(t2))
opts = {'A': drop('乙', '登记'), 'B': drop('戊', '审核'), 'C': drop('丙', '回访'), 'D': drop('乙', '发证')}
print('G1-d 补充后方案数', opts)
good = [k for k, v in opts.items() if v == 1]; assert good == ['C'], good
print('[OK] D2-G1d -> C（D 使方案数为0，是"矛盾陷阱"）')

# ---------- G1-e 匹配×工程：瓶颈指派（表中为天数）
Mx = {'甲': [7, 5, 3, 4], '乙': [6, 7, 3, 5], '丙': [4, 8, 9, 3], '丁': [3, 4, 4, 4]}
TK = ['A', 'B', 'C', 'D']
vals = []
for p in permutations(range(4)):
    a = dict(zip(Mx, p)); d = [Mx[k][a[k]] for k in Mx]
    vals.append((max(d), sum(d), {k: TK[a[k]] for k in Mx}))
vals.sort(key=lambda x: (x[0], x[1]))
best = [v for v in vals if v[0] == vals[0][0]]
print('G1-e 最晚完成最早', best, '| 总天数最少', min(vals, key=lambda x: x[1]))
assert len(best) == 1
count_options('D2-G1e', best[0][2]['甲'], {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'}, 'D')

# ---------- 拉丁方工具
rows = list(permutations(range(4)))
LS = []
for r0 in rows:
    for r1 in rows:
        if any(r0[k] == r1[k] for k in range(4)): continue
        for r2 in rows:
            if any(r2[k] in (r0[k], r1[k]) for k in range(4)): continue
            for r3 in rows:
                if any(r3[k] in (r0[k], r1[k], r2[k]) for k in range(4)): continue
                LS.append((r0, r1, r2, r3))
PP = ['张', '王', '李', '杨']; CC = ['广州', '深圳', '汕头', '湛江']
ci = {c: i for i, c in enumerate(CC)}; pi = {p: i for i, p in enumerate(PP)}
def latin(givens):
    return [L for L in LS if all(L[pi[p]][m - 1] == ci[c] for p, m, c in givens)]
cell = lambda p, m, c: (lambda L: L[pi[p]][m - 1] == ci[c])

# G2-a 一定为真（已知5格，2种完成；必然格需"城市×月份"视角）
G = [('李', 1, '湛江'), ('杨', 1, '汕头'), ('李', 2, '深圳'), ('杨', 2, '湛江'), ('王', 4, '湛江')]
S = latin(G)
for L in S: print('G2-a 完成', {PP[i]: [CC[v] for v in L[i]] for i in range(4)})
judge('D2-G2a', S, {'A': cell('张', 1, '广州'), 'B': cell('张', 3, '湛江'), 'C': cell('王', 2, '广州'), 'D': cell('杨', 4, '深圳')}, 'must', 'B')
for k, f in {'A': cell('张', 1, '广州'), 'C': cell('王', 2, '广州'), 'D': cell('杨', 4, '深圳')}.items():
    print('   ', k, '成立解数', sum(f(L) for L in S), '/', len(S))

# G2-b 补一个条件定全表（已知4格，3种完成）
G = [('王', 3, '汕头'), ('张', 4, '深圳'), ('李', 3, '深圳'), ('杨', 1, '湛江')]
S = latin(G)
print('G2-b 完成数', len(S))
opts = {'A': ('张', 1, '广州'), 'B': ('王', 1, '深圳'), 'C': ('张', 2, '湛江'), 'D': ('王', 4, '湛江')}
res = {k: len([L for L in S if cell(*v)(L)]) for k, v in opts.items()}
print('G2-b 补充后完成数', res)
assert [k for k, v in res.items() if v == 1] == ['D'] and res['C'] == 0
print('[OK] D2-G2b -> D（C 与已知矛盾）')

# G2-c 拉丁方+关联条件（甲：红黄蓝绿）
P4 = ['甲', '乙', '丙', '丁']; COL = ['红', '黄', '蓝', '绿']
pool = [L for L in LS if L[0] == (0, 1, 2, 3)]
rel = [(3, 1, 2, 3), (3, 3, 1, 0), (3, 2, 0, 3)]   # 丁2=丙4；丁4=乙1；丁3=甲4
S = [L for L in pool if all(L[i][a] == L[j][b] for i, a, j, b in rel)]
for L in S: print('G2-c 解', {P4[k]: ''.join(COL[v] for v in L[k]) for k in range(4)})
seq = lambda who, s: (lambda L: ''.join(COL[v] for v in L[P4.index(who)]) == s)
judge('D2-G2c', S, {'A': seq('乙', '黄绿红蓝'), 'B': seq('丙', '绿蓝黄红'), 'C': seq('丁', '蓝绿红黄'), 'D': seq('乙', '绿红黄蓝')}, 'must', 'B')
# 选项 A/C/D 至少不与甲行逐轮冲突
for s_ in ['黄绿红蓝', '蓝绿红黄', '绿红黄蓝']:
    assert all(COL.index(ch) != k for k, ch in enumerate(s_)), s_

# G2-d 施工队×周×标段：不可能
TM = ['甲', '乙', '丙', '丁']; SEC = ['一', '二', '三', '四']
def ok(L):
    return L[1][3] == 3 and L[3][2] == 0 and L[1][1] == L[3][0]
S = [L for L in LS if ok(L)]
for L in S: print('G2-d 解', {TM[i]: ''.join(SEC[v] for v in L[i]) for i in range(4)})
at = lambda t, w, s: (lambda L: L[TM.index(t)][w - 1] == SEC.index(s))
judge('D2-G2d', S, {'A': at('甲', 1, '二'), 'B': at('丙', 2, '一'), 'C': at('乙', 1, '三'), 'D': at('丁', 4, '二')}, 'impossible', 'C')

# ---------- G3-a 属性计数：组长须是女性且具有高级职称（组长是4人之一）
P = ['甲', '乙', '丙', '丁']
S = []
for g in product('男女', repeat=4):
    G_ = dict(zip(P, g))
    if g.count('男') != 2: continue
    for h in product([0, 1], repeat=4):
        H = dict(zip(P, h))
        if sum(h) != 2: continue
        if H['甲'] and H['丁']: continue            # ①甲和丁不都具有高级职称
        if H['乙'] != H['丙']: continue             # ②乙和丙职称情况相同
        if G_['丙'] != '男': continue               # ③丙是男性
        L = [x for x in P if G_[x] == '女' and H[x] == 1]
        for l in L: S.append((G_, H, l))           # 组长须存在
print('G3-a 解', S)
judge('D2-G3a', S, {k: (lambda x, v=v: x[2] == v) for k, v in zip('ABCD', P)}, 'must', 'B')

# ---------- G3-b 五人三属性（党员3、男性2、有基层经历2；每人至少一项；队长=有基层经历的男党员）
P = ['甲', '乙', '丙', '丁', '戊']
S = []
for m in product([0, 1], repeat=5):
    if sum(m) != 2: continue
    for d in product([0, 1], repeat=5):
        if sum(d) != 3: continue
        for j in product([0, 1], repeat=5):
            if sum(j) != 2: continue
            M_, D_, J_ = dict(zip(P, m)), dict(zip(P, d)), dict(zip(P, j))
            if any(not (M_[x] or D_[x] or J_[x]) for x in P): continue
            if M_['甲'] != M_['乙']: continue          # ①
            if D_['丙'] != D_['丁']: continue          # ②
            if D_['丙'] and D_['丁']: continue          # ③
            if J_['丙']: continue                       # ④
            for l in [x for x in P if M_[x] and D_[x] and J_[x]]:
                S.append((M_, D_, J_, l))
print('G3-b 解', S)
judge('D2-G3b', S, {k: (lambda x, v=v: x[3] == v) for k, v in zip('ABCD', ['甲', '乙', '丁', '戊'])}, 'must', 'D')

# ---------- G4-a 匹配+比较预热（3村3奖，收入互不相同）
P = ['甲', '乙', '丙']; AW = ['文旅', '生态', '数字']
S = []
for a in permutations(AW):
    A_ = dict(zip(P, a)); W_ = {v: k for k, v in A_.items()}
    for inc in permutations([1, 2, 3]):
        I_ = dict(zip(P, inc))
        if not I_[W_['文旅']] > I_['甲']: continue     # ①获文旅奖的村收入高于甲村
        if not I_['乙'] > I_[W_['文旅']]: continue     # ②乙村收入高于获文旅奖的村
        if not I_[W_['生态']] > I_['甲']: continue     # ③获生态奖的村收入高于甲村
        S.append((A_, I_, W_))
print('G4-a 解', S)
judge('D2-G4a', S, {'A': lambda x: x[0]['甲'] == '生态', 'B': lambda x: x[1]['乙'] == 3 and x[0]['乙'] == '生态',
                    'C': lambda x: x[0]['丙'] == '数字', 'D': lambda x: x[1][x[2]['数字']] > x[1]['丙']}, 'must', 'B')
