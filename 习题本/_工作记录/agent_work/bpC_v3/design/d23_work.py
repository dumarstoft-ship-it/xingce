import sys; sys.path.insert(0, '..')
from lib import *

# v1：一周锻炼（周一=1…周日=7），活动：游泳(恰2次)、骑行(恰1次)、跳绳(恰1次)、瑜伽(≥1次)、散步(其余)
ACT = ['泳', '骑', '跳', '瑜', '散']
def week(gap_swim, gap_yoga, extra=lambda d: True):
    out = []
    for days in product(ACT, repeat=7):
        sw = [i for i in range(7) if days[i] == '泳']
        if len(sw) != 2 or sw[1] - sw[0] != gap_swim: continue
        bi = [i for i in range(7) if days[i] == '骑']
        if len(bi) != 1 or abs(bi[0] - sw[0]) != 1: continue
        ju = [i for i in range(7) if days[i] == '跳']
        if len(ju) != 1 or not ju[0] < sw[1]: continue
        yo = [i for i in range(7) if days[i] == '瑜']
        if len(yo) < 1 or any(abs(x - sw[0]) != gap_yoga for x in yo): continue
        if not any(days[i] == '散' for i in range(sw[0])): continue
        if not extra(days): continue
        out.append(''.join(days))
    return out
for gs in (3, 4, 5):
    for gy in (2, 3, 4, 5):
        S = week(gs, gy)
        if 2 <= len(S) <= 6:
            print('游泳日期差', gs, '瑜伽与第一次游泳日期差', gy, '解数', len(S), S)
