import itertools
C = ['甲', '乙', '丙', '丁']
lits = [(x, True) for x in C] + [(x, False) for x in C]   # (x, True)= '选的是x', (x,False)='选的不是x'
def ev(w, l): return (w == l[0]) == l[1]
pairs = [p for p in itertools.combinations(lits, 2) if p[0][0] != p[1][0]]
out = []
for trio in itertools.combinations(pairs, 3):
    ok = lambda w, p: sum(ev(w, l) for l in p) == 1
    sol = [w for w in C if all(ok(w, p) for p in trio)]
    if len(sol) != 1: continue
    two = any(len([w for w in C if ok(w, p) and ok(w, q)]) == 1 for p, q in itertools.combinations(trio, 2))
    one = any(len([w for w in C if ok(w, p)]) == 1 for p in trio)
    out.append((one, two, trio, sol[0]))
print('total unique:', len(out), '| no single person suffices:', sum(1 for o in out if not o[0]), '| needs all three:', sum(1 for o in out if not o[1]))
t = lambda l: ('是' if l[1] else '不是') + l[0]
for one, two, trio, s in [o for o in out if not o[1]][:10]:
    print('  ', ['；'.join(t(l) for l in p) for p in trio], '->', s)
