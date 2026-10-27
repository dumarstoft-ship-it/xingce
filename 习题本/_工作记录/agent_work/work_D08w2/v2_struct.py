# For each structure, express A..D as alpha + beta*t (alpha linear in S1,S2) and classify the
# direction of the bound each order relation gives on t.
from fractions import Fraction as F
import itertools
NM = 'ABCD'
exec(open('v2_search.py').read().split('pairs = [(i, j)')[0])  # reuse solve3/param
pairs = [(i, j) for i in range(4) for j in range(i+1, 4)]
seen = set()
for xi, yi in pairs:
    for m in (2, 3):
        for s1, s2 in itertools.combinations(pairs, 2):
            pr = param((xi, yi, m), s1, s2)
            if pr is None: continue
            free, basis = pr
            # var_k = basis[0][k]*S1 + basis[1][k]*S2 + basis[2][k]*t
            beta = [basis[2][k] for k in range(4)]
            # relation P>Q : (beta_P - beta_Q) t > -(alpha_P - alpha_Q)
            def direc(p, q):
                d = beta[p] - beta[q]
                return 'none' if d == 0 else ('lower' if d > 0 else 'upper')
            dAB, dBC, dCD = direc(0, 1), direc(1, 2), direc(2, 3)
            share = bool(set(s1) & set(s2))
            ok = {dAB, dBC} == {'lower', 'upper'} and dCD in ('lower', 'upper')
            tag = 'GOOD' if ok and not share else ''
            print(f"{NM[xi]}={m}{NM[yi]}, {NM[s1[0]]}+{NM[s1[1]]}, {NM[s2[0]]}+{NM[s2[1]]} free={NM[free]} share={share} AB:{dAB} BC:{dBC} CD:{dCD} {tag}")
