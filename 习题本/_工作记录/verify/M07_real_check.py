"""M07 概率问题：独立验算题库真题（含 5 道自解题）。每题从题面数据出发计算，再与选项比对。"""
from fractions import Fraction as F
from itertools import permutations, combinations, product
from math import comb, gcd, factorial
import random

res = {}

def pick(opts, val, tol=1e-9):
    """opts: dict letter->value (number) or letter->(lo,hi) interval; return letters matching val."""
    hit = []
    for k, o in opts.items():
        if isinstance(o, tuple):
            lo, hi = o
            if (lo is None or val >= lo - tol) and (hi is None or val < hi + tol):
                hit.append(k)
        elif abs(float(o) - float(val)) < 1e-9:
            hit.append(k)
    return hit

def rec(qid, val, opts, official=None):
    h = pick(opts, val)
    res[qid] = (val, h, official)

# ---------- 自解 5 题 ----------
# 2026GD-40 全概率
rec('2026GD-40', F(3,10)*F(7,10) + F(7,10)*F(2,10), {'A':F(25,100),'B':F(35,100),'C':F(45,100),'D':F(55,100)})
# 2026GK-70 乙胜甲 0.6；乙胜丙=2x；0.6*2x=0.18
x = F(18,100) / (F(6,10)*2)
rec('2026GK-70', x, {'A':F(1,10),'B':F(12,100),'C':F(15,100),'D':F(3,10)})
# 2026GK-73 选3人，恰1人/2人都中 = 30，逐个 N 检验
sol = [N for N in range(5, 200) if F(2*comb(N-2,2), comb(N,3)) == 30*F(comb(N-2,1), comb(N,3))]
rec('2026GK-73', sol[0], {'A':15,'B':17,'C':29,'D':33})
assert sol == [33], sol
# 2026ZJA-62 13 天，A2/B3/C4 连续块，暴力枚举所有不重叠放置
tot = good = 0
for a in range(13-2+1):
    for b in range(13-3+1):
        for c in range(13-4+1):
            days = [0]*13; ok = True
            for st, ln, t in ((a,2,1),(b,3,2),(c,4,3)):
                for d in range(st, st+ln):
                    if days[d]: ok = False
                    days[d] = t
            if not ok: continue
            tot += 1
            free = [i for i in range(13) if days[i] == 0]
            if all(free[i+1]-free[i] > 1 for i in range(len(free)-1)): good += 1
rec('2026ZJA-62', F(good, tot), {'A':F(1,10),'B':F(1,15),'C':F(1,20),'D':F(1,35)})
# 2026ZJA-63 1..10 取两数互质
pairs = list(combinations(range(1,11),2))
rec('2026ZJA-63', F(sum(gcd(a,b)==1 for a,b in pairs), len(pairs)), {'A':F(2,3),'B':F(31,45),'C':F(11,15),'D':F(7,9)})

# ---------- 有官方答案的真题核对 ----------
rec('2020JSA-56', 0.6*0.8+0.4*0.7, {'A':0.73,'B':0.74,'C':0.75,'D':0.76}, 'D')
rec('2022GD-35', 1-F(comb(4,3),comb(6,3)), {'A':F(1,5),'B':F(1,2),'C':F(2,3),'D':F(4,5)}, 'D')
rec('2022JSA-54', F(2*20, 2*20+3*25), {'A':F(2,5),'B':F(3,7),'C':F(9,16),'D':F(8,23)}, 'D')
pal = [n for n in range(100,1000) if str(n)==str(n)[::-1]]
rec('2022ZJA-59', F(sum(n%2 for n in pal), len(pal)), {'A':F(2,9),'B':F(1,3),'C':F(4,9),'D':F(5,9)}, 'D')
rec('2023GK-65', (5/9)**2, {'A':(None,0.25),'B':(0.25,0.35),'C':(0.35,0.45),'D':(0.45,None)}, 'B')
rec('2023JSA-63', F(2,5)*F(3,5)*F(4,5), {'A':F(1,25),'B':F(6,125),'C':F(24,125),'D':F(3,250)}, 'C')
rec('2024HB-62', F(comb(3,1)*comb(3,2), comb(6,3)), {'A':F(9,20),'B':F(1,2),'C':F(3,5),'D':F(11,20)}, 'A')
rec('2024HB-74', F(comb(16,2), comb(45,2)), {'A':F(4,33),'B':F(11,45),'C':F(16,45),'D':F(1,3)}, 'A')
rec('2024JSA-59', 1-F(comb(6,3), comb(8,3)), {'A':F(9,20),'B':F(5,14),'C':F(11,20),'D':F(9,14)}, 'D')
rec('2024SD-51', 1-F(comb(6,3), comb(8,3)), {'A':F(5,14),'B':F(15,28),'C':F(9,14),'D':F(19,28)}, 'C')
rec('2025HB-72', 1-(1-F(3,4))*(1-F(1,3)), {'A':F(1,4),'B':F(1,2),'C':F(2,3),'D':F(5,6)}, 'D')
c = sum(1 for s in combinations(range(1,8),3) if s[2]-s[0]==2)
rec('2025SC-47', F(c, comb(7,3)), {'A':F(1,7),'B':F(1,6),'C':F(1,5),'D':F(1,4)}, 'A')
rec('2020HB-62', 1-F(20,30)**2, {'A':F(1,3),'B':F(2,3),'C':F(5,9),'D':F(7,9)}, 'C')  # 选项取自原卷第9页
# 2020JSA-65 王与(李∪张)互斥
rec('2020JSA-65', 0.2 + (0.2+0.2-0.1), {'A':0.3,'B':0.4,'C':0.5,'D':0.6}, 'C')
p = 3/20
rec('2020SC1206-47', (1-p)**2 + p**2, {'A':0.7225,'B':0.745,'C':0.825,'D':0.85}, 'B')
rec('2020SD-43', F(3, 5*4), {'A':F(3,20),'B':F(1,5),'C':F(1,9),'D':F(2,9)}, 'A')
# 2021SC2-49 两组，每组>=2县，暴力
tot = good = 0
for asg in product((0,1), repeat=5):
    n0 = asg.count(0)
    if n0 < 2 or n0 > 3: continue
    tot += 1; good += asg[0]==asg[1]
rec('2021SC2-49', F(good,tot), {'A':F(1,3),'B':F(2,5),'C':F(1,2),'D':F(3,5)}, 'B')
# 2021ZJA-58 三位全奇、恰两位相同
codes = [c for c in product((1,3,5,7,9), repeat=3) if len(set(c))==2]
rec('2021ZJA-58', F(2, len(codes)), {'A':F(1,30),'B':F(1,50),'C':F(2,59),'D':F(2,57)}, 'A')
rec('2021ZJA-69', 1 - F(5*4*3, 5**3), {'A':F(36,100),'B':F(48,100),'C':F(52,100),'D':F(64,100)}, 'C')
# 2022SC2-47 乙16 甲24
yi = 8/0.5; jia = yi+8; n = int(jia+yi)
rec('2022SC2-47', 1-comb(int(yi),3)/comb(n,3), {'A':(None,0.80),'B':(0.80,0.90),'C':(0.90,0.95),'D':(0.95,None)}, 'C')
xx = comb(9,2)/comb(10,3)*100; yy = (1-0.9**4)*100
rec('2022SD-44', xx-yy, {'A':(None,-5),'B':(-5,0),'C':(0,5),'D':(5,None)}, 'B')
# 2022ZJA-57 4专家3点每点>=1
tot = good = 0
for asg in product(range(3), repeat=4):
    if len(set(asg)) < 3: continue
    tot += 1; good += asg[0]!=asg[1]
rec('2022ZJA-57', F(good,tot), {'A':F(3,4),'B':F(1,6),'C':F(5,6),'D':F(1,4)}, 'C')
rec('2023HB-62', 0.4*0.4 + 2*0.4*0.6*0.2, {'A':0.32,'B':0.256,'C':0.24,'D':0.208}, 'B')
combos = [(a,b,c) for c in range(3) for b in range(4) for a in range(8) if 10*a+20*b+30*c==70]
rec('2023SC-49', F(sum(c>0 for a,b,c in combos), len(combos)), {'A':0.625,'B':0.5,'C':0.375,'D':0.25}, 'B')
tot = good = 0
for s in combinations(range(7),3):
    tot += 1; good += all(s[i+1]-s[i] >= 2 for i in range(2))
rec('2023ZJA-60', F(good,tot), {'A':F(1,5),'B':F(2,7),'C':F(6,35),'D':F(9,35)}, 'B')
w2 = 0.7*0.5 + 0.3*0.7; w3 = w2*0.5 + (1-w2)*0.7
rec('2024SC-54', w3, {'A':(None,0.55),'B':(0.55,0.57),'C':(0.57,0.59),'D':(0.59,None)}, 'C')
# 2024ZJA-62
Q = '甲乙丙丁戊'
zh = [p for p in permutations(Q) if p[1]=='甲' and p[3]=='丁']
wa = [p for p in permutations(Q) if p[2]=='乙']
rec('2024ZJA-62', F(sum(1 for a in zh for b in wa if a==b), len(zh)*len(wa)), {'A':F(1,72),'B':F(1,48),'C':F(1,36),'D':F(1,64)}, 'A')
# 2024ZJA-68 开始 S∈[0,60]，时长 D∈[0,60]，S+D>105（分钟，自12:15起）——精确面积
rec('2024ZJA-68', F(15*15,2)/3600, {'A':F(1,16),'B':F(1,32),'C':F(1,48),'D':F(1,64)}, 'B')
# 2025GK-79 7天，两门课各连学2天
tot = good = 0
for a in range(6):
    for b in range(6):
        d = [0]*7; ok = True
        for st in (a,b):
            for t in (st, st+1):
                if d[t]: ok = False
                d[t] = 1
        if not ok: continue
        tot += 1
        free = [i for i in range(7) if d[i]==0]
        good += all(free[i+1]-free[i] > 1 for i in range(len(free)-1))
rec('2025GK-79', F(good,tot), {'A':F(1,7),'B':F(1,8),'C':F(1,9),'D':F(1,10)}, 'D')
dia = [45.5 - 5*i for i in range(10)]  # 1环..10环外圆直径
r6, r7 = dia[5], dia[6]
rec('2025JSA-57', (r6**2 - r7**2)/dia[0]**2, {'A':(None,0.1),'B':(0.1,0.2),'C':(0.2,0.3),'D':(0.3,0.4)}, 'A')
rec('2025SD-59', 4*0.9**3*0.1 + 0.9**4, {'A':0.6597,'B':0.7074,'C':0.9477,'D':0.9963}, 'C')
tot = good = 0
for s in product(range(8), repeat=3):
    if s[0]==s[1] or s[1]==s[2]: continue
    tot += 1; good += len({x//4 for x in s})==1
rec('2025ZJA-64', good/tot, {'A':(0,0.10),'B':(0.10,0.20),'C':(0.20,0.30),'D':(0.30,0.40)}, 'B')
items = ['单杠','双杠','自由','鞍马','吊环','跳马']
ps = list(permutations(items))
g = sum(1 for p in ps if p[0]!='单杠' and p.index('自由') < p.index('双杠'))
rec('2026CQ-63', F(g, len(ps)), {'A':F(5,12),'B':F(1,2),'C':F(7,12),'D':F(2,3)}, 'A')
# 2020SC0725-48 甲20k乙10m，混合6%，总数<100
cands = [(a,b) for a in range(20,100,20) for b in range(10,100,10) if a+b<100 and F(a*5+b*10,(a+b)*100)==F(6,100)]
a, b = cands[0]; bad = b//10
rec('2020SC0725-48', comb(b-bad,3)/comb(b,3), {'A':(None,0.72),'B':(0.72,0.81),'C':(0.81,0.90),'D':(0.90,None)}, 'A')
assert len(cands)==1, cands
# 2020SC0725-53 逐项检验
P = {('甲','乙'):F(7,10),('甲','丙'):F(3,10),('甲','丁'):F(1,2),('乙','丙'):F(1,5),('乙','丁'):F(3,10),('丙','丁'):F(2,3)}
def w(x,y): return P[(x,y)] if (x,y) in P else 1-P[(y,x)]
people = ['甲','乙','丙','丁']
def champ(pairing):
    (a1,b1),(a2,b2) = pairing; out = {}
    for x in people:
        if x in (a1,b1):
            opp = b1 if x==a1 else a1; o1,o2 = a2,b2
        else:
            opp = b2 if x==a2 else a2; o1,o2 = a1,b1
        out[x] = w(x,opp)*(w(o1,o2)*w(x,o1) + w(o2,o1)*w(x,o2))
    return out
pairings = [(('甲','乙'),('丙','丁')), (('甲','丙'),('乙','丁')), (('甲','丁'),('乙','丙'))]
cs = [champ(pp) for pp in pairings]
A_ = any(c['丁'] > c['丙'] for c in cs)
B_ = any(c['乙'] > F(1,10) for c in cs)
C_ = max(range(3), key=lambda i: cs[i]['甲']) == 2
D_ = cs[0]['甲'] > cs[1]['甲']
truth = [k for k,v in zip('ABCD',(A_,B_,C_,D_)) if v]
res['2020SC0725-53'] = (None, truth, 'D')
s = [t for t in combinations(range(1,8),3) if 9 < sum(t) < 15]
rec('2020SZ1-55', F(len(s), comb(7,3)), {'A':F(20,100),'B':F(38,100),'C':F(50,100),'D':F(60,100)}, 'D')
# 2020ZJB-19 12车位(2排x6)，6辆车，逐项精确枚举（甲乙位置 + 每排车数）
spots = [(r,c) for r in range(2) for c in range(6)]
pA = F(2*comb(6,2)*comb(6,4), comb(12,6))
pairs = [(x,y) for x in spots for y in spots if x!=y]
pB = F(sum(1 for x,y in pairs if x[0]==y[0] and abs(x[1]-y[1])>1), len(pairs))
pC = F(sum(1 for x in spots if x[1] in (2,3)), 12)
pD = F(sum(1 for x,y in pairs if x[1] in (0,5) or y[1] in (0,5)), len(pairs))
vals = {'A':pA,'B':pB,'C':pC,'D':pD}
res['2020ZJB-19'] = (vals, [min(vals, key=vals.get)], 'B')
# 2021JSA-56 圆桌8座，4部门各2人相邻，暴力（座位编号固定，旋转视为不同，比例不变）
people8 = ['L','l','W','w','a','A','b','B']  # L/l 李部门, W/w 王部门
dept = {'L':0,'l':0,'W':1,'w':1,'a':2,'A':2,'b':3,'B':3}
tot = good = 0
for p in permutations(people8):
    ok = all(any(dept[p[i]]==dept[p[(i+d)%8]] for d in (1,-1)) for i in range(8))
    if not ok: continue
    # 每部门两人相邻：检查每个部门的两人座位差
    pos = {x:i for i,x in enumerate(p)}
    if not all((pos[u]-pos[v])%8 in (1,7) for u,v in (('L','l'),('W','w'),('a','A'),('b','B'))): continue
    tot += 1; good += (pos['L']-pos['W'])%8 in (1,7)
rec('2021JSA-56', F(good,tot), {'A':F(1,48),'B':F(1,24),'C':F(1,12),'D':F(1,6)}, 'D')
# 2023GK-71
tot = good = 0
for p in permutations('甲乙丙丁戊己'):
    if p[0] in '甲乙' or p[5] in '甲乙': continue
    if p.index('丙') not in (2,3): continue
    tot += 1; good += abs(p.index('丁')-p.index('戊'))==1
rec('2023GK-71', F(good,tot), {'A':F(2,9),'B':F(1,5),'C':F(2,7),'D':F(1,4)}, 'A')
# 2023HB-75 L 形网格（据原卷第19页图）：下部 x0..4,y0..2；右上 x2..4,y2..4；甲(4,4) 乙(0,0) 丙(3,1)
nodes = {(x,y) for x in range(5) for y in range(3)} | {(x,y) for x in range(2,5) for y in range(2,5)}
def npaths(s, t):
    from functools import lru_cache
    @lru_cache(None)
    def f(x,y):
        if (x,y)==t: return 1
        if (x,y) not in nodes: return 0
        r = 0
        if x>t[0] and (x-1,y) in nodes: r += f(x-1,y)
        if y>t[1] and (x,y-1) in nodes: r += f(x,y-1)
        return r
    return f(*s)
totp = npaths((4,4),(0,0)); via = npaths((4,4),(3,1))*npaths((3,1),(0,0))
rec('2023HB-75', F(via,totp), {'A':F(11,15),'B':F(12,53),'C':F(11,36),'D':F(16,53)}, 'D')
# 2024GK-74 先构造各组人数，再算概率
sizes = [s for s in combinations(range(3,37),6) if sum(s)==36 and max(s) <= 3*min(s)]
assert len(sizes)==1, sizes
k = sorted(sizes[0])[-2]
rec('2024GK-74', 1-F(comb(34,k), comb(36,k)), {'A':F(35,100),'B':F(40,100),'C':F(25,100),'D':F(30,100)}, 'B')
# 2025GD-45 3人各从6题抽2题，恰有1题无人抽到
tot = good = 0
allpairs = list(combinations(range(6),2))
for t in product(allpairs, repeat=3):
    tot += 1
    covered = set(t[0])|set(t[1])|set(t[2])
    good += (6-len(covered))==1
rec('2025GD-45', good/tot, {'A':(None,0.20),'B':(0.20,0.25),'C':(0.25,0.30),'D':(0.30,None)}, 'D')
rec('2025HB-71', (8*0.5)/((1+2**0.5+1)**2), {'A':0.25,'B':0.30,'C':0.35,'D':0.40}, 'C')  # 最接近
rec('2025ZJA-65', 1-F(75,100)**2, {'A':F(1,4),'B':F(3,8),'C':F(7,16),'D':F(1,2)}, 'C')
cm = [(a,b,c) for a in range(6) for b in range(4) for c in range(3) if 0 < 300*a+500*b+700*c <= 1600]
rec('2025ZJA-67', F(sum(300*a+500*b+700*c >= 1000 for a,b,c in cm), len(cm)), {'A':F(7,15),'B':F(8,17),'C':F(11,17),'D':F(7,10)}, 'D')
rec('2025ZJA-70', F(4, 2**3), {'A':F(1,8),'B':F(1,4),'C':F(3,8),'D':F(1,2)}, 'D')  # n/2^(n-1)
# 蒙特卡洛复核 2025ZJA-70 与 2020HB-62
import math
random.seed(1)
def same_semi(n):
    a = sorted(random.random()*2*math.pi for _ in range(n))
    gaps = [a[i+1]-a[i] for i in range(n-1)] + [2*math.pi - a[-1] + a[0]]
    return max(gaps) >= math.pi
mc70 = sum(same_semi(4) for _ in range(200000))/200000
mc62 = sum(abs(random.random()-random.random())*30 <= 10 for _ in range(200000))/200000

bad = []
for q,(v,h,off) in res.items():
    flag = ''
    if len(h) != 1: flag = '  <-- 命中选项数≠1'
    elif off and h[0] != off: flag = f'  <-- 与官方答案 {off} 不符'
    if flag: bad.append(q)
    print(f'{q:15s} 计算={v if not isinstance(v,float) else round(v,6)}  命中={h}  官方={off}{flag}')
print('MC 2025ZJA-70 ≈', round(mc70,4), ' MC 2020HB-62 ≈', round(mc62,4))
print('核对题数', len(res), '异常', bad)
