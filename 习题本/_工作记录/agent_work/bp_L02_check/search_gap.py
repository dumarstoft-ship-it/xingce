import itertools
# ---------- (1) 一人两句、每人一真一假：3 projects A,B,C, 3 people x 2 literals ----------
objs = ['A', 'B', 'C']
lits = [(o, v) for o in objs for v in (True, False)]   # (obj, claimed value)
worlds = [dict(zip(objs, vals)) for vals in itertools.product([False, True], repeat=3)]
def person_ok(w, pair):
    return sum(w[o] == v for o, v in pair) == 1
pairs = [p for p in itertools.combinations(lits, 2) if p[0][0] != p[1][0]]
found = []
for trio in itertools.combinations(pairs, 3):
    sol = [w for w in worlds if all(person_ok(w, p) for p in trio)]
    if len(sol) == 1:
        # no single person determines it alone, and any two don't either
        alone = any(len([w for w in worlds if person_ok(w, p)]) == 1 for p in trio)
        two = any(len([w for w in worlds if person_ok(w, p) and person_ok(w, q)]) == 1 for p, q in itertools.combinations(trio, 2))
        found.append((two, trio, sol[0]))
print('half-true trios with unique world:', len(found), ' of which no two people suffice:', sum(1 for f in found if not f[0]))
def lit_txt(l): return f"{l[0]}{'获批' if l[1] else '没获批'}"
for two, trio, s in found[:6]:
    print('  needs-all-three' if not two else '  two-suffice', [' / '.join(lit_txt(l) for l in p) for p in trio], '->', s)

# ---------- (2) 诚实者H/说谎者L/随机者R 各一 ----------
P = ['甲', '乙', '丙']
ids = list(itertools.permutations('HLR'))
claims = []
for x in P:
    for t in 'HLR':
        claims.append((f'{x}是{ {"H":"诚实者","L":"说谎者","R":"随机者"}[t] }', lambda a, x=x, t=t: a[x] == t))
        claims.append((f'{x}不是{ {"H":"诚实者","L":"说谎者","R":"随机者"}[t] }', lambda a, x=x, t=t: a[x] != t))
res = []
for c in itertools.product(range(len(claims)), repeat=3):
    sols = []
    for perm in ids:
        a = dict(zip(P, perm))
        ok = True
        for spk, ci in zip(P, c):
            val = claims[ci][1](a)
            if a[spk] == 'H' and not val: ok = False
            if a[spk] == 'L' and val: ok = False
        if ok: sols.append(a)
    if len(sols) == 1:
        # avoid speakers talking only about themselves
        res.append(([claims[ci][0] for ci in c], sols[0]))
print('HLR designs with unique identity:', len(res))
nice = [r for r in res if not any(t.startswith(s) for s, t in zip(P, r[0]))]
print('  of which nobody talks about himself:', len(nice))
for r in nice[:8]:
    print('  ', dict(zip(P, r[0])), '->', r[1])

# ---------- (3) 真言卫/谎言卫 3人: 选言/联言陈述 ----------
types = list(itertools.product('HL', repeat=3))
stm = []
for x, y in itertools.permutations(P, 2):
    stm.append((f'{x}和{y}都是谎言卫', lambda a, x=x, y=y: a[x] == 'L' and a[y] == 'L'))
    stm.append((f'{x}和{y}中至少有一个谎言卫', lambda a, x=x, y=y: a[x] == 'L' or a[y] == 'L'))
    stm.append((f'{x}和{y}是同一类', lambda a, x=x, y=y: a[x] == a[y]))
    stm.append((f'{x}是真言卫', lambda a, x=x: a[x] == 'H'))
stm.append(('我们三人中恰有一个真言卫', lambda a: list(a.values()).count('H') == 1))
stm.append(('我们三人中至少有两个谎言卫', lambda a: list(a.values()).count('L') >= 2))
res3 = []
for c in itertools.product(range(len(stm)), repeat=3):
    sols = []
    for tp in types:
        a = dict(zip(P, tp))
        if all((stm[ci][1](a)) == (a[spk] == 'H') for spk, ci in zip(P, c)):
            sols.append(a)
    if len(sols) == 1:
        txt = [stm[ci][0] for ci in c]
        if len(set(txt)) == 3 and sum('或' in t or '至少' in t or '恰有' in t for t in txt) >= 1:
            res3.append((txt, sols[0]))
print('H/L 3-person designs with unique identity (uses 至少/恰有):', len(res3))
for r in res3[:8]:
    print('  ', dict(zip(P, r[0])), '->', r[1])
