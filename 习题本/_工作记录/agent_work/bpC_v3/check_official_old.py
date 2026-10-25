# -*- coding: utf-8 -*-
"""穷举核对有官方答案的综合推理真题（及部分待OCR题的交叉参考）。每题从题面条件独立求解。"""
from itertools import permutations, product, combinations

RESULTS = []

def judge(qid, checks, mode, official=None):
    res = {}
    for k, vals in checks.items():
        vals = list(vals)
        if not vals:
            res[k] = None
            continue
        if mode == 'must':
            res[k] = all(vals)
        elif mode == 'possible':
            res[k] = any(vals)
        elif mode == 'impossible':
            res[k] = not any(vals)
        elif mode == 'mustfalse':          # 一定错误/为假
            res[k] = not any(vals)
        elif mode == 'notmust':            # 不能推出
            res[k] = not all(vals)
    good = sorted(k for k, v in res.items() if v)
    flag = 'OK' if official is None or good == [official] else '!!! MISMATCH'
    RESULTS.append((qid, good, official, flag))
    print(f"{qid}: {res} -> 程序答案 {good} | 官方 {official} {flag}")
    return good

# ===================== C01 =====================
# 2020JSA-99/100 赛道
def lanes():
    N = ['罗', '方', '许', '吕', '田', '石']
    out = []
    for p in permutations(range(1, 7)):
        s = dict(zip(N, p))
        if abs(s['田'] - s['石']) != 1: continue
        if not s['吕'] < s['罗']: continue
        if abs(s['田'] - s['罗']) != 3: continue
        if s['吕'] - s['方'] != 3: continue
        out.append(s)
    return out
S = lanes()
print('赛道解', S)
judge('2020JSA-99', {k: [s['田'] == v for s in S] for k, v in zip('ABCD', [3, 4, 5, 6])}, 'possible', 'A')
judge('2020JSA-100', {k: [abs(s['许'] - s['石']) == v for s in S] for k, v in zip('ABCD', [1, 2, 3, 4])}, 'must', 'C')

# 2020SC1206-85 名次（数字越小名次越高）
S = []
for p in permutations(range(1, 7)):
    r = dict(zip(range(1, 7), p))
    if not (r[1] > r[4] and r[1] < r[2]): continue
    if not r[3] > r[2]: continue
    if not (r[5] < r[3] and r[5] > r[4]): continue
    S.append(r)
opts = {'A': lambda r: r[6] > r[2], 'B': lambda r: r[6] < r[3], 'C': lambda r: r[6] > r[4], 'D': lambda r: r[6] < r[5]}
# 补充该项后，是否在所有解中 6号低于1号
checks = {}
for k, f in opts.items():
    sub = [r for r in S if f(r)]
    checks[k] = [r[6] > r[1] for r in sub] if sub else []
judge('2020SC1206-85', checks, 'must', 'A')

# 2025GD-59 名次+好友（好友关系任意对称）
P = ['甲', '乙', '丙', '丁']
pairs = list(combinations(P, 2))
S = []
for p in permutations(range(1, 5)):
    r = dict(zip(P, p))
    who = {v: k for k, v in r.items()}
    for fb in product([0, 1], repeat=len(pairs)):
        F = {frozenset(pr) for pr, b in zip(pairs, fb) if b}
        fr = lambda a, b: frozenset((a, b)) in F
        third = who[3]
        if third == '甲' or not fr('甲', third) or not r['甲'] < 3: continue
        first = who[1]
        if fr('丁', '甲') or first == '丁' or not fr('丁', first): continue
        if not r['乙'] < r['丙']: continue
        S.append((r, F))
fr2 = lambda F, a, b: frozenset((a, b)) in F
judge('2025GD-59', {
    'A': [r['丙'] >= 3 for r, F in S],
    'B': [r['甲'] < r['丙'] for r, F in S],
    'C': [fr2(F, '乙', '丁') for r, F in S],
    'D': [r['乙'] != 1 for r, F in S],
}, 'mustfalse', 'D')

# 2025JSA-96 数独（区域按截图转录）
regions = [
    [(1,1),(2,1),(3,1),(4,1),(4,2)],
    [(1,2),(2,2),(3,2),(3,3),(3,4)],
    [(1,3),(1,4),(1,5),(2,3),(2,4)],
    [(2,5),(3,5),(4,5),(5,5),(5,4)],
    [(4,3),(4,4),(5,1),(5,2),(5,3)],
]
assert sorted(c for rg in regions for c in rg) == [(i,j) for i in range(1,6) for j in range(1,6)]
given = {(1,3):'华',(2,1):'恒',(3,2):'泰',(5,3):'嵩',(5,4):'衡'}
W = ['泰','华','衡','恒','嵩']
cells = [(i,j) for i in range(1,6) for j in range(1,6)]
sols = []
grid = dict(given)
def ok(c, w):
    i, j = c
    for (a, b), x in grid.items():
        if x == w and (a == i or b == j): return False
    rg = [r for r in regions if c in r][0]
    for d in rg:
        if grid.get(d) == w: return False
    return True
def bt(k):
    if k == len(cells):
        sols.append(dict(grid)); return
    c = cells[k]
    if c in given: bt(k+1); return
    for w in W:
        if ok(c, w):
            grid[c] = w; bt(k+1); del grid[c]
bt(0)
print('数独解个数', len(sols))
ans = [tuple(s[(r,5)] for r in range(2,6)) for s in sols]
print('①-④', ans)
optsd = {'A':('泰','华','嵩','恒'),'B':('华','恒','嵩','泰'),'C':('华','嵩','恒','泰'),'D':('嵩','恒','泰','华')}
judge('2025JSA-96', {k: [a == v for a in ans] for k, v in optsd.items()}, 'must', 'C')

# 2025SC-85 方桌：座位 0..3 按俯视顺时针，面向桌心时左手边 = (i+1)%4，右手边=(i-1)%4，对面=(i+2)%4
P = ['高', '胡', '杨', '陈']
C = ['蓝', '黄', '粉', '红']
for conv in ('左=i+1', '左=i-1'):
    L = (lambda i: (i+1) % 4) if conv == '左=i+1' else (lambda i: (i-1) % 4)
    Rr = (lambda i: (i-1) % 4) if conv == '左=i+1' else (lambda i: (i+1) % 4)
    S = []
    for seat in permutations(range(4)):
        st = dict(zip(P, seat))
        at = {v: k for k, v in st.items()}
        for col in permutations(C):
            cl = dict(zip(P, col))
            wc = {v: k for k, v in cl.items()}
            if at[L(st['杨'])] != '陈': continue
            if cl['陈'] == '蓝': continue
            if at[Rr(st[wc['蓝']])] != '胡': continue
            if st[wc['黄']] != (st['杨'] + 2) % 4: continue
            if wc['黄'] == '胡': continue
            S.append((st, cl))
    opp = lambda st, a, b: (st[a] - st[b]) % 4 == 2
    judge('2025SC-85[' + conv + ']', {
        'A': [opp(st, {v:k for k,v in cl.items()}['红'], {v:k for k,v in cl.items()}['粉']) for st, cl in S],
        'B': [opp(st, '陈', {v:k for k,v in cl.items()}['黄']) for st, cl in S],
        'C': [cl['胡'] == '红' for st, cl in S],
        'D': [not opp(st, '高', '杨') for st, cl in S],
    }, 'must', 'A')

# 2021SC2-85 排班：W[d]、N[d] 为第 d 天白/夜班人员
G = ['甲', '乙', '丙']
S = []
for Wd in product(G, repeat=3):
    for Nd in product(G, repeat=3):
        okk = True
        for d in range(3):
            if Wd[d] == Nd[d]: okk = False          # ① 不连续上一整天
        for g in G:
            days = {d for d in range(3) if Wd[d] == g or Nd[d] == g}
            if len(days) == 3: okk = False          # ② 每人都有一整天休息
            ws = sum(1 for d in range(3) if Wd[d] == g); ns = sum(1 for d in range(3) if Nd[d] == g)
            if ws + ns == 0 or ws == 0 or ns == 0: okk = False  # ③ 不全白/全夜（且都有上班）
        for d in range(2):
            if Nd[d] == Wd[d+1]: okk = False        # ④ 夜班后不能接白班
        if okk: S.append((Wd, Nd))
print('排班解个数', len(S))
def works(s, g, d): return s[0][d] == g or s[1][d] == g
judge('2021SC2-85', {
    'A': [any(works(s, '乙', d) and works(s, '乙', d+1) for d in range(2)) for s in S],
    'B': [any(all(works(s, g, dd) for g in ('甲','乙') for dd in (d, d+1)) for d in range(2)) for s in S],
    'C': [s[0][0] == '丙' and s[1][2] == '丙' for s in S],
    'D': [all(s[1][d] != '丙' for d in range(3)) for s in S],
}, 'possible', 'A')

# 2021GK-114（待OCR，交叉参考）
P = ['甲','乙','丙','丁','戊','己','庚','辛']
S = []
for p in permutations(range(1, 9)):
    s = dict(zip(P, p))
    if abs(s['甲']-s['丙']) != 4: continue
    if abs(s['乙']-s['己']) != 3: continue
    if s['庚'] - s['丁'] != 3: continue
    if abs(s['辛']-s['戊']) != 2: continue
    S.append(s)
judge('2021GK-114(待OCR参考)', {k: [s['丁'] == v for s in S] for k, v in zip('ABCD', [1,2,3,4])}, 'impossible', None)

# 2023SZ-38（待OCR参考）：两种"相隔n天"口径
SH = ['篮', '滑', '牛', '凉', '拖']
for gap_mode in ('差值=n', '中间隔n天'):
    g = (lambda n: n) if gap_mode == '差值=n' else (lambda n: n + 1)
    S = []
    for days in product(SH, repeat=7):
        b = [i for i in range(7) if days[i] == '篮']
        if len(b) != 2 or b[1] - b[0] != g(3): continue
        o = [i for i in range(7) if days[i] == '牛']
        if len(o) != 1 or abs(o[0] - b[0]) != 1: continue
        sk = [i for i in range(7) if days[i] == '滑']
        if len(sk) != 1 or not sk[0] < b[1]: continue
        sd = [i for i in range(7) if days[i] == '凉']
        if len(sd) < 1 or any(abs(x - b[0]) != g(4) for x in sd): continue
        sl = [i for i in range(7) if days[i] == '拖']
        if not any(x < b[0] for x in sl): continue
        S.append(days)
    print('2023SZ-38', gap_mode, '解个数', len(S), [''.join(x) for x in S])
    judge('2023SZ-38(待OCR参考,' + gap_mode + ')', {
        'A': [d[0] == '篮' for d in S], 'B': [d[2] == '牛' for d in S],
        'C': [d[3] == '拖' for d in S], 'D': [d[4] == '滑' for d in S]}, 'must', None)

# ===================== C02 =====================
# 2023SZ-39（待OCR参考）
P = ['甲','乙','丙']; PR = ['广东','上海','四川']
S = []
for pr in permutations(PR):
    o = dict(zip(P, pr))
    for rk in permutations([1,2,3]):
        r = dict(zip(P, rk))
        by = {o[x]: r[x] for x in P}
        if o['乙'] == '四川' or r['乙'] == 3 or r['丙'] == 1 or by['广东'] == 2 or by['四川'] != 1: continue
        S.append((o, r))
judge('2023SZ-39(待OCR参考)', {
    'A': [r['甲'] != 1 for o, r in S], 'B': [r['乙'] == 1 for o, r in S],
    'C': [o['丙'] == '四川' for o, r in S], 'D': [o['乙'] == '上海' for o, r in S]}, 'must', None)

# 2020JSA-94 休假月份
S = []
for p in permutations([6,7,8,9]):
    m = dict(zip(['张','王','李','赵'], p))
    if m['赵'] == 6 or m['张'] == 9 or m['李'] not in (6,8) or m['王'] not in (7,8): continue
    S.append(m)
def implies(S, cond, concl):
    sub = [m for m in S if cond(m)]
    return [concl(m) for m in sub] if sub else [False]
judge('2020JSA-94', {
    'A': [m['张'] in (6,7) for m in S],
    'B': implies(S, lambda m: m['李'] != 6, lambda m: m['王'] == 7),
    'C': implies(S, lambda m: m['李'] == 8, lambda m: m['张'] == 7),
    'D': implies(S, lambda m: m['王'] == 7, lambda m: m['李'] == 6),
}, 'must', 'B')

# 2020JSA-97 窗口
can = {'小丽': {'登记'}, '小马': {'登记','咨询'}, '小高': {'报送','投诉'}, '老王': {'登记','咨询','报送'}, '老董': {'登记','咨询','报送','投诉','综合'}}
S = []
for p in permutations(['登记','咨询','报送','投诉','综合']):
    a = dict(zip(can.keys(), p))
    if all(a[k] in can[k] for k in a): S.append(a)
judge('2020JSA-97', {'A': [a['老董'] != '综合' for a in S], 'B': [a['小高'] == '报送' for a in S],
                     'C': [a['小马'] != '咨询' for a in S], 'D': [a['老王'] == '报送' for a in S]}, 'must', 'D')

# 2021ZJA-106 书+专题数
P = ['张','王','李','赵']
S = []
for books in product([1,2,3], repeat=4):
    for cnt in product([1,2,3], repeat=4):
        b = dict(zip(P, books)); c = dict(zip(P, cnt))
        if b['张'] == b['赵'] or c['张'] == c['赵']: continue
        if cnt.count(1) != 1 or cnt.count(2) != 2: continue
        if not (b['李'] == 3 and c['李'] == 3): continue
        if set(books) != {1,2,3} or b['王'] != 1 or b['赵'] != 1: continue
        S.append((b, c))
judge('2021ZJA-106', {
    'A': [b['张'] == b['李'] for b, c in S], 'B': [c['王'] == 2 for b, c in S],
    'C': [any((b[x] == b['李'] or c[x] == c['李']) for x in P if x != '李') for b, c in S],
    'D': [b['赵'] == 1 and c['赵'] == 2 for b, c in S]}, 'must', 'B')

# 2022JSA-103 组长
P = ['甲','乙','丙','丁']
S = []
for male in product([0,1], repeat=4):
    for party in product([0,1], repeat=4):
        for prof in product([0,1], repeat=4):
            M = dict(zip(P, male)); D = dict(zip(P, party)); F = dict(zip(P, prof))
            if any(not (M[x] or D[x] or F[x]) for x in P): continue
            if sum(party) != 3 or sum(male) != 2 or sum(prof) != 1: continue
            if M['甲'] != M['乙']: continue
            if D['乙'] != D['丙']: continue
            if D['丙'] and D['丁']: continue
            leaders = [x for x in P if M[x] and D[x] and F[x]]
            if not leaders: continue
            S.append(leaders[0])
judge('2022JSA-103', {k: [s == v for s in S] for k, v in zip('ABCD', P)}, 'must', 'C')

# 2022SC2-84
P = ['赵','王','李']
S = []
for o in permutations(['广东','广西','湖南']):
    O = dict(zip(P, o))
    for sj in permutations(['历史','文学','哲学']):
        J = dict(zip(P, sj))
        byO = {v: k for k, v in O.items()}; byJ = {v: k for k, v in J.items()}
        if O['王'] == '湖南': continue
        if O[byJ['历史']] == '湖南': continue
        if byO['广西'] == byJ['历史']: continue
        if O['王'] == '广东': continue
        if J['李'] == '哲学' or O['李'] == '湖南' or O[byJ['哲学']] == '湖南': continue
        S.append((O, J))
judge('2022SC2-84', {
    'A': [False for _ in S],  # 赵是否喜欢下棋题干未给出——不能推出
    'B': [O[{v:k for k,v in J.items()}['文学']] == '广东' for O, J in S],
    'C': [O[{v:k for k,v in J.items()}['哲学']] == '广西' for O, J in S],
    'D': [False for _ in S],  # 住隔壁的是广西与历史教授，推不出王与赵
}, 'must', 'C')

# 2023JSA-93 组长：年龄 Y/M，"丁与戊年龄相差最大"取 丁、戊 分属两个年龄段
P = ['甲','乙','丙','丁','戊']
S = []
for age in product('YM', repeat=5):
    A = dict(zip(P, age))
    if age.count('Y') != 3: continue
    if A['甲'] != A['丙'] or A['丁'] == A['戊']: continue
    for sub in product('CS', repeat=5):
        B = dict(zip(P, sub))
        if sub.count('C') != 2: continue
        if B['乙'] != B['戊'] or B['丙'] == B['丁']: continue
        L = [x for x in P if A[x] == 'M' and B[x] == 'C']
        if not L: continue
        for l in L: S.append(l)
judge('2023JSA-93', {k: [s == v for s in S] for k, v in zip('ABCD', ['甲','乙','丙','丁'])}, 'must', 'D')

# 2023ZJA-101 气球
P = ['明','军','花','飞','雅']
B = [('红','圆'),('蓝','星'),('黄','心'),('蓝','圆'),('红','心')]
S = []
for p in permutations(B):
    a = dict(zip(P, p))
    if a['花'][1] == '圆' or a['花'][0] == '蓝' or a['雅'][1] == '圆' or a['雅'][0] == '蓝': continue
    if a['军'][0] == a['雅'][0] or a['军'][1] == a['雅'][1]: continue
    if a['雅'][0] != '黄' or a['明'][0] != '蓝': continue
    if a['军'][0] != a['花'][0] or a['飞'][1] == '星': continue
    S.append(a)
judge('2023ZJA-101', {'A': [a['军'] == ('红','心') for a in S], 'B': [a['花'] == ('黄','心') for a in S],
                      'C': [a['飞'] == ('红','圆') for a in S], 'D': [a['明'] == ('蓝','星') for a in S]}, 'must', 'D')

# 2024GK-109 拉丁方
P = ['张','王','李','杨']; CT = ['上海','苏州','杭州','南京']
S = []
rows = list(permutations(CT))
for rz in rows:
    if rz[0] != '苏州' or rz[2] != '上海': continue
    for rw in rows:
        if rw[2] != '苏州': continue
        for rl in rows:
            if rl[0] != '南京': continue
            for ry in rows:
                if ry[1] != '杭州': continue
                if all(len({rz[m], rw[m], rl[m], ry[m]}) == 4 for m in range(4)):
                    S.append({'张': rz, '王': rw, '李': rl, '杨': ry})
judge('2024GK-109', {'A': [s['杨'][2] == '南京' for s in S], 'B': [s['张'][3] == '杭州' for s in S],
                     'C': [s['王'][3] == '上海' for s in S], 'D': [s['李'][1] == '苏州' for s in S]}, 'impossible', 'C')

# 2025JSA-94 交换书
P = ['甲','乙','丙','丁']; MJ = ['文学','经济','历史','社会']
S = []
for mj in permutations(MJ):
    M = dict(zip(P, mj))
    if M['丙'] != '历史' or M['丁'] != '文学': continue
    for hb in permutations(MJ):
        H = dict(zip(P, hb))
        if H['甲'] != '社会' or H['乙'] == '文学': continue
        if any(H[x] == M[x] for x in P): continue
        S.append((M, H))
judge('2025JSA-94', {'A': [M['甲'] == '经济' for M, H in S], 'B': [H['丙'] == '文学' for M, H in S],
                     'C': [M['乙'] == '社会' for M, H in S], 'D': [H['丁'] == '历史' for M, H in S]}, 'notmust', 'D')

# 2025ZJA-102 夏令营
P = ['贾','易','白','单']
S = []
for ty in product([1,2,3], repeat=4):
    for cn in product([1,2,3], repeat=4):
        T = dict(zip(P, ty)); N = dict(zip(P, cn))
        if T['贾'] == T['单'] or N['贾'] == N['单']: continue
        if cn.count(1) != 1 or cn.count(2) != 2: continue
        if not (T['白'] == 3 and N['白'] == 3): continue
        if set(ty) != {1,2,3} or T['易'] != 1 or T['单'] != 1: continue
        S.append((T, N))
judge('2025ZJA-102', {'A': [N['易'] == 2 for T, N in S], 'B': [T['贾'] == T['白'] for T, N in S],
                      'C': [any(T[x] == T['白'] or N[x] == N['白'] for x in P if x != '白') for T, N in S],
                      'D': [T['单'] == 1 and N['单'] == 2 for T, N in S]}, 'must', 'A')

# 2020SZ1-33 五轮拿球（每轮5人颜色互异 + 每人5色各一次）
P = ['甲','乙','丙','丁','戊']; COL = ['黑','白','蓝','红','黄']
jia = ('黑','白','蓝','红','黄')
S = []
rows = [r for r in permutations(COL)]
def colok(rs):
    return all(len({r[k] for r in rs}) == len(rs) for k in range(5))
for yi in rows:
    if jia[4] != yi[1]: continue
    if not colok([jia, yi]): continue
    for bing in rows:
        if bing[1] != jia[0]: continue
        if bing[4] != yi[3]: continue
        if not colok([jia, yi, bing]): continue
        for ding in rows:
            if ding[2] != bing[0] or ding[4] != bing[2]: continue
            if not colok([jia, yi, bing, ding]): continue
            for wu in rows:
                if yi[3] != wu[2]: continue
                if colok([jia, yi, bing, ding, wu]):
                    S.append({'乙': yi, '丙': bing, '丁': ding, '戊': wu})
print('2020SZ1-33 解个数', len(S))
judge('2020SZ1-33', {'A': [s['乙'] == ('白','黄','红','黑','蓝') for s in S], 'B': [s['丙'] == ('红','黑','黄','白','蓝') for s in S],
                     'C': [s['丁'] == ('白','蓝','黄','黑','红') for s in S], 'D': [s['戊'] == ('蓝','黑','白','黄','红') for s in S]}, 'possible', 'C')

# 2024SZ-40 发饰材质
P = ['簪','钗','钿','篦']
S = []
for m in permutations(['金','银','铜','玉']):
    a = dict(zip(P, m))
    imp = lambda x, y: (not x) or y
    if not imp(a['簪']=='金', a['钗']!='铜'): continue
    if not imp(a['钗']!='金', a['篦']=='玉'): continue
    if not imp(a['钗']=='金', a['钿']=='玉'): continue
    if not imp(a['钿']=='铜', a['篦']!='银'): continue
    if not imp(a['钿']!='银', a['篦']=='银'): continue
    if not imp(a['篦']=='铜', a['簪']!='玉'): continue
    S.append(a)
print('2024SZ-40 解', S)
judge('2024SZ-40', {k: [a['簪'] == v for a in S] for k, v in zip('ABCD', ['金','银','铜','玉'])}, 'must', 'C')

# 2024SZ-43 认知推理
molds = [(10,6),(10,8),(15,10),(15,12),(15,14),(20,16),(25,16),(30,12),(30,16),(30,18),(35,16)]
cand = list(molds)
cand = [m for m in cand if sum(1 for x in molds if x[0]==m[0]) > 1 and sum(1 for x in molds if x[1]==m[1]) > 1]
cand2 = [m for m in cand if sum(1 for x in cand if x[1]==m[1]) == 1]          # 小范(知W)此时知道
cand3 = [m for m in cand2 if sum(1 for x in cand2 if x[0]==m[0]) == 1]        # 小李(知L)随后也知道
print('2024SZ-43 候选', cand, cand2, cand3)
optm = {'A':(30,12),'B':(20,12),'C':(30,16),'D':(15,12)}
judge('2024SZ-43', {k: [m == v for m in cand3] for k, v in optm.items()}, 'must', 'C')

# ===================== C03 =====================
# 2022JSA-97 录用人数
P = ['甲','乙','丙','丁','戊','己']
S = []
for b in product([0,1], repeat=6):
    s = dict(zip(P, b))
    if s['丙'] + s['丁'] != 1: continue
    if not (s['甲'] or s['乙']): continue
    if s['甲'] + s['丁'] != 1: continue
    if s['乙'] != s['丙']: continue
    if s['甲'] + s['戊'] + s['己'] != 2: continue
    S.append(sum(b))
judge('2022JSA-97', {k: [n == v for n in S] for k, v in zip('ABCD', [2,3,4,5])}, 'must', 'C')

# 2022SC1-84（待OCR参考）
P = ['黄','丁','陈','李','杨','肖','贾']
S = []
for b in product([0,1], repeat=7):
    s = dict(zip(P, b))
    if sum(b) != 4: continue
    if s['黄'] + s['丁'] + s['陈'] != 2: continue
    if s['李'] + s['杨'] + s['肖'] + s['贾'] != 2: continue
    if (s['杨'] or s['贾']) and not s['陈']: continue
    S.append(s)
judge('2022SC1-84(待OCR参考)', {'A': [s['陈'] or s['肖'] for s in S], 'B': [s['黄'] or s['李'] for s in S],
                              'C': [s['丁'] or s['肖'] for s in S], 'D': [s['丁'] or s['李'] for s in S]}, 'must', None)

# 2023SZ-43（待OCR参考） 开关
S = []
for a, b, c in product([0,1], repeat=3):
    st = [1-a, b, c]
    if all(st): continue
    st = [1-a, 1-b, c]
    if all(st): continue
    st = [1-a, 1-b, 1-c]
    if all(st): continue
    S.append(tuple(st))
tog = lambda st, idx: tuple((1-x) if i in idx else x for i, x in enumerate(st))
judge('2023SZ-43(待OCR参考)', {'A': [all(tog(s, {0})) for s in S], 'B': [all(tog(s, {1})) for s in S],
                              'C': [all(tog(s, {0,1})) for s in S], 'D': [all(tog(s, {1,2})) for s in S]}, 'impossible', None)

# 2024GD-58 乐器
P = ['甲','乙','丙','丁']; I = ['钢','提','胡','筝']
pairs2 = list(combinations(I, 2))
S = []
for ch in product(pairs2, repeat=4):
    a = dict(zip(P, [set(x) for x in ch]))
    if any(sum(1 for x in P if i in a[x]) != 2 for i in I): continue
    if '钢' in a['甲'] or '筝' in a['丁'] or '钢' in a['丙'] or '提' in a['丙']: continue
    if len(a['乙'] & a['丙']) != 1: continue
    S.append(a)
judge('2024GD-58', {'A': ['提' in a['甲'] for a in S], 'B': ['胡' not in a['甲'] for a in S],
                    'C': ['筝' in a['乙'] for a in S], 'D': [len(a['甲'] & a['丁']) == 0 for a in S]}, 'must', 'A')

# 2024HB-105 上下午
P = ['赵','钱','孙','李','周','吴','郑']
S = []
for am in combinations(P, 4):
    A = set(am)
    side = lambda x: 'AM' if x in A else 'PM'
    if side('赵') == side('孙') or side('周') == side('孙'): continue
    if side('郑') == 'PM' and not (side('赵') == 'PM' and side('李') == 'PM'): continue
    if not (side('钱') == 'AM' or side('郑') == 'PM'): continue
    S.append(A)
judge('2024HB-105', {'A': [{'钱','郑'} <= s for s in S], 'B': [{'赵','郑'} <= s for s in S],
                     'C': [{'赵','周'} <= s for s in S], 'D': [{'吴','孙'} <= s for s in S]}, 'must', 'A')

# 2024SD-100
P = ['赵','钱','孙','李','周']
S = []
for age in product('YO', repeat=5):
    A = dict(zip(P, age))
    if age.count('Y') != 3: continue
    if A['赵'] != A['孙'] or A['李'] == A['周']: continue
    for mj in product('PL', repeat=5):
        M = dict(zip(P, mj))
        if mj.count('P') != 2: continue
        if M['钱'] != M['周'] or M['孙'] == M['李']: continue
        ch = [x for x in P if A[x] == 'O' and M[x] == 'P']
        if not ch: continue
        for c in ch: S.append(c)
judge('2024SD-100', {k: [c == v for c in S] for k, v in zip('ABCD', ['赵','钱','孙','李'])}, 'must', 'D')

# 2024ZJA-102 奖项
P = ['张','王','李','赵','钱','孙']
S = []
for aw in product('甲乙丙丁', repeat=6):
    a = dict(zip(P, aw))
    cnt = {k: aw.count(k) for k in '甲乙丙丁'}
    if any(not (1 <= cnt[k] <= 2) for k in cnt): continue
    if not cnt['乙'] > cnt['甲'] or not cnt['丁'] > cnt['丙']: continue
    if (a['李'] == '甲' or a['赵'] == '甲') and a['王'] != '丁': continue
    if (a['张'] == '乙' or a['李'] == '乙' or a['赵'] == '乙') and not ([x for x in P if a[x] == '丁'] == ['钱']): continue
    if a['孙'] != '丙': continue
    S.append(a)
judge('2024ZJA-102', {'A': [a['张'] == '丙' for a in S], 'B': [a['赵'] == '乙' and a['钱'] == '乙' for a in S],
                      'C': [a['王'] == '丁' and a['李'] == '丁' for a in S], 'D': [a['李'] == '丁' and a['赵'] == '丁' for a in S]}, 'must', 'D')

# 2025GD-53
P = ['赵','钱','孙','李','刘','王','吴']
S = []
for m in combinations(['赵','钱','孙'], 2):
    for f in combinations(['李','刘','王','吴'], 2):
        s = set(m) | set(f)
        if ('刘' in s or '吴' in s) and '孙' not in s: continue
        S.append(s)
judge('2025GD-53', {'A': ['赵' in s or '李' in s for s in S], 'B': ['孙' in s or '王' in s for s in S],
                    'C': ['钱' in s or '王' in s for s in S], 'D': ['孙' in s or '刘' in s for s in S]}, 'must', 'B')

# 2025HB-109
T = ['桃','李','杨','柳','松']
S = []
for b in product([0,1], repeat=5):
    s = dict(zip(T, b))
    if s['桃'] and s['松']: continue
    if s['桃'] + s['李'] != 1: continue
    if sum(b) < 3: continue
    if s['桃'] and s['杨']: continue
    if s['李'] and s['柳']: continue
    S.append(s)
judge('2025HB-109', {'A': [s['李'] and s['桃'] and not s['松'] for s in S], 'B': [s['桃'] and s['柳'] and not s['杨'] for s in S],
                     'C': [s['李'] and s['杨'] and not s['松'] for s in S], 'D': [s['杨'] and s['松'] and not s['桃'] for s in S]}, 'must', 'D')

# 2023GK-115 滑雪
P = ['石','方','白','于','叶']; E = ['单板','跳台','越野','高山']
S = []
for aw in product(E, repeat=5):
    a = dict(zip(P, aw))
    if any(not (1 <= aw.count(e) <= 2) for e in E): continue
    if (a['石'] == '高山' or a['白'] == '高山') and not (a['方'] == '单板' and a['于'] == '高山'): continue
    if (a['于'] == '高山' or a['方'] == '高山') and not (a['白'] == '单板' and a['叶'] == '单板'): continue
    if a['叶'] == '高山': continue
    S.append(a)
judge('2023GK-115', {'A': [a['方'] == '越野' for a in S], 'B': [a['叶'] != '单板' for a in S],
                     'C': [a['石'] == '高山' for a in S], 'D': [a['白'] != '跳台' for a in S]}, 'must', 'D')

# 2025SC-84 去向
P = ['甲','乙','丙','丁','戊','己','庚']
S = []
for aw in product('JKL', repeat=7):   # J就业 K考研 L留学
    a = dict(zip(P, aw))
    if any(not (2 <= aw.count(x) <= 3) for x in 'JKL'): continue
    if (a['甲'] in 'JL' or a['丙'] in 'JL') and not (a['乙'] == 'K' and a['戊'] == 'K'): continue
    if (a['乙'] in 'JK' or a['丁'] in 'JK') and not (a['己'] == 'L' and a['庚'] == 'L'): continue
    if (a['戊'] in 'KL' or a['己'] in 'KL') and not (a['乙'] == 'J' and a['丙'] == 'J'): continue
    S.append(a)
L = lambda a: {x for x in P if a[x] == 'L'}
print('2025SC-84 解', S, '留学集合', [sorted(L(a)) for a in S])
judge('2025SC-84', {'A': [{'甲','乙'} <= L(a) for a in S], 'B': [{'丙','戊'} <= L(a) for a in S],
                    'C': [{'乙','丁'} <= L(a) for a in S], 'D': [{'丁','庚'} <= L(a) for a in S]}, 'must', 'C')

# 2026CQ-100 值班点（条件(2)遮挡处补"那么"）
P = ['甲','乙','丙','丁','戊','己','庚']
S = []
for aw in product('PQRS', repeat=7):
    a = dict(zip(P, aw))
    c = {k: aw.count(k) for k in 'PQRS'}
    if any(not (1 <= c[k] <= 3) for k in c) or c['Q'] != 3: continue
    if c['R'] != c['P']: continue
    if sum(1 for x in ('甲','乙','丙') if a[x] == 'Q') <= 2 and not ([x for x in P if a[x] == 'S'] == ['丁']): continue
    if (a['丁'] != 'S' or a['戊'] != 'S') and not (a['乙'] == 'S' and a['庚'] == 'S'): continue
    S.append(a)
judge('2026CQ-100', {'A': [a['乙'] == 'Q' and a['戊'] == 'S' for a in S], 'B': [a['甲'] == 'Q' and a['丁'] == 'P' for a in S],
                     'C': [a['己'] == 'P' and a['庚'] == 'R' for a in S], 'D': [a['丙'] == 'P' and a['戊'] == 'S' for a in S]}, 'must', 'A')

# ===================== C04 =====================
# 2024GD-55
S = []
for v in product(range(0, 8), repeat=4):
    li, wang, yang, zhang = v
    if li + wang > yang + zhang and li + zhang > wang + yang and wang + zhang > li + yang:
        S.append(v)
low = lambda v, i: all(v[i] < v[j] for j in range(4) if j != i)
judge('2024GD-55', {k: [low(v, i) for v in S] for k, i in zip('ABCD', [0, 1, 2, 3])}, 'must', 'C')

# 2023ZJA-103 补前提：变量 Fn(师范女) Fx(非师范女) Mn(师范男) Mx(非师范男)
S = list(product(range(0, 7), repeat=4))
base = [s for s in S if s[0] > s[3]]   # Fn > Mx
concl = lambda s: s[0] + s[1] > s[2] + s[3]
optz = {'A': lambda s: s[0] + s[2] < s[1] + s[3], 'B': lambda s: s[0] + s[2] > s[1] + s[3],
        'C': lambda s: s[0] > s[3], 'D': lambda s: s[1] > s[3]}
judge('2023ZJA-103', {k: [concl(s) for s in base if f(s)] for k, f in optz.items()}, 'must', 'A')

# 2025JSA-99
vals = {'甲': 9472, '乙': 9496, '丙': 9480, '丁': 9502}
S = []
for est in vals:
    others = [x for x in vals if x != est]
    for p in permutations([+17, +9, -13]):
        true = {vals[o] + d for o, d in zip(others, p)}
        if len(true) == 1: S.append(est)
judge('2025JSA-99', {k: [e == v for e in S] for k, v in zip('ABCD', ['甲','乙','丙','丁'])}, 'must', 'B')

# 2020SZ1-38 打地鼠
sets4 = [set(c) for c in combinations(range(1, 8), 4) if sum(c) == 17]
S = []
for K in sets4:
    for D in sets4:
        for C_ in sets4:
            if len(K & D) == 2 and len(K & C_) == 2 and not (K & D & C_) and len(D & C_) == 1:
                S.append(D & C_)
print('2020SZ1-38 共同项', S)
judge('2020SZ1-38', {k: [v in s for s in S] for k, v in zip('ABCD', [2, 3, 4, 6])}, 'must', 'D')

# 2020SZS-73 说谎人数
scores = [1, 3, 5, 7, 9]
feas = set(sum(c) for c in product(scores, repeat=6))
claims = {'张': 10, '王': 30, '李': 33, '赵': 58}
S = []
for truth in product([0, 1], repeat=4):
    t = dict(zip(claims, truth))
    if any(t[x] and claims[x] not in feas for x in claims): continue
    S.append(4 - sum(truth))   # 说假话的人数
print('2020SZS-73 可能的说谎人数', sorted(set(S)))
judge('2020SZS-73', {'A': [n <= 3 for n in S], 'B': [n <= 2 for n in S], 'C': [n >= 1 for n in S], 'D': [n >= 2 for n in S]}, 'must', 'D')

# 2025ZJA-104 石头剪刀布：石0 剪2 布5
F = {'R': 0, 'S': 2, 'P': 5}
beats = {('R','S'), ('S','P'), ('P','R')}
S = []
def gen(seq, wl, ww, fl, fw):
    if fl > 9 or fw > 5 or len(seq) > 12: return
    if wl == 2 or ww == 2:
        if fl == 9 and fw == 5: S.append(list(seq))
        return
    for a in 'RSP':
        for b in 'RSP':
            r = 'L' if (a, b) in beats else ('W' if (b, a) in beats else 'D')
            gen(seq + [(a, b, r)], wl + (r == 'L'), ww + (r == 'W'), fl + F[a], fw + F[b])
gen([], 0, 0, 0, 0)
def li_win(s): return sum(1 for x in s if x[2] == 'L') == 2
def comeback(s, who):
    a = b = 0; behind = False
    for x in s:
        a += x[2] == 'L'; b += x[2] == 'W'
        if who == 'L' and a < b: behind = True
        if who == 'W' and b < a: behind = True
    return behind and ((who == 'L' and li_win(s)) or (who == 'W' and not li_win(s)))
def two_in_row_li(s):
    r = [x[2] for x in s]
    return li_win(s) and any(r[i] == 'L' and r[i+1] == 'L' for i in range(len(r) - 1))
def three_draws(s):
    r = [x[2] for x in s]
    return any(r[i:i+3] == ['D','D','D'] for i in range(len(r) - 2))
print('2025ZJA-104 局况数', len(S))
judge('2025ZJA-104', {'A': [two_in_row_li(s) for s in S], 'B': [three_draws(s) for s in S],
                      'C': [comeback(s, 'L') for s in S], 'D': [comeback(s, 'W') for s in S]}, 'impossible', 'D')

# ===================== C05 =====================
# 2024JSA-97/98 招聘（学历可重复；97 附加"各不相同"）
DEG = ['博', '硕', '本']
S = []
for p in product(DEG, repeat=3):
    sc, yf, cw = p
    if sc == '本' and yf != '硕': continue
    if yf == '博' and sc != '博': continue
    if cw in ('本', '硕') and yf != '本': continue
    S.append(p)
S97 = [p for p in S if len(set(p)) == 3]
judge('2024JSA-97', {'A': [p[0] == '硕' and p[2] == '本' for p in S97], 'B': [p[1] == '博' and p[2] == '硕' for p in S97],
                     'C': [p[0] == '博' and p[1] == '本' for p in S97], 'D': [p[2] == '本' and p[1] == '硕' for p in S97]}, 'possible', 'C')
S98 = [p for p in S if p[1] == '硕']
judge('2024JSA-98', {'A': [p[0] == '博' for p in S98], 'B': [p[2] == '博' for p in S98],
                     'C': [p[0] == '本' for p in S98], 'D': [p[2] == '硕' for p in S98]}, 'impossible', 'D')

# 2025JSA-95
S = []
for p in permutations(['人事', '财务', '办公']):
    a = dict(zip(['甲','乙','丙'], p))
    t = [a['甲'] == '人事', a['乙'] != '财务', a['丙'] != '人事']
    if sum(t) == 1: S.append(p)
optp = {'A': ('人事','财务','办公'), 'B': ('办公','财务','人事'), 'C': ('财务','办公','人事'), 'D': ('人事','办公','财务')}
judge('2025JSA-95', {k: [s == v for s in S] for k, v in optp.items()}, 'must', 'C')

# 2020JSA-95 籍贯（可重复）
S = []
for p in product(['苏','皖','浙'], repeat=3):
    j, y, b = p
    g1 = [j == '浙', y == '皖', b == '浙']
    g2 = [j == '浙', y == '苏', b != '苏']
    g3 = [j == '苏', y == '浙', b == '苏']
    if sum(g1) == 1 and sum(g2) == 1 and sum(g3) == 1: S.append(p)
print('2020JSA-95 解', S)
opt95 = {'A': ('苏','皖','浙'), 'B': ('浙','苏','苏'), 'C': ('皖','浙','苏'), 'D': ('苏','皖','皖')}
judge('2020JSA-95', {k: [s == v for s in S] for k, v in opt95.items()}, 'possible', 'D')

# 2020SZS-78 海岛
IS = ['巴厘', '塞舌尔', '塔希提', '塞班', '帕劳']
S = []
for p in permutations(range(1, 6)):
    pic = dict(zip(IS, p)); at = {v: k for k, v in pic.items()}
    st = [[at[4]=='巴厘', at[5]=='塞舌尔'], [at[2]=='塞班', at[5]=='塔希提'], [at[4]=='帕劳', at[2]=='塞舌尔'],
          [at[3]=='巴厘', at[4]=='塞班'], [at[5]=='塞舌尔', at[1]=='巴厘']]
    if all(sum(x) == 1 for x in st): S.append(p)
opt78 = {'A': (2,5,1,3,4), 'B': (4,1,3,5,2), 'C': (4,2,3,5,1), 'D': (3,5,1,2,4)}
judge('2020SZS-78', {k: [s == v for s in S] for k, v in opt78.items()}, 'must', 'D')

# 2021JSA-94 职业预言
P = ['甲','乙','丙','丁']
S = []
for p in permutations(['企业家','教师','歌手','会计师']):
    a = dict(zip(P, p))
    t = {'甲': a['乙'] != '歌手', '乙': a['丙'] == '会计师', '丙': a['丁'] != '企业家', '丁': a['乙'] != '教师'}
    if all(t[x] == (a[x] == '会计师') for x in P): S.append(p)
opt94 = {'A': ('企业家','教师','歌手','会计师'), 'B': ('教师','歌手','企业家','会计师'),
         'C': ('企业家','歌手','会计师','教师'), 'D': ('会计师','教师','歌手','企业家')}
judge('2021JSA-94', {k: [s == v for s in S] for k, v in opt94.items()}, 'must', 'D')

# 2021JSA-99/100 隧道（位置1=最南 … 6=最北）
T = ['长川','大美','青山','绿水','彩石','白玉']
S = []
for p in permutations(range(1, 7)):
    s = dict(zip(T, p))
    if s['白玉'] != s['彩石'] + 1: continue
    if not (s['大美'] > s['白玉'] and s['大美'] - s['白玉'] >= 2): continue
    if abs(s['长川'] - s['青山']) != 2: continue
    S.append(s)
judge('2021JSA-99', {'A': [s['长川'] == 1 for s in S], 'B': [s['绿水'] == 6 for s in S],
                     'C': [abs(s['彩石'] - s['青山']) == 2 for s in S], 'D': [abs(s['白玉'] - s['大美']) == 2 for s in S]}, 'impossible', 'A')
S100 = [s for s in S if abs(s['绿水'] - s['白玉']) == 1]
judge('2021JSA-100', {'A': [s['彩石'] == 2 for s in S100], 'B': [s['大美'] == 5 for s in S100],
                      'C': [s['长川'] == 4 for s in S100], 'D': [s['青山'] == 3 for s in S100]}, 'must', 'B')

# 2021SD-71（待OCR参考）
P = ['F','G','H','J']
S = []
for grad in P:
    rest = [x for x in P if x != grad]
    for roles in permutations(['作曲家','教师','公务员']):
        r = dict(zip(rest, roles)); r[grad] = '研究生'
        for wife in (0, 1):
            t = {'F': r['G'] != '作曲家', 'G': r['H'] == '研究生', 'H': r['J'] != '公务员', 'J': bool(wife)}
            if sum(t.values()) != 1: continue
            if not t[grad]: continue
            S.append((r, wife))
judge('2021SD-71(待OCR参考)', {'A': [w == 0 for r, w in S], 'B': [r['F'] == '研究生' for r, w in S],
                             'C': [r['G'] == '教师' for r, w in S], 'D': [r['H'] == '公务员' for r, w in S]}, 'mustfalse', None)

# 2022SC1-85（待OCR参考）
S = []
for v in product(range(1, 8), repeat=4):
    if sum(v) != 10: continue
    a, b, c, d = v
    st = [b + c == 5, c + d == 5, d + a == 5, a + b == 4]
    if all(st[i] == (v[i] != 2) for i in range(4)): S.append(v)
print('2022SC1-85 解', S)
opt85 = {'A': (2,3,2,3), 'B': (2,4,1,3), 'C': (2,2,2,4), 'D': (2,2,3,3)}
judge('2022SC1-85(待OCR参考)', {k: [s == v for s in S] for k, v in opt85.items()}, 'must', None)

# 2023HB-109 出场顺序
TM = ['红','黄','绿','蓝']
S = []
for p in permutations(range(1, 5)):
    o = dict(zip(TM, p))
    t = [(o['红'] != 1) or (o['黄'] == 2), (o['红'] != 3) or (o['蓝'] == 4), o['蓝'] != 4, o['黄'] == 2]
    if sum(t) == 1: S.append(o)
judge('2023HB-109', {k: [o['绿'] == v for o in S] for k, v in zip('ABCD', [1,2,3,4])}, 'must', 'B')

# 2023JSA-97/98 名次+性别（排在吴之前恰有两名男性）
P = ['赵','钱','孙','李','周','吴','郑']
S = []
for p in permutations(range(1, 8)):
    r = dict(zip(P, p))
    if r['赵'] != 6 or not r['郑'] < r['孙']: continue
    if not (r['吴'] < r['钱'] and r['吴'] < r['李']): continue
    for g in product('MF', repeat=7):
        G = dict(zip(P, g))
        if 'M' not in g or 'F' not in g: continue
        byr = {r[x]: G[x] for x in P}
        if any(byr[i] == 'M' and byr[i+1] == 'M' for i in range(1, 7)): continue
        if sum(1 for x in P if r[x] < r['吴'] and G[x] == 'M') != 2: continue
        S.append((r, G))
judge('2023JSA-97', {'A': [abs(r['孙']-r['吴']) == 1 for r, G in S], 'B': [abs(r['吴']-r['郑']) == 1 for r, G in S],
                     'C': [abs(r['吴']-r['李']) == 1 for r, G in S], 'D': [abs(r['周']-r['吴']) == 1 for r, G in S]}, 'impossible', 'B')
S98 = [(r, G) for r, G in S if r['周'] == 3]
judge('2023JSA-98', {k: [G[v] == 'F' for r, G in S98] for k, v in zip('ABCD', ['赵','钱','孙','李'])}, 'must', 'C')

# 2023JSA-103 身高体型
P = ['甲','乙','丙','丁']; H = [165, 168, 170, 172]
S = []
for h in permutations(H):
    hh = dict(zip(P, h))
    for th in combinations(P, 2):
        thin = {x: (x in th) for x in P}
        st = {'甲': hh['甲'] < 170, '乙': hh['丙'] == 172 and thin['丙'], '丙': hh['丁'] == 168 and not thin['丁'],
              '丁': hh['乙'] == 165 and thin['乙']}
        if all(st[x] == thin[x] for x in P): S.append((hh, thin))
judge('2023JSA-103', {'A': [h['甲'] == 165 and not t['甲'] for h, t in S], 'B': [h['乙'] == 170 and t['乙'] for h, t in S],
                      'C': [h['丙'] == 172 and t['丙'] for h, t in S], 'D': [h['丁'] == 168 and not t['丁'] for h, t in S]}, 'must', 'D')

# 2023JSA-104/105 点菜
P = ['甲','乙','丙','丁']; DS = ['芹','鲈','鸡','排']
pairsd = [frozenset(c) for c in combinations(DS, 2)]
S = []
for ch in product(pairsd, repeat=4):
    a = dict(zip(P, ch))
    cnt = {d: sum(1 for x in P if d in a[x]) for d in DS}
    if any(cnt[d] == 4 or cnt[d] == 0 for d in DS): continue
    if '芹' in a['丁'] and '鲈' not in a['甲']: continue
    if '鲈' in a['丙'] and not ('鲈' in a['乙'] and '鲈' in a['丁']): continue
    if ('芹' in a['乙'] or '鲈' in a['乙']) and '鸡' not in a['乙']: continue
    if ('芹' in a['丙'] or '鸡' in a['丙']) and '鲈' not in a['丙']: continue
    S.append(a)
judge('2023JSA-104', {'A': ['芹' in a['甲'] or '鸡' in a['甲'] for a in S], 'B': ['芹' in a['乙'] or '排' in a['乙'] for a in S],
                      'C': ['鸡' in a['丙'] or '排' in a['丙'] for a in S], 'D': ['芹' in a['丁'] or '鸡' in a['丁'] for a in S]}, 'must', 'A')
S105 = [a for a in S if len(set(a.values())) == 4]
judge('2023JSA-105', {'A': [a['甲'] == frozenset({'芹','鸡'}) for a in S105], 'B': [a['乙'] == frozenset({'鸡','排'}) for a in S105],
                      'C': [a['丙'] == frozenset({'鲈','芹'}) for a in S105], 'D': [a['丁'] == frozenset({'排','鸡'}) for a in S105]}, 'must', 'C')

# 2024JSA-104/105 调研项目
ST = ['郑','周','刘']; PF = ['王','钱','马']; PJ = ['小微','断头路','客厅','街区']
S = []
for sp in product(PJ, repeat=3):
    s = dict(zip(ST, sp))
    for pp in product(PJ, repeat=3):
        p = dict(zip(PF, pp))
        if any(not any(p[f] == s[x] for f in PF) for x in ST): continue   # 每个工作人员的项目有教授
        if any(not any(s[x] == p[f] for x in ST) for f in PF): continue   # 每位教授至少指导一位工作人员
        if s['郑'] not in ('小微', '断头路') or p['钱'] != '街区': continue
        S.append((s, p))
def inxw(s, p, who):
    return (who in s and s[who] == '小微') or (who in p and p[who] == '小微')
judge('2024JSA-104', {'A': [inxw(s, p, '王') and inxw(s, p, '马') for s, p in S], 'B': [inxw(s, p, '马') and inxw(s, p, '刘') for s, p in S],
                      'C': [inxw(s, p, '刘') and inxw(s, p, '周') for s, p in S], 'D': [inxw(s, p, '周') and inxw(s, p, '王') for s, p in S]}, 'impossible', 'C')
S105 = [(s, p) for s, p in S if s['周'] == '客厅']
judge('2024JSA-105', {'A': [s['刘'] == '街区' for s, p in S105], 'B': [p['王'] == '客厅' for s, p in S105],
                      'C': [p['马'] == '小微' for s, p in S105], 'D': [s['郑'] == '断头路' for s, p in S105]}, 'must', 'A')

# 2024SC-85 一等奖信息（各维度允许表外取值）
tab = {'甲': ('赵','男','馆员','借阅'), '乙': ('钱','女','研究馆员','咨询'), '丙': ('孙','男','馆员','借阅'),
       '丁': ('李','女','研究馆员','采编'), '戊': ('钱','女','副研究馆员','借阅')}
dims = [set(v[i] for v in tab.values()) | {'其他'} for i in range(4)]
dims[1] = {'男', '女'}
S = []
for combo in product(*dims):
    if all(sum(1 for i in range(4) if v[i] == combo[i]) == 1 for v in tab.values()): S.append(combo)
print('2024SC-85 解', S)
judge('2024SC-85', {k: [c[0] == v for c in S] for k, v in zip('ABCD', ['李','赵','孙','钱'])}, 'must', 'A')

# 2024SZ-44 诈骗（甲两句恰一真）
P = ['甲','乙','丙','丁','戊']
S = []
for b in product([0, 1], repeat=5):
    c = dict(zip(P, b))
    if (int(not c['甲']) + int(not c['丁'])) != 1: continue
    if c['乙'] and c['丙']: continue
    if not (c['乙'] or c['丁']): continue
    if c['戊'] and not c['甲']: continue
    if sum(b) < 3: continue
    S.append(frozenset(x for x in P if c[x]))
print('2024SZ-44 解', [sorted(s) for s in S])
opt44 = {'A': {'甲','乙','戊'}, 'B': {'乙','丁','戊'}, 'C': {'甲','丙','丁'}, 'D': {'甲','乙','丙','戊'}}
judge('2024SZ-44', {k: [s == frozenset(v) for s in S] for k, v in opt44.items()}, 'must', 'A')

# 2025ZJA-103 名次
P = ['甲','乙','丙','丁']
S = []
for p in permutations(range(1, 5)):
    r = dict(zip(P, p))
    t = [(r['乙'] != 2) or (r['甲'] == 3), r['丙'] == 1 or r['丁'] != 4, r['甲'] != 3, r['丙'] == 2]
    if sum(t) == 1: S.append(r)
judge('2025ZJA-103', {'A': [r['甲'] == 1 for r in S], 'B': [r['乙'] == 4 for r in S], 'C': [r['丙'] == 2 for r in S], 'D': [r['丁'] == 3 for r in S]}, 'must', 'A')

# 2020SZ1-34 供词全假（逐句取假）
P = ['赵','王','张','李']
S = []
for order in permutations(range(1, 5)):
    pos = dict(zip(P, order))
    for k in P:
        alive_arrive = lambda x: pos[x] <= pos[k]
        dead_leave = lambda x: pos[x] >= pos[k]
        # 赵：我们四人都没杀害他(假->有人杀) ；我离开时他还活着(假->赵离开时已死)
        if not dead_leave('赵'): continue
        # 王：我是第二个进(假)；我到时他已死(假->到时活着)
        if pos['王'] == 2 or not alive_arrive('王'): continue
        # 张：我是第三个进(假)；我离开时他还活着(假->离开时已死)
        if pos['张'] == 3 or not dead_leave('张'): continue
        # 李：凶手进门不比我晚(假->凶手比李晚)；我到时他已死(假->到时活着)
        if not pos[k] > pos['李'] or not alive_arrive('李'): continue
        S.append(k)
judge('2020SZ1-34', {k: [s == v for s in S] for k, v in zip('ABCD', P)}, 'must', 'A')

# 2025GK-110 方桌真假：顺时针 北东南西
SIDES = ['北','东','南','西']
S = []
for start in range(4):
    side = {x: SIDES[(start + i) % 4] for i, x in enumerate(['甲','乙','丙','丁'])}
    at = {v: k for k, v in side.items()}
    for liar_bits in product([0, 1], repeat=4):
        truth = dict(zip(['甲','乙','丙','丁'], [1 - b for b in liar_bits]))
        if sum(truth.values()) != 1: continue
        st = {'甲': truth[at['东']] == 0, '乙': truth[at['南']] == 0, '丙': side['丙'] in ('西','北'), '丁': side['丁'] == '北'}
        if all(st[x] == bool(truth[x]) for x in st): S.append(side)
judge('2025GK-110', {'A': [s['甲'] == '北' for s in S], 'B': [s['甲'] == '东' for s in S],
                     'C': [s['乙'] == '西' for s in S], 'D': [s['乙'] == '南' for s in S]}, 'must', 'A')

# 题库外可补回：2022JSA-98/99、2022JSA-104/105
P = ['甲','乙','丙','丁']
S = []
for p in permutations(range(1, 5)):
    r = dict(zip(P, p))
    zh = [r['甲']==4, r['乙']==3, r['丙']==2, r['丁']==1]
    wa = [r['甲']==3, r['乙']==2, r['丙']==4, r['丁']==1]
    li = [r['甲']==4, r['乙']==2, r['丙']==1, r['丁']==3]
    zo = [r['甲']==2, r['乙']==3, r['丙']==1, r['丁']==4]
    if sum(zh) == 0 and sum(wa) == 1 and sum(li) == 1 and sum(zo) == 1: S.append(r)
print('2022JSA-98/99 解', S)
o98 = {'A': (2,4,1,3), 'B': (3,1,4,2), 'C': (2,1,4,3), 'D': (1,4,3,2)}  # 甲乙丙丁名次
judge('2022JSA-98(题库外)', {k: [tuple(r[x] for x in P) == v for r in S] for k, v in o98.items()}, 'possible', 'C')
S99 = [r for r in S if r['甲'] == 3]
judge('2022JSA-99(题库外)', {'A': [r['丁']==4 for r in S99], 'B': [r['丙']==1 for r in S99], 'C': [r['乙']==2 for r in S99], 'D': [r['乙']==1 for r in S99]}, 'must', 'B')
S = []
for pr in permutations(['苏','浙','湘','鄂']):
    o = dict(zip(P, pr))
    for un in permutations(['师范','医科','财经','农业']):
        u = dict(zip(P, un))
        if u['甲'] == '农业': continue
        if o[{v:k for k,v in u.items()}['农业']] != '苏': continue
        if u['丙'] != '师范' or o['丁'] != '鄂': continue
        S.append((o, u))
judge('2022JSA-104(题库外)', {'A': [o['丙']=='湘' for o,u in S], 'B': [o['甲']=='浙' for o,u in S], 'C': [u['丁']=='财经' for o,u in S], 'D': [u['乙']=='农业' for o,u in S]}, 'must', 'D')
S105 = [(o,u) for o,u in S if o[{v:k for k,v in u.items()}['医科']] == '湘']
judge('2022JSA-105(题库外)', {'A': [u['甲']=='医科' for o,u in S105], 'B': [u['丁']=='财经' for o,u in S105], 'C': [o['丙']!='浙' for o,u in S105], 'D': [o['丙']!='湘' for o,u in S105]}, 'mustfalse', 'C')

print('\n==== 汇总 ====')
for r in RESULTS:
    print(r)
