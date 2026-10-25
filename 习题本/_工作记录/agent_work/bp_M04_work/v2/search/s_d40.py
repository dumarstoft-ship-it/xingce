import sys, math
sys.path.insert(0,'/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M04_work/v2')
from m04lib import *
print('=== A. 周期休息：甲走w分钟休r分钟，速度v；乙同时出发匀速u；全程S；数途中相遇次数')
def jia_tr(S, v, w, r):
    tr = Traj(0, 0); pos = F(0)
    while pos < S:
        step = min(v * w, S - pos)
        tr.move_to(pos + step, v); pos += step
        if pos < S: tr.wait(r)
    return tr
for (S, v, w, r) in [(12, F(3,40), 40, 20), (9, F(1,10), 30, 15), (12, F(1,10), 30, 10), (10, F(1,10), 20, 10)]:
    J = jia_tr(F(S), v, w, r)
    prev = None; rows = []
    for T in range(int(S / v) + 1, 400):        # 乙全程用时 T 分钟
        u = F(S, T)
        Y = Traj(0, 0).move_to(S, u)
        inner = sorted(set(m['t'] for m in meetings(J, Y) if 0 < m['x'] < S and m['t'] > 0))
        n = len(inner)
        if n != prev:
            rows.append((T, n)); prev = n
    print('S=%s v=%s w=%s r=%s 甲到达=%s' % (S, v, w, r, J.end()), rows[:20])
print('=== B. 上下山往返：山路L，甲上a下1.5a，乙上b下1.5b，同时从山脚出发，第二次迎面相遇位置')
for L in [600, 900, 1200, 1800, 2400]:
    for a, b in [(60,40),(50,40),(45,30),(40,30),(60,45),(80,60)]:
        J = Traj(0,0); Y = Traj(0,0)
        for k in range(4):
            J.move_to(L, a).move_to(0, F(3,2)*a)
            Y.move_to(L, b).move_to(0, F(3,2)*b)
        ho = [m for m in meetings(J, Y) if m['t'] > 0 and m['kind']=='head-on']
        if len(ho) >= 2 and ho[1]['x'].denominator == 1 and ho[0]['x'].denominator == 1:
            print(L, a, b, [(str(m['t']), str(m['x'])) for m in ho[:3]])
