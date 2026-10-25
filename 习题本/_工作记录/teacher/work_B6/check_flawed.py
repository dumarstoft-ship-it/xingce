import math
# --- T255x4 (2025天津): parallelogram with right angles at C (in ABC) and A (in ACD), AB = 2BC
a = 1.0                                     # BC = AD = a
C = (0.0, 0.0); B = (a, 0.0); A = (0.0, math.sqrt(3) * a); D = (-a, math.sqrt(3) * a)
def dist_line(p, q1, q2):
    (x0, y0), (x1, y1), (x2, y2) = p, q1, q2
    return abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / math.dist(q1, q2)
angB = math.degrees(math.acos(((A[0]-B[0])*(C[0]-B[0]) + (A[1]-B[1])*(C[1]-B[1])) / math.dist(A, B) / math.dist(C, B)))
print("angle B =", round(angB, 3))
# big circle tangent to BA, BC with shortest distance from B = AD/2
r1 = (a / 2) / (1 / math.sin(math.radians(angB / 2)) - 1)
bis = (math.cos(math.radians(180 - angB / 2)), math.sin(math.radians(180 - angB / 2)))
O1 = (B[0] + bis[0] * r1 / math.sin(math.radians(angB / 2)), B[1] + bis[1] * r1 / math.sin(math.radians(angB / 2)))
print("r1 =", round(r1, 4), "dist to BA", round(dist_line(O1, B, A), 4), "to BC", round(dist_line(O1, B, C), 4),
      "to AC", round(dist_line(O1, A, C), 4), "to DC", round(dist_line(O1, D, C), 4))
inr = (a + math.sqrt(3) * a - 2 * a) / 2
print("incircle radius of ABC =", round(inr, 4))
# alternative: big circle tangent to AB, AC (angle A = 30°)
def f(d):
    u = (0.2588190451, -0.9659258263)       # bisector at A between AC (down) and AB
    O = (A[0] + d * u[0], A[1] + d * u[1]); r = d * math.sin(math.radians(15))
    return math.dist(O, B) - r - a / 2, r
lo, hi = 0.5, 1.4
for _ in range(100):
    mid = (lo + hi) / 2
    if f(mid)[0] > 0: lo = mid
    else: hi = mid
rA = f(lo)[1]
print("alt r1 (tangent AB,AC) =", round(rA, 4), "area ratio =", round((rA / (a / 5)) ** 2, 3))
print("intended ratio (5/2)^2 =", (5 / 2) ** 2)
# --- T241x1 (2017吉林甲): cylinder circumference 5, height 12; B directly below A
print("straight-up speed =", 12 / (5 / 0.5), " helix speed =", math.hypot(5, 12) / (5 / 0.5))
