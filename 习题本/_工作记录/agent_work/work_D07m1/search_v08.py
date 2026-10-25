from fractions import Fraction as F
import math
def sq(v):
    # v Fraction; is it a perfect square of a Fraction with denominator dividing 20?
    if v < 0: return None
    for den in (1, 2, 4, 5, 10, 20):
        x = v*den*den
        if x.denominator == 1:
            r = math.isqrt(int(x))
            if r*r == x: return F(r, den)
    return None
for R10 in range(30, 81):      # radius 3.0 .. 8.0
    R = F(R10, 10)
    for w10 in range(15, 41):  # width 1.5 .. 4.0
        w = F(w10, 10)
        h1 = sq(R*R - w*w)      # one side, hugging centre line
        h2 = sq(R*R - w*w/4)    # centred
        if h1 and h2 and 2.5 <= h1 <= 5:
            print(f"R={float(R)} w={float(w)} h_side={float(h1)} h_centered={float(h2)}")
