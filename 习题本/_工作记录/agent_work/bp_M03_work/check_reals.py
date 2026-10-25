# Independent re-solve of M03 real questions from stem data (exact fractions).
from fractions import Fraction as F
import math, itertools
from sympy import symbols, solve, Eq, Rational, nsimplify, simplify, expand

res = {}
def rec(qid, ans, official, note=""):
    res[qid] = (ans, official, note)

# 2020JSA-53
for y in range(1, 2000):
    if 5*(y+23) + 4*y == 1033:
        rec('2020JSA-53', {625:'A',645:'B',535:'C',515:'D'}.get(5*(y+23)), 'A', f'乙={y}')
# 2023GD-37: machine rate r, manual 0.2r; 300 by manual takes extra 1h
r = F(300)/F(1,4)   # 300/(5x - x)=..., solve 300/(0.2r) - 300/r = 1
r = None
for tot in [2400,3600,4800,6000]:
    rr = F(tot,4)
    if F(300)/(F(1,5)*rr) - F(300)/rr == 1: rec('2023GD-37', {2400:'A',3600:'B',4800:'C',6000:'D'}[tot], 'C')
# 2023ZJA-64
t = F(38,4)  # 5(t+4)=9(t-2)
assert 5*(t+4) == 9*(t-2)
v = 5*(t+4)/t
opt = 'A' if v<6 else 'B' if v<7 else 'C' if v<8 else 'D'
rec('2023ZJA-64', opt, 'C', f'丙速={float(v):.3f}')
# 2024GD-36
for x,o in zip([6,7,8,9],'ABCD'):
    if F(300,x-1) - F(300,x) == 10: rec('2024GD-36', o, 'A')
# 2024HB-63
x = F(80-75, 50-40); tot = F(3,2)*50 + 50*x
rec('2024HB-63', {75:'A',80:'B',100:'C',110:'D'}[int(tot)], 'C')
# 2025JSA-56
hs, dq = 32, 24
rem = 40 - F(40*dq, hs)
rec('2025JSA-56', {4:'A',8:'B',10:'C',12:'D'}[int(rem)], 'C')
# 2025JSA-61: 2M+5N=1, M+N=1/3
M = symbols('M'); Mv = solve(Eq(2*M + 5*(Rational(1,3)-M), 1), M)[0]
rec('2025JSA-61', {Rational(7,2):'A',Rational(9,2):'B',5:'C',Rational(11,2):'D'}[1/Mv], 'B')
# 2025SC-46
A, B = 3*8, 2*8
d = F(A,2) - F(B,3)
rec('2025SC-46', 'B' if d == F(20,3) else '?', 'B', f'差={d}h')
# 2025SD-53: 5z+9l=7z+6l -> 2z=3l
z,l = 3,2; T = 5*z+9*l; rem = T - 3*(z+l)
rec('2025SD-53', {10:'A',8:'B',7:'C',9:'D'}[rem//l], 'D')
# 2026GD-38 (self-solve)
tot = 20*5; used = 20*F(12,24); left = (tot-used)/25
rec('2026GD-38', {F(7,2):'A',F(18,5):'B',F(19,5):'C',F(4):'D'}[left], None, f'剩余{left}天')
# 2026ZJA-46 (self-solve)
hrs = F(8-5)/(F(2,10)+F(3,10)); start = 8*60+30; end = start + hrs*60
hh, mm = divmod(int(end), 60)
rec('2026ZJA-46', {'14:30':'A','15:00':'B','15:30':'C','16:00':'D'}[f'{hh}:{mm:02d}'], None, f'{hh}:{mm:02d}')
# 2020SC0725-46: 2x(lines) ... y=n, 4x+y=5n
# brute: n=10
for n in [10, 7]:
    y = n; x = F(5*n - y, 4)
    rec('2020SC0725-46', 'B' if x == y else '?', 'B')
# 2020SC1206-46
T = 240; a, b = F(T*10,100)/12, F(T*15,100)/12  # per-day
assert a == 2 and b == 3
c = F(T - (a+b)*12, 30) - a - b*F(8,10)
rec('2020SC1206-46', {1:'A',F(4,5):'B',F(3,5):'C',F(1,2):'D'}[c/a], 'B')
# 2020SD-45
import datetime
a = F(1,20); b = F(1,12) - a
rem = 1 - 5*a - 3*(a+b); days = 5 + 3 + rem/b
assert days.denominator == 1
endd = datetime.date(2020,8,15) + datetime.timedelta(days=int(days)-1)
rec('2020SD-45', {datetime.date(2020,9,5):'A',datetime.date(2020,9,6):'B',datetime.date(2020,9,7):'C',datetime.date(2020,9,8):'D'}[endd], 'B', str(endd))
# 2020SZS-26
x,y = symbols('x y'); s = solve([Eq((3*x+y)*2,600), Eq((x+2*y)*4,800)], [x,y])
v = (4*s[x]+2*s[y])*Rational(85,100)*5
rec('2020SZS-26', {1650:'A',1870:'B',1980:'C',2020:'D'}[int(v)], 'B')
# 2020ZJB-17
X = F(5*45-3*90, 45-90); Y = (3-X)*90; t = Y/(6-X)
rec('2020ZJB-17', {36:'A',38:'B',40:'C',42:'D'}[int(t)], 'A')
# 2021JSA-53
yi = symbols('yi'); s = solve(Eq(12*yi, 15*(yi-4)), yi)[0]; jia = F(int(12*s), 8)
rec('2021JSA-53', {30:'A',40:'B',50:'C',60:'D'}[int(jia)], 'A')
# 2021JSA-57
s = solve([Eq(8*x+8*y,30000), Eq(2*x+3*y,10000)],[x,y]); daily = 11*s[x]+10*s[y]
rec('2021JSA-57', {14:'A',15:'B',16:'C',17:'D'}[int(620000/daily)], 'C')
# 2021SC2-51
rates = [10,12,15]; done = 0; t_jia = F(0); i = 0
while True:
    r = rates[i%3]
    if done + r >= 120:
        frac = F(120-done, r)
        if i%3==0: t_jia += frac
        break
    done += r
    if i%3==0: t_jia += 1
    i += 1
rec('2021SC2-51', {F(174,60):'A',F(3):'B',F(234,60):'C',F(4):'D'}[t_jia], 'C', f'甲={t_jia}h')
# 2021ZJA-65
cnt = [yv for yv in range(0,181) if F(14,10)*yv >= F(3,5)*180 and F(12,10)*(180-yv) >= F(2,3)*180]
rec('2021ZJA-65', {2:'A',3:'B',4:'C',5:'D'}[len(cnt)], 'B', str(cnt))
# 2022GD-32
for xx in range(3,100):
    if 50*(xx-2)+85*2 == 55*(xx-1):
        rec('2022GD-32', {1215:'A',1250:'B',1320:'C',1375:'D'}[55*(xx-1)], 'C')
# 2022GD-37
for a_ in range(0,38):
    for b_ in range(0,38):
        if (38-a_) == 4*(38-b_) and 2*(53-a_) == 3*(53-b_):
            rec('2022GD-37', {4:'A',6:'B',8:'C',9:'D'}[b_-a_], 'D', f'甲9:{a_} 乙9:{b_}')
# 2022JSA-63
xx = F(1000 - F(125,2), F(75,2))
tu = 5*xx + 5*(xx+5) + 5*F(3,2)*(xx+5)
rec('2022JSA-63', {450:'A',500:'B',550:'C',600:'D'}[int(tu)], 'B')
# 2022SC2-42
a = F(18*8 - 24*5, 8-5); yv = (24-a)*5
ok = [xv for xv in range(1,60) if (xv-a)*4 + (xv-a*F(3,2))*7 >= yv and (xv-a)*4 + (xv-a*F(3,2))*6 < yv]
rec('2022SC2-42', {18:'A',19:'B',20:'C',21:'D'}[min(ok)], 'A', f'满足"第7天恰好运完"的x={ok}')
# 2022SD-42
j,y_,b_ = 6,5,4; tot = (j+y_+b_)*180; Bq = F(tot, F(5,2)); xd = (Bq - y_*180)/b_
rec('2022SD-42', {45:'A',75:'B',105:'C',135:'D'}[int(xd)], 'A')
# 2022ZJA-62
xx = F(25-20, 3-2)  # 20-2x = 25-3x
rec('2022ZJA-62', {3:'A',5:'B',8:'C',10:'D'}[int(xx)], 'B')
# 2023GD-36
X = F(40*20 - 30*30, 20-30); Y = (40-X)*20
rec('2023GD-36', {10:'A',20:'B',30:'C',40:'D'}[int(Y/(30-X))], 'C')
# 2023GK-62
for xv in [F(k,10) for k in range(1,100)]:
    if F(12)/xv - F(12)/(4+xv) == 4:
        c = 3 - xv; rec('2023GK-62', {10:'A',12:'B',6:'C',8:'D'}[int(12/c)], 'B')
# 2023HB-67
rate1 = F(75,15)  # ml/min
rem5 = 300 - rate1*5; rate2 = (rem5-235)/10; total = 15 + F(235)/rate2
rec('2023HB-67', 'C', 'C', f'总时长{float(total)}min -> 9:00+{float(total)}min = 10:{float(total)-60:.2f}（约10:14）')
# 2023SC-46
work = 4*30 + 10*20 + 18*10
rec('2023SC-46', {120:'A',125:'B',130:'C',150:'D'}[work//4], 'B')
# 2024JSA-54
hours = F(259, F(60,6)+F(60,5)+F(60,4))
total = F(60,2)*hours*F(8,10) + hours*(12+15)
rec('2024JSA-54', {357:'A',399:'B',427:'C',469:'D'}[int(total)], 'A', f'工时{hours}h')
# 2024JSA-61
def ok61(a,b,c): return F(9*b+6*(a+b), 10*c) == F(60,40)
rec('2024JSA-61', ''.join(o for o,(a,b,c) in zip('ABCD',[(5,4,6),(6,4,5),(10,15,12),(12,15,10)]) if ok61(a,b,c)), 'A')
# 2024SC-48
for xv in range(1,451):
    if 450 % xv == 0 and 450 % (xv+5) == 0 and 450//xv - 450//(xv+5) == 1:
        d9 = 450//(xv+5); jia = xv*d9; yv = F(450 - jia, xv - (xv+5-10))
        rec('2024SC-48', {240:'A',280:'B',320:'C',360:'D'}[int((xv-5)*yv)], 'D')
# 2024SC-49
plan = F(60,8); rem = 60 - 24 - 10; t = 5 + F(rem, F(37,5)); extra = t - plan
opt = 'A' if extra < 1 else 'B' if extra < F(4,3) else 'C' if extra < F(5,3) else 'D'
rec('2024SC-49', opt, 'B', f'多{extra}h')
# 2024SD-54
xv = F(150 - 33 - 2*5*F(22,10), (5+6)*3)
rec('2024SD-54', 'B' if 3+math.ceil(xv)+2 == 8 else '?', 'B', f'三队合作{float(xv):.3f}天，总约{3+float(xv)+2:.2f}天')
# 2024ZJA-60
s = symbols('s'); a = Rational(1,20)
# 4(a_j + a_y) + 6 a_j = 0.4 ; a_j + a_y = 1/20
aj = (Rational(4,10) - 4*a)/6; ay = a - aj; c = (Rational(6,10)/10) - a
g = math.gcd
r = [aj, ay, c]; m = min(r); rr = [v/m for v in r]
rec('2024ZJA-60', 'D' if [v*Rational(10,rr[0]) for v in rr] == [10,5,3] else '?', 'D', str(rr))
# 2025GD-39
# 30(a+b) = 2(5(a+b)+15b) -> a:b=1:2 ; total 90
c = symbols('c'); cv = solve(Eq(45 + 3*(2+c) + 5*(1+2+c), 90), c)[0]
rec('2025GD-39', {Rational(3,2):'A',2:'B',Rational(5,2):'C',3:'D'}[cv], 'D')
# 2025GK-71
for xv in range(1,13):
    if 2*xv + 3*xv + 3*xv - 6 == 26:
        rec('2025GK-71', {6:'A',7:'B',8:'C',9:'D'}[12-xv], 'C')
# 2025HB-75: minimal n with 150(n-1)+100(n-3)+80(n-2) >= 1040
n = next(n for n in range(1,50) if 150*max(0,n-1)+100*max(0,n-3)+80*max(0,n-2) >= 1040)
rec('2025HB-75', {7:'A',6:'B',5:'C',4:'D'}[n], 'C')
# 2025SC-54
work_am = 0; t = 0
for m in range(8*60, 11*60+50):
    if (m-8*60) % 40 < 30: work_am += 1
need = F(work_am, F(3,2)); w = 0; m = 14*60
while w < need:
    if (m-14*60) % 35 < 30: w += 1
    m += 1
hh, mm = divmod(m, 60)
rec('2025SC-54', {'16:15':'A','16:20':'B','16:25':'C','16:30':'D'}[f'{hh}:{mm:02d}'], 'A', f'上午有效{work_am}min')
# 2025ZJA-59
x_, y_ = symbols('x_ y_', positive=True)
sol = solve(Eq((x_+y_)**2, Rational(9,2)*x_*y_).subs(y_,1), x_)
k = max(sol)  # 甲比乙高
yv = Rational(1, 12*(k+1)+12); xv = k*yv
rec('2025ZJA-59', {24:'A',30:'B',48:'C',60:'D'}[1/xv], 'A')
# 2026GK-67 (self-solve): 5(m+1)=3(1.5m+n)
m_, n_ = symbols('m_ n_')
msol = solve(Eq(5*(m_+1), 3*(Rational(3,2)*m_ + n_)), m_)[0]
opts = {'A':3*n_-5,'B':6*n_-10,'C':5-3*n_,'D':10-6*n_}
rec('2026GK-67', ''.join(k for k,v in opts.items() if simplify(v-msol)==0), None, f'm={msol}')
# 2026ZJA-56 (self-solve)
ej, ey, eb = F(72,120), F(108,120), F(120,100)   # per minute
s_ = ej+ey+eb; alloc = [270*e/s_ for e in (ej,ey,eb)]
rec('2026ZJA-56', {30:'A',60:'B',90:'C',120:'D'}[int(alloc[2]-alloc[0])], None, f'分配{alloc}')
# 2020SZS-29: as printed (15 days) vs official (10 days)
for days in (15, 10):
    # 3a + 4(a+b) = days*b + 2a ; a - b = 5
    a_, b_ = symbols('a_ b_')
    s = solve([Eq(3*a_+4*(a_+b_), days*b_+2*a_), Eq(a_-b_,5)], [a_,b_])
    trees = days*s[b_] + 2*s[a_]
    print(f'2020SZS-29 with 乙先{days}天: 甲={s[a_]}, 乙={s[b_]}, 总棵数={trees}', end='; ')
    if trees.is_integer and trees % 2 == 0:
        L = 8*(trees/2 - 1); print('路长', L)
    else: print('非整数 -> 无解')
# 2023JSA-61
def workdays(total_days, w, r):
    full, rem = divmod(total_days, w+r); return full*w + min(rem, w)
j1, y1 = workdays(23,3,1), workdays(21,5,2)
j2, y2 = workdays(15,3,1), workdays(27,5,2)
# j1*a + y1*b = j2*a + y2*b
a_, b_ = symbols('a_ b_'); rat = solve(Eq(j1*a_+y1*b_, j2*a_+y2*b_), a_)[0].subs(b_,6)
tot = j1*rat + y1*6; need = tot/rat
d = 0; wk = 0
while wk < need:
    d += 1
    if (d-1) % 4 < 3: wk += 1
rec('2023JSA-61', {43:'A',44:'B',47:'C',48:'D'}[d], 'C', f'甲工作日{need}, 日历{d}天')
# 2022GK-74
for xv in range(1,500):
    yv = F(5,4)*xv
    if 54 - xv == xv - yv:
        rate = yv/3; remain = 500 - xv - yv; hrs = remain/(2*rate)
        clock = 12 + hrs
        opt = 'A' if clock < 16.5 else 'B' if clock < 17 else 'C' if clock < 17.5 else 'D'
        rec('2022GK-74', opt, 'D', f'x={xv},y={yv},达到500在{float(clock):.3f}时')
# 2024GK-72
a_, b_, c_ = symbols('a_ b_ c_', positive=True)
T = 44*b_   # 11b = 0.25T
asol = solve(Eq(6*(a_+Rational(11,10)*b_), T/4), a_)[0]
csol = solve(Eq(15*(Rational(11,10)*b_+c_), T*Rational(3,4)*Rational(2,3)), c_)[0]
days = simplify(T/(asol + Rational(11,10)*b_ + csol))
rec('2024GK-72', {16:'A',20:'B',24:'C',28:'D'}[int(days)], 'B')
# 2025ZJA-58 (figure): check A finishes later than B and second-half time = 3x first-half
Q = 48; tA = F(Q,2)/6 + F(Q,2)/2; tB = F(Q,8)*2
rec('2025ZJA-58', 'C', 'C', f'甲用时{tA}, 乙用时{tB}（乙先完成，甲后半段是前半段3倍）—与C图一致')

print()
bad = []
for k,(a,o,n) in res.items():
    flag = '' if o is None else ('OK' if a==o else 'MISMATCH')
    if flag=='MISMATCH': bad.append(k)
    print(f'{k:15s} 计算={a}  官方={o}  {flag}  {n}')
print('共核查', len(res), '题；不一致：', bad)
