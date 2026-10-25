import itertools, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_check')
from tf import *

def one_of(names):
    return [{'w': x} for x in names]

# V1 (巩固) 民生项目 F L P, 只有一假, 问一定为真
W = list(bools(['F', 'L', 'P']))
v, r = solve(W, [lambda w: w['F'] or w['L'], lambda w: not w['F'] and not w['L'], lambda w: w['P'] or w['L'], lambda w: w['P']], false_exactly(1),
             {'A 建长者饭堂': lambda w: w['F'], 'B 不建社区图书馆': lambda w: not w['L'], 'C 建口袋公园': lambda w: w['P'], 'D 甲的说法正确': lambda w: w['F'] or w['L']})
report('V1', v, r, ['C 建口袋公园'])

# V2 (巩固) 中标设计院, 只有一真, 问说真话的是
W = one_of('甲乙丙丁')
S = {'赵': lambda w: w['w'] == '甲', '钱': lambda w: w['w'] != '甲', '孙': lambda w: w['w'] in '乙丙', '李': lambda w: w['w'] != '丁'}
v, r = solve(W, list(S.values()), exactly(1), {k: S[k] for k in S})
report('V2', v, r, ['钱'])

# V3 (深化) 隐性矛盾 条件句, 只有一真
W = list(bools(['甲', '乙']))
v, r = solve(W, [lambda w: (not w['甲']) or w['乙'], lambda w: w['甲'] and not w['乙'], lambda w: not w['甲'], lambda w: w['乙']], exactly(1),
             {'A 都参加': lambda w: w['甲'] and w['乙'], 'B 甲参加乙未': lambda w: w['甲'] and not w['乙'], 'C 甲未乙参加': lambda w: (not w['甲']) and w['乙'], 'D 都未参加': lambda w: not w['甲'] and not w['乙']})
report('V3', v, r, ['B 甲参加乙未'])

# V4 (深化) '丁说的是假话' 制造矛盾, 只有一真
W = list(bools(['A', 'B', 'C', 'D']))
sd = lambda w: w['C']
v, r = solve(W, [lambda w: w['B'], lambda w: not sd(w), lambda w: (not w['C']) and (not w['A']), sd], exactly(1),
             {'A 乙没有完成': lambda w: not w['B'], 'B 丙完成了': lambda w: w['C'], 'C 甲完成了': lambda w: w['A'], 'D 甲和丙都完成了': lambda w: w['A'] and w['C']})
report('V4', v, r, ['A 乙没有完成'])

# V5 (拓展) 都 vs 至少一个没 + 只有一假
W = list(bools(['S', 'Z', 'M']))
v, r = solve(W, [lambda w: w['S'] and w['Z'] and w['M'], lambda w: not (w['S'] and w['Z'] and w['M']), lambda w: (not w['S']) or w['Z'], lambda w: w['S'] and not w['M']], false_exactly(1),
             {'A 三支都晋级': lambda w: w['S'] and w['Z'] and w['M'], 'B 只有深圳': lambda w: w['S'] and not w['Z'] and not w['M'], 'C 深珠晋级澳门未': lambda w: w['S'] and w['Z'] and not w['M'], 'D 珠澳都晋级': lambda w: w['Z'] and w['M']})
report('V5', v, r, ['C 深珠晋级澳门未'])

# V6 (巩固) 两真两假, 问哪两句为真
W = list(bools(['甲', '乙', '丙', '丁']))
S6 = [lambda w: not any(w.values()), lambda w: not w['乙'], lambda w: (not w['乙']) or (not w['丙']), lambda w: any(w.values())]
v, r = solve(W, S6, exactly(2), {'A (1)(2)': lambda w: S6[0](w) and S6[1](w), 'B (2)(3)': lambda w: S6[1](w) and S6[2](w), 'C (3)(4)': lambda w: S6[2](w) and S6[3](w), 'D (1)(3)': lambda w: S6[0](w) and S6[2](w)})
report('V6', v, r, ['C (3)(4)'])
_, r2 = solve(W, S6, exactly(2), {'乙被通报': lambda w: w['乙'], '丙未被通报': lambda w: not w['丙']})
print('     V6 side facts must be true:', r2)

# V7 (深化) 5句只有两真: 要么 vs 都或都不
W = list(bools(['X', 'Y']))
v, r = solve(W, [lambda w: w['X'] != w['Y'], lambda w: w['X'] == w['Y'], lambda w: w['X'], lambda w: (not w['X']) or w['Y'], lambda w: not w['Y']], exactly(2),
             {'A 都报': lambda w: w['X'] and w['Y'], 'B 只报选调生': lambda w: w['X'] and not w['Y'], 'C 只报三支一扶': lambda w: (not w['X']) and w['Y'], 'D 都没报': lambda w: not w['X'] and not w['Y']})
report('V7', v, r, ['C 只报三支一扶'])

# V8 (深化) 两真两假, 问可能为真
W = list(bools(['甲', '乙', '丙', '丁']))
v, r = solve(W, [lambda w: all(w.values()), lambda w: not all(w.values()), lambda w: w['甲'], lambda w: w['甲'] or w['乙']], exactly(2),
             {'A 甲报名了': lambda w: w['甲'], 'B 乙没报名': lambda w: not w['乙'], 'C 四人都报名了': lambda w: all(w.values()), 'D 丙和丁都没报名': lambda w: not w['丙'] and not w['丁']}, 'may_true')
report('V8', v, r, ['D 丙和丁都没报名'])

# V9 (拓展) 两组矛盾 + 只有两真 -> 第五句必假
W = list(bools(['N', 'Q', 'H']))
v, r = solve(W, [lambda w: w['N'], lambda w: not w['N'], lambda w: (not w['Q']) or w['H'], lambda w: w['Q'] and not w['H'], lambda w: w['H']], exactly(2),
             {'A 南沙入选': lambda w: w['N'], 'B 前海入选': lambda w: w['Q'], 'C 横琴没有入选': lambda w: not w['H'], 'D 前海横琴都入选': lambda w: w['Q'] and w['H']})
report('V9', v, r, ['C 横琴没有入选'])

# V10 (巩固) 反对关系 + 只有一假, 问说假话的是
region = {'老林': '天河', '小吴': '天河', '小陈': '越秀', '小郑': '海珠'}
W = one_of(list(region))
S = {'甲': lambda w: region[w['w']] == '天河', '乙': lambda w: w['w'] == '老林', '丙': lambda w: region[w['w']] == '海珠', '丁': lambda w: w['w'] != '小陈'}
v, r = solve(W, list(S.values()), false_exactly(1), {k: (lambda f: (lambda w: not f(w)))(S[k]) for k in S})
report('V10', v, r, ['丙'])

# V11 (巩固) 下反对 有的/有的不 + 只有一真
W = list(bools(['甲', '乙', '丙']))
v, r = solve(W, [lambda w: any(w.values()), lambda w: not all(w.values()), lambda w: not w['甲']], exactly(1),
             {'A 都达标': lambda w: all(w.values()), 'B 都没达标': lambda w: not any(w.values()), 'C 甲达标乙未': lambda w: w['甲'] and not w['乙'], 'D 只有甲达标': lambda w: w['甲'] and not w['乙'] and not w['丙']})
report('V11', v, r, ['A 都达标'])

# V12 (深化) 反对是陷阱, 用推出关系
W = one_of('ABCD')
v, r = solve(W, [lambda w: w['w'] == 'A', lambda w: w['w'] == 'B', lambda w: w['w'] != 'C', lambda w: w['w'] in 'AB'], exactly(1),
             {x: (lambda x: (lambda w: w['w'] == x))(x) for x in 'ABCD'})
report('V12', v, r, ['D'])

# V13 (拓展) 至多一假 + 反对 + 计数
W = list(bools(['G', 'C', 'X']))
cnt = lambda w: w['G'] + w['C'] + w['X']
v, r = solve(W, [lambda w: cnt(w) >= 2, lambda w: w['G'] and not w['C'] and not w['X'], lambda w: not w['C'], lambda w: w['X']], false_at_most(1),
             {'A 只有广绣': lambda w: w['G'] and not w['C'] and not w['X'], 'B 广绣醒狮获奖潮绣未': lambda w: w['G'] and w['X'] and not w['C'], 'C 三件都获奖': lambda w: cnt(w) == 3, 'D 只有醒狮': lambda w: w['X'] and not w['G'] and not w['C']})
report('V13', v, r, ['B 广绣醒狮获奖潮绣未'])

# V14 (巩固) 只有一名专家错误, 问一定为真
W = one_of('甲乙丙')
v, r = solve(W, [lambda w: w['w'] == '甲', lambda w: w['w'] == '乙', lambda w: w['w'] != '丙'], false_exactly(1),
             {'A 甲获批': lambda w: w['w'] == '甲', 'B 乙获批': lambda w: w['w'] == '乙', 'C 丙没有获批': lambda w: w['w'] != '丙', 'D 专家一二都正确': lambda w: w['w'] == '甲' and w['w'] == '乙'})
report('V14', v, r, ['C 丙没有获批'])

# V15 (深化) 3件作品 8世界, 只有一真
W = list(bools(['Q', 'X', 'P']))
c3 = lambda w: w['Q'] + w['X'] + w['P']
v, r = solve(W, [lambda w: c3(w) == 3, lambda w: c3(w) == 1, lambda w: not w['Q'], lambda w: w['X']], exactly(1),
             {'A 骑楼获奖': lambda w: w['Q'], 'B 醒狮没有获奖': lambda w: not w['X'], 'C 侨批没有获奖': lambda w: not w['P'], 'D 只有一件获奖': lambda w: c3(w) == 1})
report('V15', v, r, ['C 侨批没有获奖'])
print('     V15 valid worlds:', v)

# V16 (拓展) 4选2, 只有一真, 代入
P = ['甲', '乙', '丙', '丁']
W = [{'s': frozenset(c)} for c in itertools.combinations(P, 2)]
v, r = solve(W, [lambda w: '甲' in w['s'], lambda w: '甲' in w['s'] or '乙' in w['s'], lambda w: '丙' not in w['s'] and '丁' not in w['s'], lambda w: ('丁' not in w['s']) or ('甲' in w['s'])], exactly(1),
             {'A 甲丁': lambda w: w['s'] == frozenset('甲丁'), 'B 乙丙': lambda w: w['s'] == frozenset('乙丙'), 'C 乙丁': lambda w: w['s'] == frozenset('乙丁'), 'D 丙丁': lambda w: w['s'] == frozenset('丙丁')})
report('V16', v, r, ['C 乙丁'])
