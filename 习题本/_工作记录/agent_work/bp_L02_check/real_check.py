import itertools, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_check')
from tf import *

# 2023GD-63: one of 甲乙丙 passes; exactly 1 expert right; ask which is NECESSARILY FALSE
W = [{'w': x} for x in '甲乙丙']
v, r = solve(W, [lambda w: w['w'] != '甲', lambda w: w['w'] == '乙', lambda w: w['w'] != '丙'], exactly(1),
             {'A': lambda w: w['w'] != '甲', 'B': lambda w: w['w'] != '丙', 'C': lambda w: w['w'] == '甲', 'D': lambda w: w['w'] == '乙'}, 'must_false')
report('2023GD-63', v, r, ['D'])

# 2023SD-66: only one false
cont = {'法国': 'EU', '克罗地亚': 'EU', '德国': 'EU', '阿根廷': 'SA', '巴西': 'SA', '摩洛哥': 'AF'}
W = []
for ch in cont:
    for argtop4 in [False, True]:
        if ch == '阿根廷' and not argtop4:
            continue
        W.append({'ch': ch, 'arg4': argtop4})
v, r = solve(W, [lambda w: cont[w['ch']] == 'EU', lambda w: w['ch'] == '法国', lambda w: cont[w['ch']] == 'SA', lambda w: not w['arg4']],
             false_exactly(1),
             {'A': lambda w: cont[w['ch']] != 'EU', 'B': lambda w: w['ch'] != '法国', 'C': lambda w: cont[w['ch']] != 'SA', 'D': lambda w: w['arg4']})
report('2023SD-66', v, r, ['C'])

# 2023ZJA-102: two false
W = list(bools(['秦', '魏', '汉']))
v, r = solve(W, [lambda w: (not w['魏']) or w['汉'], lambda w: (not w['秦']) and (not w['魏']), lambda w: w['秦'] or w['魏']], false_exactly(2),
             {'A': lambda w: w['魏'] and w['汉'], 'B': lambda w: (not w['魏']) and w['汉'], 'C': lambda w: w['魏'] and not w['汉'], 'D': lambda w: (not w['魏']) and not w['汉']})
report('2023ZJA-102', v, r, ['C'])

# 2025HB-110: 5 people, champion/runner-up/third distinct; exactly one true
P = ['周', '吴', '郑', '王', '钱']
W = [{'c': a, 'y': b, 'j': c} for a, b, c in itertools.permutations(P, 3)]
top3 = lambda w, x: x in (w['c'], w['y'], w['j'])
v, r = solve(W, [lambda w: w['c'] == '郑', lambda w: w['c'] in ('吴', '周', '钱'), lambda w: w['c'] != '郑', lambda w: not top3(w, '钱'), lambda w: w['y'] != '王'],
             exactly(1), {'A': lambda w: w['y'] == '王', 'B': lambda w: w['y'] == '吴', 'C': lambda w: w['y'] == '郑', 'D': lambda w: w['y'] == '钱'})
report('2025HB-110', v, r, ['A'])

# 2025SD-94: exactly one true
W = list(bools(['体', '实', '教']))
v, r = solve(W, [lambda w: w['体'] or w['实'], lambda w: (not w['体']) and not w['实'], lambda w: w['实'] or not w['教']], exactly(1),
             {'A': lambda w: w['体'], 'B': lambda w: w['实'], 'C': lambda w: w['教'], 'D': lambda w: w['体'] and w['教']})
report('2025SD-94', v, r, ['C'])

# 2020SD-66: two true two false
W = list(bools(['甲', '乙', '丙', '丁']))
v, r = solve(W, [lambda w: not any(w.values()), lambda w: not w['丁'], lambda w: (not w['乙']) or (not w['丁']), lambda w: any(w.values())], exactly(2),
             {'A': lambda w: not w['甲'], 'B': lambda w: w['乙'], 'C': lambda w: not w['丙'], 'D': lambda w: w['丁']})
report('2020SD-66', v, r, ['D'])

# 2020SZS-67: door; s3 true (s3 = exactly one of s1,s2 true)
W = [{'d': d} for d in (1, 2, 3)]
s1 = lambda w: w['d'] == 1
s2 = lambda w: w['d'] != 2
v, r = solve(W, [lambda w: (s1(w) + s2(w)) == 1], exactly(1), {'A': lambda w: w['d'] == 1, 'B': lambda w: w['d'] == 2, 'C': lambda w: w['d'] == 3})
report('2020SZS-67', v, r, ['C'])

# 2020SZS-71: six members, exactly two lie; ask number completed among 甲乙丙
names = ['甲', '乙', '丙', '丁', '戊', '己']
W = list(bools(names))
st_yi = lambda w: w['丙']
v, r = solve(W, [lambda w: not w['甲'], st_yi, lambda w: not any(w.values()), lambda w: not st_yi(w), lambda w: w['乙'], lambda w: w['甲'] != w['丙']],
             false_exactly(2), {k: (lambda kk: (lambda w: (w['甲'] + w['乙'] + w['丙']) == kk))(kk) for k, kk in zip('ABCD', (0, 1, 2, 3))})
report('2020SZS-71', v, r, ['C'])

# 2022GD-61: exactly one guess correct
W = list(bools(['稻', '播']))
v, r = solve(W, [lambda w: w['稻'] and w['播'], lambda w: w['稻'] != w['播'], lambda w: not w['稻'], lambda w: w['播']], exactly(1),
             {'A': lambda w: w['稻'], 'B': lambda w: not w['稻'], 'C': lambda w: w['播'], 'D': lambda w: not w['播']})
report('2022GD-61', v, r, ['D'])

# 2022GK-109
W = list(bools(['陈', '李', '刘']))
v, r = solve(W, [lambda w: w['陈'] and w['李'], lambda w: not (w['陈'] and w['李']), lambda w: w['陈'] and not w['李'], lambda w: (not w['陈']) and w['李'], lambda w: (not w['陈']) or w['刘']],
             exactly(1), {'A': lambda w: not w['陈'] and not w['李'], 'B': lambda w: w['陈'] and w['刘'], 'C': lambda w: not w['李'] and not w['刘'], 'D': lambda w: w['陈'] and w['李']})
report('2022GK-109', v, r, ['D'])

# 2022SD-75
W = list(bools(['甲', '乙', '丙']))
v, r = solve(W, [lambda w: w['甲'], lambda w: not all(w.values()), lambda w: any(w.values())], exactly(1),
             {'A': lambda w: w['乙'] and not w['丙'], 'B': lambda w: w['甲'] and not w['乙'], 'C': lambda w: not w['乙'] and not w['丙'], 'D': lambda w: w['丙'] and not w['甲']})
report('2022SD-75', v, r, ['C'])

# 2022ZJA-101
W = list(bools(['甲', '乙']))
v, r = solve(W, [lambda w: (not w['甲']) or w['乙'], lambda w: w['甲'], lambda w: w['甲'] and not w['乙'], lambda w: w['甲'] or w['乙']], exactly(2),
             {'A': lambda w: w['甲'] and w['乙'], 'B': lambda w: not w['甲'] and not w['乙'], 'C': lambda w: w['甲'] and not w['乙'], 'D': lambda w: not w['甲'] and w['乙']})
report('2022ZJA-101', v, r, ['D'])

# 2023SC-85: each person shop(True) or movie(False)
W = list(bools(['甲', '乙', '丙', '丁']))
v, r = solve(W, [lambda w: w['丁'], lambda w: (not w['甲']) or (not w['乙']), lambda w: w['丁'] or (not w['丙']), lambda w: w['甲'] and w['乙']], exactly(1),
             {'A': lambda w: w['乙'] and not w['甲'], 'B': lambda w: w['丙'] and not w['乙'], 'C': lambda w: w['丙'] and not w['丁'], 'D': lambda w: not w['甲'] and not w['乙']})
report('2023SC-85', v, r, ['C'])

# 2024HB-102: which two mothers are right
W = list(bools(['陈', '林']))
S = {'吴': lambda w: w['陈'] or not w['林'], '李': lambda w: w['陈'], '郑': lambda w: w['陈'] or w['林'], '张': lambda w: w['林'] and not w['陈']}
v, r = solve(W, list(S.values()), exactly(2),
             {'A': lambda w: S['李'](w) and S['郑'](w), 'B': lambda w: S['吴'](w) and S['张'](w), 'C': lambda w: S['吴'](w) and S['李'](w), 'D': lambda w: S['郑'](w) and S['张'](w)})
report('2024HB-102', v, r, ['D'])

# 2024SC-84: tourists 王, 郑, X; each buys subset of {白,青,彩}
types = ['白', '青', '彩']
subsets = [frozenset(c) for k in range(4) for c in itertools.combinations(types, k)]
W = [{'王': a, '郑': b, 'X': c} for a in subsets for b in subsets for c in subsets]
allp = ['王', '郑', 'X']
v, r = solve(W, [lambda w: all(len(w[p]) > 0 for p in allp), lambda w: '白' in w['王'], lambda w: any(len(w[p]) == 0 for p in allp), lambda w: ('青' in w['郑']) or ('白' in w['王'])],
             exactly(2), {'A': lambda w: len(w['王']) == 0, 'B': lambda w: '青' in w['郑'], 'C': lambda w: '白' in w['王'], 'D': lambda w: any('青' not in w[p] for p in allp)})
report('2024SC-84', v, r, ['B'])

# 2020SZS-80 meta puzzle: culprit X; each accuses one of the other two; 甲 truthful.
P3 = ['甲', '乙', '丙']
worlds = []
for X in P3:
    for a in ['乙', '丙']:
        for b in ['甲', '丙']:
            for c in ['甲', '乙']:
                worlds.append({'X': X, '甲': a, '乙': b, '丙': c})
truth = lambda w, p: w[p] == w['X']
base = [w for w in worlds if truth(w, '甲')]
ded = {}
for s in (True, False):
    cands = {w['X'] for w in base if truth(w, '丙') == s}
    ded[s] = cands
    print('   丙 status told =', s, '-> culprit candidates', cands)
told = [s for s in ded if len(ded[s]) == 1]
final = [w for w in base if truth(w, '丙') in told]
opts = {'A': lambda w: w['X'] == '乙', 'B': lambda w: truth(w, '乙'), 'C': lambda w: not truth(w, '丙'), 'D': lambda w: w['X'] == '丙'}
res = [k for k, f in opts.items() if all(f(w) for w in final)]
print(('OK ' if res == ['A'] else 'BAD'), '2020SZS-80: answer', res, 'expect [A]')
