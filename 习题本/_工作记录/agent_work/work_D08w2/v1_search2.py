# a*x + b*y = N, x,y>=1, restriction x >= y.
# zero solution (0, N/b) exists (violates x>=y); (N/a, 0) should NOT exist.
# equality x=y exists (strict reading -> C-1). want g>=12, 3<=a',b'<=9, C 7..10, T-C>=3
from math import gcd
vals = [36,40,42,45,48,54,56,60,63,64,70,72,75,78,80,84,90,96,98,100,105,108,112,120,126,135,140,144,150,160,168,180,200,210,225,240,250,270,280,300]
out = []
for a in vals:
    for b in vals:
        if a == b: continue
        g = gcd(a, b)
        if g < 12: continue
        ap, bp = a // g, b // g
        if min(ap, bp) < 3 or max(ap, bp) > 9: continue
        for N in range(1000, 15001, 100):
            if N % g: continue
            sols = [(x, (N - a*x)//b) for x in range(1, N//a + 1) if (N - a*x) % b == 0 and (N - a*x)//b >= 1]
            T = len(sols); C = sum(1 for x, y in sols if x >= y); Cs = sum(1 for x, y in sols if x > y)
            if not (N % b == 0 and N % a != 0): continue
            if 7 <= C <= 10 and Cs == C - 1 and T - C >= 3 and T <= 2*C + 3:
                out.append((g, N, a, b, ap, bp, C, T))
for o in sorted(out, key=lambda o: (-o[0], o[1])): print(o)
print(len(out))
