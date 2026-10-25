import itertools, random
random.seed(2026)
def bools(names):
    return [dict(zip(names, v)) for v in itertools.product([False, True], repeat=len(names))]
def lib_people(N, sub=None):
    L = []
    for x in N:
        L.append((f'{x}完成了', lambda w, x=x: w[x]))
        L.append((f'{x}没完成', lambda w, x=x: not w[x]))
    for x, y in itertools.combinations(sub or N, 2):
        L.append((f'{x}和{y}都完成了', lambda w, x=x, y=y: w[x] and w[y]))
        L.append((f'{x}和{y}至少一人没完成', lambda w, x=x, y=y: (not w[x]) or (not w[y])))
        L.append((f'{x}或{y}完成了', lambda w, x=x, y=y: w[x] or w[y]))
        L.append((f'{x}和{y}都没完成', lambda w, x=x, y=y: (not w[x]) and (not w[y])))
    for x, y in itertools.permutations(sub or N, 2):
        L.append((f'如果{x}完成，那么{y}也完成', lambda w, x=x, y=y: (not w[x]) or w[y]))
    return L
def contra(f, g, W):
    return all(f(w) != g(w) for w in W)

# (a) 5 people, exactly one liar; one statement is "X说的是假话" about another speaker
N5 = ['甲', '乙', '丙', '丁', '戊']
W5 = bools(N5)
L5 = lib_people(N5, ['甲', '乙', '丙', '丁'])
found = []
for _ in range(300000):
    pick = random.sample(L5, 4)
    tgt = random.randrange(4)
    st = pick[:]
    f_ref = st[tgt][1]
    st.append((f'{N5[tgt]}说的是假话', lambda w, f=f_ref: not f(w)))
    valid = [w for w in W5 if sum(1 for _, f in st if not f(w)) == 1]
    if not valid: continue
    liars = {tuple(i for i, (_, f) in enumerate(st) if not f(w)) for w in valid}
    cnt = {sum(w.values()) for w in valid}
    if len(liars) == 1 and len(cnt) == 1 and 2 <= len(valid) <= 4:
        found.append(([t for t, _ in st], liars, cnt, len(valid)))
        if len(found) >= 8: break
print('(a) one liar designs:')
for f in found: print('   ', f)

# (b) 7 statements over A,B,C,D: two contradiction pairs + 3 others; exactly 3 true -> forced facts
V4 = ['甲', '乙', '丙', '丁']
W4 = bools(V4)
L4 = lib_people(V4)
found = []
pairs = [(i, j) for i in range(len(L4)) for j in range(i + 1, len(L4)) if contra(L4[i][1], L4[j][1], W4)]
for _ in range(200000):
    p1, p2 = random.sample(pairs, 2)
    others = random.sample(range(len(L4)), 3)
    idx = list(p1) + list(p2) + others
    if len(set(idx)) < 7: continue
    st = [L4[i] for i in idx]
    # no further contradictions among the others
    if any(contra(st[i][1], st[j][1], W4) for i in range(4, 7) for j in range(i + 1, 7)): continue
    valid = [w for w in W4 if sum(f(w) for _, f in st) == 3]
    if not valid: continue
    sols = {tuple(sorted(k for k in V4 if w[k])) for w in valid}
    if len(sols) == 1:
        found.append(([t for t, _ in st], sols))
        if len(found) >= 6: break
print('(b) 7-statement exactly-3-true designs:')
for f in found: print('   ', f)

# (c) 5 statements over 4 people: one contradiction pair; "说真话的比说假话的多" (>=3 true) -> unique world
found = []
for _ in range(300000):
    i, j = random.choice(pairs)
    others = random.sample(range(len(L4)), 3)
    idx = [i, j] + others
    if len(set(idx)) < 5: continue
    st = [L4[k] for k in idx]
    if any(contra(st[a][1], st[b][1], W4) for a in range(2, 5) for b in range(a + 1, 5)): continue
    valid = [w for w in W4 if sum(f(w) for _, f in st) >= 3]
    sols = {tuple(sorted(k for k in V4 if w[k])) for w in valid}
    if len(sols) == 1:
        found.append(([t for t, _ in st], sols))
        if len(found) >= 6: break
print('(c) >=3 true of 5 designs:')
for f in found: print('   ', f)

# (d) contrary + subcontrary pairs, exactly 2 true of 5, over A,B,C
V3 = ['甲', '乙', '丙']
W3 = bools(V3)
d_found = []
S = [('甲、乙都达标', lambda w: w['甲'] and w['乙']), ('甲、乙都没达标', lambda w: not w['甲'] and not w['乙']),
     ('乙或丙达标', lambda w: w['乙'] or w['丙']), ('乙、丙至少一个没达标', lambda w: not w['乙'] or not w['丙'])]
extra = [(t, f) for t, f in lib_people(V3) if '完成' in t]
for t, f in extra:
    st = S + [(t, f)]
    for k in (1, 2, 3):
        valid = [w for w in W3 if sum(g(w) for _, g in st) == k]
        sols = {tuple(sorted(x for x in V3 if w[x])) for w in valid}
        if len(sols) == 1:
            d_found.append((k, t, sols))
print('(d) contrary+subcontrary designs:')
for f in d_found: print('   ', f)

# (e) choose 2 of 4, exactly one false of 4 statements, no contradictory pair, unique set
P = ['甲', '乙', '丙', '丁']
dom = [frozenset(c) for c in itertools.combinations(P, 2)]
C = []
for x in P:
    C.append((f'{x}入选', lambda s, x=x: x in s)); C.append((f'{x}没有入选', lambda s, x=x: x not in s))
for x, y in itertools.combinations(P, 2):
    C.append((f'{x}、{y}至少一人入选', lambda s, x=x, y=y: x in s or y in s))
    C.append((f'{x}、{y}都没有入选', lambda s, x=x, y=y: x not in s and y not in s))
for x, y in itertools.permutations(P, 2):
    C.append((f'如果{x}入选，那么{y}也入选', lambda s, x=x, y=y: (x not in s) or (y in s)))
def rel(f, g):
    a = [f(s) for s in dom]; b = [g(s) for s in dom]
    return all(p != q for p, q in zip(a, b)) or not any(p and q for p, q in zip(a, b)) or all(p or q for p, q in zip(a, b))
e_found = []
for combo in itertools.combinations(range(len(C)), 4):
    fs = [C[i] for i in combo]
    if any(rel(fs[i][1], fs[j][1]) for i in range(4) for j in range(i + 1, 4)): continue
    if not any('如果' in t for t, _ in fs): continue
    sol = [s for s in dom if sum(f(s) for _, f in fs) == 3]
    if len(sol) == 1:
        e_found.append(([t for t, _ in fs], ''.join(sorted(sol[0], key=P.index))))
print('(e) 4选2 only-one-false designs:', len(e_found))
for f in random.sample(e_found, min(10, len(e_found))): print('   ', f)
