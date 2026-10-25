# Re-search 2-10-1 data: answer r must differ from every number in the stem, distractors clean.
from fractions import Fraction as F
from math import lcm

def clean(x, den=4):
    return x > 0 and (x * den).denominator == 1

rows = []
for T1 in range(6, 41):
    for T2 in range(T1 + 1, 61):
        if (T1, T2) == (12, 20):
            continue
        W = lcm(T1, T2); e1 = F(W, T1); e2 = F(W, T2)
        T0 = W / (e1 + e2)
        if (T0 * 2).denominator != 1:
            continue
        for t1 in range(1, 8):
            if t1 >= T0:
                continue
            for q in [F(1, 4), F(2, 5), F(1, 3), F(3, 10), F(1, 2)]:
                e2n = e2 * (1 - q)
                for L4 in range(2, 13):
                    L = F(L4, 4)
                    T = T0 + L
                    r = (t1 * (e1 + e2) + (e1 + e2n) * (T - t1) - W) / e2n
                    if not clean(r, 2) or T - t1 - r <= 0:
                        continue
                    # 维修期间不能已完工
                    if t1 * (e1 + e2) + e1 * r >= W:
                        continue
                    E1 = (T - t1) - (W - t1 * (e1 + e2)) / (e1 + e2n)      # 漏算维修期间甲
                    E3 = ((e1 + e2) * T - W) / e2                          # 忽略降效
                    naive = L                                               # 晚几小时修几小时
                    vals = {r, E1, E3, naive}
                    if len(vals) < 4 or not all(clean(v, 2) for v in vals):
                        continue
                    stem_nums = {F(T1), F(T2), F(t1), L, q * 100}
                    if r in stem_nums:
                        continue
                    rows.append((T1, T2, str(T0), t1, str(q), str(L), str(r), str(E1), str(E3)))
for row in rows:
    print(row)
print(len(rows))
