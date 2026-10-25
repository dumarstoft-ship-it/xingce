import itertools, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_check')
from tf import *
# D36-4 six members, two liars; ask who lied
N = ['甲', '乙', '丙', '丁', '戊', '己']
W = list(bools(N))
s_wu = lambda w: (not w['甲']) or (not w['丙'])
S = {'甲': lambda w: w['甲'] != w['乙'], '乙': lambda w: not any(w.values()), '丙': lambda w: w['乙'] != w['丙'],
     '丁': lambda w: not s_wu(w), '戊': s_wu, '己': lambda w: w['甲']}
liar = lambda w, p: not S[p](w)
v, r = solve(W, list(S.values()), false_exactly(2),
             {'乙和戊': lambda w: liar(w, '乙') and liar(w, '戊'), '丁和己': lambda w: liar(w, '丁') and liar(w, '己'),
              '乙和丁': lambda w: liar(w, '乙') and liar(w, '丁'), '甲和戊': lambda w: liar(w, '甲') and liar(w, '戊')})
report('D36-4 6人2谎 问说谎者', v, r, ['乙和戊'])
print('     甲乙丙完成人数:', sorted({w['甲'] + w['乙'] + w['丙'] for w in v}))

# D36-7 恰2人 vs 不是2人 + 甲乙都参加 + 丙丁戊都没参加, 两真两假
W = list(bools(['A', 'B', 'C', 'D', 'E']))
n = lambda w: sum(w.values())
v, r = solve(W, [lambda w: n(w) == 2, lambda w: n(w) != 2, lambda w: w['A'] and w['B'], lambda w: not (w['C'] or w['D'] or w['E'])], exactly(2),
             {'恰有2人参加': lambda w: n(w) == 2, '甲参加了': lambda w: w['A'], '参加的不是2人': lambda w: n(w) != 2, '丙参加了': lambda w: w['C']})
report('D36-7 数量矛盾 两真两假', v, r, ['参加的不是2人'])

# D36-11 4选2, 只有两真
P = ['甲', '乙', '丙', '丁']
W = [{'s': frozenset(c)} for c in itertools.combinations(P, 2)]
v, r = solve(W, [lambda w: '甲' in w['s'], lambda w: '甲' in w['s'] or '乙' in w['s'], lambda w: '甲' not in w['s'] and '丙' not in w['s'], lambda w: ('乙' not in w['s']) or ('甲' in w['s'])], exactly(2),
             {k: (lambda k: (lambda w: w['s'] == frozenset(k)))(k) for k in ('甲乙', '乙丙', '乙丁', '丙丁')})
report('D36-11 4选2只有两真', v, r, ['乙丁'])

# D36-19 一人全对、一人全错、一人半对
C = ['甲', '乙', '丙', '丁', '戊']
spk = {'小赵': (lambda w: w == '甲', lambda w: w != '乙'), '小钱': (lambda w: w == '甲', lambda w: w != '丁'), '小孙': (lambda w: w == '乙', lambda w: w != '丙')}
sols = [(w, {k: a(w) + b(w) for k, (a, b) in spk.items()}) for w in C if sorted(a(w) + b(w) for a, b in spk.values()) == [0, 1, 2]]
print(('OK ' if len(sols) == 1 and sols[0][0] == '乙' else 'BAD'), 'D36-19 全对/全错/半对:', sols)

# D36-20 诚实/说谎/随机, 问随机者
P3 = ['甲', '乙', '丙']
sols = []
for perm in itertools.permutations('HLR'):
    a = dict(zip(P3, perm))
    says = {'甲': a['乙'] != 'H', '乙': a['甲'] == 'H', '丙': a['甲'] == 'L'}
    if all(not ((a[p] == 'H' and not says[p]) or (a[p] == 'L' and says[p])) for p in P3): sols.append(a)
print(('OK ' if sols == [{'甲': 'H', '乙': 'R', '丙': 'L'}] else 'BAD'), 'D36-20 随机者是乙:', sols)
