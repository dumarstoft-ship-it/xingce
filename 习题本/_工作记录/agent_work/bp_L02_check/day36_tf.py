import itertools, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_check')
from tf import *
exec(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_check/later_tf.py').read().split('# ================= DAY 14 =================')[0].split('from tf import *')[1])

C5 = ['甲', '乙', '丙', '丁', '戊']
half27 = [((lambda w: w == '甲'), (lambda w: w != '乙')), ((lambda w: w == '乙'), (lambda w: w in ('丙', '戊'))), ((lambda w: w == '丁'), (lambda w: w in ('乙', '戊')))]
sol = [w for w in C5 if all((a(w) + b(w)) == 1 for a, b in half27)]
print(('OK ' if sol == ['戊'] else 'BAD'), 'D27-18(fixed) 一人两句(含或):', sol)

W = list(bools(['A', 'B', 'C', 'D']))
v, r = solve(W, [lambda w: (not w['A']) or w['B'], lambda w: w['A'] and not w['B'], lambda w: all(w.values()), lambda w: not all(w.values()), lambda w: w['C'], lambda w: not w['D']], exactly(2),
             {'甲完成': lambda w: w['A'], '乙没完成': lambda w: not w['B'], '丙没完成丁完成': lambda w: (not w['C']) and w['D'], '都完成': lambda w: all(w.values())})
report('D36-1 两组隐性矛盾 只有两真', v, r, ['丙没完成丁完成'])

W = list(bools(['A', 'B', 'C', 'D']))
v, r = solve(W, [lambda w: w['A'] or w['B'], lambda w: not w['A'] and not w['B'], lambda w: (not w['C']) or not w['A'], lambda w: w['C'], lambda w: (not w['B']) or w['D'], lambda w: not w['D']], false_exactly(1),
             {'只有C入选': lambda w: w['C'] and not w['A'] and not w['B'] and not w['D'], 'A和C入选': lambda w: w['A'] and w['C'], 'B入选': lambda w: w['B'], 'C和D入选': lambda w: w['C'] and w['D']})
report('D36-2 矛盾+推出 只有一假 连推', v, r, ['只有C入选'])

W = list(bools(['X', 'Y']))
v, r = solve(W, [lambda w: w['X'], lambda w: not w['X'], lambda w: w['X'] and w['Y'], lambda w: not w['Y']], exactly(1),
             {'X入选Y没入选': lambda w: w['X'] and not w['Y'], 'X没入选Y入选': lambda w: (not w['X']) and w['Y'], '都入选': lambda w: w['X'] and w['Y'], '都没入选': lambda w: not w['X'] and not w['Y']})
report('D36-3 评价链 只有一真', v, r, ['X没入选Y入选'])

names = ['甲', '乙', '丙', '丁', '戊', '己']
W = list(bools(names))
st_yi = lambda w: w['丙']
S71 = [lambda w: not w['甲'], st_yi, lambda w: not any(w.values()), lambda w: not st_yi(w), lambda w: w['乙'], lambda w: w['甲'] != w['丙']]
for k in (1, 3):
    valid = [w for w in W if sum(f(w) for f in S71) == 6 - k]
    print('   2020SZS-71 with', k, 'liars: count(甲乙丙 completed) values =', sorted({w['甲'] + w['乙'] + w['丙'] for w in valid}), '| #worlds', len(valid))

W = list(bools(['A', 'B', 'C']))
v, r = solve(W, [lambda w: w['A'] != w['B'], lambda w: w['A'] == w['B'], lambda w: w['C'], lambda w: (not w['B']) or w['C']], exactly(2),
             {'没去B也没去C': lambda w: not w['B'] and not w['C'], '去了A': lambda w: w['A'], '去了B': lambda w: w['B'], '三个都去': lambda w: all(w.values())})
report('D36-5 要么/都或都不 两真两假', v, r, ['没去B也没去C'])

W = list(bools(['A', 'B', 'C']))
v, r = solve(W, [lambda w: w['A'], lambda w: not w['A'], lambda w: w['B'] and w['C'], lambda w: (not w['B']) or not w['C'], lambda w: w['B'], lambda w: w['A'] or w['B']], exactly(3),
             {'甲获奖乙未获奖': lambda w: w['A'] and not w['B'], '丙获奖': lambda w: w['C'], '乙获奖': lambda w: w['B'], '甲乙都未获奖': lambda w: not w['A'] and not w['B']})
report('D36-6 6句三真三假', v, r, ['甲获奖乙未获奖'])

W = list(bools(['A', 'B', 'C', 'D', 'E']))
n = lambda w: sum(w.values())
S7 = [lambda w: n(w) >= 3, lambda w: n(w) <= 2, lambda w: w['A'] and w['B'], lambda w: w['C'], lambda w: not w['D'] and not w['E']]
valid = [w for w in W if sum(f(w) for f in S7) == 2]
facts = {'甲乙都参加': lambda w: w['A'] and w['B'], '丙参加': lambda w: w['C'], '丙没参加': lambda w: not w['C'], '丁戊至少一人参加': lambda w: w['D'] or w['E'], '参加人数不少于3': lambda w: n(w) >= 3, '参加人数至多2': lambda w: n(w) <= 2, '甲乙中至少一人没参加': lambda w: not (w['A'] and w['B'])}
print('   D36-7 probe: #valid', len(valid), '| forced:', [k for k, f in facts.items() if all(f(w) for w in valid)], '| impossible:', [k for k, f in facts.items() if not any(f(w) for w in valid)])

W = list(bools(['A', 'B', 'C']))
v, r = solve(W, [lambda w: w['A'] and w['B'], lambda w: not w['A'] and not w['B'], lambda w: w['A'] or w['C'], lambda w: (not w['A']) or not w['C']], exactly(1),
             {'甲达标': lambda w: w['A'], '乙达标': lambda w: w['B'], '乙丙恰一个达标': lambda w: w['B'] != w['C'], '都达标': lambda w: all(w.values())})
report('D36-8 反对+下反对 只有一真', v, r, ['乙丙恰一个达标'])

W = one_of('甲乙丙丁戊')
v, r = solve(W, [lambda w: w['w'] == '甲', lambda w: w['w'] == '乙', lambda w: w['w'] != '丙', lambda w: w['w'] in '甲丁', lambda w: w['w'] != '戊'], false_at_most(1),
             {x: (lambda x: (lambda w: w['w'] == x))(x) for x in '甲乙丙丁戊'})
report('D36-9 反对+至多一假', v, r, ['甲'])

W = list(bools(['G', 'C', 'X']))
c3 = lambda w: w['G'] + w['C'] + w['X']
v, r = solve(W, [lambda w: c3(w) == 1, lambda w: c3(w) == 2, lambda w: w['G'], lambda w: (not w['C']) or not w['X'], lambda w: w['C']], false_at_most(1),
             {'广绣潮绣获奖醒狮未': lambda w: w['G'] and w['C'] and not w['X'], '只有广绣': lambda w: w['G'] and not w['C'] and not w['X'], '三件都获奖': lambda w: c3(w) == 3, '广绣醒狮获奖': lambda w: w['G'] and w['X']})
report('D36-10 数量反对+至多一假', v, r, ['广绣潮绣获奖醒狮未'])

S12 = [lambda w: w['A'] and w['B'], lambda w: (not w['C']) or w['A'], lambda w: not w['B'], lambda w: w['A'] or w['C']]
allst = {''.join(k for k in 'ABC' if s[k]) or '都没有': s for s in [dict(zip('ABC', b)) for b in itertools.product([0, 1], repeat=3)]}
three = [k for k, s in allst.items() if sum(f(s) for f in S12) == 3]
print(('OK ' if sorted(three) == sorted(['A', 'AB', 'ABC', 'AC']) else 'BAD'), 'D36-12 恰三真的状态:', three, '-> 只有C不可能:', 'C' not in three)

# D36-13 补充第四句型
base = [lambda w: w['A'] and w['B'], lambda w: not w['A'], lambda w: (not w['B']) or w['C']]
cands = {'B没有入选': lambda w: not w['B'], 'C没有入选': lambda w: not w['C'], 'A入选了': lambda w: w['A'], 'B和C都入选了': lambda w: w['B'] and w['C']}
W = list(bools(['A', 'B', 'C']))
res = {}
for k, f in cands.items():
    valid = [w for w in W if sum(g(w) for g in base + [f]) == 1]
    res[k] = (len(valid), bool(valid) and all(w['C'] for w in valid))
print('   D36-13 补充句: {option: (#worlds, C一定入选?)} =', res)

fp = fixed_points(4, lambda t, w: [sum(t) == 1, sum(t) == 2, sum(t) == 3, sum(t) == 0])
print(('OK ' if fp == [((True, False, False, False), None)] else 'BAD'), 'D36-15 自我指涉计数4人:', fp)

P3 = ['甲', '乙', '丙']
worlds = [{'X': X, '甲': a, '乙': b, '丙': c} for X in P3 for a in ['乙', '丙'] for b in ['甲', '丙'] for c in ['甲', '乙']]
truth = lambda w, p: w[p] == w['X']
base_w = [w for w in worlds if truth(w, '乙')]
ded = {s: {w['X'] for w in base_w if truth(w, '丙') == s} for s in (True, False)}
told = [s for s in ded if len(ded[s]) == 1]
final = [w for w in base_w if truth(w, '丙') in told]
opts = {'甲是真凶': lambda w: w['X'] == '甲', '丙是真凶': lambda w: w['X'] == '丙', '甲说了真话': lambda w: truth(w, '甲'), '丙说了假话': lambda w: not truth(w, '丙')}
res = [k for k, f in opts.items() if all(f(w) for w in final)]
print(('OK ' if res == ['甲是真凶'] else 'BAD'), 'D36-14 元信息换皮:', ded, '->', res)

ok_lines = {}
for line, f in {'我是说谎者': lambda a, me, other: a[me] == 'L', '我是诚实者': lambda a, me, other: a[me] == 'H', '我的同伴是说谎者': lambda a, me, other: a[other] == 'L', '我们两人都是说谎者': lambda a, me, other: a[me] == 'L' and a[other] == 'L'}.items():
    possible = any(f(dict(甲=x, 乙=y), '甲', '乙') == (x == 'H') for x in 'HL' for y in 'HL')
    ok_lines[line] = possible
print(('OK ' if [k for k, p in ok_lines.items() if not p] == ['我是说谎者'] else 'BAD'), 'D36-16 不可能说出的话:', ok_lines)

boxes = ['红', '黄', '蓝']
stm = {'红': lambda p: p == '黄', '黄': lambda p: p != '黄', '蓝': lambda p: p == '红'}
ded = {s: [p for p in boxes if stm['红'](p) == s] for s in (True, False)}
known = [s for s in ded if len(ded[s]) == 1]
print(('OK ' if known == [True] and ded[True] == ['黄'] else 'BAD'), 'D36-17 元信息(盒子):', ded)

s = ident_solve(P3, list(itertools.product('HL', repeat=3)),
                {'甲': lambda a: a['甲'] == 'L' and a['乙'] == 'L', '乙': lambda a: a['甲'] == 'L' or a['丙'] == 'L', '丙': lambda a: a['乙'] == 'L'})
print(('OK ' if s == [{'甲': 'L', '乙': 'H', '丙': 'L'}] else 'BAD'), 'D36-18 身份型3人(自含):', s)

W = one_of('甲乙丙丁')
S21 = [lambda w: w['w'] == '乙', lambda w: w['w'] in '丙丁', lambda w: w['w'] != '丁', lambda w: w['w'] != '甲']
counts = {w['w']: sum(f(w) for f in S21) for w in W}
print(('OK ' if max(counts.values()) == 3 else 'BAD'), 'D36-21 真话最多几人:', counts, 'max=', max(counts.values()), 'min=', min(counts.values()))
