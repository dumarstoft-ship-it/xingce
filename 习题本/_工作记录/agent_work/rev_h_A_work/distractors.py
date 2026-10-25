# Where do the distractors come from? (common error paths) -- blind, before key.
from fractions import Fraction as Fr
from math import comb

print("Q1 options 224/240/280/320")
# ignore 9:00 delay: share by speed ratio 3:5:8
print("  ignore delay:", Fr(560 * 8, 16))
# misread C speed as 280/4=70, keep delay
T = Fr(560 + 70, 30 + 50 + 70); print("  C speed 70 + delay:", 70 * (T - 1))
# forget C late start but use T=4
print("  80*4:", 80 * 4)

print("Q2 options 26/30/36/46")
for name, rhs in [("forget return supply", lambda N: 20 * N), ("correct", lambda N: 20 * N - 30),
                  ("return supply 2x(10 days)", lambda N: 20 * N - 60)]:
    print("  ", name, [N for N in range(7, 200) if 23 * (N - 6) == rhs(N)])
print("   remaining members =", 36 - 6)

print("Q3 options 13/15/16/19")
for h in range(0, 7):
    for sub in (True, False):
        lhs_const = -6 if sub else 0
        # 6n + lhs_const = 72 + 6*h
        n = Fr(72 + 6 * h - lhs_const, 6)
        if n.denominator == 1 and n in (13, 15, 16, 19):
            print("   inflow hours", h, "subtract 3x2" if sub else "no -6", "->", n)

print("Q4 options 50/52/53/55")
print("  floor partial:", 50 + (300 - 275) // 11, " full block:", 55)

print("Q5 options 21/25/30/70")
for name, f in [("correct", lambda T: (T/2)/Fr(14,10) + (T/2)/Fr(6,10) - T),
                ("down40% read as /1.4 eff -> time*1.4", lambda T: (T/2)/Fr(14,10) + (T/2)*Fr(14,10) - T),
                ("time halves", lambda T: Fr(0))]:
    print("  ", name, [T for T in range(1, 200) if f(Fr(T)) == 4])
print("   actual duration:", 21 + 4)

print("Q6 options 3640/6250/7000/7840: 125*50 =", 125*50, " 140*56 =", 140*56, " 65*56 =", 65*56)

print("Q8 steady-state count (buses from Yi departing in (dep-48, dep+48)):",
      len([s for s in range(-200, 200, 8) if 16 - 48 < s < 16 + 48]))

print("Q10 options 196/200/204/209: no diagonals:", comb(12,3) - 12 - 4,
      " rows counted once:", comb(12,3) - 3 - 4 - 4)

print("Q11 options 270/780/810/1620: labeled", 1680 - 60, " /6:", (1680 - 60)//6,
      " 1680/2-60:", 1680//2 - 60)

print("Q12 options 20/21/35/56: all sent C(7,2)=", comb(7,2), " leftover>=1 C(7,3)=", comb(7,3),
      " C(6,3)=", comb(6,3))

print("Q13 options 10250/12000/12500/13600: AM-GM =", 2 * (200*300*600) ** 0.5,
      " x=50:", 200*50 + 300*12, " x=40:", 200*40 + 300*15)
# 10250 feasible at all?
import math
disc = 10250**2 - 4*200*180000
print("   10250 attainable by any rectangle of area 600? disc =", disc)

print("Q14 options 40/75/105/110 (x5): 1+p+q+r =", 1+2+1+4, " pq+qr+rp+1 =", 1+2+4+8,
      " p(1+q)+q(1+r)+r(1+p) =", 2*2+1*5+4*3)
