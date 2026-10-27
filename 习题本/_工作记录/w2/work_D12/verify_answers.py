from fractions import Fraction as F
import itertools, math
res = {}
def pick(opts, val, tol=1e-9):
    hits = [k for k, v in opts.items() if abs(float(v) - float(val)) < tol]
    return hits

# T084: 40% + 4kg water -> 30%; then + M pure -> 50%
# 0.4S = 0.3(S+4) -> S=12
S = F(12); alc = F(2,5)*S; water = S + 4 - alc
M = water - alc  # need alc+M = water (50%)
res['T084'] = (M, pick({'A':8,'B':12,'C':F(46,10),'D':F(64,10)}, M))

# 2017GK-61: 20% 12kg sugar water, add rest sugar -> 25%; price 15/kg
sugar0 = F(12)*F(1,5); water = 12 - sugar0
total = water / F(3,4); sugar = total - water
res['2017GK-61'] = (sugar*15, pick({'A':45,'B':48,'C':36,'D':42}, sugar*15))

# 2021SD-40: symbolic check with random numbers
import random
ok = True
for _ in range(1000):
    a = random.uniform(0.01, 0.3); X = random.uniform(1, 10)
    Y = a*X / random.uniform(0.01,0.3)  # arbitrary; condition Xa=Yb defines b
    b = a*X/Y
    conc = (a*X + b*X) / (2*X - X)
    Z = conc / b
    ok &= abs(b/a - 1/(Z-1)) < 1e-9
res['2021SD-40'] = ('b/a == 1/(Z-1) always' if ok else 'FAIL', ['B'] if ok else [])

# 2025JSA-63: m, c; (mc+30)/(m+50)=c ; mc/(m+20) = (mc+15)/(m+50)
sols = []
for m in range(1, 1000):
    c = F(30, 50)
    if F(m)*c/(m+20) == (F(m)*c + 15)/(m+50): sols.append(m)
res['2025JSA-63'] = (sols, pick({'A':100,'B':110,'C':120,'D':150}, sols[0]))

# 2016JSA-64: x*1/2*1/3*1/4 = 2.5%
x = F(25,1000)*24
res['2016JSA-64'] = (x, pick({'A':F(60,100),'B':F(55,100),'C':F(50,100),'D':F(45,100)}, x))

# T085: 50%, pour 1/4, refill 20%, 3 times
c = F(1,2)
for _ in range(3): c = c*F(3,4) + F(1,4)*F(1,5)
res['T085'] = (float(c), [k for k,v in {'A':0.327,'B':0.303,'C':0.270,'D':0.294}.items() if abs(v-float(c))<0.0005])

# 2024SC-51: 70% 100g; pour 40, add 40g 20%, 5 times
c = F(7,10)
for _ in range(5): c = c*F(6,10) + F(4,10)*F(2,10)
cf = float(c)
rng = {'A': cf < 0.23, 'B': 0.23 <= cf <= 0.25, 'C': 0.25 < cf <= 0.27, 'D': cf > 0.27}
res['2024SC-51'] = (cf, [k for k,v in rng.items() if v])

# 2019JSA-52: 12% x + 24% y, +50 water = 600g 18%
y = None
for xx in range(0, 551):
    yy = 550 - xx
    if F(12,100)*xx + F(24,100)*yy == F(18,100)*600: y=(xx,yy)
r = F(y[0], y[1])
res['2019JSA-52'] = (y, pick({'A':F(6,5),'B':F(1,1),'C':F(5,6),'D':F(4,7)}, r))

# 2015JSA-35: a+b=34, b+c=46, a+b+c=54
b = 34 + 46 - 54
res['2015JSA-35'] = (b, pick({'A':21,'B':22,'C':26,'D':37}, b))

# 2017JSA-63
# (a+b)/2=45, (a/2 + b/4)/(3/4) = 40 -> (2a+b)/3=40
a = F(120 - 90); bb = F(90) - a
mix = (a*F(1,5) + bb*F(4,5))
res['2017JSA-63'] = ((a, bb, mix), pick({'A':48,'B':50,'C':54,'D':60}, mix))

# 2022SZ-54: 10% (2), 40% (3), 60% (n) -> 52%
for n in [F(k,2) for k in range(1,200)]:
    if (2*10 + 3*40 + n*60) == 52*(5+n): N=n
res['2022SZ-54'] = (N/2, pick({'A':F(9,2),'B':F(11,2),'C':F(13,2),'D':F(15,2)}, N/2))

# 2023JSA-62: x+y+z=240, 72y+78z=76(y+z), 68x+72y+78z=74*240
sol=[]
for y in range(0,241):
    for z in range(0,241-y):
        x = 240-y-z
        if 72*y+78*z == 76*(y+z) and 68*x+72*y+78*z == 74*240: sol.append((x,y,z))
res['2023JSA-62'] = (sol, pick({'A':30,'B':40,'C':48,'D':60}, sol[0][1]))

# T088: 1000g 20% + 200g A(2x) + 400g B(x) -> 15%
# 200 + 200*2x + 400x = 1600*0.15
xB = F(240-200, 800)
res['T088'] = (2*xB, pick({'A':F(5,100),'B':F(6,100),'C':F(8,100),'D':F(10,100)}, 2*xB))

# 2021ZJA-60: 1/4 at T-6, 3/4 at T+10, avg 140
T = 140 - (F(1,4)*(-6) + F(3,4)*10)
res['2021ZJA-60'] = (T, pick({'A':116,'B':125,'C':134,'D':139}, T))

# 2019GK-71
# 12a+20b = 8(a+3)+24(b+1) -> 4a - 4b = 48
d = F(48,4)
res['2019GK-71'] = (d, pick({'A':8,'B':12,'C':14,'D':15}, d))

# 2026GK-76: 甲4 avg a, 乙4 avg 32; move p from 甲 to 乙, both avg +2
sols=[]
for a in range(20,80):
    for p in range(18,80):
        if F(4*32+p,5) == 34 and F(4*a-p,3) == a+2: sols.append((a,p,a+2))
res['2026GK-76'] = (sols, pick({'A':50,'B':48,'C':46,'D':44}, sols[0][2]))

# 2025ZJA-60: 乙 avg b, 甲 avg b+1.5 (6 ppl), 乙 4 ppl; 小张 s, 老张 s+20
# (6(b+1.5)+s)/7 = (4b+s+20)/5 - 2  -> find (s+20) - b
import sympy as sp
b_, s_ = sp.symbols('b s')
eq = sp.Eq((6*(b_+sp.Rational(3,2))+s_)/7, (4*b_+s_+20)/5 - 2)
s_sol = sp.solve(eq, s_)[0]
diff = sp.simplify(s_sol + 20 - b_)
res['2025ZJA-60'] = (diff, pick({'A':5,'B':7.5,'C':12.5,'D':15}, float(diff)))

# 2019JSA-60: table 10:2,9:2,8:4, 2:5,1:3,0:8 ; >=3 avg 2x ; <=7 avg x
x_, N_, S_ = sp.symbols('x N S', positive=True)
e1 = sp.Eq(S_ - (2*5+1*3+0*8), 2*x_*(N_-16))
e2 = sp.Eq(S_ - (10*2+9*2+8*4), x_*(N_-8))
solN = sp.solve([e1,e2],[N_,S_])[N_]
res['2019JSA-60'] = (sp.simplify(solN), ['A'] if sp.simplify(solN - (57/x_+24))==0 else [])

# 2022SD-37: 甲=乙+1.2, 甲=总+0.5 -> 总=乙+0.7; 甲:乙 = 0.7:0.5
n_jia = F(96)*F(7,12); n_yi = 96 - n_jia
diffp = n_jia - n_yi
opt = 'C' if diffp > 10 else ('B' if diffp > 0 else ('A' if diffp > -10 else 'D'))
res['2022SD-37'] = ((n_jia, n_yi, diffp), [opt])

# 2016ZJA-63: music men 1/4, art men 2/5, total 30%
ratio = (F(2,5)-F(3,10)) / (F(3,10)-F(1,4))
res['2016ZJA-63'] = (ratio, pick({'A':F(5,2),'B':F(5,1),'C':F(3,1),'D':F(2,1)}, ratio))

# 2022SC2-41
# 甲:乙 = (88-78):(78-70)=10:8 ; 乙:丙 = (82-74):(88-82)=8:6
j, y, bng = 10, 8, 6
avg = F(70*j + 88*y + 74*bng, j+y+bng)
res['2022SC2-41'] = (avg, pick({'A':75,'B':77,'C':79,'D':81}, avg))

# 2025GD-43: 蜜柚 +40%, 柠檬 -20%, total +4%
share = (F(4)-(-20)) / ((F(4)-(-20)) + (40-4))
res['2025GD-43'] = (share, pick({'A':F(6,10),'B':F(5,10),'C':F(4,10),'D':F(3,10)}, share))

# 2020SD-40: A +10%, B +25%, total +18% ; ask 2017 ratio
A0, B0 = 25-18, 18-10
r17 = F(A0)*F(11,10) / (F(B0)*F(125,100))
res['2020SD-40'] = (r17, pick({'A':F(7,8),'B':F(8,7),'C':F(176,175),'D':F(77,100)}, r17))

# 2024GK-64: x+y=960, 0.2x+0.15y=172 -> today 0.8x - 0.85y
xx = (F(172) - F(15,100)*960) / (F(20,100)-F(15,100)); yy = 960 - xx
d64 = F(8,10)*xx - F(85,100)*yy
res['2024GK-64'] = ((xx,yy,d64), ['D'] if d64 == 108 else [])

# 2023GK-74: 2020 甲=J, 乙=Y, 丙=J+Y ; 2021: J+400, Y-100 = (J+400)/2 ; 丙*1.3 ; total +20%
J_, Y_ = sp.symbols('J Y')
s = sp.solve([sp.Eq(Y_-100, (J_+400)/2), sp.Eq((J_+400)+(Y_-100)+sp.Rational(13,10)*(J_+Y_), sp.Rational(12,10)*2*(J_+Y_))],[J_,Y_])
d74 = s[J_]-s[Y_]
res['2023GK-74'] = ((s[J_], s[Y_], d74), pick({'A':900,'B':1100,'C':400,'D':600}, d74))

# 2023SZ-55: (69a+68b) = 1.05(60a+80b)
a_, b2 = sp.symbols('a b2', positive=True)
r = sp.solve(sp.Eq(69*a_+68*b2, sp.Rational(105,100)*(60*a_+80*b2)), a_)[0]/b2
res['2023SZ-55'] = (r, pick({'A':1,'B':F(5,3),'C':F(8,3),'D':2}, float(r)))

# T184
nB = F(40)*F(68-65, 72-68)  # A:B = 4:3
avgB = (nB*72 + 2*48) / (nB+2)
res['T184'] = ((nB, avgB, avgB-65), pick({'A':4,'B':4.5,'C':5,'D':5.5}, avgB-65))

# 2021SC2-52: 50 ppl avg 81.5 range<=10 ; max # with >=83 -> others >= 73
best = 0
for n in range(0,51):
    # n at >=83 (min 83), rest >= 73 and < 83 ; min total = 83n + 73(50-n) must be <= 4075 ;
    # also feasible max: all <= 83+10? if n>0 then rest in [73, 83) ... total achievable range covers 4075?
    lo = 83*n + 73*(50-n)
    hi = 93*n + 83*(50-n) if n>0 else 83*50
    # range constraint: with values in [73,83] for all ppl (taking min=73, max=83) feasible
    if lo <= 4075 <= hi: best = max(best, n)
res['2021SC2-52'] = (best, pick({'A':40,'B':42,'C':44,'D':46}, best))

# 2024SD-59: x harmonic, y arithmetic; x<=y always (equality if prices equal)
okx = all(2/(1/p+1/q) <= (p+q)/2 + 1e-12 for p in [5,7,9.3] for q in [5,6,8.8])
res['2024SD-59'] = ('x<=y (HM<=AM, equal when p=q)', ['D'] if okx else [])

for k,v in res.items():
    print(f'{k:12s} -> value {v[0]} | option {v[1]}')
