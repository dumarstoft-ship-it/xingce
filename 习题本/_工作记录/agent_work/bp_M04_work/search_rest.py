import sys
sys.path.insert(0, '.')
from m04lib import *
def walker_rest(speed_kmh, walk, rest, T, start=0):
    v = F(speed_kmh, 60)  # km/min
    tr = Traj(0, 0)
    if start: tr.wait(start)
    while tr.t < T:
        tr.move_for(walk, v)
        tr.wait(rest)
    return tr
res = []
for a in [4, 5, 6, 8, 9, 10, 12]:
    for w in [20, 30, 40, 50]:
        for r in [10, 15, 20]:
            for b in [3, 4, 4.5, 5, 6, 7.5, 8]:
                b = F(b).limit_denominator(10)
                if b >= a: continue
                avg = F(a) * w / (w + r)
                if b <= avg * F(1, 2): continue
                T = 120
                A = walker_rest(a, w, r, T + 60); B = Traj(0, 0).move_for(T + 60, F(b, 60))
                ms = [m for m in meetings(A, B) if 0 < m['t'] <= T]
                if not ms: continue
                # 排除端点接触（相遇时刻恰为甲的走/停切换点）
                bps = A.breakpoints()
                if any(m['t'] in bps for m in ms): continue
                if all(m['t'].denominator == 1 for m in ms):
                    res.append((a, w, r, float(b), len(ms), [int(m['t']) for m in ms], [str(m['x']) for m in ms]))
for x in res[:40]:
    print('甲%skm/h 走%s休%s 乙%skm/h -> 2h内相遇%s次 时刻%s 位置%s' % x)
print(len(res))
