"""Independent solutions for all 74 M01 real questions (from stem data), compared with official answers."""
import json
from fractions import Fraction as F
from itertools import product
S='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
m=json.load(open(S+'/tasks_in/M01.json'))
off={r['id']:r['answer_official'] for r in m['real']}

def pick(val, opts, tol=1e-9):
    """opts: dict letter->value (number) or predicate; return letters matching"""
    hits=[]
    for k,v in opts.items():
        if callable(v):
            if v(val): hits.append(k)
        elif isinstance(v,(int,float,F)):
            if abs(float(val)-float(v))<tol: hits.append(k)
        else:
            if val==v: hits.append(k)
    return hits

R={}
# --- 2026 self-solve ---
# 2026GD-36: wind 40%, PV 35%, biomass 25%; PV-biomass=120
tot=F(120)/(F(35,100)-(1-F(40,100)-F(35,100)))
R['2026GD-36']=pick(tot,{'A':600,'B':800,'C':1000,'D':1200})
# 2026GD-37: sat=1.5 sun clients, sat amount=0.8 sun amount, 40 clients, 720 total
for sun in range(1,41):
    sat=F(3,2)*sun
    if sat==int(sat) and sat+sun==40:
        sun_amt=F(720)/(1+F(8,10)); avg=sun_amt/sun
R['2026GD-37']=pick(avg,{'A':15,'B':20,'C':25,'D':10})
# 2026GK-66: a=2b, c=b-2, a+b+c=10
sol=[(2*b,b,b-2) for b in [F(x,10) for x in range(1,200)] if 2*b+b+(b-2)==10]
R['2026GK-66']=pick(sol[0][2],{'A':1,'B':2,'C':3,'D':4})
# 2026ZJA-50: s+d=14 tables, doubles people(4d)=1.5*singles people(2s); singles boys 13, doubles boys 15
for s in range(0,15):
    d=14-s
    if 4*d==F(3,2)*2*s: sg=2*s-13; dg=4*d-15; diff=sg-dg
R['2026ZJA-50']=pick(diff,{'A':-4,'B':4,'C':-6,'D':6})
# --- others ---
R['2020HB-63']=pick([x for x in range(1,100) if 5*x-4==4*x+8][0],{'A':9,'B':10,'C':11,'D':12})
# 2020JSA-51 people 4:3, total 5:4, 甲 avg 300
R['2020JSA-51']=pick(F(300)*F(4,5)*F(4,3)**-1*F(4,3)**0 if False else (F(300)*4/5*4)/3* (1) / (4/F(4)) ,{'A':270,'B':290,'C':320,'D':350})
# direct: 甲总=300*4k, 乙总=300*4k*4/5, 乙人均=乙总/3k
R['2020JSA-51']=pick(F(300*4)*F(4,5)/3,{'A':270,'B':290,'C':320,'D':350})
# 2020JSA-61: 3L=5S, 100L+200S=11000
for S_ in range(1,200):
    L=F(5,3)*S_
    if 100*L+200*S_==11000: ans=(S_,L)
R['2020JSA-61']=pick(ans,{'A':(24,40),'B':(30,50),'C':(36,60),'D':(27,45)})
# 2020JSA-64
k=F(126,14); third_people=10*k; third_total=F(162000)*F(1,6)
R['2020JSA-64']=pick(third_total/third_people,{'A':250,'B':300,'C':350,'D':400})
# 2020SC1206-45: run = 2/9 T + 2000 = 5/12 T
T=F(2000)/(F(5,12)-F(2,9)); R['2020SC1206-45']=pick(T*F(7,12),{'A':5000,'B':5300,'C':6000,'D':6400})
# 2021GK-63
for x in range(1,100):
    d1=x; d2=F(3,2)*x; d3=d1+d2-15
    if d1+d2+d3==65: d4=2*d1-5; days=[d1,d2,d3,d4]
R['2021GK-63']=pick(max(days)-min(days),{'A':9,'B':10,'C':11,'D':12})
# 2021SC2-53
for y in range(1,50):
    for z in range(1,50):
        if 2*y+F(1,2)*z==F(3,2)*(y+z): r=F(z,y)
R['2021SC2-53']=pick(r,{'A':F(1,3),'B':F(1,2),'C':F(2,3),'D':F(3,2)})
# 2021SC2-54 ratios a:d=4:3, a:o=5:2 -> 20:15:8 ; 6d-7o=3400
x=F(3400)/(6*15-7*8); R['2021SC2-54']=pick(5*20*x+6*15*x+7*8*x,{'A':22800,'B':23400,'C':24000,'D':24600})
# 2021ZJA-61
g3=F(72)/F(9,10); g12=2*g3*F(3,4); R['2021ZJA-61']=pick((g12+g3+72)/4,{'A':64,'B':66,'C':68,'D':72})
# 2022GD-31
R['2022GD-31']=pick(200*F(5,100)+F(200,4)*F(8,100),{'A':15,'B':14,'C':12,'D':10})
# 2022GK-61
x=[n for n in range(1,200) if 100*n+550==120*n-630][0]; R['2022GK-61']=pick((100*x+550+2510)/80-x,{'A':50,'B':53,'C':56,'D':59})
# 2022GK-64
for xx in range(1,2000):
    # 甲-乙=3xx ; after moving 150: (甲-150)-(乙+150)=2xx
    if 3*xx-300==2*xx: jia=(5000+3*xx)/2
R['2022GK-64']=pick(jia,{'A':2500,'B':2750,'C':2950,'D':3500})
R['2022JSA-53']=pick((10*F(9,10)+380*F(8,10)+35*F(2,10))*12,{'A':320,'B':640,'C':1920,'D':3840})
# 2022SC1-49: a=3c, a+b+c=53, 17b=33a+13c+1
for c in range(0,54):
    a=3*c; b=53-a-c
    if b>=0 and 17*b==33*a+13*c+1: diff=17*b-13*c
R['2022SC1-49']=pick(diff,{'A':385,'B':415,'C':466,'D':496})
# 2022ZJA-60 (nurses per patient interpretation)
R['2022ZJA-60']=pick(900*F(2,10)-200*F(6,10),{'A':80,'B':60,'C':40,'D':20})
R['2023GD-31']=pick(20*F(8,10)*F(7,10),{'A':10,'B':F(104,10),'C':F(112,10),'D':F(126,10)})
# 2023GD-33 last year p:n=1:3 total 4x; this year total 4.8x, p:n=1:2 -> p=1.6x ; 1.6x-x=6
x=F(6)/F(6,10); R['2023GD-33']=pick(F(16,10)*x,{'A':16,'B':24,'C':32,'D':48})
# 2023HB-64
ab=(F(424000)*F(1,10)-400)/2; R['2023HB-64']=pick(ab/3,{'A':3500,'B':7000,'C':14000,'D':21400})
# 2023HB-66: 5L+S=3, L+5S=2
S_=F(2*5-3,24); L=(3-S_)/5
import math
R['2023HB-66']=pick(math.floor(1/S_),{'A':2,'B':3,'C':4,'D':5})
# 2023HB-72 small 2 -> loses 1; big 20 loses 4
R['2023HB-72']=pick(F(20-4,2-1),{'A':16,'B':10,'C':8,'D':6})
kcal=84*F(20,100)+120*F(388,100)+40*F(612,100)+120*F(54,100)
R['2023JSA-51']=pick(kcal/132*F(1,2),{'A':F(3,2),'B':3,'C':F(9,2),'D':6})
# 2023JSA-52
c_now=20; c_old=F(20)/F(25,10); old_tot=84-35
for y in [F(i,10) for i in range(1,1000)]:
    x_=old_tot-c_old-y
    if F(15,10)*x_+F(16,10)*y+c_now==84: R['2023JSA-52']=pick(y,{'A':16,'B':20,'C':25,'D':36})
# 2023JSA-54 sizes 8:7:5 (x=1), male total 15 of 20
mj=8*F(7,10); my=7*F(6,7); mb=15-mj-my; fb=5-mb; r=mb/fb
R['2023JSA-54']=pick(r,{'A':F(7,2),'B':F(4,1),'C':F(15,4),'D':F(17,8)})
# 2023SC-48
first25=25*F(64,100); first20=first25-5; R['2023SC-48']=pick(first20+5+first20,{'A':23,'B':25,'C':27,'D':29})
# 2024GD-39
y=[v for v in range(1,2000) if (v+100)+F(6,10)*v==1260]; R['2024GD-39']=pick(2*y[0]+100,{'A':1450,'B':1500,'C':1550,'D':1600})
# 2024GK-62
for x in range(1,100):
    if (2*x-1)==F(6,10)*(3*x+4): d=(5*x-4)-(4*x+1)
R['2024GK-62']=pick(d,{'A':-22,'B':22,'C':-12,'D':12})
# 2024GK-63: 30x=2*60y ; 20x-30y=30000
for y in range(1,5000):
    x=4*y
    if 20*x-30*y==30000: tot=x+y
R['2024GK-63']=pick(tot,{'A':2400,'B':2700,'C':3000,'D':3300})
for b in range(1,100):
    a=2*b; c=240-3*b
    if c>=0 and 30*a+24*b+20*c==6000: R['2024GK-67']=pick(c,{'A':90,'B':75,'C':60,'D':45})
for x in range(1,100):
    if F(3*x-2,4*x-1)==F(2,3): R['2024HB-65']=pick(4*x,{'A':10,'B':12,'C':14,'D':16})
R['2024JSA-51']=pick(F(500)*F(9,10)/(10*F(2,100))*F(35,2),{'A':35875,'B':36375,'C':37625,'D':39375})
budget=450; pc=budget//18; ps=budget//30; pb=budget//50
R['2024JSA-57']=pick(F(budget-6*pc-8*ps,pb),{'A':10,'B':14,'C':20,'D':26})
for x20 in range(0,7):
    x10=x20+2; x30=6-x10-x20
    if x30>=0 and 10*x10+20*x20+30*x30==110: R['2024SD-53']=pick(x30,{'A':2,'B':3,'C':4,'D':5})
orig=F(50)/F(40,100); total=orig/F(25,100); R['2024SZ-54']=pick(total-50,{'A':450,'B':125,'C':500,'D':75})
# 2025GK-66: 10x+15y=1.5*10x -> x/y
R['2025GK-66']=pick(F(15,5),{'A':3,'B':F(5,2),'C':2,'D':F(3,2)})
x=F(4)/(F(1)/F(12,10)-F(1)/F(15,10)) # 3月 m: jan=m/1.2 feb=m/1.5 ; jan-feb=4
mar=x; R['2025GK-67']=pick(mar+mar/F(12,10)+mar/F(15,10),{'A':48,'B':52,'C':56,'D':60})
# 2025HB-68: old:mid=5:2, mid:young=3:4 -> 15:6:8 ; speed 1:2:3 ; young total 80
w=[15*1,6*2,8*3]; R['2025HB-68']=pick(F(80)*sum(w)/w[2],{'A':170,'B':212,'C':255,'D':298})
R['2025JSA-62']=pick(F(2080)/F(26,10),{'A':780,'B':800,'C':1280,'D':1300})
v=150*F(8,10)*F(115,100)*F(75,100); R['2025SD-51']=pick(round(v),{'A':114,'B':104,'C':128,'D':138})
# 2025ZJA-56: 甲有效 x, 乙有效 36-x, 乙无效 30-(36-x)
R['2025ZJA-56']=pick(F(6),{'A':6,'B':12,'C':-6,'D':-12})
R['2026CQ-56']=pick(((220-40)*F(6,10),(220-40)*F(8,10)),{'A':(108,132),'B':(132,144),'C':(108,144),'D':(144,176)})
# 2020HB-70 2a+5b=4c, c+2a=5b -> ratio
for a,b,c in product(range(1,10),repeat=3):
    if 2*a+5*b==4*c and c+2*a==5*b:
        g=math.gcd(math.gcd(a,b),c); rr=(a//g,b//g,c//g); break
R['2020HB-70']=pick(rr,{'A':(2,1,3),'B':(2,3,4),'C':(3,2,1),'D':(3,2,4)})
# 2020JSA-60
cai=(168+10)/2; yu=168-cai; ban=172-cai; guo=180-ban; zong=guo-5
R['2020JSA-60']=pick(F(ban+yu+guo+cai+zong)/5,{'A':84,'B':86,'C':88,'D':90})
# 2020SC0725-52: 3a+b=1.2(a+2b) -> b=9a/7 ; new: (1.5a+2b)/(3a+b)
a=F(7); b=F(9); R['2020SC0725-52']=pick((F(3,2)*a+2*b)/(3*a+b),{'A':F(90,100),'B':F(95,100),'C':1,'D':F(105,100)})
gas=F(22)/F(2,10)*164
R['2020SD-37']=pick(gas,{'A':lambda v:v<16000,'B':lambda v:16000<=v<=17000,'C':lambda v:17000<v<=18000,'D':lambda v:v>18000})
for xx in [F(i,10) for i in range(1,100)]:
    if 20*xx==25*(xx-F(1,2)): R['2020SZS-18']=pick(xx,{'A':2,'B':F(5,2),'C':3,'D':F(7,2)})
R['2020SZS-20']=pick(F(92+91-93,2),{'A':44,'B':45,'C':46,'D':47})
# 2021GK-62: T=6n+12 ; 1.3T=8n+10
for n in range(1,200):
    T=6*n+12
    if F(13,10)*T==8*n+10:
        T2=F(18,10)*T; n2=n+10; per=math.floor(T2/n2)
R['2021GK-62']=pick(per,{'A':8,'B':9,'C':10,'D':12})
# 2021GK-66
for x in range(1,500):
    for y in range(1,500):
        if F(6,10)*x==F(75,100)*y-3 and F(4,10)*F(4,10)*x+F(75,100)*F(25,100)*y==24:
            res=x-y
R['2021GK-66']=pick(res,{'A':-3,'B':-11,'C':3,'D':11})
# 2021GK-72: budget B: 基建0.4B, 图书 0.3B, 信息 0.24B, other 4.5 (万) ; spend = B-0.3
B=F(48,10)/(1-F(4,10)-F(3,10)-F(24,100)) # (0.06B = 4.5+0.3)
books_cost=F(3,10)*B*10000; bought=books_cost/25; donated=bought/F(12,10)
R['2021GK-72']=pick(bought+donated,{'A':lambda v:v<11000,'B':lambda v:11000<=v<=14000,'C':lambda v:14000<v<=17000,'D':lambda v:v>17000})
# 2021JSA-51
for y in [F(i,10) for i in range(1,100)]:
    x=1
    if (5*x+y)*5==(9*x+y)*3: inc=3*y/24
R['2021JSA-51']=pick(inc,{'A':F(125,1000),'B':F(15,100),'C':F(175,1000),'D':F(2,10)})
# 2021ZJA-63
for yb in range(1,1000):
    ja=F(3,2)*yb
    if ja==int(ja) and (ja-30)==F(12,10)*(yb+30):
        tot=ja+yb; extra=(ja-30)-tot/2
R['2021ZJA-63']=pick(extra,{'A':20,'B':22,'C':24,'D':25})
# 2022GK-62: solve generic: choose ding as 0 -> wu=10, bing=ding+6.5
ding=F(0); wu=ding+10; bing=ding+F(13,2)
order=sorted([('丙',bing),('丁',ding),('戊',wu)],key=lambda t:-t[1]); od=''.join(t[0] for t in order)
R['2022GK-62']=pick(od,{'A':'丙丁戊','B':'丙戊丁','C':'丁丙戊','D':'戊丙丁'})
# 2022GK-71: total rice 48x (jia 2x people, bing x) ; 12y + 4(3x+y)=48x
x=F(1); y=F(9,4)*x; avg=48*x/(y+x)
R['2022GK-71']=pick(avg,{'A':lambda v:v<14,'B':lambda v:14<=v<15,'C':lambda v:15<=v<16,'D':lambda v:v>=16})
# 2022HB-66 forward-check from candidate originals
def hb66(a,b,c):
    a,b=a-b,b+b; b,c=b-c,c+c; c,a=c-a,a+a; return a,b,c
cand={'A':36,'B':48,'C':56,'D':66}
res=[]
for L,a0 in cand.items():
    for b0 in range(1,144):
        c0=144-a0-b0
        if c0>0 and hb66(a0,b0,c0)==(48,48,48): res.append(L)
R['2022HB-66']=res
# 2022JSA-57: 甲 4x:x, 乙 3x:2x ; 女党员 甲 2y, 乙 4y ; 男党 甲 9y, 乙 18y
# 甲: 男女 4x:x ; 乙: 3y:2y ; 合并 7:3 -> x=y (两部门人数相等)
# 女党员占本部门比重 乙=2×甲 -> 甲女党 2t, 乙女党 4t ; 男党: 甲 9:2 -> 9t, 乙 9:4 -> 9t
R['2022JSA-57']=pick(F(9+9,2+4),{'A':F(18,5),'B':F(27,8),'C':3,'D':F(27,10)})
# 2022ZJA-63
for x in range(1,200):
    if (x-10)+(x+1)+F(x,2)+2*x==4*x-2: groups=[x-10,x+1,F(x,2),2*x]
R['2022ZJA-63']=pick(max(groups)-min(groups),{'A':15,'B':21,'C':24,'D':32})
# 2023GK-73
for x in range(1,1000):
    p1=x; p3=3*x; p2=p3-300
    if p2*F(4,10)==F(1,2)*p3*F(4,10):
        yshare=F(20)/((p2-p1)*F(4,10))
R['2023GK-73']=pick(1-yshare,{'A':F(4,10),'B':F(5,10),'C':F(6,10),'D':F(75,100)})
# 2023GK-74: b21=x, a21=2x ; a20=2x-400 ; b20=x+100 ; c20=a20+b20 ; c21=1.3 c20
for x in range(1,5000):
    a20=2*x-400; b20=x+100; c20=a20+b20; tot20=a20+b20+c20; tot21=2*x+x+F(13,10)*c20
    if tot21==F(12,10)*tot20: R['2023GK-74']=pick(a20-b20,{'A':900,'B':1100,'C':400,'D':600})
# 2023SC-51
for j in range(12,200,12):
    for yy in range(12,200,12):
        if F(5,12)*(j+yy)==30 and (F(j,3)+F(yy,4))==F(11,10)*(F(j,4)+F(yy,3)):
            R['2023SC-51']=pick(F(5,12)*j,{'A':12,'B':15,'C':18,'D':20})
# 2024GK-64
for x in range(0,961):
    y=960-x
    if F(2,10)*x+F(15,100)*y==172: d=F(8,10)*x-F(85,100)*y
R['2024GK-64']=pick(d,{'A':-160,'B':160,'C':-108,'D':108})
# 2024HB-73: a+b=50, 15a+p b=1150 ; second: b/4 乙, 70-b/4 甲 ; cost
sols=set()
for b in range(4,51,4):
    a=50-b
    p=F(1150-15*a,b)
    cost2=15*(70-F(b,4))+p*F(b,4); sols.add(cost2)
R['2024HB-73']=pick(list(sols)[0],{'A':1150,'B':1725,'C':2300,'D':2875}) if len(sols)==1 else ['MULTI',sols]
# 2024SZ-51
for z in range(0,253):
    for yv in range(0,253):
        xv=252-yv-z
        if xv>=0 and xv+2*yv+5*z==400 and 4*yv+10*z==400: R['2024SZ-51']=pick(z,{'A':32,'B':33,'C':34,'D':35})
# 2024ZJA-64
for k in range(1,100):
    if (18*k-120)*5==(17*k-160)*6: R['2024ZJA-64']=pick(35*k,{'A':630,'B':720,'C':1050,'D':1400})
# 2026CQ-57 restored: singles s, group h=2s-1, s+h=68 ; family=2/3 h ; pairs: fm,fc,mc ; child_in_group = (father_in_group+mother_in_group)/2 ; child single = f+m singles +1
res=set()
for s in range(1,68):
    h=2*s-1
    if s+h!=68: continue
    fam=F(2,3)*h
    pairs=h-fam
    for fm in range(0,int(pairs)+1):
        for fc in range(0,int(pairs)-fm+1):
            mc=pairs-fm-fc
            child_g=fam+fc+mc; fa_g=fam+fm+fc; mo_g=fam+fm+mc
            if child_g*2==fa_g+mo_g:
                for cs in range(0,s+1):
                    if (s-cs)+1==cs: res.add(child_g+cs)
R['2026CQ-57']=pick(list(res)[0],{'A':52,'B':48,'C':45,'D':37}) if len(res)==1 else ['MULTI',res]
# 2020HB-75 fractions 2/13, 9/16, 1/3 ; 丙 pays 90
for T in range(100,2000):
    j=F(2,15)*(T-100)+100; yv=F(9,25)*(T-100)+100; bv=F(1,4)*(T-90)+90
    if j+yv+bv==T: R['2020HB-75']=pick(T,{'A':850,'B':900,'C':950,'D':1000})
# 2020SC1206-48: symbolic: north = east(sales x)+2
# 2020SC1206-48: N=E+1, S=N+4 ; equal after rotation N gets S's sales, E gets N's, S gets E's
# brute force with numbers: choose sizes, sales dept sizes n,e,s ; N-n+s = E-e+n = S-s+e
hits=set()
for E in range(5,40):
    N=E+1; S_=N+4
    for e in range(0,E+1):
        for n in range(0,N+1):
            for s_ in range(0,S_+1):
                a=N-n+s_; b=E-e+n; c=S_-s_+e
                if a==b==c: hits.add(n-e)
R['2020SC1206-48']=pick(list(hits)[0],{'A':1,'B':-1,'C':'2x-1','D':2}) if len(hits)==1 else ['MULTI',hits]
# 2021GK-64
for n in range(1,200):
    if (12*n-8-10*n)-(8*n-11-7*n)==20:
        masks=12*n-8; suits=8*n-11
        best=None
        for k in range(1,100):
            if 2*k*n>=masks and k*n>=suits:
                buy=(2*k*n-masks)+(k*n-suits); best=buy if best is None else min(best,buy)
R['2021GK-64']=pick(best,{'A':54,'B':63,'C':75,'D':87})
# 2021GK-67
x=F(1)
for x in [F(i,10) for i in range(1,1000)]:
    s3=8*x; s2=7*x; s1=s2/F(14,10); front=s1+s2+s3; back=3*front; tot=front+back
    s5=tot*F(25,100); s4=s5/F(11,10); s6=back-s4-s5
    if s6-s5==16: diff=s6-s3
R['2021GK-67']=pick(diff,{'A':lambda v:v<100,'B':lambda v:100<=v<=120,'C':lambda v:v>140,'D':lambda v:120<v<=140})
# 2021SD-37: a+b+c=700 ; second a+2b+c/2=700 ; value 2.5a:3.5b:2c=5:14:16
for a in range(1,700):
    for b in range(1,700-a):
        c=700-a-b
        if a+2*b+F(c,2)==700 and F(5,2)*a*14==F(7,2)*b*5 and F(7,2)*b*16==2*c*14:
            R['2021SD-37']=pick(b-a,{'A':100,'B':50,'C':-100,'D':-50})
# 2023ZJA-68: share 10% -> 8% -> 5%; inv2=10 inv1
# 甲 value fixed fraction: before1 value V1, after1 V1+I ; 0.1V1/(V1+I)=0.08 -> I=V1/4 ; before2 V2, 0.08V2/(V2+10I)=0.05 -> V2=50I/3
I=F(1); V1=4*I; V2=F(50,3)*I
R['2023ZJA-68']=pick(V1/V2,{'A':F(24,100),'B':F(28,100),'C':F(32,100),'D':F(36,100)})

bad=0
for r in m['real']:
    i=r['id']; mine=R.get(i)
    o=off[i]
    flag=''
    if mine is None: flag='NOT SOLVED'
    elif len(mine)!=1: flag='AMBIG '+str(mine)
    elif o and mine[0]!=o: flag='MISMATCH official=%s'%o
    if flag: bad+=1
    print(f"{i:16s} mine={mine} official={o} {flag}")
print('problems',bad)
