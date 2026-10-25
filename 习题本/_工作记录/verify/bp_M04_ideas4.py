from fractions import Fraction as F
def schedule(L, v, trips, stayB, start=F(0)):
    """返回分段 [(t0,t1,x0,x1)]：从 A 出发，到 B 停 stayB，再回 A，往返 trips 次，结束停 A"""
    segs = []; t = F(start); x = F(0)
    if start > 0: segs.append((F(0), start, F(0), F(0)))
    for k in range(trips):
        segs.append((t, t + L / v, F(0), F(L))); t += L / v
        if stayB: segs.append((t, t + stayB, F(L), F(L))); t += stayB
        segs.append((t, t + L / v, F(L), F(0))); t += L / v
    return segs, t
def pos(segs, tend, t):
    if t >= tend: return F(0)
    for a, b, x0, x1 in segs:
        if a <= t <= b:
            return x0 + (x1 - x0) * (t - a) / (b - a) if b > a else x0
    return F(0)
def maxdist(L, v1, v2, trips, s1, s2):
    A, ta = schedule(F(L), F(v1), trips, F(s1)); B, tb = schedule(F(L), F(v2), trips, F(s2))
    bps = sorted(set([a for a, *_ in A] + [b for _, b, *_ in A] + [a for a, *_ in B] + [b for _, b, *_ in B] + [ta, tb]))
    best = max((abs(pos(A, ta, t) - pos(B, tb, t)), t) for t in bps)
    return best, ta, tb
res = []
for L in [20, 24, 30, 36, 40, 45, 48, 60]:
    for v1, v2 in [(100, 80), (90, 60), (80, 60), (72, 60), (60, 40), (90, 75), (120, 80), (100, 60), (60, 45)]:
        for s1 in [F(0), F(1, 10), F(1, 5), F(1, 4), F(1, 3)]:
            for trips in [1, 2]:
                (m, t), ta, tb = maxdist(L, v1, v2, trips, s1, 0)
                if m < L and m.denominator == 1 and t != ta and s1 > 0:
                    res.append((L, v1, v2, s1, trips, m, t, ta, tb))
for r in res[:25]:
    print("L=%s 甲%s(到B停%s h) 乙%s trips=%s -> 最远 %s 于 t=%s (甲完%s 乙完%s)" % r)
print("对照 无停留:", maxdist(30, 100, 80, 2, 0, 0))
print("甲停 6 分钟:", maxdist(30, 100, 80, 2, F(1, 10), 0))
