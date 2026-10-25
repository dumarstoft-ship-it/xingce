import itertools
C = ['甲', '乙', '丙', '丁', '戊']
st = []
for x in C:
    st.append((f'是{x}', lambda w, x=x: w == x))
    st.append((f'不是{x}', lambda w, x=x: w != x))
for x, y in itertools.combinations(C, 2):
    st.append((f'是{x}或{y}', lambda w, x=x, y=y: w in (x, y)))
pairs = [p for p in itertools.combinations(range(len(st)), 2)]
out = []
import random
random.seed(1)
for trio in itertools.combinations(pairs, 3):
    def ok(w, p): return (st[p[0]][1](w) + st[p[1]][1](w)) == 1
    sol = [w for w in C if all(ok(w, p) for p in trio)]
    if len(sol) != 1: continue
    if any(len([w for w in C if ok(w, p) and ok(w, q)]) == 1 for p, q in itertools.combinations(trio, 2)):
        continue
    # avoid degenerate pairs (one statement implies the other or they are complementary)
    bad = False
    for p in trio:
        a = [st[p[0]][1](w) for w in C]; b = [st[p[1]][1](w) for w in C]
        if all(x != y for x, y in zip(a, b)) or all(x == y for x, y in zip(a, b)): bad = True
    if bad: continue
    out.append(([st[p[0]][0] + '；' + st[p[1]][0] for p in trio], sol[0]))
print('needs-all-three designs:', len(out))
lit_only = [o for o in out if not any('或' in s for s in o[0])]
print('  literal-only:', len(lit_only))
for o in (lit_only[:6] + out[:6]):
    print('  ', o)

print('---- designs with 或, each speaker uses distinct names, answer not mentioned positively ----')
cnt = 0
for o in out:
    txt = o[0]
    if sum('或' in s for s in txt) < 2: continue
    if any(s.count('是甲') + s.count('甲或') > 1 for s in txt): continue
    firsts = [s.split('；')[0] for s in txt]
    if len(set(firsts)) < 3: continue
    if any(('是' + o[1]) in s and ('不是' + o[1]) not in s for s in txt): continue
    print('  ', o)
    cnt += 1
    if cnt >= 12: break
