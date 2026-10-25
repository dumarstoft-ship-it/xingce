from fractions import Fraction as F
def unfold(d, L):
    p = d % (2 * L); return p if p <= L else 2 * L - p
def exact_max(L, v1, v2, trips, delay2=0):
    """同端 A 出发；乙晚 delay2 小时出发；各往返 trips 次后停在 A。分段线性 => 最大值在断点处取得"""
    L, v1, v2, delay2 = F(L), F(v1), F(v2), F(delay2)
    T1 = 2 * L * trips / v1; T2 = delay2 + 2 * L * trips / v2
    bps = {F(0), T1, T2, delay2}
    for k in range(0, 4 * trips + 2):
        t = k * L / v1
        if t <= T1: bps.add(t)
        t = delay2 + k * L / v2
        if t <= T2: bps.add(t)
    def p1(t): return unfold(min(v1 * t, 2 * L * trips), L)
    def p2(t): return unfold(min(v2 * max(t - delay2, 0), 2 * L * trips), L)
    best = max((abs(p1(t) - p2(t)), t) for t in bps)
    return best
seen = []
for L in [20, 24, 30, 36, 40, 45, 48, 60]:
    for v1 in [60, 72, 80, 90, 100, 120]:
        for v2 in [40, 45, 48, 50, 60, 64, 75, 80]:
            if v2 >= v1: continue
            for trips in [1, 2]:
                for delay in [0]:
                    m, t = exact_max(L, v1, v2, trips, delay)
                    if m < L and m.denominator == 1 and trips == 2:
                        seen.append((L, v1, v2, trips, int(m), float(t)))
for s in seen[:30]: print("L=%d v1=%d v2=%d trips=%d -> max=%d at t=%.3f h" % s)
print("orig 2022SC1-47:", exact_max(30, 100, 80, 2))
print("D31 idea L40 80/60 1trip:", exact_max(40, 80, 60, 1))
# 甲乙从两端相向出发、各往返 2 次（各回到自己出发地后停）：最大距离（不含 t=0）
def opp_max(L, v1, v2, trips):
    L, v1, v2 = F(L), F(v1), F(v2)
    T1 = 2 * L * trips / v1; T2 = 2 * L * trips / v2
    bps = set()
    for k in range(0, 4 * trips + 2):
        if k * L / v1 <= T1: bps.add(k * L / v1)
        if k * L / v2 <= T2: bps.add(k * L / v2)
    bps |= {T1, T2}
    def p1(t): return unfold(min(v1 * t, 2 * L * trips), L)
    def p2(t): return unfold(L + min(v2 * t, 2 * L * trips), L)
    return sorted(((abs(p1(t) - p2(t)), t) for t in bps if t > 0), reverse=True)[:3]
print("opp:", opp_max(60, 90, 60, 1))
print("---- 乙晚出发 ----")
from fractions import Fraction as F
for L in [24, 30, 36, 40, 45, 60]:
    for v1, v2 in [(100, 80), (90, 60), (80, 60), (72, 60), (60, 40), (90, 75), (120, 80)]:
        for dl in [F(1, 20), F(1, 10), F(3, 20), F(1, 5), F(1, 4), F(1, 3), F(1, 2)]:
            for trips in [1, 2]:
                m, t = exact_max(L, v1, v2, trips, dl)
                T1 = F(2 * L * trips, v1)
                if m < L and m.denominator == 1 and t != T1 and t != dl:
                    print("L=%d v1=%d v2=%d delay=%s h trips=%d -> max=%s at t=%s (甲完成于%s)" % (L, v1, v2, dl, trips, m, t, T1))
print("---- 快车晚出发 ----")
def exact_max2(L, vfast, vslow, trips, delay_fast):
    L, v1, v2, d = F(L), F(vfast), F(vslow), F(delay_fast)
    T1 = d + 2 * L * trips / v1; T2 = 2 * L * trips / v2
    bps = {F(0), T1, T2, d}
    for k in range(0, 4 * trips + 2):
        t = d + k * L / v1
        if t <= T1: bps.add(t)
        t = k * L / v2
        if t <= T2: bps.add(t)
    def p1(t): return unfold(min(v1 * max(t - d, 0), 2 * L * trips), L)
    def p2(t): return unfold(min(v2 * t, 2 * L * trips), L)
    return max((abs(p1(t) - p2(t)), t) for t in bps), T1, T2
for L in [24, 30, 36, 40, 45, 60]:
    for v1, v2 in [(100, 80), (90, 60), (80, 60), (72, 60), (60, 40), (90, 75), (120, 80), (100, 60)]:
        for dl in [F(1, 20), F(1, 10), F(3, 20), F(1, 5), F(1, 4), F(1, 3), F(1, 2)]:
            for trips in [1, 2]:
                (m, t), T1, T2 = exact_max2(L, v1, v2, trips, dl)
                if m < L and m.denominator == 1 and t not in (T1, T2):
                    print("L=%d 快%d(晚%s h) 慢%d trips=%d -> max=%s at t=%s (快完成%s,慢完成%s)" % (L, v1, dl, v2, trips, m, t, T1, T2))
