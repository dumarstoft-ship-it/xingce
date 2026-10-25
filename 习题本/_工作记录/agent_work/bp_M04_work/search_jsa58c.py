import sys
sys.path.insert(0, '.')
from m04lib import *
def jia_traj(L, v, walk, rest, start):
    tr = Traj(0, 0)
    if start: tr.wait(start)
    seg = v * walk
    while tr.x < L:
        nx = min(L, tr.x + seg)
        tr.move_to(nx, v)
        if nx < L: tr.wait(rest)
    return tr
def scan(L, v, walk, rest, jia_start, label, Tlo=30, Thi=400, step=F(1, 4)):
    jia = jia_traj(L, v, walk, rest, jia_start)
    print('==', label, '甲到达时刻', jia.end())
    prev = None; T = F(Tlo)
    while T <= Thi:
        yi = Traj(0, 0).move_to(L, F(L) / T)
        ms = [m for m in meetings(jia, yi) if 0 < m['x'] < L and m['t'] > 0]
        xs = sorted(set(m['x'] for m in ms))
        n = len(xs)
        if n != prev:
            print('  乙用时 %s min: 途中相遇 %d 次 %s' % (T, n, [str(x) for x in xs]))
            prev = n
        T += step
# 原题：乙早 15 分钟（以乙出发为 0，甲 15 分钟后出发），甲 6km/h 走30休15，AB=9
scan(9, F(1, 10), 30, 15, 15, '原题 2022JSA-58')
# 变式：甲 6km/h 走40休20，AB=12，乙早 20 分钟
scan(12, F(1, 10), 40, 20, 20, '变式A')
# 变式：甲 6km/h 走30休10，AB=9，乙早 10 分钟
scan(9, F(1, 10), 30, 10, 10, '变式B')
