import itertools
C = ['甲', '乙', '丙', '丁', '戊']
lit = [(f'是{x}', lambda w, x=x: w == x) for x in C] + [(f'不是{x}', lambda w, x=x: w != x) for x in C]
def consistent(a, b): return any(lit[a][1](w) and lit[b][1](w) for w in C) and any(not lit[a][1](w) or not lit[b][1](w) for w in C)
def nontrivial(a, b):
    va = [lit[a][1](w) for w in C]; vb = [lit[b][1](w) for w in C]
    return va != vb and any(x != y for x, y in zip(va, vb))
pairs = [p for p in itertools.combinations(range(len(lit)), 2) if consistent(*p) and nontrivial(*p)]
found = []
for trio in itertools.combinations(pairs, 3):
    sols = set()
    for w in C:
        roles = tuple(lit[a][1](w) + lit[b][1](w) for a, b in trio)
        if sorted(roles) == [0, 1, 2]:
            sols.add((w, roles))
    if len(sols) == 1:
        txt = [lit[a][0] + '；' + lit[b][0] for a, b in trio]
        if sum(t.count('不是') for t in txt) in (2, 3):
            found.append((txt, sols))
print('consistent-pair designs:', len(found))
for f in found[:10]: print('  ', f)
