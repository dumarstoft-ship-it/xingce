# Four quantities A>B>C>D>=1 (integers). Relations: X = m*Y ; P1+Q1 = S1 ; P2+Q2 = S2.
from fractions import Fraction as F
from math import lcm
import itertools
from collections import defaultdict
NM = 'ABCD'
def solve3(M, rhs):
    M = [list(map(F, r)) + [F(b)] for r, b in zip(M, rhs)]
    for c in range(3):
        p = next((r for r in range(c, 3) if M[r][c] != 0), None)
        if p is None: return None
        M[c], M[p] = M[p], M[c]
        for r in range(3):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [a - f*b for a, b in zip(M[r], M[c])]
    return [M[i][3] / M[i][i] for i in range(3)]
def param(mult, s1, s2):
    xi, yi, m = mult
    rows = []
    r = [0]*4; r[xi] = 1; r[yi] = -m; rows.append(r)
    r = [0]*4; r[s1[0]] += 1; r[s1[1]] += 1; rows.append(r)
    r = [0]*4; r[s2[0]] += 1; r[s2[1]] += 1; rows.append(r)
    for free in range(4):
        others = [k for k in range(4) if k != free]
        M = [[row[k] for k in others] for row in rows]
        basis = []
        bad = False
        for (e0, e1, e2, tt) in [(0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]:
            rhs = [e0 - rows[0][free]*tt, e1 - rows[1][free]*tt, e2 - rows[2][free]*tt]
            s = solve3(M, rhs)
            if s is None: bad = True; break
            vec = [None]*4; vec[free] = F(tt)
            for k, v in zip(others, s): vec[k] = v
            basis.append(vec)
        if not bad:
            return free, basis  # var_k = basis[0][k]*S1 + basis[1][k]*S2 + basis[2][k]*t
    return None
pairs = [(i, j) for i in range(4) for j in range(i+1, 4)]
results = defaultdict(list)
for xi, yi in pairs:
    for m in (2, 3):
        for s1, s2 in itertools.permutations(pairs, 2):
            if s1 > s2: continue
            pr = param((xi, yi, m), s1, s2)
            if pr is None: continue
            free, basis = pr
            den = 1
            for vec in basis:
                for v in vec: den = lcm(den, v.denominator)
            coef = [[int(vec[k]*den) for vec in basis] for k in range(4)]
            for S1 in range(20, 131):
                for S2 in range(10, 131):
                    fam = []
                    for t in range(1, 160):
                        vals = []
                        ok = True
                        for k in range(4):
                            num = coef[k][0]*S1 + coef[k][1]*S2 + coef[k][2]*t
                            if num % den: ok = False; break
                            v = num // den
                            if v < 1: ok = False; break
                            vals.append(v)
                        if ok: fam.append(tuple(vals))
                    full = [v for v in fam if v[0] > v[1] > v[2] > v[3]]
                    if len(full) != 1: continue
                    obvious = [v for v in fam if v[0] > v[1] > v[2]]
                    if not (3 <= len(obvious) <= 4): continue
                    noAB = [v for v in fam if v[1] > v[2] > v[3]]
                    noBC = [v for v in fam if v[0] > v[1] and v[2] > v[3]]
                    results[((xi, yi, m), s1, s2)].append((S1, S2, full[0], len(obvious), len(noAB), len(noBC)))
for k, v in results.items():
    (xi, yi, m), s1, s2 = k
    chain = bool(set(s1) & set(s2))
    desc = f"{NM[xi]}={m}{NM[yi]}, {NM[s1[0]]}+{NM[s1[1]]}=S1, {NM[s2[0]]}+{NM[s2[1]]}=S2, share={chain}"
    print(desc, 'count', len(v))
    for r in v[:8]: print('    ', r)
