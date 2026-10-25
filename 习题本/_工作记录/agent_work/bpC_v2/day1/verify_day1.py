# -*- coding: utf-8 -*-
"""第1天（C01 首次·试点日）13 道改编骨架的独立穷举验算。"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bpC_v2')
from lib import *
from itertools import permutations, product

print('=' * 30, '考法一 直线排位')
# V1-1 窗口：必然->可能
N = ['社保', '医保', '税务', '公积金', '不动产', '户政']
base = [lambda s: s['税务'] == s['社保'] + 1,
        lambda s: s['公积金'] - s['税务'] >= 2,
        lambda s: abs(s['医保'] - s['户政']) == 3]
S0 = line(N, 6, base)
S = [s for s in S0 if s['不动产'] == 6]
print('V1-1 基础解数', len(S0), '附加后', [fmt_line(s) for s in S])
judge('V1-1', S, {'A': lambda s: s['社保'] == 1, 'B': lambda s: s['公积金'] == 4,
                  'C': lambda s: s['户政'] == 1, 'D': lambda s: s['医保'] == 5}, 'possible', 'C')

# V1-2 展位：能确定几家
N = ['A', 'B', 'C', 'D', 'E', 'F']
S = line(N, 6, [lambda s: s['A'] == s['B'] + 1, lambda s: s['C'] - s['A'] >= 2,
                lambda s: s['E'] - s['D'] == 2, lambda s: s['F'] not in (1, 6)])
print('V1-2 解', [fmt_line(s) for s in S])
fixed = [x for x in N if len({s[x] for s in S}) == 1]
print('   确定者', fixed)
count_options('V1-2', len(fixed), {'A': 1, 'B': 2, 'C': 3, 'D': 4}, 'B')

# V1-3 老街：自西向东 1..6；选项用"从东往西数第k家"= 7-pos
N = ['凉茶', '云吞', '肠粉', '烧腊', '糖水', '早茶']
S = line(N, 6, [lambda s: s['云吞'] == s['凉茶'] + 1, lambda s: s['肠粉'] - s['云吞'] == 2,
                lambda s: s['烧腊'] not in (1, 6), lambda s: s['糖水'] < s['早茶']])
print('V1-3 解（自西向东）', [fmt_line(s) for s in S])
E = lambda s, x: 7 - s[x]
judge('V1-3', S, {'A': lambda s: E(s, '烧腊') == 3, 'B': lambda s: E(s, '肠粉') == 3,
                  'C': lambda s: E(s, '云吞') == 2, 'D': lambda s: E(s, '早茶') == 2}, 'impossible', 'C')
# 陷阱核查：若把"从东往西"误读成"从西往东"
judge('V1-3[误读方向]', S, {'A': lambda s: s['烧腊'] == 3, 'B': lambda s: s['肠粉'] == 3,
                          'C': lambda s: s['云吞'] == 2, 'D': lambda s: s['早茶'] == 2}, 'impossible', None, show=True) if False else None
for k, x, v in [('A', '烧腊', 3), ('B', '肠粉', 3), ('C', '云吞', 2), ('D', '早茶', 2)]:
    print('   误读方向时', k, '可能?', any(s[x] == v for s in S))

# V1-4 货架：同品牌不相邻、两端同品牌、乙1在甲1左边；附加 丙1在3号
N = ['甲1', '甲2', '乙1', '乙2', '丙1', '丙2']
brand = lambda x: x[0]
def nonadj(s):
    return all(abs(s[b + '1'] - s[b + '2']) != 1 for b in '甲乙丙')
def ends_same(s):
    at = {v: k for k, v in s.items()}
    return brand(at[1]) == brand(at[6])
S0 = line(N, 6, [nonadj, ends_same, lambda s: s['乙1'] < s['甲1']])
S = [s for s in S0 if s['丙1'] == 3]
print('V1-4 基础解数', len(S0), '附加后', [fmt_line(s) for s in S])
def endbrand(s):
    at = {v: k for k, v in s.items()}
    return brand(at[1])
judge('V1-4', S, {'A': lambda s: s['乙1'] == 1, 'B': lambda s: abs(s['甲1'] - s['丙1']) == 1,
                  'C': lambda s: s['丙2'] == 5, 'D': lambda s: endbrand(s) == '乙'}, 'must', 'C')
for k, f in {'A': lambda s: s['乙1'] == 1, 'B': lambda s: abs(s['甲1'] - s['丙1']) == 1,
             'D': lambda s: endbrand(s) == '乙'}.items():
    print('   ', k, '成立的解数', sum(f(s) for s in S), '/', len(S))

# V1-5 七个房间：奇偶占位
N = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
S = line(N, 7, [lambda s: abs(s['甲'] - s['乙']) == 3, lambda s: s['丁'] == s['丙'] + 1,
                lambda s: abs(s['戊'] - s['己']) == 2, lambda s: s['庚'] not in (1, 7)])
print('V1-5 解数', len(S), '庚的可能位置', sorted({s['庚'] for s in S}))
judge('V1-5', S, {'A': lambda s: s['庚'] == 2, 'B': lambda s: s['庚'] == 3,
                  'C': lambda s: s['庚'] == 4, 'D': lambda s: s['庚'] == 6}, 'impossible', 'B')

# V1-6 主席台：位置+城市
P = ['甲', '乙', '丙', '丁', '戊']
CT = ['广州', '深圳', '佛山', '东莞', '珠海']
S = []
for st in permutations(range(1, 6)):
    s = dict(zip(P, st)); at = {v: k for k, v in s.items()}
    if s['甲'] != 3: continue
    if not (s['丙'] == s['丁'] + 1 and s['丁'] not in (1, 5)): continue
    for ct in permutations(CT):
        c = dict(zip(P, ct)); wc = {v: k for k, v in c.items()}
        if s[wc['深圳']] != s['甲'] - 1: continue
        if wc['佛山'] == '乙' or {s['乙'], s[wc['佛山']]} != {1, 5}: continue
        if s[wc['珠海']] != 4: continue
        S.append((s, c))
print('V1-6 解', [(fmt_line(s), c) for s, c in S])
judge('V1-6', S, {'A': lambda x: x[1]['甲'] == '广州', 'B': lambda x: x[1]['丙'] == '佛山',
                  'C': lambda x: x[0]['乙'] == 5, 'D': lambda x: x[1]['戊'] == '东莞'}, 'must', 'B')

print('=' * 30, '考法二 名次排序链（数字小=名次高）')
# V2-1 补条件使全部名次唯一
N = ['甲', '乙', '丙', '丁', '戊', '己']
S = line(N, 6, [lambda r: r['甲'] < r['乙'] < r['丙'], lambda r: r['戊'] < r['丁'] < r['丙'],
                lambda r: r['甲'] < r['戊']])
print('V2-1 基础解数', len(S))
add_cond_unique('V2-1', S, {'A': lambda r: r['己'] == 1, 'B': lambda r: r['乙'] > r['丁'],
                            'C': lambda r: r['乙'] < r['戊'] and r['己'] > r['丙'], 'D': lambda r: r['丁'] == 4},
                key=lambda r: tuple(r[x] for x in N), expect='C')
for k, f in {'A': lambda r: r['己'] == 1, 'B': lambda r: r['乙'] > r['丁'], 'D': lambda r: r['丁'] == 4}.items():
    print('   ', k, '剩余解数', sum(f(r) for r in S))

# V2-2 同单位（可传递）
P = ['甲', '乙', '丙', '丁', '戊']
def partitions(n):
    def rec(i, cur, m):
        if i == n:
            yield tuple(cur); return
        for v in range(m + 1):
            yield from rec(i + 1, cur + [v], max(m, v + 1))
    yield from rec(0, [], 0)
S = []
for p in permutations(range(1, 6)):
    r = dict(zip(P, p)); at = {v: k for k, v in r.items()}
    for u in partitions(5):
        U = dict(zip(P, u)); same = lambda a, b: U[a] == U[b]
        if at[2] == '甲' or not same('甲', at[2]) or not r['甲'] > 2: continue
        if same('乙', '甲') or at[4] == '乙' or not same('乙', at[4]): continue
        if not r['丙'] < r['丁']: continue
        if at[1] == at[5] or not same(at[1], at[5]): continue
        S.append((r, U, at))
print('V2-2 解数(名次×单位划分)', len(S), '名次排列数', len({tuple(r[x] for x in P) for r, U, at in S}))
judge('V2-2', S, {'A': lambda x: x[0]['甲'] == 5, 'B': lambda x: x[0]['乙'] == 1,
                  'C': lambda x: x[0]['丁'] == 2, 'D': lambda x: x[1][x[2][2]] == x[1][x[2][4]]}, 'mustfalse', 'D')

# V2-3 两链合并，能确定几人
N = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
S = line(N, 7, [lambda r: r['甲'] < r['乙'] < r['丙'] < r['丁'] < r['戊'],
                lambda r: r['甲'] < r['己'] < r['丙'], lambda r: r['庚'] > r['丁']])
print('V2-3 解', [fmt_line(r) for r in S])
fixed = [x for x in N if len({r[x] for r in S}) == 1]
print('   确定者', fixed)
count_options('V2-3', len(fixed), {'A': 2, 'B': 3, 'C': 4, 'D': 5}, 'B')

# V2-4 报送顺序
N = ['发改', '财政', '人社', '住建', '交通', '文旅']
S0 = line(N, 6, [lambda s: s['财政'] - s['发改'] == 2, lambda s: s['住建'] == s['人社'] + 1,
                 lambda s: s['交通'] not in (1, 6), lambda s: s['文旅'] < s['财政']])
S = [s for s in S0 if s['文旅'] == 1]
print('V2-4 基础解数', len(S0), '附加后', [fmt_line(s) for s in S])
judge('V2-4', S, {'A': lambda s: s['发改'] == 2, 'B': lambda s: s['人社'] == 5,
                  'C': lambda s: s['住建'] == 6, 'D': lambda s: s['交通'] == s['财政'] - 1}, 'must', 'D')

print('=' * 30, '考法三 环形/方桌（座位按俯视顺时针编号；面向桌心时 左手边=顺时针下一位）')
# V3-1 方桌+茶
P = ['发改', '教育', '交通', '文旅']; T = ['单丛', '普洱', '红茶', '绿茶']
n = 4
L = lambda i, k=1: (i + k) % n; R = lambda i, k=1: (i - k) % n; O = lambda i: (i + 2) % n
S = []
for st in permutations(range(n)):
    s = dict(zip(P, st))
    if s['发改'] != 0: continue     # 旋转对称，固定发改
    for tt in permutations(T):
        t = dict(zip(P, tt)); wt = {v: k for k, v in t.items()}
        if s['交通'] != R(s['发改']): continue
        if s[wt['普洱']] != O(s['教育']): continue
        if L(s[wt['单丛']]) != s['发改']: continue
        if t['教育'] == '绿茶' or t['文旅'] == '红茶': continue
        S.append((s, t))
for s, t in S:
    at = {v: k for k, v in s.items()}
    print('V3-1 解(顺时针)', [(at[i], t[at[i]]) for i in range(n)])
wt_ = lambda t, x: {v: k for k, v in t.items()}[x]
judge('V3-1', S, {'A': lambda x: x[1]['文旅'] == '绿茶', 'B': lambda x: x[0]['交通'] == O(x[0]['教育']),
                  'C': lambda x: x[0][wt_(x[1], '单丛')] == L(x[0]['文旅']), 'D': lambda x: x[1]['发改'] == '红茶'}, 'must', 'A')
# 左右手画反的考生会怎样？
L2 = lambda i, k=1: (i - k) % n; R2 = lambda i, k=1: (i + k) % n
S2 = []
for st in permutations(range(n)):
    s = dict(zip(P, st))
    if s['发改'] != 0: continue
    for tt in permutations(T):
        t = dict(zip(P, tt)); wt = {v: k for k, v in t.items()}
        if s['交通'] != R2(s['发改']): continue
        if s[wt['普洱']] != O(s['教育']): continue
        if L2(s[wt['单丛']]) != s['发改']: continue
        if t['教育'] == '绿茶' or t['文旅'] == '红茶': continue
        S2.append((s, t))
print('   左右画反时的解', [({v: k for k, v in s.items()}, t) for s, t in S2])

# V3-2 六人圆桌
P = ['甲', '乙', '丙', '丁', '戊', '己']; n = 6
L = lambda i, k=1: (i + k) % n; R = lambda i, k=1: (i - k) % n; O = lambda i: (i + 3) % n
adj = lambda a, b: (a - b) % n in (1, n - 1)
S = []
for p in permutations(range(1, n)):
    s = dict(zip(P, (0,) + p))
    if s['乙'] != O(s['甲']): continue
    if s['丙'] != L(s['甲'], 2): continue
    if not adj(s['丁'], s['丙']): continue
    if adj(s['戊'], s['甲']): continue
    S.append(s)
print('V3-2 解(顺时针从甲)', [[{v: k for k, v in s.items()}[i] for i in range(n)] for s in S])
judge('V3-2', S, {'A': lambda s: s['己'] == R(s['甲']), 'B': lambda s: s['丁'] == R(s['乙']),
                  'C': lambda s: s['戊'] == O(s['丙']), 'D': lambda s: s['戊'] == R(s['乙'])}, 'must', 'A')

# V3-3 方桌+东南西北（绝对方位）：俯视顺时针 北0 东1 南2 西3；面向桌心 左手=i+1，右手=i-1
P = ['发改', '住建', '水务', '交通']; Dn = ['北', '东', '南', '西']
def solve33(conv):
    Lf = (lambda i: (i + 1) % 4) if conv == 'ok' else (lambda i: (i - 1) % 4)
    Rt = (lambda i: (i - 1) % 4) if conv == 'ok' else (lambda i: (i + 1) % 4)
    out = []
    for p in permutations(range(4)):
        s = dict(zip(P, p))
        if s['发改'] not in (1, 2): continue
        if s['水务'] not in (1, 2): continue
        if s['水务'] != Rt(s['住建']): continue
        out.append((s, Lf, Rt))
    return out
for conv in ('ok', 'rev'):
    S = solve33(conv)
    print('V3-3', conv, [{k: Dn[v] for k, v in s.items()} for s, _, _ in S])
    opts = {'A': lambda x: x[0]['发改'] == 2, 'B': lambda x: x[0]['住建'] == 3,
            'C': lambda x: x[0]['交通'] == 1, 'D': lambda x: x[0]['发改'] == x[1](x[0]['住建'])}
    if conv == 'ok':
        judge('V3-3', S, opts, 'must', 'B')
    else:
        print('   左右画反者会选:', [k for k, f in opts.items() if all(f(x) for x in S)])
