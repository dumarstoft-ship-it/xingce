import itertools, random, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_check')
from tf import bools
random.seed(36)
# ---- D36-4: six members 甲..己, two liars, one statement of the form 'X说的是假话' ----
N = ['甲', '乙', '丙', '丁', '戊', '己']
W = list(bools(N))
lib = []
for x in N:
    lib.append((f'{x}完成了', lambda w, x=x: w[x]))
    lib.append((f'{x}没完成', lambda w, x=x: not w[x]))
for x, y in itertools.combinations(N[:4], 2):
    lib.append((f'{x}和{y}都完成了', lambda w, x=x, y=y: w[x] and w[y]))
    lib.append((f'{x}和{y}中只有一人完成', lambda w, x=x, y=y: w[x] != w[y]))
    lib.append((f'{x}和{y}至少一人没完成', lambda w, x=x, y=y: (not w[x]) or (not w[y])))
lib.append(('大家都没完成', lambda w: not any(w.values())))
best = None
tries = 0
while tries < 200000:
    tries += 1
    pick = random.sample(range(len(lib)), 5)
    target = random.randrange(5)          # speaker index whose statement the 'liar-claim' refers to
    claim_pos = random.randrange(6)
    if claim_pos == target: continue
    stm = []
    k = 0
    for pos in range(6):
        if pos == claim_pos:
            stm.append(None)
        else:
            stm.append(lib[pick[k]]); k += 1
    ref = stm[target] if target < claim_pos else stm[target]
    if ref is None: continue
    f_ref = ref[1]
    full = [s if s is not None else (f'{N[target]}说的是假话', lambda w, f=f_ref: not f(w)) for s in stm]
    if any(s[0].startswith(N[i]) and '说的是假话' not in s[0] and False for i, s in enumerate(full)): pass
    valid = [w for w in W if sum(1 for s in full if not s[1](w)) == 2]
    if not valid: continue
    liars = {tuple(i for i, s in enumerate(full) if not s[1](w)) for w in valid}
    cnt = {w['甲'] + w['乙'] + w['丙'] for w in valid}
    if len(liars) == 1 and len(cnt) == 1:
        texts = [s[0] for s in full]
        if sum('都' in t or '只有' in t or '至少' in t for t in texts) >= 2:
            best = (texts, liars, cnt)
            break
print('D36-4 design:', best, 'after', tries, 'tries')

# ---- D36-11: choose 2 of 4, only two true, no contradictory pair ----
P = ['甲', '乙', '丙', '丁']
dom = [frozenset(c) for c in itertools.combinations(P, 2)]
cands = []
for x in P:
    cands.append((f'{x}入选', lambda s, x=x: x in s)); cands.append((f'{x}没有入选', lambda s, x=x: x not in s))
for x, y in itertools.combinations(P, 2):
    cands.append((f'{x}和{y}至少有1人入选', lambda s, x=x, y=y: x in s or y in s))
    cands.append((f'{x}和{y}都没有入选', lambda s, x=x, y=y: x not in s and y not in s))
for x, y in itertools.permutations(P, 2):
    cands.append((f'如果{x}入选，那么{y}也入选', lambda s, x=x, y=y: (x not in s) or (y in s)))
def contra(f, g): return all(f(s) != g(s) for s in dom)
out = []
for combo in itertools.combinations(range(len(cands)), 4):
    fs = [cands[i] for i in combo]
    if any(contra(fs[i][1], fs[j][1]) for i in range(4) for j in range(i + 1, 4)): continue
    sol = [s for s in dom if sum(f(s) for _, f in fs) == 2]
    if len(sol) == 1:
        t = [x for x, _ in fs]
        if any('如果' in x for x in t) and any('至少' in x for x in t) and any('都没有' in x for x in t):
            out.append((t, ''.join(sorted(sol[0], key=P.index))))
print('D36-11 designs:', len(out)); [print('  ', o) for o in out[:5]]

# ---- D36-19: one speaker both true, one both false, one half (single choice among 5) ----
C = ['甲', '乙', '丙', '丁', '戊']
lit = [(f'是{x}', lambda w, x=x: w == x) for x in C] + [(f'不是{x}', lambda w, x=x: w != x) for x in C]
found = []
for trio in itertools.combinations(itertools.combinations(range(len(lit)), 2), 3):
    sols = set()
    for w in C:
        cnts = sorted(lit[a][1](w) + lit[b][1](w) for a, b in trio)
        if cnts == [0, 1, 2]:
            roles = tuple(lit[a][1](w) + lit[b][1](w) for a, b in trio)
            sols.add((w, roles))
    if len(sols) == 1:
        found.append(([lit[a][0] + '；' + lit[b][0] for a, b in trio], sols))
print('D36-19 designs (unique world & roles):', len(found))
for f in found[:6]: print('  ', f)

# ---- D36-20: H/L/R one each, nobody talks about himself, ask who is R; avoid D27-19 pattern ----
P3 = ['甲', '乙', '丙']
ids = list(itertools.permutations('HLR'))
nm = {'H': '诚实者', 'L': '说谎者', 'R': '随机者'}
claims = []
for x in P3:
    for t in 'HLR':
        claims.append((x, f'{x}是{nm[t]}', lambda a, x=x, t=t: a[x] == t))
        claims.append((x, f'{x}不是{nm[t]}', lambda a, x=x, t=t: a[x] != t))
claims.append((None, '我们三人中丙不是诚实者', lambda a: a['丙'] != 'H'))
res = []
for c in itertools.product(range(len(claims)), repeat=3):
    if any(claims[ci][0] == spk for spk, ci in zip(P3, c)): continue
    sols = []
    for perm in ids:
        a = dict(zip(P3, perm))
        if all(not ((a[spk] == 'H' and not claims[ci][2](a)) or (a[spk] == 'L' and claims[ci][2](a))) for spk, ci in zip(P3, c)):
            sols.append(a)
    if len(sols) == 1 and sols[0]['丙'] != 'H' and sols[0]['甲'] == 'H':
        res.append(([claims[ci][1] for ci in c], sols[0]))
print('D36-20 designs with 甲=H:', len(res)); [print('  ', r) for r in res[:6]]
