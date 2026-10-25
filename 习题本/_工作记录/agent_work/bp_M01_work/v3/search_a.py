from fractions import Fraction as F
import itertools, math
print("== 15-1-1 reserve HR: RHR 60, intensity 60-80%, HR range 130-150")
def zone(a, rhr=60, lo=F(6,10), hi=F(8,10)):
    m = 220 - a
    return rhr + (m - rhr) * lo, rhr + (m - rhr) * hi
ok = [a for a in range(18, 90) if zone(a)[0] <= 130 and zone(a)[1] >= 150]
print(ok)
for a in (30, 42, 45, 48):
    print(a, zone(a), 'simple', ((220-a)*F(6,10), (220-a)*F(8,10)))

print("== 15-5-2 depots ratio a:b:c:d, A->C x, D->B y ; then A=B and C = r*D")
sols = []
for ra in itertools.permutations(range(2, 9), 4):
    if not (ra[0] > ra[1] > ra[2] > ra[3]): continue
    if ra == (5, 4, 3, 2): continue
    for y in (4, 5, 6, 8, 10, 12):
        for r in (F(3,2), 2, F(5,2), 3):
            for k in range(2, 40):
                A, B, C, D = [v * k for v in ra]
                x = A - B - y          # A - x = B + y
                if x <= 0: continue
                if C + x == r * (D - y) and D - y > 0:
                    sols.append((ra, y, r, k, x, A))
for s in sols[:40]: print(s)
