# -*- coding: utf-8 -*-
"""第1天（试点）13道改编：独立穷举验算（v3 重写，不复用旧脚本）。座位编号约定见各题注释。"""
from lib import *

print('=' * 20, 'G1 考法一 直线排位')
# V1：政务窗口 1..6 从左到右
N = ['社保', '医保', '税务', '公积金', '不动产', '户政']
base = line(N, 6, [lambda s: s['税务'] == s['社保'] + 1,
                   lambda s: s['公积金'] - s['税务'] >= 2,
                   lambda s: abs(s['医保'] - s['户政']) == 3])
S = [s for s in base if s['不动产'] == 6]
print('V1 基础解数', len(base), '附加后', [fmt_line(s) for s in S])
judge('D1-V1', S, {'A': lambda s: s['社保'] == 1, 'B': lambda s: s['公积金'] == 4,
                   'C': lambda s: s['户政'] == 1, 'D': lambda s: s['医保'] == 5}, 'possible', 'C')

# V2：招商展位
N = list('ABCDEF')
S = line(N, 6, [lambda s: s['A'] == s['B'] + 1, lambda s: s['C'] - s['A'] >= 2,
                lambda s: s['E'] - s['D'] == 2, lambda s: s['F'] not in (1, 6)])
print('V2 解', [fmt_line(s) for s in S], '确定者', determined(S, N))
value('D1-V2', len(determined(S, N)), {'A': 1, 'B': 2, 'C': 3, 'D': 4}, 'B')

# V3：老街（位置=自西向东第几家；从东往西数第k家 = 7-位置）
N = ['凉茶', '云吞', '肠粉', '烧腊', '糖水', '早茶']
S = line(N, 6, [lambda s: s['云吞'] == s['凉茶'] + 1, lambda s: s['肠粉'] - s['云吞'] == 2,
                lambda s: s['烧腊'] not in (1, 6), lambda s: s['糖水'] < s['早茶']])
E = lambda s, k: 7 - s[k]
print('V3 解(自西向东)', [fmt_line(s) for s in S])
judge('D1-V3', S, {'A': lambda s: E(s, '烧腊') == 3, 'B': lambda s: E(s, '肠粉') == 3,
                   'C': lambda s: E(s, '云吞') == 2, 'D': lambda s: E(s, '早茶') == 2}, 'impossible', 'C')
# 误把"从东往西"按自西向东去数时，各项是否"可能"
print('   误读方向时各项可能?', {k: any(f(s) for s in S) for k, f in {'A': lambda s: s['烧腊'] == 3, 'B': lambda s: s['肠粉'] == 3,
                                                          'C': lambda s: s['云吞'] == 2, 'D': lambda s: s['早茶'] == 2}.items()})

# V4：主席台5座 + 籍贯
P = ['甲', '乙', '丙', '丁', '戊']; C = ['广州', '深圳', '佛山', '东莞', '珠海']
S = []
for st in line(P, 5, [lambda s: s['甲'] == 3, lambda s: s['丙'] == s['丁'] + 1, lambda s: s['丁'] not in (1, 5),
                      lambda s: s['乙'] in (1, 5)]):
    at = {v: k for k, v in st.items()}
    for cc in permutations(C):
        ci = dict(zip(P, cc)); who = {v: k for k, v in ci.items()}
        if st[who['深圳']] != 2: continue                          # 深圳嘉宾在甲(3号)左侧相邻
        if not ({st['乙'], st[who['佛山']]} == {1, 5}): continue    # 乙和佛山嘉宾分坐两端
        if st[who['珠海']] != 4: continue
        S.append((st, ci))
print('V4 解', [(fmt_line(a), b) for a, b in S])
judge('D1-V4', S, {'A': lambda x: x[1]['甲'] == '广州', 'B': lambda x: x[1]['丙'] == '佛山',
                   'C': lambda x: x[0]['乙'] == 5, 'D': lambda x: x[1]['戊'] == '东莞'}, 'must', 'B')

# V5：货架 同品牌不相邻、两端同品牌、乙1在甲1左边；附加 丙1在3号
items = ['甲1', '甲2', '乙1', '乙2', '丙1', '丙2']
brand = lambda x: x[0]
base = []
for p in permutations(items):
    if any(brand(p[i]) == brand(p[i + 1]) for i in range(5)): continue
    if brand(p[0]) != brand(p[5]): continue
    if p.index('乙1') > p.index('甲1'): continue
    base.append(p)
S = [p for p in base if p[2] == '丙1']
print('V5 基础解数', len(base), '附加后', [' '.join(p) for p in S])
judge('D1-V5', S, {'A': lambda p: p[0] == '乙1', 'B': lambda p: abs(p.index('甲1') - 2) == 1,
                   'C': lambda p: p[4] == '丙2', 'D': lambda p: brand(p[0]) == '乙'}, 'must', 'C')
for k, f in {'A': lambda p: p[0] == '乙1', 'B': lambda p: abs(p.index('甲1') - 2) == 1, 'D': lambda p: brand(p[0]) == '乙'}.items():
    print(f'    {k} 成立 {sum(f(p) for p in S)}/{len(S)}')

# V6：7间房 奇偶
P = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
S = line(P, 7, [lambda s: abs(s['甲'] - s['乙']) == 3, lambda s: s['丁'] == s['丙'] + 1,
                lambda s: abs(s['戊'] - s['己']) == 2, lambda s: s['庚'] not in (1, 7)])
print('V6 解数', len(S), '庚可能位置', sorted({s['庚'] for s in S}))
judge('D1-V6', S, {'A': lambda s: s['庚'] == 2, 'B': lambda s: s['庚'] == 3,
                   'C': lambda s: s['庚'] == 4, 'D': lambda s: s['庚'] == 6}, 'impossible', 'B')

print('=' * 20, 'G2 考法二 名次链（数字小=名次高）')
# V7：补条件使名次唯一
P = ['甲', '乙', '丙', '丁', '戊', '己']
base = line(P, 6, [lambda r: r['甲'] < r['乙'] < r['丙'], lambda r: r['戊'] < r['丁'] < r['丙'],
                   lambda r: r['甲'] < r['戊']])
opts = {'A': lambda r: r['己'] == 1, 'B': lambda r: r['乙'] > r['丁'],
        'C': lambda r: r['乙'] < r['戊'] and r['己'] > r['丙'], 'D': lambda r: r['丁'] == 4}
add_cond('D1-V7', base, opts, key=lambda r: tuple(sorted(r.items())), expect='C')
for k, f in opts.items():
    print(f'    补{k}后剩余 {sum(f(r) for r in base)} 种')
print('    补C后唯一排名', [fmt_line(r) for r in base if opts['C'](r)])

# V8：同一单位（等价关系，任意划分）
from itertools import product as _p
def set_partitions(lst):
    if not lst:
        yield []
        return
    first, rest = lst[0], lst[1:]
    for part in set_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part
P5 = ['甲', '乙', '丙', '丁', '戊']
parts = list(set_partitions(P5))
S = []
for r in permutations(range(1, 6)):
    rk = dict(zip(P5, r)); who = {v: k for k, v in rk.items()}
    for part in parts:
        unit = {x: i for i, blk in enumerate(part) for x in blk}
        same = lambda a, b: unit[a] == unit[b]
        second, fourth, first, fifth = who[2], who[4], who[1], who[5]
        if second == '甲' or not same('甲', second) or not rk['甲'] > 2: continue
        if same('乙', '甲'): continue
        if fourth == '乙' or not same('乙', fourth): continue
        if not rk['丙'] < rk['丁']: continue
        if not same(first, fifth): continue
        S.append((rk, unit))
print('V8 可行(名次,单位划分)数', len(S), '名次排列数', len({tuple(sorted(x[0].items())) for x in S}))
inv = lambda rk: {v: k for k, v in rk.items()}
judge('D1-V8', S, {'A': lambda x: x[0]['甲'] == 5, 'B': lambda x: x[0]['乙'] == 1, 'C': lambda x: x[0]['丁'] == 2,
                   'D': lambda x: x[1][inv(x[0])[2]] == x[1][inv(x[0])[4]]}, 'impossible', 'D')

# V9：两链合并
P = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
S = line(P, 7, [lambda r: r['甲'] < r['乙'] < r['丙'] < r['丁'] < r['戊'], lambda r: r['甲'] < r['己'] < r['丙'],
                lambda r: r['庚'] > r['丁']])
print('V9 解', [fmt_line(r) for r in S], '确定者', determined(S, P))
value('D1-V9', len(determined(S, P)), {'A': 2, 'B': 3, 'C': 4, 'D': 5}, 'B')

# V10：报送顺序
P = ['发改', '财政', '人社', '住建', '交通', '文旅']
base = line(P, 6, [lambda r: r['财政'] - r['发改'] == 2, lambda r: r['住建'] == r['人社'] + 1,
                   lambda r: r['交通'] not in (1, 6), lambda r: r['文旅'] < r['财政']])
S = [r for r in base if r['文旅'] == 1]
print('V10 基础解数', len(base), '附加后', [fmt_line(r) for r in S])
judge('D1-V10', S, {'A': lambda r: r['发改'] == 2, 'B': lambda r: r['人社'] == 5, 'C': lambda r: r['住建'] == 6,
                    'D': lambda r: r['财政'] == r['交通'] + 1}, 'must', 'D')

print('=' * 20, 'G3 考法三 方桌/圆桌（座位按俯视顺时针编号；面向桌心时，左手边=顺时针下一位，右手边=逆时针下一位）')
def solve_square(L, R):
    P = ['发改', '教育', '交通', '文旅']; T = ['单丛', '普洱', '红茶', '绿茶']
    out = []
    for seat in permutations(range(4)):
        st = dict(zip(P, seat)); at = {v: k for k, v in st.items()}
        for tt in permutations(T):
            te = dict(zip(P, tt)); who = {v: k for k, v in te.items()}
            if at[R(st['发改'])] != '交通': continue                 # 交通坐在发改的右手边
            if st[who['普洱']] != (st['教育'] + 2) % 4: continue      # 喝普洱的坐在教育对面
            if at[L(st[who['单丛']])] != '发改': continue            # 喝单丛的人左手边是发改
            if te['教育'] == '绿茶' or te['文旅'] == '红茶': continue
            out.append((st, te))
    return out
Lf = lambda i: (i + 1) % 4; Rf = lambda i: (i - 1) % 4
S = solve_square(Lf, Rf)
print('V11 解', S)
def opp(st, a, b): return (st[a] - st[b]) % 4 == 2
judge('D1-V11', S, {'A': lambda x: x[1]['文旅'] == '绿茶', 'B': lambda x: opp(x[0], '交通', '教育'),
                    'C': lambda x: {v: k for k, v in x[0].items()}[Lf(x[0]['文旅'])] == {v: k for k, v in x[1].items()}['单丛'],
                    'D': lambda x: x[1]['发改'] == '红茶'}, 'must', 'A')
S_rev = solve_square(Rf, Lf)
print('   左右画反时的解（茶的分配）', [x[1] for x in S_rev])

# V12：6人圆桌（0..5 俯视顺时针；左手边=+1）
P = ['甲', '乙', '丙', '丁', '戊', '己']
S = []
for p in permutations(range(1, 6)):
    st = dict(zip(P, (0,) + p))
    if (st['乙'] - st['甲']) % 6 != 3: continue
    if st['丙'] != (st['甲'] + 2) % 6: continue          # 丙在甲左手边第二个位置
    if (st['丁'] - st['丙']) % 6 not in (1, 5): continue
    if (st['戊'] - st['甲']) % 6 in (1, 5): continue
    S.append(st)
at = lambda st, i: {v: k for k, v in st.items()}[i % 6]
print('V12 解', [[at(s, i) for i in range(6)] for s in S])
judge('D1-V12', S, {'A': lambda s: at(s, s['甲'] - 1) == '己', 'B': lambda s: at(s, s['乙'] - 1) == '丁',
                    'C': lambda s: (s['戊'] - s['丙']) % 6 == 3, 'D': lambda s: at(s, s['乙'] - 1) == '戊'}, 'must', 'A')

# V13：绝对方位方桌（面向桌心）：南面的人右手=东，西面的人右手=南，北面的人右手=西，东面的人右手=北
right_of = {'南': '东', '西': '南', '北': '西', '东': '北'}
left_of = {v: k for k, v in right_of.items()}   # 东面的人左手=南 …（即 right_of 的逆）
left_of = {'南': '西', '西': '北', '北': '东', '东': '南'}
def solve_abs(rmap):
    P = ['发改', '住建', '水务', '交通']
    out = []
    for d in permutations(['东', '南', '西', '北']):
        s = dict(zip(P, d))
        if s['发改'] not in ('东', '南') or s['水务'] not in ('东', '南'): continue
        if rmap[s['住建']] != s['水务']: continue           # 水务坐在住建的右手边
        out.append(s)
    return out
S = solve_abs(right_of)
print('V13 解', S)
judge('D1-V13', S, {'A': lambda s: s['发改'] == '南', 'B': lambda s: s['住建'] == '西', 'C': lambda s: s['交通'] == '东',
                    'D': lambda s: left_of[s['住建']] == s['发改']}, 'must', 'B')
S_rev = solve_abs(left_of)
print('   左右画反时的解', S_rev, '→ 会误选', [k for k, f in {'A': lambda s: s['发改'] == '南', 'B': lambda s: s['住建'] == '西',
                                                       'C': lambda s: s['交通'] == '东'}.items() if all(f(x) for x in S_rev)])
summary()
