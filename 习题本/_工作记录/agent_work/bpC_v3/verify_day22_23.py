# -*- coding: utf-8 -*-
"""第22、23天改编中写明答案的设计：独立穷举验算。"""
from lib import *

print('=' * 20, 'Day 22')
P = ['甲', '乙', '丙', '丁']
# 22-1 奇数说真话、偶数说假话
S = []
for a in product(range(1, 8), repeat=4):
    if sum(a) != 10: continue
    A, B, C, D = a
    st = [B + C == 3, C + D == 6, D + A == 6, A + B == 6]
    if all(st[i] == (a[i] % 2 == 1) for i in range(4)): S.append(a)
judge('22-1', S, {'A': lambda a: a == (3, 1, 2, 4), 'B': lambda a: a == (2, 2, 2, 4), 'C': lambda a: a == (1, 2, 3, 4), 'D': lambda a: a == (3, 2, 1, 4)}, 'must', 'A')
# 22-2 各不相同共10项；获奖最多者说假话
S = []
for perm in permutations([1, 2, 3, 4]):
    v = dict(zip(P, perm)); mx = max(v, key=v.get)
    st = {'甲': v['乙'] - v['丁'] == 2, '乙': v['甲'] != 1, '丙': v['乙'] - v['丁'] == 1, '丁': v['甲'] - v['丁'] == 1}
    if all(st[p] == (p != mx) for p in P): S.append(v)
print('22-2 解', S)
judge('22-2', S, {'A': lambda v: v['甲'] == 3, 'B': lambda v: v['乙'] == 3, 'C': lambda v: v['丙'] == 3, 'D': lambda v: v['丁'] == 2}, 'must', 'B')
# 22-3 每题对+5错-2，10题全答；甲26 乙29 丙36，丁："乙说的是真话"；只有一人说真话
feas = {7 * x - 20 for x in range(11)}
S = []
for t in product([True, False], repeat=4):
    tj, ty, tb, td = t
    if sum(t) != 1: continue
    if tj and 26 not in feas: continue
    if ty and 29 not in feas: continue
    if tb and 36 not in feas: continue
    if td != ty: continue
    S.append(t)
print('22-3 真话分布', S)
value('22-3', [(36 + 20) // 7 for t in S if t[2]][0] if all(t[2] for t in S) else None, {'A': 6, 'B': 7, 'C': 8, 'D': 9}, 'C')
# 22-4 判断表，每人恰对一项（闭世界）
tab = {'甲': ('王', '男', '本科', '财务科'), '乙': ('李', '男', '硕士', '法规科'), '丙': ('黄', '男', '博士', '财务科'),
       '丁': ('陈', '女', '本科', '综合科'), '戊': ('黄', '女', '硕士', '综合科')}
dims = [sorted({v[i] for v in tab.values()}) for i in range(4)]
S = [c for c in product(*dims) if all(sum(v[i] == c[i] for i in range(4)) == 1 for v in tab.values())]
print('22-4 解', S)
judge('22-4', S, {'A': lambda c: c[0] == '王' and c[2] == '博士', 'B': lambda c: c[0] == '黄' and c[2] == '硕士',
                  'C': lambda c: c[0] == '李' and c[3] == '法规科', 'D': lambda c: c[0] == '陈' and c[2] == '本科'}, 'must', 'A')
# 22-5 每人恰对两项
tab = {'甲': ('市发改局', '南沙区', '生物医药', '二等奖'), '乙': ('市发改局', '黄埔区', '人工智能', '三等奖'),
       '丙': ('市发改局', '南沙区', '人工智能', '一等奖'), '丁': ('市工信局', '天河区', '生物医药', '一等奖')}
dims = [sorted({v[i] for v in tab.values()}) for i in range(4)]
S = [c for c in product(*dims) if all(sum(v[i] == c[i] for i in range(4)) == 2 for v in tab.values())]
print('22-5 解', S)
judge('22-5', S, {'A': lambda c: c[1] == '南沙区', 'B': lambda c: c[2] == '人工智能', 'C': lambda c: c[3] == '一等奖' and c[1] == '黄埔区', 'D': lambda c: c[0] == '市工信局'}, 'must', 'C')
# 22-6 猜对个数各不相同（3、2、1、0）
tab = {'甲': ('湛江', '经济学', '华南师大'), '乙': ('汕头', '中文', '中山大学'), '丙': ('汕头', '法学', '华南师大'), '丁': ('汕头', '法学', '中山大学')}
dims = [sorted({v[i] for v in tab.values()}) for i in range(3)]
S = [c for c in product(*dims) if sorted(sum(v[i] == c[i] for i in range(3)) for v in tab.values()) == [0, 1, 2, 3]]
print('22-6 解', S)
judge('22-6', S, {'A': lambda c: c == tab['甲'], 'B': lambda c: c == tab['乙'], 'C': lambda c: c == tab['丙'], 'D': lambda c: c == tab['丁']}, 'must', 'B')
# 22-7 只有一人预测正确且他是选调生
R = ['选调生', '教师', '医生', '律师']
S = []
for perm in permutations(R):
    a = dict(zip(P, perm))
    tv = {'甲': a['乙'] != '选调生', '乙': a['丁'] == '律师', '丙': a['甲'] != '教师', '丁': a['丙'] == '选调生'}
    g = [p for p in P if a[p] == '选调生'][0]
    if sum(tv.values()) == 1 and tv[g]: S.append(a)
print('22-7 解', S)
judge('22-7', S, {'A': lambda a: a['甲'] == '选调生', 'B': lambda a: a['乙'] == '选调生' and a['丁'] == '律师',
                  'C': lambda a: a['丙'] == '教师', 'D': lambda a: a['丁'] == '医生'}, 'must', 'B')
# 22-8 丁的预测与身份无关（去西藏支教 E）
S = []
for perm in permutations(R):
    a = dict(zip(P, perm))
    for E in (True, False):
        tv = {'甲': a['丁'] != '律师', '乙': a['丁'] == '选调生', '丙': a['甲'] != '教师', '丁': E}
        g = [p for p in P if a[p] == '选调生'][0]
        if sum(tv.values()) == 1 and tv[g]: S.append((a, E))
print('22-8 解', S)
judge('22-8(问错误)', S, {'A': lambda x: not x[1], 'B': lambda x: x[0]['丙'] == '选调生', 'C': lambda x: x[0]['乙'] == '教师',
                          'D': lambda x: x[0]['甲'] == '律师'}, 'impossible', 'D')
# 22-9 只有冠军的预测对了
S = []
for perm in permutations([1, 2, 3, 4]):
    r = dict(zip(P, perm)); champ = [p for p in P if r[p] == 1][0]
    st = {'甲': r['丙'] != 4, '乙': r['甲'] != 1, '丙': r['甲'] == 4, '丁': r['甲'] != 3}
    if all(st[p] == (p == champ) for p in P): S.append(perm)
print('22-9 解', S)
judge('22-9', S, {'A': lambda t: t == (3, 1, 4, 2), 'B': lambda t: t == (2, 1, 4, 3), 'C': lambda t: t == (3, 2, 4, 1), 'D': lambda t: t == (4, 1, 3, 2)}, 'must', 'A')
# 22-10 三名岛民
S = []
for tv in product([True, False], repeat=3):
    t = dict(zip(['甲', '乙', '丙'], tv))
    st = {'甲': not t['丙'], '乙': not t['甲'], '丙': t['丙'] == t['乙']}
    if all(st[p] == t[p] for p in t): S.append(t)
print('22-10 解', S)
judge('22-10', S, {'A': lambda t: t['甲'], 'B': lambda t: not t['乙'], 'C': lambda t: t['丙'], 'D': lambda t: t['甲'] == t['丙']}, 'must', 'C')
# 22-11 五名岛民：第k人说"我们中恰有k个说谎者"
S = []
for tv in product([True, False], repeat=5):
    liars = 5 - sum(tv)
    if all((liars == k + 1) == tv[k] for k in range(5)): S.append(liars)
print('22-11 说谎者人数', S)
value('22-11', S[0] if len(S) == 1 else None, {'A': 2, 'B': 3, 'C': 4, 'D': 5}, 'C')
# 22-12 一排6人，每人说"我的邻座中至少有一个说谎者"
mins = []
for tv in product([True, False], repeat=6):
    ok = True
    for i in range(6):
        nb = [tv[j] for j in (i - 1, i + 1) if 0 <= j < 6]
        stmt = any(not x for x in nb)
        if stmt != tv[i]: ok = False
    if ok: mins.append(6 - sum(tv))
print('22-12 可能的说谎者人数', sorted(set(mins)))
value('22-12(至少几个说谎者)', min(mins), {'A': 1, 'B': 2, 'C': 3, 'D': 4}, 'B')

print('=' * 20, 'Day 23')
ACT = ['泳', '骑', '跳', '瑜', '散']
def week(gs, gy):
    out = []
    for days in product(ACT, repeat=7):
        sw = [i for i in range(7) if days[i] == '泳']
        if len(sw) != 2 or sw[1] - sw[0] != gs: continue
        bi = [i for i in range(7) if days[i] == '骑']
        if len(bi) != 1 or abs(bi[0] - sw[0]) != 1: continue
        ju = [i for i in range(7) if days[i] == '跳']
        if len(ju) != 1 or not ju[0] < sw[1]: continue
        yo = [i for i in range(7) if days[i] == '瑜']
        if len(yo) < 1 or any(abs(x - sw[0]) != gy for x in yo): continue
        if not any(days[i] == '散' for i in range(sw[0])): continue
        out.append(days)
    return out
# 23-1 "中间隔着2天"（日期差3）两处，问可能
S = week(3, 3)
print('23-1 解', [''.join(d) for d in S])
judge('23-1', S, {'A': lambda d: d[1] == '骑', 'B': lambda d: d[2] == '跳', 'C': lambda d: d[5] == '泳', 'D': lambda d: d[1] == '瑜'}, 'possible', 'B')
# 23-2 "日期相差5天""日期相差3天"，问一定为真；误读成"中间隔着"时瑜伽在周六
S = week(5, 3)
print('23-2 解', [''.join(d) for d in S])
judge('23-2', S, {'A': lambda d: d[4] == '瑜', 'B': lambda d: d[5] == '瑜', 'C': lambda d: d[3] == '跳', 'D': lambda d: d[2] == '泳'}, 'must', 'A')
print('   若把瑜伽条件误读为"中间隔着3天"（日期差4）:', [''.join(d) for d in week(5, 4)])
# 23-3 工序带时长 A2 B3 C2 D1 E2
DUR = {'A': 2, 'B': 3, 'C': 2, 'D': 1, 'E': 2}
def sched(o):
    d = {}; t = 1
    for x in o:
        for k in range(DUR[x]): d[t + k] = x
        t += DUR[x]
    return d
S = []
for o in permutations('ABCDE'):
    p = {x: i for i, x in enumerate(o)}
    if p['A'] < p['B'] and p['A'] != 0 and p['B'] != 4 and p['D'] == p['C'] + 1: S.append(o)
print('23-3 顺序', [''.join(o) for o in S])
judge('23-3', S, {'A': lambda o: sched(o)[6] == 'A', 'B': lambda o: sched(o)[6] == 'B', 'C': lambda o: sched(o)[6] == 'C', 'D': lambda o: sched(o)[6] == 'E'}, 'must', 'B')
# 23-6 间隔最值
P6 = ['甲', '乙', '丙', '丁', '戊', '己']
S = line(P6, 6, [lambda s: s['甲'] < s['乙'], lambda s: abs(s['丙'] - s['丁']) == 1, lambda s: s['戊'] not in (1, 6),
                 lambda s: abs(s['己'] - s['甲']) == 2, lambda s: s['丙'] < s['甲']])
value('23-6', max(s['乙'] - s['甲'] - 1 for s in S), {'A': 0, 'B': 1, 'C': 2, 'D': 3}, 'C')
# 23-7 10座，两端不坐、任意两人不相邻：最多几人，及坐满最多人数时的选座方案数
best = 0; cnt = 0
for k in range(1, 6):
    for c in combinations(range(2, 10), k):
        if all(c[i + 1] - c[i] >= 2 for i in range(k - 1)):
            if k > best: best, cnt = k, 0
            if k == best: cnt += 1
print('23-7 最多', best, '人，方案数', cnt)
value('23-7', best, {'A': 3, 'B': 4, 'C': 5, 'D': 6}, 'B')
# 23-8 名次最值：乙最高第几
P7 = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
S = line(P7, 7, [lambda r: r['乙'] - r['甲'] == 2, lambda r: r['丙'] < r['丁'], lambda r: r['戊'] > 3,
                 lambda r: r['己'] > r['庚'], lambda r: r['丁'] < r['乙'], lambda r: r['庚'] < r['甲']])
value('23-8', min(r['乙'] for r in S), {'A': 3, 'B': 4, 'C': 5, 'D': 6}, 'C')
# 23-9 10座，至少已坐几人才能使后来者无论坐哪都与人相邻
mn = min(k for k in range(1, 11) for c in combinations(range(1, 11), k)
         if all(any(abs(e - o) == 1 for o in c) for e in range(1, 11) if e not in c))
value('23-9', mn, {'A': 3, 'B': 4, 'C': 5, 'D': 6}, 'B')
# 23-10 圆桌三对夫妻（丈夫甲乙丙，妻子A/B/C 对应），每位丈夫坐在自己妻子的左手边；甲的对面是丙的妻子
H = ['甲', '乙', '丙']; W = ['A', 'B', 'C']
S = []
for p in permutations(range(1, 6)):
    st = dict(zip(H + W, (0,) + p))
    if any(st[h] != (st[w] + 1) % 6 for h, w in zip(H, W)): continue
    if (st['C'] - st['甲']) % 6 != 3: continue
    S.append(st)
at = lambda st, i: {v: k for k, v in st.items()}[i % 6]
print('23-10 解', [[at(s, i) for i in range(6)] for s in S])
judge('23-10', S, {'A': lambda s: at(s, s['甲'] + 1) == '乙', 'B': lambda s: at(s, s['乙'] + 1) == 'C',
                   'C': lambda s: at(s, s['丙'] - 1) == 'A', 'D': lambda s: (s['丙'] - s['B']) % 6 in (1, 5)}, 'must', 'B')
# 23-13 4条陈述恰有1条不成立
S = [s for s in line(P6, 6, [lambda s: s['甲'] == 2])
     if sum([abs(s['戊'] - s['甲']) == 3, abs(s['丁'] - s['戊']) == 3, abs(s['丁'] - s['乙']) == 3, abs(s['丙'] - s['丁']) == 1]) == 3]
bad = lambda s: [i for i, ok in enumerate([abs(s['戊'] - s['甲']) == 3, abs(s['丁'] - s['戊']) == 3, abs(s['丁'] - s['乙']) == 3, abs(s['丙'] - s['丁']) == 1]) if not ok][0]
print('23-13 解', [fmt_line(s) for s in S])
judge('23-13', S, {k: (lambda s, i=i: bad(s) == i) for k, i in zip('ABCD', range(4))}, 'must', 'B')
# 23-11 8人圆桌男女相间、夫妻不相邻；甲左手边是乙妻；丙在甲对面
M = ['甲', '乙', '丙', '丁']; F = ['A', 'B', 'C', 'D']
S = []
for pm in permutations([2, 4, 6]):
    for pf in permutations([1, 3, 5, 7]):
        st = dict(zip(M, (0,) + pm)); st.update(dict(zip(F, pf)))
        if any((st[f] - st[m]) % 8 in (1, 7) for m, f in zip(M, F)): continue
        if st['B'] != (st['甲'] + 1) % 8: continue
        if (st['丙'] - st['甲']) % 8 != 4: continue
        S.append(st)
at8 = lambda st, i: {v: k for k, v in st.items()}[i % 8]
judge('23-11', S, {'A': lambda s: at8(s, s['甲'] - 1) == 'D', 'B': lambda s: (s['A'] - s['乙']) % 8 in (1, 7),
                   'C': lambda s: s['D'] == (s['丙'] + 1) % 8, 'D': lambda s: (s['B'] - s['C']) % 8 == 4}, 'must', 'C')
summary()
