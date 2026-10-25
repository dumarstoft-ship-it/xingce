import itertools
P = ['甲', '乙', '丙', '丁']
worlds = [frozenset(c) for c in itertools.combinations(P, 2)]   # choose 2 of 4
allw16 = [frozenset(c) for k in range(5) for c in itertools.combinations(P, k)]
cands = []
for x in P:
    cands.append((f'{x}入选', lambda w, x=x: x in w))
    cands.append((f'{x}没有入选', lambda w, x=x: x not in w))
for x, y in itertools.combinations(P, 2):
    cands.append((f'{x}和{y}至少有1人入选', lambda w, x=x, y=y: x in w or y in w))
    cands.append((f'{x}和{y}都入选', lambda w, x=x, y=y: x in w and y in w))
    cands.append((f'{x}和{y}都没有入选', lambda w, x=x, y=y: x not in w and y not in w))
for x, y in itertools.permutations(P, 2):
    cands.append((f'如果{x}入选，那么{y}也入选', lambda w, x=x, y=y: (x not in w) or (y in w)))

def related(f, g, dom):
    # contradictory / contrary / subcontrary / implication within the domain
    a = [f(w) for w in dom]; b = [g(w) for w in dom]
    if all(p != q for p, q in zip(a, b)): return 'contra'
    if not any(p and q for p, q in zip(a, b)): return 'contrary'
    if all(p or q for p, q in zip(a, b)): return 'subcontrary'
    if all((not p) or q for p, q in zip(a, b)) or all((not q) or p for p, q in zip(a, b)): return 'implies'
    return None

good = []
for combo in itertools.combinations(range(len(cands)), 4):
    fs = [cands[i] for i in combo]
    # require: no relation between any two statements within the 2-of-4 domain
    if any(related(fs[i][1], fs[j][1], worlds) in ("contra","contrary","subcontrary") for i in range(4) for j in range(i + 1, 4)):
        continue
    # require each named person appears, statements are diverse in type
    for k, label in ((1, 'only1true'), (3, 'only1false')):
        sol = [w for w in worlds if sum(f(w) for _, f in fs) == k]
        if len(sol) == 1:
            good.append((label, [t for t, _ in fs], ''.join(sorted(sol[0], key=P.index))))
print(len(good))
import random
random.seed(7)
# prefer combos that use one conditional, one 'at least', one literal, one 'both not'
def score(texts):
    s = 0
    s += any('如果' in t for t in texts) * 2
    s += any('至少' in t for t in texts)
    s += any('都没有' in t for t in texts)
    s += any(t.endswith('入选') and len(t) <= 4 for t in texts)
    return s
good.sort(key=lambda g: -score(g[1]))
for g in good[:25]:
    print(g)
