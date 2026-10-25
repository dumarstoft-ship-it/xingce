# Proposed fix for D03-math-1-v02: keep both conditions, ask for the total length.
from fractions import Fraction as F
R1, D1, R2, D2 = F(1, 3), 800, F(5, 6), 3000
# brute force over L (1 m grid) and speed share a (1/1000 grid): a*L*R1 == D1 and (1-a)*L*R2 == D2
sols = set()
for L in range(1000, 20001):
    a = F(D1) / (L * R1)
    if 0 < a < 1 and (1 - a) * L * R2 == D2:
        sols.add((L, a))
print('solutions (L, a):', sols)
L, a = sols.pop()
# with ONLY condition 1, L is not determined (show two different L values fit cond. 1)
print('cond.1 alone fits L=4800 (a=1/2) and L=8000 (a=3/10):', F(800)/(4800*R1), F(800)/(8000*R1))
# meeting point from A with cond. 1 alone (any L):
print('meeting from A from cond.1 alone =', D1 / R1)
# distractors for the "total length" ask
print('4560 = (800+3000)/(5/6):', F(D1 + D2) / R2)
print('4800 = 2*800*3 (assume meeting at midpoint):', 2 * D1 * 3)
print('5400 = 800*3 + 3000 (scale only 甲):', D1 * 3 + D2)
print('6000 correct:', D1 / R1 + D2 / R2)
