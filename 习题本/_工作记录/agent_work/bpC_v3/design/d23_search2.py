import sys; sys.path.insert(0, '..')
from lib import *
import random
random.seed(31)

# (a) 工序带时长：随机找"某一天在做哪道工序唯一"的设计
names = 'ABCDE'
best = []
for trial in range(20000):
    DUR = {x: random.choice([1, 2, 3]) for x in names}
    if sum(DUR.values()) not in (9, 10): continue
    cons = random.sample([
        ('B在A完成后才开始', lambda p: p['A'] < p['B']),
        ('D紧接在C之后', lambda p: p['D'] == p['C'] + 1),
        ('E不是最后一道', lambda p: p['E'] != 4),
        ('A不是第一道', lambda p: p['A'] != 0),
        ('C在E之前', lambda p: p['C'] < p['E']),
        ('B不是最后一道', lambda p: p['B'] != 4),
        ('E紧接在B之后', lambda p: p['E'] == p['B'] + 1),
    ], 4)
    sols = []
    for order in permutations(names):
        pos = {x: i for i, x in enumerate(order)}
        if all(f(pos) for _, f in cons): sols.append(order)
    if not (2 <= len(sols) <= 4): continue
    def sched(o):
        d = {}; t = 1
        for x in o:
            for k in range(DUR[x]): d[t + k] = x
            t += DUR[x]
        return d
    T = sum(DUR.values())
    uniq = [d for d in range(3, T) if len({sched(o)[d] for o in sols}) == 1 and len({o for o in sols}) > 1]
    nontriv = [d for d in uniq if len({o.index(sched(sols[0])[d]) for o in sols}) > 1]
    if nontriv:
        best.append((DUR, [c[0] for c in cons], [''.join(o) for o in sols], nontriv, sched(sols[0])))
        if len(best) >= 5: break
for b in best: print(b)

# (e) 两排对坐长桌
P = ['甲', '乙', '丙', '丁', '戊', '己']
side = lambda x: 0 if x <= 3 else 1
col = lambda x: (x - 1) % 3
opp = lambda a, b: side(a) != side(b) and col(a) == col(b)
diag = lambda a, b: side(a) != side(b) and abs(col(a) - col(b)) == 1
pool = [
    ('甲的正对面是乙', lambda s: opp(s['甲'], s['乙'])),
    ('丙与甲在同一侧且相邻', lambda s: side(s['丙']) == side(s['甲']) and abs(col(s['丙']) - col(s['甲'])) == 1),
    ('丁坐在戊的斜对面', lambda s: diag(s['丁'], s['戊'])),
    ('己不坐在两端', lambda s: col(s['己']) == 1),
    ('甲坐在北侧', lambda s: side(s['甲']) == 0),
    ('丙坐在西端', lambda s: col(s['丙']) == 0),
    ('戊与乙在同一侧', lambda s: side(s['戊']) == side(s['乙'])),
    ('丁不坐在南侧', lambda s: side(s['丁']) == 0),
]
for combo in combinations(range(len(pool)), 5):
    S = line(P, 6, [pool[i][1] for i in combo])
    if len(S) == 1:
        print('(e)', [pool[i][0] for i in combo], fmt_line(S[0]))

# (f) 6人一排，4条陈述恰有1条不成立，另给确定信息
random.seed(41)
P = ['甲', '乙', '丙', '丁', '戊', '己']
def st_pool():
    out = []
    for a, b in permutations(P, 2):
        out.append((f'{a}与{b}相邻', lambda s, a=a, b=b: abs(s[a] - s[b]) == 1))
        out.append((f'{a}在{b}左边', lambda s, a=a, b=b: s[a] < s[b]))
        for k in (1, 2):
            out.append((f'{a}与{b}中间隔着{k}人', lambda s, a=a, b=b, k=k: abs(s[a] - s[b]) == k + 1))
    for a in P:
        out.append((f'{a}不在两端', lambda s, a=a: s[a] not in (1, 6)))
    return out
SP = st_pool()
found = 0
for trial in range(40000):
    sts = random.sample(SP, 4)
    fixed = random.choice(P); fpos = random.choice(range(1, 7))
    base = line(P, 6, [lambda s: s[fixed] == fpos])
    S = [s for s in base if sum(f(s) for _, f in sts) == 3]
    bad = {[i for i, (_, f) in enumerate(sts) if not f(s)][0] for s in S}
    if S and len(bad) == 1 and len(S) <= 3:
        print('(f)', fixed, fpos, [t for t, _ in sts], '不成立第', [b + 1 for b in bad], '解', [fmt_line(s) for s in S])
        found += 1
        if found >= 6: break
