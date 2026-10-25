# Recompute every distractor value claimed in the jiexi (scratch check, not a verify script).
from fractions import Fraction as F
from math import isclose

ok = []
def chk(name, got, want):
    ok.append((name, got == want if not isinstance(got, float) else isclose(got, want, rel_tol=1e-9)))
    print(f'{name:55s} got {got!s:12s} want {want}')

# v01 (rev 2: H=4.5, h=1.8): true shadow = h*d/(H-h) = (2/3)d -> growth 4;
# wrong ratio shadow = d*h/H = 0.4d -> growth 2.4, tip moves 6+2.4
chk('v01 A shadow growth only', F(6) * F(18, 45 - 18), 4)
chk('v01 C wrong ratio tip move', F(6) + F(6) * F(18, 45), F(84, 10))
chk('v01 B walk distance', 9 - 3, 6)
# v02
chk('v02 B half', 64 // 2, 32)
chk('v02 C north count', sum(range(1, 9)), 36)
# v03
chk('v03 C cube', F(27, 6), F(9, 2))
chk('v03 D count only', F(9), 9)
chk('v03 radius-ratio only -> lower 50%', F(3, 6), F(1, 2))
# v04
chk('v04 B three equal sides', 20 * (60 - 2 * 20), 400)
chk('v04 A four sides fenced', 15 * 15, 225)
chk('v04 D x(60-x) max', max(x * (60 - x) for x in range(61)), 900)
# v05
chk('v05 C square 5.5 x2', 2 * 5.5 * 5.5, 60.5)
chk('v05 D 6x6 x2 (needs 48 pieces)', 2 * 36, 72)
# v06: maximise x*y under alternative (wrong) budget equations a*x + b*y = 24000 -> x=12000/a, y=12000/b
def best(a, b): return F(12000, a) * F(12000, b)
chk('v06 A river side also iron (400x+600y)', best(400, 600), 600)
chk('v06 C parallel at 200 (400x+200y)', best(400, 200), 1800)
chk('v06 D one perpendicular side (200x+300y)', best(200, 300), 2400)
# v07
chk('v07 A one side only', 45 + 125 + 75, 245)
chk('v07 C average sides', 45 + 125 + 2 * F(45 + 125, 2), 340)
chk('v07 D area ratio as base ratio', 45 + 125 + 2 * F(45 * 125, 45), 420)
# v08: correct conversion 1.25; wrong 1.2
c = F(25) / F(2, 10); d = c * F(12, 10); y = c + 20; j = y * F(12, 10)
chk('v08 D 1.2 times path', j + y + c + d, 594)
# sum rule: 1.25y + c = y + c + 25 -> y = 100
y2 = F(25) / F(1, 4); c2 = y2 - 20; d2 = c2 + 25; j2 = y2 * F(5, 4)
chk('v08 B sum rule', j2 + y2 + c2 + d2, 410)
chk('v08 A forgot ding', 150 + 120 + 100, 370)
# v09: total 300
chk('v09 B half of ABC', F(1, 2) * F(1, 2) * 24 * 15, 90)
chk('v09 C reversed AO:OC (ABC*3/5)', F(1, 2) * 24 * 15 * F(3, 5), 108)
chk('v09 D 2/5 of trapezoid', F(300) * F(2, 5), 120)
# v10
base = 16 * F(8, 10) + 12 * F(4, 10) + 24 * F(6, 10)
chk('v10 A lychee-longan paired', base + F(16 * 12, 24) * 1, 40)
chk('v10 B longan-wampee paired', base + F(12 * 24, 16) * 1, 50)
chk('v10 C simple average', (F(8, 10) + F(4, 10) + F(6, 10) + 1) / 4 * (16 + 12 + 24 + 32), F(588, 10))
print('ALL OK' if all(x for _, x in ok) else 'MISMATCH: ' + str([n for n, x in ok if not x]))
