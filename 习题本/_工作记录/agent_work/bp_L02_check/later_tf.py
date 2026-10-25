import itertools, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_check')
from tf import *
one_of = lambda names: [{'w': x} for x in names]
def ident_solve(people, types, says):
    """says: dict speaker->function(assign)->bool. H tells truth, L lies, R anything."""
    sols = []
    for tp in types:
        a = dict(zip(people, tp))
        ok = True
        for spk, f in says.items():
            v = f(a)
            if a[spk] == 'H' and not v: ok = False
            if a[spk] == 'L' and v: ok = False
        if ok: sols.append(a)
    return sols
def fixed_points(n, conds, extra_worlds=(None,)):
    """truth vectors t (len n) consistent with conds(t, world)->list of bools that t must equal."""
    out = []
    for w in extra_worlds:
        for t in itertools.product([False, True], repeat=n):
            if list(t) == conds(t, w): out.append((t, w))
    return out

# ================= DAY 14 =================
W = list(bools(['甲', '乙', '丙']))
S = [lambda w: w['甲'] and w['乙'], lambda w: not (w['甲'] and w['乙']), lambda w: (not w['甲']) and w['乙'], lambda w: (not w['乙']) or w['丙'], lambda w: w['丙']]
v, r = solve(W, S, exactly(1), {f'第{i+1}人': (lambda f: f)(S[i]) for i in range(5)})
report('D14-1 问猜对的是', v, r, ['第1人'])

W = list(bools(['A', 'B']))
v, r = solve(W, [lambda w: (not w['B']) or w['A'], lambda w: w['B'] and not w['A'], lambda w: w['A'] and w['B'], lambda w: not w['A']], exactly(1),
             {'只办海丝': lambda w: w['A'] and not w['B'], '只办龙舟': lambda w: w['B'] and not w['A'], '都办': lambda w: w['A'] and w['B'], '都不办': lambda w: not w['A'] and not w['B']})
report('D14-2 除非否则的矛盾', v, r, ['只办海丝'])

W = list(bools(['A', 'B', 'C', 'D']))
v, r = solve(W, [lambda w: all(w.values()), lambda w: not all(w.values()), lambda w: w['A'], lambda w: (not w['B']) or w['C'], lambda w: not w['D']], exactly(1),
             {f'{k}人': (lambda k: (lambda w: sum(w.values()) == k))(k) for k in (1, 2, 3, 4)})
report('D14-3 问人数', v, r, ['2人'])

W = list(bools(['Z', 'W']))
v, r = solve(W, [lambda w: w['Z'] or not w['W'], lambda w: w['Z'], lambda w: w['Z'] or w['W'], lambda w: w['W'] and not w['Z']], exactly(2),
             {'张去王不去': lambda w: w['Z'] and not w['W'], '王去张不去': lambda w: w['W'] and not w['Z'], '都去': lambda w: w['Z'] and w['W'], '都不去': lambda w: not w['Z'] and not w['W']})
report('D14-4 两真两假问真实情况', v, r, ['王去张不去'])

W = list(bools(['A', 'B']))
v, r = solve(W, [lambda w: (not w['A']) or w['B'], lambda w: w['A'], lambda w: w['A'] and not w['B'], lambda w: (not w['A']) or not w['B']], exactly(3),
             {'甲乙都进': lambda w: w['A'] and w['B'], '甲进乙不进': lambda w: w['A'] and not w['B'], '甲不进乙进': lambda w: (not w['A']) and w['B'], '都不进': lambda w: not w['A'] and not w['B']})
report('D14-5 三真一假', v, r, ['甲进乙不进'])

W = list(bools(['A', 'B', 'C', 'D', 'E']))
v, r = solve(W, [lambda w: w['B'], lambda w: not w['C'], lambda w: w['C'], lambda w: w['A'] and w['C'], lambda w: not w['A']], false_exactly(2),
             {'乙完成了': lambda w: w['B'], '丙完成了': lambda w: w['C'], '甲没完成': lambda w: not w['A'], '甲丙都完成': lambda w: w['A'] and w['C']})
report('D14-6 矛盾+反对叠加 5人2谎', v, r, ['乙完成了'])

W = list(bools(['甲', '乙', '丙']))
S7 = [lambda w: not any(w.values()), lambda w: not w['丙'], lambda w: (not w['乙']) or (not w['丙']), lambda w: any(w.values())]
valid = [w for w in W if sum(f(w) for f in S7) == 2]
opts = {'甲捐了': lambda w: w['甲'], '乙捐了': lambda w: w['乙'], '丙捐了': lambda w: w['丙'], '(1)为假': lambda w: not S7[0](w)}
undet = [k for k, f in opts.items() if len({f(w) for w in valid}) == 2]
print(('OK ' if undet == ['甲捐了'] else 'BAD'), 'D14-7 问无法确定: undetermined =', undet)

W = list(bools(['L', 'Z', 'W']))
v, r = solve(W, [lambda w: w['L'] and w['Z'], lambda w: (not w['L']) and not w['Z'], lambda w: w['Z'], lambda w: (not w['Z']) or w['W']], false_exactly(1),
             {'三人都入选': lambda w: all(w.values()), '只有小林小周': lambda w: w['L'] and w['Z'] and not w['W'], '小林没入选': lambda w: not w['L'], '小吴没入选': lambda w: not w['W']})
report('D14-8 联言反对+只有一假', v, r, ['三人都入选'])

W = list(bools(['A', 'B', 'C']))
v, r = solve(W, [lambda w: w['A'] or w['B'], lambda w: (not w['A']) or (not w['B']), lambda w: w['A'] and not w['C'], lambda w: w['C']], exactly(1),
             {'三人都没去': lambda w: not any(w.values()), '只有甲去': lambda w: w['A'] and not w['B'] and not w['C'], '只有乙去': lambda w: w['B'] and not w['A'] and not w['C'], '甲乙都去': lambda w: w['A'] and w['B']})
report('D14-9 选言下反对+只有一真', v, r, ['三人都没去'])

W = list(bools(['Y', 'N']))  # Y=粤菜师傅案例获奖, N=南粤家政案例获奖
v, r = solve(W, [lambda w: w['Y'] and w['N'], lambda w: w['Y'] != w['N'], lambda w: not w['Y'], lambda w: w['N']], false_exactly(1),
             {'只有南粤家政获奖': lambda w: w['N'] and not w['Y'], '只有粤菜师傅获奖': lambda w: w['Y'] and not w['N'], '都获奖': lambda w: w['Y'] and w['N'], '都没获奖': lambda w: not w['Y'] and not w['N']})
report('D14-10 只有一假', v, r, ['只有南粤家政获奖'])

W = one_of('甲乙丙丁')
S11 = [lambda w: w['w'] == '甲', lambda w: w['w'] in '甲乙', lambda w: w['w'] == '丙', lambda w: w['w'] == '丁']
v, r = solve(W, S11, exactly(1),
             {'A 甲获批': lambda w: w['w'] == '甲', 'B 专家一二都对': lambda w: S11[0](w) and S11[1](w), 'C 专家二三都错': lambda w: (not S11[1](w)) and not S11[2](w), 'D 专家三四都对': lambda w: S11[2](w) and S11[3](w)}, 'may_true')
report('D14-11 推出关系+可能为真', v, r, ['C 专家二三都错'])

def cnt_true(st, w): return sum(f(w) for f in st)
S12 = [lambda w: w['A'] and w['B'], lambda w: (not w['C']) or w['A'], lambda w: not w['B'], lambda w: w['A'] or w['C']]
states = {'三个都获资助': dict(A=1, B=1, C=1), '只有A': dict(A=1, B=0, C=0), '只有C': dict(A=0, B=0, C=1), '只有B': dict(A=0, B=1, C=0)}
good = [k for k, s in states.items() if cnt_true(S12, s) == 1]
print(('OK ' if good == ['只有B'] else 'BAD'), 'D14-12 代入选项(恰一真):', good, {k: cnt_true(S12, s) for k, s in states.items()})

W = [{'d': d} for d in (1, 2, 3)]
s1 = lambda w: w['d'] == 1; s2 = lambda w: w['d'] != 2
v, r = solve(W, [lambda w: (s1(w) + s2(w)) == 1], exactly(0), {'奖在1号': lambda w: w['d'] == 1, '奖在2号': lambda w: w['d'] == 2, '奖不在3号': lambda w: w['d'] != 3, '奖在3号': lambda w: w['d'] == 3})
report('D14-13 3号说假话', v, r, ['奖不在3号'])

fp = fixed_points(3, lambda t, w: [not t[1], not t[2], (not t[0]) and (not t[1])])
print(('OK ' if fp == [((False, True, False), None)] else 'BAD'), 'D14-14 链式指控3人 fixed points:', fp)

fp = fixed_points(3, lambda t, w: [sum(t) == 1, sum(t) == 2, sum(t) == 0])
print(('OK ' if fp == [((True, False, False), None)] else 'BAD'), 'D14-15 自我指涉计数3人:', fp)

s = ident_solve(['甲', '乙'], list(itertools.product('HL', repeat=2)), {'甲': lambda a: a['乙'] == 'L', '乙': lambda a: a['甲'] == a['乙']})
print(('OK ' if s == [{'甲': 'H', '乙': 'L'}] else 'BAD'), 'D14-16 身份型2人:', s)

s = ident_solve(['甲', '乙', '丙'], list(itertools.product('HL', repeat=3)),
                {'甲': lambda a: 'L' in a.values(), '乙': lambda a: a['丙'] == 'H', '丙': lambda a: a['甲'] == 'L'})
print(('OK ' if s == [{'甲': 'H', '乙': 'L', '丙': 'L'}] else 'BAD'), 'D14-17 身份型3人:', s)

C5 = ['甲', '乙', '丙', '丁', '戊']
half = [((lambda w: w == '甲'), (lambda w: w != '乙')), ((lambda w: w == '甲'), (lambda w: w != '丙')), ((lambda w: w != '甲'), (lambda w: w == '丁'))]
sol = [w for w in C5 if all((a(w) + b(w)) == 1 for a, b in half)]
pair_sols = [[w for w in C5 if all((a(w) + b(w)) == 1 for a, b in (half[i], half[j]))] for i, j in ((0, 1), (0, 2), (1, 2))]
print(('OK ' if sol == ['戊'] else 'BAD'), 'D14-18 一人两句半真半假:', sol, '| any two speakers ->', pair_sols)

for cand in ('甲乙丙', '甲乙丙丁'):
    W = one_of(cand)
    counts = {w['w']: sum(f(w) for f in [lambda w: w['w'] == '乙', lambda w: w['w'] == '丙', lambda w: w['w'] != '丙', lambda w: w['w'] != '乙']) for w in W}
    print(('OK ' if set(counts.values()) == {2} else 'BAD'), 'D14-19 两组矛盾真话数恒定', cand, counts)

# ================= DAY 27 =================
W = list(bools(['甲', '乙', '丙', '丁']))  # True = 线下
v, r = solve(W, [lambda w: w['丁'], lambda w: (not w['甲']) or (not w['乙']), lambda w: (not w['丁']) or (not w['丙']), lambda w: w['甲'] and w['乙']], false_exactly(1),
             {'A 丙线上丁线下': lambda w: (not w['丙']) and w['丁'], 'B 甲线上': lambda w: not w['甲'], 'C 乙线下': lambda w: w['乙'], 'D 甲乙都线下': lambda w: w['甲'] and w['乙']})
report('D27-1 二值域隐性矛盾 只有一假', v, r, ['A 丙线上丁线下'])

W = one_of('ABC')
v, r = solve(W, [lambda w: w['w'] == 'A', lambda w: w['w'] in 'BC', lambda w: w['w'] != 'B', lambda w: w['w'] == 'C'], exactly(1),
             {x: (lambda x: (lambda w: w['w'] == x))(x) for x in 'ABC'})
report('D27-2 域内矛盾', v, r, ['B'])

W = list(bools(['N', 'T', 'V']))
v, r = solve(W, [lambda w: (not w['N']) or w['T'], lambda w: w['N'] and not w['T'], lambda w: (not w['V']) or w['N'], lambda w: w['V'], lambda w: not w['T']], false_exactly(1),
             {'推出N和V未推T': lambda w: w['N'] and w['V'] and not w['T'], '三项都推出': lambda w: all(w.values()), '只推出V': lambda w: w['V'] and not w['N'] and not w['T'], '推出T未推N': lambda w: w['T'] and not w['N']})
report('D27-3 只有才的矛盾+条件链 只有一假', v, r, ['推出N和V未推T'])

people = ['王', '郑', 'X']
W = list(bools(people))
v, r = solve(W, [lambda w: all(w.values()), lambda w: w['王'], lambda w: not all(w.values()), lambda w: w['郑'] or w['王']], exactly(3),
             {'小王通过': lambda w: w['王'], '小郑通过': lambda w: w['郑'], '都通过': lambda w: all(w.values()), '有人没通过': lambda w: not all(w.values())})
report('D27-4 三真一假 所有/有的', v, r, ['小王通过'])

W = list(bools(['A', 'B', 'C']))
v, r = solve(W, [lambda w: not (w['A'] and w['B']), lambda w: w['A'] and not w['C'], lambda w: w['A'] and w['B'], lambda w: (not w['A']) or w['C'], lambda w: not w['B']], exactly(3),
             {'甲去了': lambda w: w['A'], '乙没去': lambda w: not w['B'], '丙去了': lambda w: w['C'], '甲去丙没去': lambda w: w['A'] and not w['C']})
report('D27-5 两组矛盾+第五句 三真两假', v, r, ['乙没去'])

W = list(bools(['A', 'B', 'C', 'D', 'E', 'F']))
sA = lambda w: not w['B']
v, r = solve(W, [sA, lambda w: not sA(w), lambda w: w['D'], lambda w: w['C'] and w['D'], lambda w: w['B'], lambda w: not w['D']], false_exactly(2),
             {'乙丙丁都完成': lambda w: w['B'] and w['C'] and w['D'], '甲完成了': lambda w: w['A'], '丁没完成': lambda w: not w['D'], '说谎的是甲和戊': lambda w: (not sA(w)) and (not w['B'])})
report('D27-6 6人2谎', v, r, ['乙丙丁都完成'])

W = list(bools(['A', 'B', 'C', 'D', 'E']))
n = lambda w: sum(w.values())
v, r = solve(W, [lambda w: n(w) >= 3, lambda w: n(w) <= 2, lambda w: w['A'] and w['B'], lambda w: not (w['C'] or w['D'] or w['E']), lambda w: (not w['A']) or w['C']], exactly(1),
             {'甲乙都报名': lambda w: w['A'] and w['B'], '甲报名乙丙都没报': lambda w: w['A'] and not w['B'] and not w['C'], '丁戊都报名': lambda w: w['D'] and w['E'], '报名人数为2': lambda w: n(w) == 2})
report('D27-7 数量矛盾 至少3/至多2', v, r, ['甲报名乙丙都没报'])

W = list(bools(['甲', '乙', '丙']))  # True = 能在8级风中作业
v, r = solve(W, [lambda w: not w['甲'], lambda w: any(w.values()), lambda w: not all(w.values())], exactly(1),
             {'(1)为真': lambda w: not w['甲'], '(2)为真': lambda w: any(w.values()), '(3)为真': lambda w: not all(w.values())})
report('D27-8 下反对 问哪句为真', v, r, ['(2)为真'])

W = list(bools(['A', 'B', 'C']))
v, r = solve(W, [lambda w: all(w.values()), lambda w: not any(w.values()), lambda w: w['A'], lambda w: w['B']], false_at_most(1),
             {'所有窗口都实现': lambda w: all(w.values()), '只有AB实现': lambda w: w['A'] and w['B'] and not w['C'], 'C没实现': lambda w: not w['C'], '甲说了假话': lambda w: not all(w.values())})
report('D27-9 反对+至多一假', v, r, ['所有窗口都实现'])

W = list(bools(['A', 'B', 'C']))
v, r = solve(W, [lambda w: any(w.values()), lambda w: not w['A'], lambda w: w['B'], lambda w: all(w.values())], exactly(1),
             {'B社区没达标': lambda w: not w['B'], 'A社区达标': lambda w: w['A'], '都没达标': lambda w: not any(w.values()), 'C社区达标': lambda w: w['C']})
report('D27-10 下反对(有的/某个不)', v, r, ['B社区没达标'])

W = one_of('甲乙丙丁戊')
v, r = solve(W, [lambda w: w['w'] == '甲', lambda w: w['w'] == '乙', lambda w: w['w'] in '甲丙', lambda w: w['w'] != '丙', lambda w: w['w'] in '乙戊'], exactly(2),
             {x: (lambda x: (lambda w: w['w'] == x))(x) for x in '甲乙丙丁戊'})
report('D27-11 反对+下反对+推出 只有两真', v, r, ['戊'])

W = list(bools(['Q', 'X', 'P']))
c3 = lambda w: w['Q'] + w['X'] + w['P']
v, r = solve(W, [lambda w: c3(w) == 3, lambda w: c3(w) == 1, lambda w: not w['Q'], lambda w: w['X']], exactly(2),
             {'骑楼获奖': lambda w: w['Q'], '醒狮没获奖': lambda w: not w['X'], '侨批获奖': lambda w: w['P'], '三件都获奖': lambda w: c3(w) == 3})
report('D27-12 3件作品只有两真', v, r, ['侨批获奖'])

states = {'只有A': dict(A=1, B=0, C=0), '只有C': dict(A=0, B=0, C=1), 'A和B': dict(A=1, B=1, C=0), 'B和C': dict(A=0, B=1, C=1)}
good = [k for k, s in states.items() if cnt_true(S12, s) == 2]
print(('OK ' if good == ['只有C'] else 'BAD'), 'D27-13 代入选项(恰两真):', good, {k: cnt_true(S12, s) for k, s in states.items()})

W = [{'d': d} for d in (1, 2, 3, 4)]
t1 = lambda w: w['d'] == 1; t2 = lambda w: w['d'] != 1; t3 = lambda w: w['d'] != 3
v, r = solve(W, [lambda w: (t1(w) + t2(w) + t3(w)) == 1], exactly(1), {f'{d}号门': (lambda d: (lambda w: w['d'] == d))(d) for d in (1, 2, 3, 4)})
report('D27-14 4门 4号说真话', v, r, ['3号门'])

fp = fixed_points(4, lambda t, w: [not t[1], not t[2], not t[3], (not t[0]) and (not t[1])])
print(('OK ' if fp == [((True, False, True, False), None)] else 'BAD'), 'D27-15 链式指控4人:', fp)

fp = fixed_points(3, lambda t, w: [t[1] != t[2], t[0] and (w == 'A'), sum(t) <= 1], extra_worlds=('A', 'B'))
print(('OK ' if fp == [((True, True, False), 'A')] else 'BAD'), 'D27-16 自我指涉+内容 (奖品在A/B箱):', fp)

sols = []
for a_ in itertools.product('HL', repeat=2):
    for ex in ('左', '右'):
        a = {'甲': a_[0], '乙': a_[1]}
        s1 = (a['甲'] == 'L' or a['乙'] == 'L'); s2 = (ex == '左')
        if (s1 == (a['甲'] == 'H')) and (s2 == (a['乙'] == 'H')): sols.append((a, ex))
print(('OK ' if sols == [({'甲': 'H', '乙': 'L'}, '右')] else 'BAD'), 'D27-17 身份型+内容:', sols)

half27 = [((lambda w: w in ('甲', '乙')), (lambda w: w != '丙')), ((lambda w: w == '丙'), (lambda w: w != '丁')), ((lambda w: w == '乙'), (lambda w: w in ('丙', '丁')))]
sol = [w for w in C5 if all((a(w) + b(w)) == 1 for a, b in half27)]
print(('OK ' if len(sol) == 1 else 'BAD'), 'D27-18 一人两句(含或):', sol)

s = ident_solve(['甲', '乙', '丙'], list(itertools.permutations('HLR')), {'甲': lambda a: a['乙'] == 'H', '乙': lambda a: a['甲'] == 'H', '丙': lambda a: a['甲'] == 'L'})
print(('OK ' if s == [{'甲': 'L', '乙': 'R', '丙': 'H'}] else 'BAD'), 'D27-19 诚实/说谎/随机各一:', s)
