from fractions import Fraction as F
from math import gcd

def reverse(N, p, q, t):
    A3, C3 = q * t, p * t
    B3 = N - A3 - C3
    if B3 <= 0: return None
    A2, B2 = F(A3, 2), F(B3, 2); C2 = N - A2 - B2
    A1, C1 = A2 / 2, C2 / 2; B1 = N - A1 - C1
    B0, C0 = B1 / 2, C1 / 2; A0 = N - B0 - C0
    states = [(A0, B0, C0), (A1, B1, C1), (A2, B2, C2), (A3, B3, C3)]
    for s in states:
        for v in s:
            if v.denominator != 1 or v <= 0: return None
    # givers must give positive amounts: day1 A gives B0+C0 ; day2 B gives A1+C1; day3 C gives A2+B2
    if A0 - A1 <= 0 or B1 - B2 <= 0 or C2 - C3 <= 0: return None
    return [tuple(int(v) for v in s) for s in states]

res = []
for N in range(120, 361, 6):
    for q in range(2, 40):
        for p in range(1, q):
            if gcd(p, q) != 1: continue
            sols = []
            for t in range(1, N):
                r = reverse(N, p, q, t)
                if r: sols.append((t, r))
            if len(sols) == 1:
                t, r = sols[0]
                # want integer constraint to matter: count t values that pass positivity only
                pos = [tt for tt in range(1, N) if N - (p+q)*tt > 0]
                res.append((N, p, q, t, r, len(pos)))
# prefer cases where positivity alone allows several t (so integrality is what pins it), moderate numbers
res = [x for x in res if x[5] >= 4]
res.sort(key=lambda x: (-x[5], x[0]))
for x in res[:25]:
    print(x)
print(len(res))
