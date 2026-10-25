# real 2026GD-41: an irregular quadrilateral plot is cut by its diagonals into four regions. In the
# figure, going around the intersection point: qingcai (top), maodou (right), qiezi (bottom),
# fanqie (left)  ->  qingcai is opposite qiezi, maodou is opposite fanqie.
# Given: qingcai = 1.4 * maodou; fanqie = qiezi + 40; fanqie = qingcai - 140.
# Asked: maodou - qiezi.
# Geometry: with OA=p, OB=q, OC=r, OD=s, areas are (1/2)sin(t) * (pq, qr, rs, sp) around O.
import sympy as sp

q, r, s = sp.symbols('q r s', positive=True)
p, k = sp.Integer(1), sp.Integer(1)          # fix the scale: OA = 1, (1/2) sin(t) = 1
qingcai, maodou, qiezi, fanqie = k * p * q, k * q * r, k * r * s, k * s * p
eqs = [sp.Eq(qingcai, sp.Rational(14, 10) * maodou),
       sp.Eq(fanqie, qiezi + 40),
       sp.Eq(fanqie, qingcai - 140)]
sols = [d for d in sp.solve(eqs, [q, r, s], dict=True) if all(v.is_positive for v in d.values())]
assert len(sols) == 1, sols
d = sols[0]
vals = {n: sp.nsimplify(v.subs(d)) for n, v in
        (('qingcai', qingcai), ('maodou', maodou), ('qiezi', qiezi), ('fanqie', fanqie))}
diff = vals['maodou'] - vals['qiezi']

# reading the figure wrongly gives nothing usable: pairing qingcai with fanqie has no positive
# solution; pairing qingcai with maodou gives irrational areas with maodou SMALLER than qiezi.
Q, M, Z, T = sp.symbols('Q M Z T', positive=True)
base = [sp.Eq(Q, sp.Rational(14, 10) * M), sp.Eq(T, Z + 40), sp.Eq(T, Q - 140)]
assert sp.solve(base + [sp.Eq(Q * T, M * Z)], [Q, M, Z, T], dict=True) == []
wrong = sp.solve(base + [sp.Eq(Q * M, Z * T)], [Q, M, Z, T], dict=True)
assert all(not (w[M] - w[Z]).is_rational and (w[M] - w[Z]) < 0 for w in wrong), wrong

opts = {'A': 60, 'B': 70, 'C': 90, 'D': 100}
hit = [kk for kk, v in opts.items() if v == diff]
assert len(hit) == 1, (vals, hit)
print(vals, 'maodou - qiezi =', diff)
print(hit[0])
