import itertools, random
V = ['A', 'B', 'C']
W = [dict(zip(V, v)) for v in itertools.product([False, True], repeat=3)]
lib = []
for x in V:
    lib.append((f'{x}获资助', lambda w, x=x: w[x]))
    lib.append((f'{x}没获资助', lambda w, x=x: not w[x]))
for x, y in itertools.permutations(V, 2):
    lib.append((f'如果{x}获资助，那么{y}也获资助', lambda w, x=x, y=y: (not w[x]) or w[y]))
for x, y in itertools.combinations(V, 2):
    lib.append((f'{x}和{y}都获资助', lambda w, x=x, y=y: w[x] and w[y]))
    lib.append((f'{x}或{y}获资助', lambda w, x=x, y=y: w[x] or w[y]))
    lib.append((f'{x}和{y}都没获资助', lambda w, x=x, y=y: (not w[x]) and (not w[y])))
def rel(f, g):
    a = [f(w) for w in W]; b = [g(w) for w in W]
    if all(p != q for p, q in zip(a, b)): return 'contra'
    if not any(p and q for p, q in zip(a, b)): return 'contrary'
    if all(p or q for p, q in zip(a, b)): return 'sub'
    return None
def search(k_true, need_cond=True):
    out = []
    for combo in itertools.combinations(range(len(lib)), 4):
        fs = [lib[i] for i in combo]
        if any(rel(fs[i][1], fs[j][1]) for i in range(4) for j in range(i + 1, 4)):
            continue
        if need_cond and not any('如果' in t for t, _ in fs):
            continue
        sol = [w for w in W if sum(f(w) for _, f in fs) == k_true]
        if len(sol) == 1:
            s = sol[0]
            # the solution should not be trivially named by one statement
            out.append(([t for t, _ in fs], ''.join(k for k in V if s[k]) or '无'))
    return out
for k in (1, 2):
    res = search(k)
    print('exactly', k, 'true -> designs', len(res))
    random.seed(k)
    for r in random.sample(res, min(12, len(res))):
        print('   ', r)
