# real 2026CQ-100  7人分去P、Q、R、S四个值班点（每点1~3人，Q点3人），哪项必然为真？
# 回忆版条件(2)缺字"****"，按最自然的补全"如果……，那么只有丁去S值班点"（S点只有丁一人）求解；
# 另附"那么丁去S"的读法作对照，说明"只有"二字不可少。
from itertools import product

PEOPLE = ['甲', '乙', '丙', '丁', '戊', '己', '庚']

def solve(cond2):
    out = []
    for asg in product('PQRS', repeat=7):
        a = dict(zip(PEOPLE, asg))
        cnt = {k: asg.count(k) for k in 'PQRS'}
        if any(not 1 <= c <= 3 for c in cnt.values()) or cnt['Q'] != 3:
            continue
        if cnt['R'] != cnt['P']:                                       # (1)
            continue
        if not cond2(a):                                               # (2)
            continue
        S = {x for x in PEOPLE if a[x] == 'S'}
        if ('丁' not in S or '戊' not in S) and not ({'乙', '庚'} <= S):  # (3) 只有乙和庚去S，丁或戊才不去S
            continue
        out.append(a)
    return out

def at_most_two_abc_in_Q(a):
    return sum(a[x] == 'Q' for x in '甲乙丙') <= 2

def cond2_only_ding(a):     # 甲乙丙至多2人去Q → S点只有丁
    return (not at_most_two_abc_in_Q(a)) or {x for x in PEOPLE if a[x] == 'S'} == {'丁'}

def cond2_ding_in_S(a):     # 对照读法：甲乙丙至多2人去Q → 丁去S
    return (not at_most_two_abc_in_Q(a)) or a['丁'] == 'S'

OPTS = {
    'A': lambda a: a['乙'] == 'Q' and a['戊'] == 'S',
    'B': lambda a: a['甲'] == 'Q' and a['丁'] == 'P',
    'C': lambda a: a['己'] == 'P' and a['庚'] == 'R',
    'D': lambda a: a['丙'] == 'P' and a['戊'] == 'S',
}

alt = solve(cond2_ding_in_S)
print('对照读法解数', len(alt), '必然为真的选项', [k for k, f in OPTS.items() if all(f(a) for a in alt)])

sols = solve(cond2_only_ding)
for a in sols:
    print({k: ''.join(x for x in PEOPLE if a[x] == k) for k in 'PQRS'})
assert sols
hits = [k for k, f in OPTS.items() if all(f(a) for a in sols)]
assert len(hits) == 1, hits
print(hits[0])
