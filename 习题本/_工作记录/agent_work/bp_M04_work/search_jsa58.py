import sys
sys.path.insert(0, '.')
from m04lib import *
def jia_traj(L, speed_per_min, walk, rest, start):
    tr = Traj(0, 0)
    if start: tr.wait(start)
    seg = speed_per_min * walk
    k = 0
    while tr.x < L:
        nx = min(L, tr.x + seg)
        tr.move_to(nx, speed_per_min)
        if nx < L: tr.wait(rest)
    return tr
def count_inner(L, jia, yi_start, Tyi):
    yi = Traj(0, 0)
    if yi_start: yi.wait(yi_start)
    yi.move_to(L, F(L) / Tyi)
    ms = [m for m in meetings(jia, yi) if 0 < m['x'] < L and m['t'] > 0]
    xs = sorted(set(m['x'] for m in ms))
    return xs, ms
# 方案：AB=9km，甲 6km/h 走30休15，乙晚出发 d 分钟不休息；扫描乙全程用时 T（分钟）
for d in [15, 30]:
    print('== 乙晚出发', d)
    jia = jia_traj(9, F(1, 10), 30, 15, 0)
    prev = None
    for T10 in range(300, 2000, 5):
        T = F(T10, 10)
        xs, ms = count_inner(9, jia, d, T)
        n = len(xs)
        if n != prev:
            print('  乙用时 %.1f min: 途中相遇 %d 次 %s' % (float(T), n, [str(x) for x in xs]))
            prev = n
