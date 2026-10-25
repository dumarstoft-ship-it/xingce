import sys, math
sys.path.insert(0,'/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M04_work/v2')
from m04lib import *
print('=== B2. 甲从山脚上山(a)、乙从山顶下山(1.5b)同时出发，到对方出发地后立即返回（甲下山1.5a，乙上山b）')
for L in [600, 900, 1200, 1500, 1800, 2400, 3000, 3600]:
    for a, b in [(60,40),(50,40),(45,30),(40,30),(60,45),(80,60),(40,40),(60,60),(30,20),(50,30)]:
        J = Traj(0,0); Y = Traj(0,L)
        J.move_to(L, a).move_to(0, F(3,2)*a).move_to(L, a)
        Y.move_to(0, F(3,2)*b).move_to(L, b).move_to(0, F(3,2)*b)
        ms = [m for m in meetings(J, Y) if m['t'] > 0]
        if len(ms) >= 2 and ms[1]['x'].denominator == 1 and ms[0]['x'].denominator == 1:
            print(L, a, b, [(str(m['t']), str(m['x']), m['kind']) for m in ms[:3]])
print('=== B3. 同时从山脚出发往返，问"甲第一次下山途中与乙相遇处" 与 "乙第一次下山途中被甲…"')
