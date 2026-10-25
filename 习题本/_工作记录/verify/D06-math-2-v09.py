# D06-math-2-v09: two people arrive uniformly in [0,60] minutes, independently;
# first to arrive waits at most 12 minutes. P(meet) = P(|x-y| <= 12).
from fractions import Fraction as F

T, t = 60, 12

def L(x):
    # length of y in [0,T] with |x - y| <= t
    return min(F(T), x + t) - max(F(0), x - t)

# L is piecewise linear with breakpoints 0, t, T-t, T -> trapezoid rule is exact
pts = sorted({F(0), F(t), F(T - t), F(T)})
area = sum((pts[i + 1] - pts[i]) * (L(pts[i]) + L(pts[i + 1])) / 2 for i in range(len(pts) - 1))
P = area / (T * T)

# independent numeric cross-check on a midpoint grid
N = 600
cnt = 0
for i in range(N):
    x = (i + 0.5) * T / N
    for j in range(N):
        y = (j + 0.5) * T / N
        if abs(x - y) <= t:
            cnt += 1
assert abs(cnt / N / N - float(P)) < 0.005

opts = {'A': F(20, 100), 'B': F(36, 100), 'C': F(40, 100), 'D': F(64, 100)}
hit = [k for k, v in opts.items() if v == P]
assert len(hit) == 1, (P, hit)
print('P =', P)
print(hit[0])
