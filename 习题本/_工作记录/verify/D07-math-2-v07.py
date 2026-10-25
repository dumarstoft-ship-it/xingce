# D07-math-2-v07: trapezoid ABCD, AD // BC, diagonals meet at O.
# Given area(AOD) = 45 and area(BOC) = 125, find the area of the trapezoid.
# Real coordinates: fix AD, find BC by bisection so that area(BOC)/area(AOD) matches, then scale the
# height so that area(AOD) = 45. Repeat for several shapes to show the answer does not depend on them.


def inter(p1, p2, p3, p4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def area(*p):
    s = 0
    for i in range(len(p)):
        s += p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1]
    return abs(s) / 2


def pieces(ad, bc, h, off):
    A, D = (off, h), (off + ad, h)
    B, C = (0.0, 0.0), (bc, 0.0)
    O = inter(A, C, B, D)
    return area(A, O, D), area(B, O, C), area(A, B, C, D)


S_AOD, S_BOC = 45.0, 125.0
results = []
for ad, off in ((1.0, 0.3), (1.0, -0.7), (2.5, 1.1)):
    lo, hi = 1e-6, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        a1, a2, _t = pieces(ad, mid, 1.0, off)
        if a2 / a1 < S_BOC / S_AOD:
            lo = mid
        else:
            hi = mid
    bc = (lo + hi) / 2
    a1, a2, tot = pieces(ad, bc, 1.0, off)
    k = S_AOD / a1                         # every area scales linearly with the height
    assert abs(a2 * k - S_BOC) < 1e-6
    results.append(tot * k)
assert max(results) - min(results) < 1e-6
total = results[0]
opts = {'A': 245, 'B': 320, 'C': 340, 'D': 420}
hit = [kk for kk, v in opts.items() if abs(v - total) < 1e-6]
assert len(hit) == 1, (total, hit)
print('trapezoid area', round(total, 9))
print(hit[0])
