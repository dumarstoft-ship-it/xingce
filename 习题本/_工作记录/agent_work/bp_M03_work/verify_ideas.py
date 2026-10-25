# Independent checks of the suggested data in blueprint ideas (planning-level; final questions are re-verified later).
from fractions import Fraction as F
import itertools, math, datetime
R = []
def chk(key, got, expect, opts=None):
    ok = (got == expect)
    uniq = ''
    if opts is not None:
        hits = [o for o in opts if o == got]
        uniq = f' 选项命中{len(hits)}'
        ok = ok and len(hits) == 1
    R.append((key, ok, f'{got}{uniq}'))

def sim_alternate(total, seq_rates, step=F(1)):
    """seq_rates: list of per-hour rates in order (cycle). returns time to first reach >= total (exact)."""
    level = F(0); t = F(0); i = 0
    while True:
        r = seq_rates[i % len(seq_rates)]
        if r > 0 and level + r*step >= total:
            return t + (total - level)/r
        level += r*step; t += step; i += 1
        if t > 10000: return None

# ---------------- Day 2 ----------------
# 一-巩固: 甲6天乙5天=735, 甲=乙-15/天, 求乙产量
sol = [(a,b) for b in range(1,500) for a in [b-15] if a>0 and 6*a+5*b==735]
chk('D2-一-巩固 乙产量', 5*sol[0][1], 375, [375,345,385,350])
opts_pass_div = [o for o in [375,345,385,350] if o%5==0 and (735-o)%6==0]
chk('D2-一-巩固 整除筛后剩', sorted(opts_pass_div), [345,375])
# 一-深化: 3L+2S=240, 2L+5S=270; 4L + sS, 3天>=1500
L = next(L for L in range(1,200) for S in [ (240-3*L)/2 ] if S==int(S) and 2*L+5*S==270); S=(240-3*L)//2
s = next(s for s in range(0,100) if 3*(4*L+s*S) >= 1500)
chk('D2-一-深化 至少小型台数', (L,S,s), (60,30,9), None)
# 二-巩固: 效率+20% 提前4天, 6000户 -> 原每天
T = next(T for T in range(5,100) if F(T) - F(T)*F(5,6) == 4); chk('D2-二-巩固 原每天户数', 6000//T, 250, [200,250,300,240])
# 三-巩固: 甲30, 合作18 -> 乙45; 9/20开工, 甲先6天, 合作x, 乙y, 10/19完工
D = (datetime.date(2026,10,19)-datetime.date(2026,9,20)).days + 1
xs = [x for x in range(0,D) for y in [D-6-x] if y>=0 and 3*6+5*x+2*y==90]
chk('D2-三-巩固 合作天数', xs, [8])
# 三-深化: 两两 10/12/15, 三队4天后甲撤, 乙丙还需
tot=60; ab,bc,ac = F(tot,10),F(tot,12),F(tot,15); s3=(ab+bc+ac)/2
chk('D2-三-深化 乙丙还需', (tot-4*s3)/bc, 6, [5,6,7,8])
# 三-拓展: 甲20乙30, 甲周日休, 乙周六日休, 周一开工
level=0; day=0
while level<60:
    day+=1; wd=(day-1)%7  # 0=Mon
    if wd!=6: level+=3
    if wd<5: level+=2
chk('D2-三-拓展 完工星期', ['一','二','三','四','五','六','日'][(day-1)%7]+f'(第{day}天)', '一(第15天)')
# 四-巩固: 5z+9l=1, 3(z+l)+9l=1 -> 张单独
# solve: 5z+9l = 3z+12l -> 2z=3l ; z=3,l=2 ; T=33
z,l=3,2; assert 5*z+9*l == 3*(z+l)+9*l
chk('D2-四-巩固 张单独', F(5*z+9*l, z), 11, [10,11,12,F(33,2)])
# 四-深化: 甲=2乙, A=3B, 乙完成B后支援, 又2小时A完成
for t in range(1,50):
    B=1*t; A=3*B; rem=A-2*t
    if rem>0 and F(rem,3)==2: chk('D2-四-深化 甲单独A', F(A,2), 9, [8,9,10,12]); break
# 五-巩固: N: 甲完成时乙剩12丙剩20; 乙完成时丙剩10
Ns=[N for N in range(21,500) if N - F(N*(N-20),(N-12)) == 10]; chk('D2-五-巩固 每车间任务量', Ns, [60])
# 五-深化: 1200m隧道, A半程时B完成40%, 之后A+20% B+50%, A完工时B剩
a0,b0 = F(600),F(480); ra,rb = a0,b0  # per T0
ra2, rb2 = ra*F(6,5), rb*F(3,2); tA = F(600)/ra2
chk('D2-五-深化 B剩余米数', 1200-480-rb2*tA, 120, [120,180,240,320])
# 六-巩固a: 12台5天, 运行t小时后停3台, 剩余恰又用6天 -> t
ts=[t for t in range(1,120) if F(60) - F(12*t,24) == 9*6]; chk('D2-六-巩固a 停机前小时', ts, [12])
# 六-巩固b: 15N, 5天后+20人, 提前2天用完
Ns=[N for N in range(1,1000) if 10*N == 8*(N+20)]; chk('D2-六-巩固b 原有人数', Ns, [80])
# 六-深化: 8大4小 6天, 大=2小; 2天后大-4 小+4
tot=(8*2+4)*6; left=tot-2*(8*2+4); chk('D2-六-深化 还可天数', F(left, 4*2+8), 5, [4,F(9,2),5,6])
# 七-巩固: 27头6天, 23头9天 -> 永远吃不完最多
x=F(27*6-23*9, 6-9); chk('D2-七-巩固 最多头数', x, 15, [12,15,18,21])
# 七-深化: 5台6h, 8台3h, 4h内至少
x=F(5*6-8*3,6-3); Y=(5-x)*6; n=next(n for n in range(1,100) if (n-x)*4>=Y); chk('D2-七-深化 至少台数', n, 7, [5,6,7,8])
# 七-拓展: 10亩12头10天, 15亩20头6天, 24亩8天
p1,p2=F(12*10,10),F(20*6,15); g=(p1-p2)/(10-6); y=p1-g*10
chk('D2-七-拓展 需牛数', 24*(y+g*8)/8, 30, [24,28,30,36])
# 八-巩固: 甲6h满, 乙10h空, 先甲2h再同开
chk('D2-八-巩固 还需小时', (1-F(2,6))/(F(1,6)-F(1,10)), 10, [8,10,12,15])
# 八-深化: 甲9m 乙3m 面积2:1 甲降0.25/h, 7:30起
rise=F(1,4)*2; t=F(6)/(F(1,4)+rise); hh=7*60+30+t*60
chk('D2-八-深化 水深相同时刻', f'{int(hh//60)}:{int(hh%60):02d}', '15:30')
# 八-拓展: 4h满, 半高处漏 1/12 满池/h
chk('D2-八-拓展 注满小时', F(1,2)/F(1,4) + F(1,2)/(F(1,4)-F(1,12)), 5, [F(9,2),5,6,F(13,2)])
# 九-巩固: 合作18天计划; 3天后甲调走, 乙又9天完成一半; 丙=3甲加入, c天后甲回, 提前1天
j,yv = 1,2; tot=18*(j+yv); assert 2*(3*(j+yv)+9*yv) == tot
cs=[]
for c in range(1,10):
    rest = F(tot//2 - c*(yv+3*j), j+yv+3*j)
    if rest>0 and 3+9+c+rest == 17: cs.append(c)
chk('D2-九-巩固 甲返回(丙加入后天数)', cs, [3])
# 九-深化: 合作20天; 4天后乙退出x天(甲继续), 回归再合作10天完工, 推迟3天 -> 甲单独
x = 23-4-10; ja = (1 - F(14,20))/x; chk('D2-九-深化 甲单独', 1/ja, 30, [25,30,36,40])
# 九-拓展: 3:2:4, 甲乙4天, 乙6天, 乙丙4天; 84万按工作量
w=(4*3, (4+6+4)*2, 4*4); chk('D2-九-拓展 丙得(万)', F(84*w[2], sum(w)), 24, [16,21,24,28])
# 十-巩固: 甲12 乙20, 合作3h, 乙修r h, 修后效率降50%, 实际比计划晚1.5h
rs=[r for r in [F(k,2) for k in range(1,12)] if 3 + r + (60-24-5*r)/F(13,2) - F(15,2) == F(3,2)]
chk('D2-十-巩固 维修时长', rs, [2])
# 十-深化: 新工艺效率+25%, 一开始用提前4天; 工作k天后才用, 提前2天
T=next(T for T in range(1,200) if T - F(T*4,5) == 4); ks=[k for k in range(0,T) if (T-k) - F((T-k)*4,5) == 2]
chk('D2-十-深化 第几天后换工艺', ks, [10])
# 十一-巩固: 甲9h 乙12h 轮流 甲先 vs 乙先
ta=sim_alternate(36,[4,3]); tb=sim_alternate(36,[3,4]); chk('D2-十一-巩固 早几分钟', (tb-ta)*60, 5, [0,5,10,15])
# 十一-深化: 甲12h 乙18h, 甲2h乙1h交替
t=sim_alternate(36,[3,3,2]); chk('D2-十一-深化 共需', t, F(40,3))
# 十一-拓展: 甲6h注满 乙9h排空 交替 从甲开始 首次注满
t=sim_alternate(18,[3,-2]); chk('D2-十一-拓展 首次注满', t, 31, [30,31,35,36])

# ---------------- Day 16 ----------------
# 一-深化: 甲10天完成后一半支援乙一半支援丙, 乙15天, 丙18天, 乙比丙多2/天
for a in range(1,200):
    b = F(10*a - 5*F(a,2), 15); c = F(10*a - 8*F(a,2), 18)
    if b - c == 2: chk('D16-一-深化 甲每天', (a,b,c), (12,6,4)); break
# 一-拓展: 加班成本最低(整小时,每人≤4h), 多产>=12000
best=min((300*x+500*y,x,y) for x in range(5) for y in range(5) if 1250*x+2500*y>=12000)
chk('D16-一-拓展 最低加班成本', best[0], 2600)
# 二-深化: 先完成1/3, 后效率+25%, 提前4天
T=next(T for T in range(1,300) if F(2*T,3) - F(2*T,3)*F(4,5) == 4); chk('D16-二-深化 原计划', T, 30, [24,30,36,45])
# 二-拓展: 1200件, 每人多派20少2人; 工资200/人, 超额每件3元
x=next(x for x in range(1,1200) if 1200 % x==0 and 1200%(x+20)==0 and 1200//x - 1200//(x+20) == 2)
n0=1200//x; n1=1200//(x+20); chk('D16-二-拓展 成本变化', n1*200 + n1*20*3 - n0*200, 200)
# 三-巩固: 丙12h, 乙丙6h, 乙单独比甲乙合作多8h -> 甲
yi=F(1,6)-F(1,12); hz = 1/yi - 8; chk('D16-三-巩固 甲单独', 1/(1/hz - yi), 6, [4,6,8,12])
# 三-深化: 甲6天完成1/4, 乙3天完成剩下1/3, 余下合作
ja=F(1,4)/6; yi=F(3,4)*F(1,3)/3; chk('D16-三-深化 还需天数', (F(3,4)*F(2,3))/(ja+yi), 4, [3,4,5,6])
# 四-巩固: 4a+6b=0.4T, 9c=0.3T -> 只有一个选项满足
opts=[(3,2,2),(2,2,1),(4,3,2),(3,3,2)]
chk('D16-四-巩固 满足选项', [o for o in opts if F(4*o[0]+6*o[1], 9*o[2]) == F(4,3)], [(3,2,2)])
# 四-深化: 甲6+乙9 = 乙12+丙12 = 甲9+丙9 = 1
# solve by brute rational search over singles
sol=None
for A in range(2,100):
    for B in range(2,100):
        if F(6,A)+F(9,B)!=1: continue
        Cinv = (1 - F(12,B))/12
        if Cinv<=0: continue
        if F(9,A)+9*Cinv==1: sol=(A,B,1/Cinv)
chk('D16-四-深化 三人合作', 1/(F(1,sol[0])+F(1,sol[1])+1/sol[2]), 6, [5,6,F(36,5),8])
# 五-巩固: 单独6,4,3小时, 分配360
e=[F(1,6),F(1,4),F(1,3)]; chk('D16-五-巩固 乙分到', 360*e[1]/sum(e), 120)
# 五-深化: 20/25/30天, 直播 x2,x3,xk 同时卖完
x=F(25-20,(3-1)-(2-1)); T=20-x*(2-1); k=(30-T)/x+1; chk('D16-五-深化 荔枝倍数', k, 4)
# 六-深化: 2万人30天, 10天后+0.5万人, 每天补给0.5万人用量
chk('D16-六-深化 还能用', F(60-20, F(5,2)-F(1,2)), 20, [16,20,24,25])
# 六-拓展: 4块电池x30分, 3架同时 -> 最长; 构造检验
T=F(4*30,3); slots=4; # 4 slots of 10 min, battery i idle in slot i
use=[[b for b in range(4) if b!=s] for s in range(slots)]
assert all(len(u)==3 for u in use) and all(sum(1 for u in use if b in u)*10==30 for b in range(4))
chk('D16-六-拓展 最长分钟', T, 40, [30,36,40,45])
# 七-巩固: 4窗30分, 6窗15分; 先4窗10分再6窗
x=F(4*30-6*15, 30-15); Y=(4-x)*30; rem=Y-(4-x)*10; chk('D16-七-巩固 共用分钟', 10+rem/(6-x), 20, [18,20,22,25])
# 七-深化: 每天30车6天, 24车9天; 3天后产量+50%, 之后5天内运完, 每天至少
x=F(30*6-24*9, 6-9); Y=(30-x)*6
n=next(n for n in range(1,200) if Y - 3*(n-x) - 5*(n-x*F(3,2)) <= 0); chk('D16-七-深化 至少车数', (x,Y,n), (12,108,30))
# 八-巩固: 甲4h 乙6h 进, 丙3h 排
chk('D16-八-巩固 三管齐开', 1/(F(1,4)+F(1,6)-F(1,3)), 12)
# 八-深化: 甲10m 乙2m 面积3:1 甲降0.2/h, 8:00起, 第二次相差2米
rise=F(1,5)*3; ts=sorted(t for t in [ (8-2)/(F(1,5)+rise), (8+2)/(F(1,5)+rise)])
hh=8*60+ts[1]*60; chk('D16-八-深化 第二次相差2米', f'{int(hh//60)}:{int(hh%60):02d}', '20:30')
# 九-巩固: 计划36天, 12天甲10%乙15%, 乙降至80%, 至少增加几台甲同产能线
tot=240; j=F(tot*10,100)/12; yv=F(tot*15,100)/12; need=F(tot-(j+yv)*12, 24) - j - yv*F(4,5)
chk('D16-九-巩固 至少台数', math.ceil(need/j), 2, [1,2,3,4])
# 九-深化: 合作24天, 甲:乙=2:3, 4天后乙退出x天, 回归带丙(=甲), 按期
xs=[x for x in range(1,20) if 4*5 + 2*x + (24-4-x)*7 == 120]; chk('D16-九-深化 乙退出天数', xs, [8], None)
# 九-拓展: 3/1开工, 甲40乙60, 3/11起甲调走d天, 3/27完工
D=27; ds=[d for d in range(0,20) if 5*D - 3*d == 120]; chk('D16-九-拓展 调走天数', ds, [5])
# 十-巩固: 甲30天(4/天->总120 units*30?) 用比例: 甲=3, 乙=4 (高1/3), 总90; 单支持x2, 双支持x(1+n); 甲乙2天, 三队4天, 最后1天乙休
ns=[n for n in [F(k,10) for k in range(1,30)] if 2*7 + 4*7*(1+n) + 1*3*2 == 90]; chk('D16-十-巩固 双支持提高', ns, [F(3,2)])
# 十-深化: 单台160分钟, 甲共60分钟, 等间隔d
ds=[d for d in range(1,30) if 4*d + 10*d + 18*(60-2*d) == 4*160]; chk('D16-十-深化 间隔', ds, [20])
# 十-拓展: 首日200每天+20, 5600件; 老线320/天
s=0;n=0
while s<5600: n+=1; s+=200+20*(n-1)
chk('D16-十-拓展 新线早几天', math.ceil(5600/320)-n, 2)
# 十一-深化: 甲工3休1, 乙工5休2, 同日开始第21天完工, 乙单独30个工作日 -> 甲单独日历天
def wd(days,w,r): f,rm=divmod(days,w+r); return f*w+min(rm,w)
ja=F(30-wd(21,5,2), wd(21,3,1))  # in units of 乙
need=F(30)/ja; d=0;k=0
while k<need:
    d+=1
    if (d-1)%4<3: k+=1
chk('D16-十一-深化 甲单独日历天', (need,d), (32,42))
# 十一-拓展: 工单池300, 每小时+40, A100/h B70/h 轮流(A先)
level=F(300); t=F(0); i=0
while True:
    r = (100 if i%2==0 else 70) - 40
    if level - r <= 0: t += level/r; break
    level -= r; t += 1; i += 1
chk('D16-十一-拓展 首次清空', t, F(13,2))
# 十二-巩固: 甲8:20 乙8:35 同效率, 甲=1.5乙
t=next(t for t in range(36,200) if (t-20)*2 == 3*(t-35)); chk('D16-十二-巩固 时刻', f'{8+t//60}:{t%60:02d}', '9:05')
# 十二-深化: 1900人; A150/min,1min; B120,2min; C100,1min,延迟2min
n=next(n for n in range(1,30) if 150*max(0,n-1)+120*max(0,n-2)+100*max(0,n-1-2) >= 1900); chk('D16-十二-深化 至少分钟', n, 7, [6,7,8,9])
# 十五-巩固: 甲20 乙30 合作6天后甲离开, 9万按工作量
jw=F(6,20); chk('D16-十五-巩固 乙得(万)', 9*(1-jw), F(63,10))
# 十五-深化: 甲20天1.2万/天, 乙30天0.7万/天, 15天内, 最省
best=None
for fj in [F(k,100) for k in range(0,101)]:
    fy=1-fj
    if fj*20<=15 and fy*30<=15:
        c=fj*20*F(12,10)+fy*30*F(7,10)
        best=c if best is None or c<best else best
chk('D16-十五-深化 最低费用', best, F(45,2))

# ---------------- Day 30 ----------------
# 一-深化: A6分 B4分 系统1.5分, 1/5复核(用时为新办一半), 8小时
A,B=480//6,480//4; sysn=int(480/F(3,2)); review=sysn//5
chk('D30-一-深化 最多办结', sysn + (A+B) - F(review,2), 488, [456,472,488,520])
# 一-拓展: 12a+7b=151, b>a
sols=[(a,b) for a in range(1,13) for b in range(0,30) if 12*a+7*b==151 and b>a]; chk('D30-一-拓展 熟练人数', sols, [(5,13)])
# 二-深化: 任务+20% 效率+50% 少4天
T=next(T for T in range(1,200) if T - F(T*6,5)/F(3,2) == 4); chk('D30-二-深化 原用时', T, 20)
# 二-拓展: 相向开挖 东段5/9, 东比西多2米/天, 西单独比东单独多20天
e=10; w=8; assert F(e,w)==F(5,4) and e-w==2
Ls=[L for L in range(100,3000) if F(L,w)-F(L,e)==20]; chk('D30-二-拓展 隧道长', Ls, [800], None)
# 三-深化: 甲乙2天1/4, 乙丙3天剩余1/2, 甲丙4天完成; 甲占比
ab=F(1,8); bc=F(3,8)/3; ac=F(3,8)/4; ja=(ab+ac-bc)/2; chk('D30-三-深化 甲占比', 6*ja, F(9,32))
# 三-拓展: 20/24/30/40, 至少两队, 12天内
rates=[F(1,20),F(1,24),F(1,30),F(1,40)]
cnt=sum(1 for k in range(2,5) for c in itertools.combinations(rates,k) if 1/sum(c) <= 12); chk('D30-三-拓展 方案数', cnt, 7, [5,6,7,8])
# 四-深化: 甲比合作多9天, 乙比合作多16天
ts=[t for t in range(1,100) if F(1,t+9)+F(1,t+16)==F(1,t)]; chk('D30-四-深化 合作天数', ts, [12])
# 四-拓展: 环形每隔6米, 甲3+乙8 = 合作5, 甲比乙多10棵/天
for b in range(1,200):
    a=b+10
    if 3*a+8*b==5*(a+b): chk('D30-四-拓展 周长', 6*5*(a+b), 1500, [1494,1500,1506,750]); break
# 五-深化: 48个, 手工2/h 机器6/h; 甲先机后手各一半; 乙手t机t; 相等时刻(非起点)
def ja_(t): return 6*t if t<=4 else 24+2*(t-4)
def yi_(t): return 2*t if t<=6 else 12+6*(t-6)
ts=[F(k,10) for k in range(1,121) if ja_(F(k,10))==yi_(F(k,10))]; chk('D30-五-深化 相等时刻', ts, [10])
# 五-拓展: 2:3:5 900个 计划6h, 1h后丙降1/3, 重新分配, 丙转出
r=[30,45,75]; rem_c=75*5; S1=30+45+50; T1=F(900-150,S1); chk('D30-五-拓展 丙转出', rem_c-50*T1, 75, [50,60,75,100])
# 六-深化: 600人30天, 10天后+200, 又5天后-400
left=18000-6000-5*800; total_days=15+F(left,400); chk('D30-六-深化 推迟', total_days-30, 5)
# 七-深化: 20头10天, 15头15天; 20头4天后卖5头
x=F(20*10-15*15,10-15); Y=(20-x)*10; rem=Y-(20-x)*4; chk('D30-七-深化 还能吃', rem/(15-x), 9, [6,8,9,11])
# 七-拓展: 4闸30h, 6闸18h; 开7闸6h后来水x3
x=F(4*30-6*18,30-18); Y=(4-x)*30; rem=Y-(7-x)*6; chk('D30-七-拓展 还需小时', rem/(7-3*x), F(27,2))
# 八-深化: 甲4h进 乙6h进 丙3h排, 甲乙丙各1h轮流
chk('D30-八-深化 首次注满', sim_alternate(12,[3,2,-4]), 23)
# 八-拓展: A 20m2x2m, B 30m2x2m, 进水10/h, B排水4/h(有水时)
chk('D30-八-拓展 两池都满', F(40,10)+F(60,10-4), 14, [10,14,16,F(50,3)])
# 九-深化: 计划20天 3:2:1, 推迟2天, 甲乙都请假
sols=[(a,b) for a in range(1,23) for b in range(1,23) if 3*(22-a)+2*(22-b)+22==120]; chk('D30-九-深化 甲请假', sols, [(2,3)])
# 十-深化: 150台, y快充x1.5, 余x1.2; 快充>=46%, 升级>=80%; 最大提高
ys=[y for y in range(0,151) if F(3,2)*y>=F(46,100)*150 and F(6,5)*(150-y)>=F(80,100)*150]
best=max((F(3,2)*y+F(6,5)*(150-y))/150-1 for y in ys); chk('D30-十-深化 最大提高', (ys[0],ys[-1],best), (46,50,F(3,10)))
# 十-拓展: n台每台(110-10n)/h, 1500件最少
best=min(F(1500, n*(110-10*n)) for n in range(1,11)); chk('D30-十-拓展 最少小时', best, 5)
# 十一-深化: 白班8-20 1.5m/h, 夜班1m/h, 周一8:00开工, 100m
t=F(0); d=F(0)
while d<100:
    h=(8+t)%24; rate=F(3,2) if 8<=h<20 else 1
    step=F(1,60)
    if d+rate*step>=100: t+= (100-d)/rate; d=100; break
    d+=rate*step; t+=step
end=8+t; day=int(end//24); hh=end-24*day
chk('D30-十一-深化 完工', (['周一','周二','周三','周四','周五'][day], int(hh), int((hh-int(hh))*60)), ('周四',14,40))
# 十一-拓展: 甲6 乙8 丙12, 三队轮流各1h, 最早完工
best=min(sim_alternate(24,[ {'甲':4,'乙':3,'丙':2}[p] for p in perm]) for perm in itertools.permutations('甲乙丙'))
chk('D30-十一-拓展 最早', best, F(23,3))
# 十二-深化: 同效率, 甲60件时乙a件; 乙60件时甲=2a; 乙8:30开工 30件/h; 合计300时刻
a=next(a for a in range(1,60) if 60+(60-a)==2*a); d=60-a; t=F(300-d, 60)
mins=8*60+30+t*60; chk('D30-十二-深化 时刻', f'{int(mins//60)}:{int(mins%60):02d}', '13:10')
# 十二-拓展: 880人, 前门120/min 150m, 侧门80/min 75m, 步行75m/min
n=next(n for n in range(1,30) if 120*max(0,n-2)+80*max(0,n-1) >= 880); chk('D30-十二-拓展 至少分钟', n, 6)
# 十三-深化: A: 甲10乙15, B: 甲12乙9; 最短 (LP 枚举)
best=None
for a in [F(k,1000) for k in range(0,1001)]:
    for b in [F(0), F(1,100)]:
        T=max(10*a+12*b, 15*(1-a)+9*(1-b))
        best=T if best is None or T<best else best
chk('D30-十三-深化 最短天数', best, F(48,5))
# 十三-拓展: 三工程各180, 6:5:4, 丁3, 同时完工
T=F(540,18); chk('D30-十三-拓展 丁帮C天数', (180-4*T)/3, 20)
# 十四-巩固: 6(m+1)=5(0.8m+n)
for nn in [2,3,4]:
    m=(F(5)*nn-6)/2  # from 6m+6=4m+5n
    assert 6*(m+1)==5*(F(4,5)*m+nn) and m==F(5,2)*nn-3
chk('D30-十四-巩固 关系', 'm=2.5n-3', 'm=2.5n-3')
# 十四-深化: 订单甲6n 乙n, 合作x, 分开y(乙完成), 合作z=2x
for n_ in [6,12,30]:
    y=n_; x=F(6*n_-y, 6); assert 2*x+y+2*(2*x)==6*n_
chk('D30-十四-深化 关系', F(x,y), F(5,6))
# 十五-巩固: 合作10天, 甲6万 乙4万
chk('D30-十五-巩固 乙单独', F(10,F(4,10)), 25)
# 十五-深化: 甲20/2万 乙30/1.5万 丙60/0.6万, 12天内
best=None
for f1 in [F(k,100) for k in range(0,61)]:
    for f3 in [F(k,100) for k in range(0,21)]:
        f2=1-f1-f3
        if f2<0 or f2*30>12: continue
        c=f1*20*2+f2*30*F(3,2)+f3*60*F(6,10)
        best=c if best is None or c<best else best
chk('D30-十五-深化 最低费用', best, F(201,5))
# 十五-拓展: 合同30天, 提前奖1万/天, 推迟罚2万/天; 甲40天0.5万/天, 乙60天0.3万/天
def net(days, cost): return cost + (2*(days-30) if days>30 else -(30-days))
plans={'合作': net(24, 24*F(8,10)), '甲单独': net(40, 40*F(1,2)), '乙单独': net(60, 60*F(3,10)), '合作15天后乙退出': net(30, 30*F(1,2)+15*F(3,10))}
chk('D30-十五-拓展 最优方案', min(plans,key=plans.get)+f'={plans["合作"]}', '合作=66/5')


# ---- distractor sanity + backup ideas ----
cont = min(300*x/10+500*y/10 for x in range(0,41) for y in range(0,41) if 1250*x/10+2500*y/10>=12000)
chk('D16-一-拓展 连续时长陷阱值', cont, 2480)
chk('D30-十五-深化 干扰39.2(甲超期)', F(12,60)*60*F(6,10) + F(8,10)*20*2, F(196,5))
chk('D30-十五-深化 干扰42(漏丙)', F(6,10)*20*2 + F(4,10)*30*F(3,2), 42)
# backup for 2020SZS-29: 一侧两端都种, 每隔8米; 3a+4(a+b)=10b+2a, a-b=5
for b in range(1,100):
    a=b+5
    if 3*a+4*(a+b)==10*b+2*a:
        chk('备用-2020SZS-29 路长', 8*(10*b+2*a-1), 2472); break
# backup for 2022SC1-46
ac=F(1,4)/3; bc=F(3,4)*F(4,10)/3; ab=(1-F(1,4)-F(3,4)*F(4,10))/3; S=(ab+bc+ac)/2
chk('备用-2022SC1-46 乙占比', 6*(S-ac), F(1,2))
chk('备用-2022SC1-46 三者效率为正', all(v>0 for v in (S-bc, S-ac, S-ab)), True)

bad=[r for r in R if not r[1]]
for k,ok,info in R: print(('OK ' if ok else 'XX ')+k+' -> '+info)
print(f'\n共 {len(R)} 项检查，未通过 {len(bad)} 项')
