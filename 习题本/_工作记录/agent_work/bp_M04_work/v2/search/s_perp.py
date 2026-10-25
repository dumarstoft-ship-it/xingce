import math
from fractions import Fraction as F
res = []
for A in range(8, 41):          # 甲地在丙正西 A
    for B in range(6, 41):      # 乙地在丙正北 B
        for (rn, rd) in [(3,5),(4,5),(3,4),(2,3),(1,2),(5,4),(4,3)]:
            for k in [2, 3]:
                # 所有整数速度组合中，满足 1h 后距离 d1、(1+k)h 后距离 d2 且两人都已过丙的
                sols = {}
                for p in range(1, 31):
                    if (p * rn) % rd: continue
                    q = p * rn // rd
                    d1 = math.hypot(A - p, B - q)
                    T = 1 + k
                    if p * T < A or q * T < B: continue
                    d2 = math.hypot(A - p * T, B - q * T)
                    if abs(d1 - round(d1)) < 1e-9 and abs(d2 - round(d2)) < 1e-9:
                        sols.setdefault((round(d1), round(d2)), []).append((p, q))
                for (d1, d2), lst in sols.items():
                    if len(lst) == 1:
                        p, q = lst[0]
                        # 唯一性：只给 d1、d2、比例时，所有正实数速度中也唯一？粗查整数即可
                        diff = (F(A, p) - F(B, q)) * 60
                        if diff.denominator == 1 and d1 > 0 and d2 > 0:
                            res.append((A, B, '%d/%d' % (rn, rd), k, d1, d2, p, q, diff))
print(len(res))
for r in res[:60]: print(r)
