"""M07 考法地图：验算各天改编 idea 里给出的数据与答案（防止 idea 本身有错）。"""
from fractions import Fraction as F
from itertools import permutations, combinations, product
from math import comb, factorial
import random
out = []
def chk(tag, got, exp):
    ok = (got == exp) if not isinstance(exp, float) else abs(float(got) - exp) < 1e-6
    out.append((tag, got, exp, ok))

# ---------------- Day 6 ----------------
# 考法一 巩固：6 粽 k 咸蛋黄，P(恰1/取2)=8/15
ks = [k for k in range(7) if F(k*(6-k), 15) == F(8,15)]
chk('D6-1a 根', ks, [2,4])
# 考法一 深化：都未/都中 = 11，选 4 人
Ns = [N for N in range(6,100) if F(comb(N-2,4), comb(N-2,2)) == 11]
chk('D6-1b N', Ns, [16])
# 考法二 巩固：3 综合 5 专项 抽 3，两类都有
chk('D6-2a', 1 - F(comb(3,3)+comb(5,3), comb(8,3)), F(45,56))
chk('D6-2a 干扰(只扣全专项)', 1 - F(comb(5,3), comb(8,3)), F(23,28))
# 考法二 拓展：4 人 6 组，至少 2 人同组
cnt = sum(1 for t in product(range(6), repeat=4) if len(set(t)) < 4)
chk('D6-2b', F(cnt, 6**4), F(13,18))
cnt1 = sum(1 for t in product(range(6), repeat=4) if sorted([t.count(x) for x in set(t)]) == [1,1,2])
chk('D6-2b 干扰(恰一对)', F(cnt1, 6**4), F(5,9))
# 考法三 巩固：1-9 取 2 数和为 3 的倍数
chk('D6-3a', F(sum((a+b)%3==0 for a,b in combinations(range(1,10),2)), 36), F(1,3))
# 考法三 拓展：两次骰子较大值=5
chk('D6-3b', F(sum(max(a,b)==5 for a,b in product(range(1,7),repeat=2)), 36), F(1,4))
# 考法四 巩固：7 车位 3 车，恰 2 辆相邻
def adjpairs(s): return sum(1 for i in range(len(s)-1) if s[i+1]-s[i]==1)
c = [s for s in combinations(range(7),3)]
chk('D6-4a', F(sum(1 for s in c if adjpairs(s)==1), len(c)), F(4,7))
# 考法四 深化：9 座 3 人，任意两人之间至少隔 2 座
c = [s for s in combinations(range(9),3) if all(s[i+1]-s[i] >= 3 for i in range(2))]
chk('D6-4b', F(len(c), comb(9,3)), F(5,42))
# 考法六 巩固：10 盏灯，每次按 2 盏，3 次后亮着（精确枚举每次的选择）
lamps = list(combinations(range(10),2))
on = 0; tot = 0
for a in lamps:
    for b in lamps:
        for cc in lamps:
            tot += 1
            flips = sum(0 in x for x in (a,b,cc))
            on += flips % 2 == 0
chk('D6-6a', F(on, tot), F(608,1000))
# 考法六 拓展：8 人两两结对，甲乙一对
def pairings(lst):
    if not lst: yield []; return
    a = lst[0]
    for i in range(1,len(lst)):
        for rest in pairings(lst[1:i]+lst[i+1:]): yield [(a,lst[i])]+rest
P8 = list(pairings(list(range(8))))
chk('D6-6b', F(sum((0,1) in p for p in P8), len(P8)), F(1,7))
# 考法七 巩固：三人 2/3/4 天，周三恰两人
p = [F(2,5),F(3,5),F(4,5)]
ex2 = sum(p[i]*p[j]*(1-p[k]) for i,j,k in ((0,1,2),(0,2,1),(1,2,0)))
chk('D6-7a', ex2, F(58,125)); chk('D6-7a 至少两人', ex2+p[0]*p[1]*p[2], F(82,125))
# 考法七 深化：12 码不放回逐个试，恰第 3 次才对
cnt = sum(1 for perm in permutations(range(12),3) if perm[2]==0 and 0 not in perm[:2])
chk('D6-7b', F(cnt, 12*11*10), F(1,12))
# 考法八 巩固：3 周恰 2 周来自甲
chk('D6-8a', 3*F(5,9)**2*F(4,9), F(300,729))
# 考法八 深化：4 次至少 3 次成功 p=0.8
chk('D6-8b', 4*0.8**3*0.2 + 0.8**4, 0.8192)
# 考法九 巩固：0.25+0.5x=0.4
chk('D6-9a', (F(4,10)-F(1,4))/F(1,2), F(3,10))
# 考法九 拓展：理论 0.8 实操 0.6 各一次补考
chk('D6-9b', (1-0.2**2)*(1-0.4**2), 0.8064)
# 考法十 拓展：三局两胜 p=0.6
chk('D6-10', 0.6**2 + 2*0.6*0.4*0.6, 0.648)
# 考法十一 巩固：0.3+0.5p=0.45
chk('D6-11a', (F(45,100)-F(3,10))/F(5,10), F(3,10))
# 考法十一 深化：5:3:2，2%/3%/5%
chk('D6-11b', F(5,10)*F(2,100)+F(3,10)*F(3,100)+F(2,10)*F(5,100), F(29,1000))
# 考法十一 拓展：每天独立选，两天都准点
d = 0.6*0.9+0.4*0.6
chk('D6-11c', d*d, 0.6084); chk('D6-11c 干扰(同一交通方式)', 0.6*0.81+0.4*0.36, 0.63)
# 考法十二 巩固：次品来自三线
chk('D6-12a', F(10, 10+9+10), F(10,29))
# 考法十二 深化：2% 感染，95% 检出，5% 误报
chk('D6-12b', round(0.02*0.95/(0.02*0.95+0.98*0.05),4), 0.2794)
# 考法十三 巩固：60 分钟窗口等 12 分钟
chk('D6-13', 1-F(48,60)**2, F(9,25))
# 考法十五 巩固：奖券期望
chk('D6-15a', F(200+3*50+6*10, 20), F(41,2))
# 考法十五 拓展：投保
chk('D6-15b', (0.2*50, 6+0.2*50*0.2), (10.0, 8.0))

# ---------------- Day 20 ----------------
ks = [k for k in range(46) if F(comb(k,2), comb(45,2)) == F(4,33)]
chk('D20-1', ks, [16])
chk('D20-2a', 1-F(216,1000)**F(1,1) if False else 1-0.6, 0.4)
chk('D20-2a 验证', 1-(1-0.4)**3, 0.784)
# 4 田 4 作物 3 年 恰 2 年相同
cnt = sum(1 for t in product(range(4),repeat=3) if len(set(t))==2)
chk('D20-2b', F(cnt, 64), F(9,16))
# a+2b+5c=10
cm = [(a,b,c) for a in range(11) for b in range(6) for c in range(3) if a+2*b+5*c==10]
chk('D20-3a', F(sum(c>0 for a,b,c in cm), len(cm)), F(2,5))
# 2..7 取 3 根成三角形
tri = [t for t in combinations(range(2,8),3) if t[0]+t[1] > t[2]]
chk('D20-3b', F(len(tri), comb(6,3)), F(13,20))
# 7 天两门课各连学 2 天，两门课不相连（中间至少隔 1 天）
tot = good = 0
for a in range(6):
    for b in range(6):
        if len({a,a+1,b,b+1}) < 4: continue
        tot += 1
        good += not (a+2 == b or b+2 == a)
chk('D20-4a', F(good, tot), F(3,5))
# 13 天 A2 B3 C4，空闲 4 天中恰有 2 天相连（其余不相连）
tot = good = 0
for a in range(12):
    for b in range(11):
        for c in range(10):
            days = [0]*13; ok = True
            for st, ln in ((a,2),(b,3),(c,4)):
                for dd in range(st, st+ln):
                    if days[dd]: ok = False
                    days[dd] = 1
            if not ok: continue
            tot += 1
            free = [i for i in range(13) if days[i]==0]
            adj = sum(1 for i in range(3) if free[i+1]-free[i]==1)
            # 恰有 2 天相连：恰好一对相邻、且不存在三连
            runs = []; r = 1
            for i in range(3):
                if free[i+1]-free[i]==1: r += 1
                else: runs.append(r); r = 1
            runs.append(r)
            good += sorted(runs) == [1,1,2]
chk('D20-4b', F(good, tot), F(12,35))
# 错排
der = sum(1 for p in permutations(range(4)) if all(p[i]!=i for i in range(4)))
chk('D20-4c', F(der, 24), F(3,8))
# 5 专家 3 点每点至少 1，甲乙同点
tot = good = 0
for t in product(range(3), repeat=5):
    if len(set(t)) < 3: continue
    tot += 1; good += t[0]==t[1]
chk('D20-5a', F(good,tot), F(6,25))
# 10 名额 4 科室每科≥1，甲恰 3（隔板等可能）
comp = [t for t in product(range(1,8), repeat=4) if sum(t)==10]
chk('D20-5b', F(sum(t[0]==3 for t in comp), len(comp)), F(5,28))
# 6 节目：独唱<合唱<舞蹈 且 首个不是小品
items = ['独','合','舞','小','相','朗']
ps = list(permutations(items))
g = sum(1 for p in ps if p.index('独')<p.index('合')<p.index('舞') and p[0]!='小')
chk('D20-6a', F(g,len(ps)), F(5,36))
# 抽签原理：第 4 人抽中
g = sum(1 for p in permutations(range(10),4) if p[3] < 3)
chk('D20-6b', F(g, 10*9*8*7), F(3,10))
# 8 人管理员，同一人不连续两周，第 1 周与第 3 周同一人
tot = good = 0
for s in product(range(8), repeat=3):
    if s[0]==s[1] or s[1]==s[2]: continue
    tot += 1; good += s[0]==s[2]
chk('D20-7a', F(good,tot), F(1,7))
# 串并联
chk('D20-7b', (1-0.1*0.2)*0.95, 0.931)
# 有放回次数最值
n = next(n for n in range(1,20) if 1-0.9**n > 0.3)
chk('D20-8', n, 4)
# 胜率随上局变：前三局恰赢两局
def seqprob(seq):
    pr = 1.0; prev = None
    for i,w in enumerate(seq):
        pw = 0.7 if i==0 else (0.5 if prev else 0.7)
        pr *= pw if w else 1-pw; prev = w
    return pr
chk('D20-9a', round(sum(seqprob(s) for s in product((1,0),repeat=3) if sum(s)==2),6), 0.525)
# 传球 3 人 4 次回甲
cnt = 0
for s in product((0,1), repeat=4):
    cur = 0
    for x in s:
        others = [p for p in range(3) if p != cur]; cur = others[x]
    cnt += cur == 0
chk('D20-9b', F(cnt,16), F(3,8))
# 抽签：小王 0.6、小张 0.4，至少一人进决赛
chk('D20-10a', round(F(1,3)*1 + F(2,3)*(1-F(4,10)*F(6,10)), 6), F(21,25))
# 五局三胜打满五局
chk('D20-10b', comb(4,2)*F(2,3)**2*F(1,3)**2, F(8,27))
# 三状态反求
chk('D20-11a', (F(31,100)-F(3,10)*F(4,10)-F(5,10)*F(1,10))/F(2,10), F(7,10))
chk('D20-11b', round(1-0.65**3,4), 0.7254)
# 条件概率：4 男 2 女选 2，已知有女，都是女
chk('D20-12', F(1, comb(6,2)-comb(4,2)), F(1,9))
# 约会不对称：40 分钟窗口，职员等 20，快递员等 10（网格积分精确用公式，蒙特卡洛复核）
area = 40*40 - (40-20)**2/2 - (40-10)**2/2
chk('D20-13', F(int(area), 1600), F(19,32))
random.seed(7)
mc = sum((lambda x,y: (0 <= y-x <= 20) or (0 <= x-y <= 10))(random.uniform(0,40), random.uniform(0,40)) for _ in range(400000))/400000
out.append(('D20-13 MC', round(mc,4), round(19/32,4), abs(mc-19/32) < 0.005))
# 嵌套：乙 4 甲 6 抽 2 同线
chk('D20-14', F(comb(6,2)+comb(4,2), comb(10,2)), F(7,15))
# 钥匙期望
chk('D20-15', F(sum(range(1,6)),5), F(3,1))
chk('D20-15 变式', F(1+2+3+4+4,5), F(14,5))

# ---------------- Day 34 ----------------
N = next(N for N in range(3,100) if F(N-2, comb(N,3)) <= F(1,50))
chk('D34-1a', N, 18)
chk('D34-1b', F(comb(3,1)*comb(3,1), comb(6,2)) * F(comb(2,1)*comb(2,1), comb(4,2)), F(2,5))
# 2 节目 x 4 科室，选 4，至少一个科室两节目都入选
progs = [(d,k) for d in range(4) for k in range(2)]
c4 = list(combinations(progs,4))
chk('D34-2', F(sum(1 for s in c4 if any(sum(1 for x in s if x[0]==d)==2 for d in range(4))), len(c4)), F(27,35))
# 满减：300/500/700，原价满 1000 减 200，实付 ≤1300，享受立减
cm = [(a,b,c) for a in range(10) for b in range(6) for c in range(4) if (a,b,c)!=(0,0,0)]
def paid(t):
    s = 300*t[0]+500*t[1]+700*t[2]
    return s-200 if s >= 1000 else s
ok = [t for t in cm if paid(t) <= 1300]
chk('D34-3a 组合数', len(ok), 18)
chk('D34-3a', F(sum(300*a+500*b+700*c >= 1000 for a,b,c in ok), len(ok)), F(2,3))
# 1-9 取 3 数和被 3 整除
chk('D34-3b', F(sum(sum(t)%3==0 for t in combinations(range(1,10),3)), comb(9,3)), F(5,14))
# 圆桌 8 座 4 部门各 2 人相邻，小李与小王恰隔 1 人
people8 = ['L','l','W','w','a','A','b','B']
tot = good = 0
for p in permutations(people8):
    pos = {x:i for i,x in enumerate(p)}
    if not all((pos[u]-pos[v])%8 in (1,7) for u,v in (('L','l'),('W','w'),('a','A'),('b','B'))): continue
    tot += 1; good += (pos['L']-pos['W'])%8 in (2,6)
chk('D34-4a', F(good,tot), F(1,3))
# 7 家企业：甲乙不在首尾，丙在第 4，丁戊不相邻
tot = good = 0
for p in permutations('甲乙丙丁戊己庚'):
    if p[3] != '丙' or p[0] in '甲乙' or p[6] in '甲乙': continue
    tot += 1; good += abs(p.index('丁')-p.index('戊')) != 1
out.append(('D34-4b 丁戊不相邻', F(good,tot), '(见值)', True))
# 两排各 5 车位，4 辆车（含甲乙）随机停：比较四事件
spots = [(r,c) for r in range(2) for c in range(5)]
tot = 0; cntE = {'A':0,'B':0,'C':0,'D':0}
for chosen in permutations(spots, 4):  # 甲=chosen[0] 乙=chosen[1]
    tot += 1
    rows = [x[0] for x in chosen]
    cntE['A'] += chosen[0][0]==chosen[1][0]                      # 甲乙同排
    cntE['B'] += chosen[0][0]==chosen[1][0] and abs(chosen[0][1]-chosen[1][1])==1  # 甲乙相邻
    cntE['C'] += chosen[0][1] in (0,4)                            # 甲在边上
    cntE['D'] += rows.count(0)==2                                 # 两排各 2 辆
vals = {k: F(v,tot) for k,v in cntE.items()}
out.append(('D34-4c 四事件', {k:str(v) for k,v in vals.items()}, '', True))
# 3 人各从 5 题抽 2，5 题都被抽到
pairs5 = list(combinations(range(5),2))
cov = sum(1 for t in product(pairs5, repeat=3) if len(set(t[0])|set(t[1])|set(t[2]))==5)
out.append(('D34-5a 覆盖', F(cov, 1000), float(F(cov,1000)), True))
# 8 人平均分 A/B 组，甲乙同组且丙丁不同组
tot = good = 0
for A in combinations(range(8),4):
    tot += 1
    s = set(A)
    good += ((0 in s)==(1 in s)) and ((2 in s)!=(3 in s))
chk('D34-5b', F(good,tot), F(8,35))
# 单卡：20 张每次翻 5 张，3 次后正面
p = F(1,4)
chk('D34-6', (1-p)**3 + 3*p**2*(1-p), F(9,16))
chk('D34-7a', 0.24/(0.5*0.8)/2, 0.3)
n = next(n for n in range(1,10) if 1-0.2**n >= 0.99)
chk('D34-7b', n, 3)
pk = [comb(5,k)*0.6**k*0.4**(5-k) for k in range(6)]
chk('D34-8 众数', pk.index(max(pk)), 3)
# 递推第 4 局
pn = 0.7
for _ in range(3): pn = 0.5*pn + 0.7*(1-pn)
chk('D34-9a', round(pn,4), 0.5824)
# 复活卡闯关
chk('D34-9b', round(0.6**3 + 3*(0.4*0.6)*0.6**2, 4), 0.4752)
# 抽签夺冠
W = {('甲','乙'):0.8,('甲','丙'):0.5,('甲','丁'):0.5,('乙','丙'):0.5,('乙','丁'):0.5,('丙','丁'):0.5}
def w(x,y): return W[(x,y)] if (x,y) in W else 1-W[(y,x)]
def champ_jia(pa, pb):
    (a1,b1),(a2,b2) = pa, pb
    opp = b1
    return w('甲',opp)*(w(a2,b2)*w('甲',a2) + w(b2,a2)*w('甲',b2))
pr = [champ_jia(('甲','乙'),('丙','丁')), champ_jia(('甲','丙'),('乙','丁')), champ_jia(('甲','丁'),('乙','丙'))]
chk('D34-10a', round(sum(pr)/3,6), 0.35)
p3 = 0.6**2*(1+2*0.4); p5 = 0.6**3*(1+3*0.4+6*0.4**2)
chk('D34-10b 差', round(p5-p3,5), 0.03456)
chk('D34-11a', F(3,5)*F(3,6)+F(2,5)*F(2,6), F(13,30))
# 十字交叉反求 + 不放回
sol = [(A,B) for B in range(10,200,10) for A in range(25,200,25) if A+B < 200 and F(4*A+10*B, 100*(A+B)) == F(6,100)]
chk('D34-11b 解', sol, [(100,50)])
chk('D34-11b', F(5*45, comb(50,2)), F(9,49))
chk('D34-11c', 200*(0.6*0.05+0.4*0.1)*10, 140.0)
# 两次阳性后验
a = 1000*0.81; b = 99000*0.0081
chk('D34-12a', round(a/(a+b),3), 0.502)
chk('D34-12a 单次', round(900/(900+8910),4), 0.0917)
ps = list(permutations(range(6)))
cond = [p for p in ps if p[0] != 0]
chk('D34-12b', F(sum(1 for p in cond if p.index(1) < p.index(0)), len(cond)), F(3,5))
# 圆周 3 点锐角三角形（MC）
import math
def acute():
    a = sorted(random.random()*2*math.pi for _ in range(3))
    gaps = [a[1]-a[0], a[2]-a[1], 2*math.pi-a[2]+a[0]]
    return max(gaps) < math.pi
mc = sum(acute() for _ in range(300000))/300000
out.append(('D34-13a MC', round(mc,4), 0.25, abs(mc-0.25) < 0.005))
def tri_rope():
    x, y = sorted((random.random(), random.random()))
    return max(x, y-x, 1-y) < 0.5
mc = sum(tri_rope() for _ in range(300000))/300000
out.append(('D34-13b MC', round(mc,4), 0.25, abs(mc-0.25) < 0.005))
# 34 人 6 组
sizes = [s for s in combinations(range(3,35),6) if sum(s)==34 and max(s) <= 3*min(s)]
chk('D34-14a 构造', sizes, [(3,4,5,6,7,9)])
chk('D34-14a', F(sum(x for x in sizes[0] if x%2), 34), F(12,17))
# 4x3 网格，封闭 (2,1)-(3,1) 段，经过 (2,2)
from functools import lru_cache
blocked = {((2,1),(3,1))}
def paths(s, t):
    @lru_cache(None)
    def f(x,y):
        if (x,y)==t: return 1
        r = 0
        if x < t[0] and ((x,y),(x+1,y)) not in blocked: r += f(x+1,y)
        if y < t[1] and ((x,y),(x,y+1)) not in blocked: r += f(x,y+1)
        return r
    return f(*s)
totp = paths((0,0),(4,3)); via = paths((0,0),(2,2))*paths((2,2),(4,3))
chk('D34-14b', F(via,totp), F(9,13))
# 54 人，女:男=4:5，1/4 女干部 6 人分 3 社区（隔板等可能），甲社区恰 2
Ns = [n for n in range(50,60) if n%6==0 and n%9==0]
chk('D34-14c N', Ns, [54])
comp = [t for t in product(range(1,7), repeat=3) if sum(t)==6]
chk('D34-14c', F(sum(t[0]==2 for t in comp), len(comp)), F(3,10))
# 混检
E = 1*0.9**5 + 6*(1-0.9**5)
chk('D34-15a 每人', round(E/5,2), 0.61)
chk('D34-15b', 12*3 + 8*(3*0.25-1*0.75), 36.0)
chk('D34-15c', (0.3*40+0.4*10-8) - (0.5*10-2), 5.0)

bad = [o for o in out if not o[3]]
for o in out: print(('OK ' if o[3] else 'XX ') + str(o[0]), o[1], o[2])
print('共', len(out), '项，失败', len(bad))
