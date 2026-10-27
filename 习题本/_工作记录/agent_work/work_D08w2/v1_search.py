# Search a*x + b*y = N (x,y>=1), restriction y >= x  (y-item count not less than x-item count)
# want: g=gcd(a,b)>=5, a/g,b/g>=3; C (with restriction) 7..10; equality x=y exists;
# zero solution (0, N/b) exists (passes restriction); T (no restriction) distinct
from math import gcd
cands = []
vals = [30,36,40,45,48,50,54,60,64,70,72,75,80,84,90,96,100,105,108,112,120,125,126,135,140,144,150,160,168,175,180,200,210,225,240,250,270,280,300]
for a in vals:
    for b in vals:
        if a == b: continue
        g = gcd(a, b)
        if g < 5: continue
        ap, bp = a // g, b // g
        if min(ap, bp) < 3 or max(ap, bp) > 9: continue
        for N in range(500, 20001, 50):
            if N % g: continue
            sols = [(x, (N - a * x) // b) for x in range(1, N // a + 1) if (N - a * x) % b == 0 and (N - a * x) // b >= 1]
            T = len(sols)
            C = sum(1 for x, y in sols if y >= x)
            Cs = sum(1 for x, y in sols if y > x)
            zero_ok = (N % b == 0)  # (0, N/b) all y-items, passes y>=x
            zero_x = (N % a == 0)   # (N/a, 0) all x-items, fails y>=x
            R = sum(1 for x, y in sols if x >= y)
            if 7 <= C <= 10 and Cs == C - 1 and zero_ok and T >= C + 3 and T <= 2 * C + 2:
                cands.append((N % 100 != 0, N, a, b, g, ap, bp, C, T, R, zero_x))
cands.sort()
for c in cands[:80]:
    print(c)
print(len(cands))
