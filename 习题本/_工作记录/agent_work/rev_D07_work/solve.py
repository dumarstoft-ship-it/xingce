# Independent solver for D07 math (M08 geometry) adapted questions.
# Each solver starts from stem data only; then we match against option values.
import json, math, itertools
from fractions import Fraction as F

Q = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/review/D07_math_questions.json'))
Q = {q['vid']: q for q in Q}
pi = math.pi

def optval(s):
    """Parse option text into a float."""
    s = s.strip().replace('$', '')
    rep = {r'26+0.6\pi': 26 + 0.6 * pi, r'26+1.2\pi': 26 + 1.2 * pi,
           r'2\sqrt{6}': 2 * math.sqrt(6), r'4\sqrt{3}': 4 * math.sqrt(3),
           r'8\sqrt{2}': 8 * math.sqrt(2), r'8\sqrt{3}': 8 * math.sqrt(3),
           r'\frac{8}{3}': 8 / 3, r'\frac{20}{3}': 20 / 3}
    if s in rep:
        return rep[s]
    if s.endswith('%'):
        return float(s[:-1]) / 100
    return float(s)

res = {}

# 1-v01: rectangle L,W; (L-2)(W-2) = LW - 44 -> perimeter. Brute force over many (L,W) real pairs.
def s1v01():
    perims = set()
    for L10 in range(21, 400):
        L = L10 / 10
        # (L-2)(W-2) = LW-44 -> -2L -2W + 4 = -44 -> W = 24 - L
        W = 24 - L
        if W > 2 and L > 2:
            assert abs((L - 2) * (W - 2) - (L * W - 44)) < 1e-9
            perims.add(round(2 * (L + W), 9))
    assert len(perims) == 1
    return perims.pop()
res['D07-math-1-v01'] = s1v01()

# 1-v02: track 8 lanes, width 1.25, lane-1 inner radius 36, straight 85; inner edge of each lane.
def s1v02():
    def lap(lane):
        r = 36 + (lane - 1) * 1.25
        return 2 * 85 + 2 * 3.14 * r
    return lap(8) - lap(1)
res['D07-math-1-v02'] = s1v02()

# 1-v03: circle radius 0.3 rolling outside 8x5 rectangle: simulate the offset curve numerically.
def s1v03():
    r = 0.3
    # straight parts: center translates along each side by side length
    L = 2 * (8 + 5)
    # corners: center rotates about the corner by 90 degrees each (exterior angle) -> arc r*pi/2
    L += 4 * r * pi / 2
    # numeric check: sample Minkowski boundary
    import numpy as np
    pts = []
    corners = [(0, 0), (8, 0), (8, 5), (0, 5)]
    # boundary of rectangle offset by r: parametrise by angle around rectangle
    N = 200000
    tot = 0
    prev = None
    for k in range(N + 1):
        th = 2 * pi * k / N
        d = (math.cos(th), math.sin(th))
        # support point of offset rectangle in direction d (convex => boundary param by normal)
        cx = 8 if d[0] > 0 else 0
        cy = 5 if d[1] > 0 else 0
        p = (cx + r * d[0], cy + r * d[1])
        if prev is not None:
            tot += math.dist(p, prev)
        prev = p
    # the support param skips straight segments (jumps) -> distance between jumps equals the side: included by dist
    assert abs(tot - L) < 1e-3, (tot, L)
    return L
res['D07-math-1-v03'] = s1v03()

# 1-v04: cylinder r=6 water depth 9 -> cone with top diameter 18 filled exactly -> height
def s1v04():
    V = pi * 6 ** 2 * 9
    R = 18 / 2
    return V / (pi * R ** 2 / 3)
res['D07-math-1-v04'] = s1v04()

# 1-v05: cube edge a, cut slab 0.5 thick; remaining surface smaller by 24 -> a. Search.
def s1v05():
    sols = []
    for a100 in range(51, 10000):
        a = a100 / 100
        orig = 6 * a * a
        rem = 2 * a * a + 4 * a * (a - 0.5)
        if abs(orig - rem - 24) < 1e-9:
            sols.append(a)
    assert len(sols) == 1, sols
    return sols[0]
res['D07-math-1-v05'] = s1v05()

# 1-v06: cone r6 h8 melted, 10% loss, spheres r2 -> max count
def s1v06():
    V = pi * 36 * 8 / 3 * 0.9
    v = 4 / 3 * pi * 8
    return math.floor(V / v + 1e-12)
res['D07-math-1-v06'] = s1v06()

# 1-v07: tank 40x30, water 8; cube 20 placed on bottom -> rise
def s1v07():
    Vw = 40 * 30 * 8
    # find final level h by bisection: water volume = (base - cube footprint)*h if h<=20 else base*h - 8000
    def vol(h):
        return (1200 - 400) * h if h <= 20 else 1200 * h - 8000
    lo, hi = 0, 100
    for _ in range(200):
        mid = (lo + hi) / 2
        if vol(mid) < Vw:
            lo = mid
        else:
            hi = mid
    return lo - 8
res['D07-math-1-v07'] = s1v07()

# 1-v08: semicircle radius 5; box from x=0 (centerline) to x=w, top at 4 -> max w
def s1v08():
    best = 0
    for w1000 in range(0, 5001):
        w = w1000 / 1000
        # all points of box (x in [0,w], y in [0,4]) inside circle x^2+y^2<=25 -> check corner (w,4)
        if w * w + 16 <= 25 + 1e-12:
            best = w
    return best
res['D07-math-1-v08'] = s1v08()

# 1-v09: square side 13, A(0,0) B(13,0) C(13,13) D(0,13); E inside with EA=5, EB=12 -> area BCE
def s1v09():
    # circle intersection
    x = (25 - 144 + 169) / (2 * 13)
    y = math.sqrt(25 - x * x)
    E = (x, y)  # y>0 is inside
    assert 0 < x < 13 and 0 < y < 13
    B, C = (13, 0), (13, 13)
    area = abs((B[0] - E[0]) * (C[1] - E[1]) - (C[0] - E[0]) * (B[1] - E[1])) / 2
    return area, E
a9, E9 = s1v09()
res['D07-math-1-v09'] = a9

# 1-v10: lotus 0.5 above water, tip touches water 1.5 horizontally -> depth
def s1v10():
    sols = []
    for h1000 in range(1, 20000):
        h = h1000 / 1000
        if abs((h + 0.5) ** 2 - (h * h + 1.5 ** 2)) < 1e-9:
            sols.append(h)
    assert len(sols) == 1
    return sols[0]
res['D07-math-1-v10'] = s1v10()

# 1-v11: integer right triangles with a leg 12
def s1v11():
    tri = set()
    for b in range(1, 1000):
        c2 = 144 + b * b
        c = math.isqrt(c2)
        if c * c == c2:
            tri.add(tuple(sorted((12, b, c))))
    return len(tri), sorted(tri)
n11, t11 = s1v11()
res['D07-math-1-v11'] = n11

def bearing_vec(bdeg, d):
    # bearing measured clockwise from north; x=east, y=north
    t = math.radians(bdeg)
    return (d * math.sin(t), d * math.cos(t))

# 1-v12: B at N20E 8, C at S40E 8 -> BC
def s1v12():
    B = bearing_vec(20, 8)
    C = bearing_vec(180 - 40, 8)
    return math.dist(B, C)
res['D07-math-1-v12'] = s1v12()

# 1-v13: O origin; go dir theta (east-north) 15 -> P; turn right 90, reach Q on positive x-axis with OQ=25;
# continue until |OR| = 39; how much further from Q
def s1v13():
    sols = []
    for k in range(1, 900000):
        th = math.radians(k / 10000)  # 0..90 deg
        P = (15 * math.cos(th), 15 * math.sin(th))
        d = (math.cos(th - pi / 2), math.sin(th - pi / 2))  # right turn
        # reach y=0: P.y + t*d.y = 0
        t = -P[1] / d[1]
        Qx = P[0] + t * d[0]
        if abs(Qx - 25) < 1e-4:
            sols.append((th, P, d, t))
    th, P, d, t = sols[0]
    # continue: find s>t with |P + s d| = 39
    # |P|^2 + s^2 = 39^2 since P.d = 0
    pd = P[0] * d[0] + P[1] * d[1]
    assert abs(pd) < 1e-9
    s = math.sqrt(39 ** 2 - 15 ** 2)
    return s - t
res['D07-math-1-v13'] = s1v13()

# 1-v14: Jia N30E 6 from Yi (origin), Bing S60E 8; circumradius
def s1v14():
    A = bearing_vec(30, 6)
    O = (0, 0)
    C = bearing_vec(120, 8)
    a = math.dist(O, C); b = math.dist(A, C); c = math.dist(A, O)
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return a * b * c / (4 * area)
res['D07-math-1-v14'] = s1v14()

# 1-v15: Jia 30 km/h N40E, Yi 40 km/h E40S (bearing 130) -> time to be 140 apart
def s1v15():
    va = bearing_vec(40, 30)
    vb = bearing_vec(130, 40)
    rel = math.dist(va, vb)
    return 140 / rel
res['D07-math-1-v15'] = s1v15()

# 2-v01: lamp 4.8, person 1.6 at 3 then 9 m; shadow tip displacement
def s2v01():
    def tip(d):
        # line from lamp (0,4.8) through head (d,1.6) hits ground
        return 4.8 * d / (4.8 - 1.6)
    return tip(9) - tip(3)
res['D07-math-2-v01'] = s2v01()

# 2-v02: equilateral triangle side 4 m, tiles 0.5 m; count tiles pointing opposite (vertex to south)
def s2v02():
    n = int(4 / 0.5)
    up = down = 0
    # row k from top (1..n): row has k up-triangles and k-1 down-triangles
    for k in range(1, n + 1):
        up += k
        down += k - 1
    assert up + down == n * n
    return down
res['D07-math-2-v02'] = s2v02()

# 2-v03: 4G radius 1.2 km, 5G radius 0.4 km, unit cost 1/6 -> % more
def s2v03():
    A = 1000.0  # arbitrary city area
    n4 = A / (pi * 1.2 ** 2)
    n5 = A / (pi * 0.4 ** 2)
    c4 = 1.0; c5 = 1 / 6
    return n5 * c5 / (n4 * c4) - 1
res['D07-math-2-v03'] = s2v03()

# 2-v04: wall + 60 m fence 3 sides; max area
def s2v04():
    best = 0
    for x1000 in range(1, 30000):
        x = x1000 / 1000  # perpendicular side
        y = 60 - 2 * x
        best = max(best, x * y)
    return best
res['D07-math-2-v04'] = s2v04()

# 2-v05: 46 unit fences, two rectangles equal perimeter, integer sides, max total area
def s2v05():
    best = 0
    for a1 in range(1, 24):
        for b1 in range(1, 24):
            for a2 in range(1, 24):
                for b2 in range(1, 24):
                    if a1 + b1 != a2 + b2:
                        continue
                    if 2 * (a1 + b1) + 2 * (a2 + b2) > 46:
                        continue
                    best = max(best, a1 * b1 + a2 * b2)
    return best
res['D07-math-2-v05'] = s2v05()

# 2-v06: river side free; parallel side 300/m, two perpendicular 200/m each; budget 24000
def s2v06():
    best = 0
    for y100 in range(1, 6000):
        y = y100 / 100  # perpendicular side
        x = (24000 - 400 * y) / 300
        if x <= 0:
            break
        best = max(best, x * y)
    return best
res['D07-math-2-v06'] = s2v06()

# 2-v07: trapezoid, S_AOD=45, S_BOC=125 -> total. Construct a concrete trapezoid and compute.
def s2v07():
    # AD:BC = sqrt(45/125) = 3/5. Choose AD=3t, BC=5t, height h; S_AOD = 45.
    # Build coordinates and solve for scale numerically
    k = math.sqrt(45 / 125)
    # take BC=5, AD=5k, height H, then scale area
    B = (0, 0); C = (5, 0); A = (1.3, 1); D = (1.3 + 5 * k, 1)
    def inter(P1, P2, P3, P4):
        x1, y1 = P1; x2, y2 = P2; x3, y3 = P3; x4, y4 = P4
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        px = ((x1 * y1 - y1 * x1) * 0)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    O = inter(A, C, B, D)
    def tri(P, Q_, R):
        return abs((Q_[0] - P[0]) * (R[1] - P[1]) - (R[0] - P[0]) * (Q_[1] - P[1])) / 2
    sAOD = tri(A, O, D); sBOC = tri(B, O, C)
    scale = 45 / sAOD
    assert abs(sBOC * scale - 125) < 1e-9
    tot = (tri(A, O, D) + tri(B, O, C) + tri(A, O, B) + tri(C, O, D)) * scale
    return tot
res['D07-math-2-v07'] = s2v07()

# 2-v08: quadrilateral split by diagonals; from figure: Jia & Bing opposite, Yi & Ding opposite.
# Yi = 0.8 Jia; Bing = Ding - 25; Yi = Bing + 20.  Opposite products equal.
def s2v08():
    sols = []
    for a10 in range(1, 100000):
        a = F(a10, 10)
        yi = a * F(4, 5)
        bing = yi - 20
        ding = bing + 25
        if bing <= 0:
            continue
        if a * bing == yi * ding:
            sols.append((a, yi, bing, ding))
    assert len(sols) == 1, sols
    a, yi, bing, ding = sols[0]
    return float(a + yi + bing + ding), sols[0]
r8, s8 = s2v08()
res['D07-math-2-v08'] = r8

# 2-v09: trapezoid AD=16, BC=24, h=15 -> S_AOB. Coordinates.
def s2v09():
    B = (0, 0); C = (24, 0); A = (3, 15); D = (19, 15)
    def inter(P1, P2, P3, P4):
        x1, y1 = P1; x2, y2 = P2; x3, y3 = P3; x4, y4 = P4
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    O = inter(A, C, B, D)
    def tri(P, Q_, R):
        return abs((Q_[0] - P[0]) * (R[1] - P[1]) - (R[0] - P[0]) * (Q_[1] - P[1])) / 2
    return tri(A, O, B)
res['D07-math-2-v09'] = s2v09()

# 2-v10: lychee 16, longan 12, wampee 24 (lychee opposite wampee) -> starfruit = 16*24/12
def s2v10():
    lz, ly, hp = 16, 12, 24
    yt = F(lz * hp, ly)
    return float(lz * F(8, 10) + ly * F(4, 10) + hp * F(6, 10) + yt * 1)
res['D07-math-2-v10'] = s2v10()

mine = {}
for vid, val in res.items():
    opts = Q[vid]['options']
    matches = []
    for k, s in opts.items():
        v = optval(s)
        tol = 0.6 if vid == 'D07-math-1-v02' else 1e-6
        if abs(v - val) < tol:
            matches.append(k)
    # nearest for approximate items
    near = min(opts, key=lambda k: abs(optval(opts[k]) - val))
    mine[vid] = near
    print(f"{vid}: computed={val:.6f}  matches={matches}  nearest={near}")

print()
print('1-v09 E =', E9)
print('1-v11 triangles =', t11)
print('2-v08 areas (jia, yi, bing, ding) =', s8)
json.dump(mine, open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/rev_D07_work/my_answers.json', 'w'), indent=1)
