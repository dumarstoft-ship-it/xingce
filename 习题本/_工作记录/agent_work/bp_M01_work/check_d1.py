from fractions import Fraction as F
import math
out={}
# V1 carbon reverse: coef water .9 elec .8 gas .2 ; monthly water 10t gas 35 ; yearly total 3072 -> elec?
yearly=3072; m=F(yearly,12); e=(m-10*F(9,10)-35*F(2,10))/F(8,10); out['V1']=(e, 'distractors', m/F(8,10), e*12, e*F(8,10))
# V2 scale 1:5000, 8cm x 6cm, 35% green -> ha
L=8*5000/100; W=6*5000/100; area=L*W; out['V2']=(area*0.35/10000, 'no35%',area/10000,'wrong ha=1000m2',area*0.35/1000, 'rest65%',area*0.65/10000)
# V3 completed is 37.5% less than not-completed; total 2080
nc=F(2080)/(1+F(5,8)); out['V3']=(nc,'done',2080-nc,'using1.6',F(2080)/F(26,10),'x0.375',2080*F(3,8))
# V4 jia stock = yi+120 ; sold 75% jia, 60% yi, total sold 1170 -> remaining
y=(1170-F(3,4)*120)/(F(3,4)+F(3,5)); j=y+120; out['V4']=(j+y-1170,'y',y,'j',j,'total',j+y,'jia_left',j/4,'yi_left',y*F(2,5))
# V5 chain A=1.25B=1.5C=2D, B-D=18
for A in range(1,1000):
    B=F(A)/F(5,4); C=F(A)/F(3,2); D=F(A,2)
    if B-D==18: out['V5']=(A+B+C+D,'A,B,C,D',A,B,C,D,'BCD',B+C+D); break
# V6 AA: 甲1260 乙780 丙420 丁0 -> 甲 gets back
tot=1260+780+420; avg=F(tot,4); out['V6']=(1260-avg,'avg',avg,'yi',780-avg,'bing',420-avg)
# V7 bread: 甲5 乙3 箱, 丙 pays 48
each=F(8,3); g1=5-each; g2=3-each; out['V7']=(48*g1/(g1+g2),'by5:3',48*F(5,8),'yi',48*g2/(g1+g2))
# V8 maintenance 7200/yr ; first half by 5:4:3 (240 households: 100,80,60) ; 2nd half with D 60 households
h1=F(3600)*F(5,12); h2=F(3600)*F(100,300); out['V8']=(h1+h2,'h1',h1,'h2',h2,'all5/12',F(7200)*F(5,12),'all1/3',F(7200,3))
# V9 transfer: total 3600, jia-yi=840, after transfer yi-jia=160
mv=F(840+160,2); out['V9']=(mv,'nohalf',840+160,'diff',840-160)
# V10 two warehouses 120, step1 甲->乙 amount=乙 ; step2 乙->甲 amount=甲 ; final equal
for a in range(1,120):
    b=120-a
    a1,b1=a-b,2*b
    if a1<0: continue
    a2,b2=2*a1,b1-a1
    if a2==b2==60: out['V10']=(a,'b',b)
# V11 wind 35% ; PV = wind+10pp=45% ; storage rest 20% ; total 1600 ; PV - storage
out['V11']=(1600*F(45-20,100),'10pp',1600*F(10,100),'PV',1600*F(45,100),'storage',1600*F(20,100),'if PV=35%*1.1',None)
# V12 lychee 12, longan 8, wampee 6 ; l:lo=3:4, lo:w=6:5 -> 9:12:10 ; longan sales - wampee sales = 1800
k=F(1800,8*12-6*10); out['V12']=(12*9*k,'k',k,'qty',9*k,12*k,10*k,'longan',8*12*k,'wampee',6*10*k,'total',12*9*k+8*12*k+6*10*k)
# V13 three streets 180: 甲 = 1/2(乙+丙) ; 乙 = 1/3(甲+丙)
j=F(180,3); y=F(180,4); out['V13']=(180-j-y,'j',j,'y',y)
# V14 budget = 24 calc = 40 stapler = 60 box ; buy 15 box + 10 stapler -> calc
B=120; c=B/24; s=B/40; bx=B/60; out['V14']=((B-15*bx-10*s)/c,)
# V15 5000 CNY ; 100 CNY = 108 HKD ; 1 HKD = 1.03 MOP
out['V15']=(5000*F(108,100)*F(103,100),'HKD',5000*F(108,100),'wrongdiv',5000*F(108,100)/F(103,100),'direct',5000*F(103,100))
# V16 Sat+Sun 50 clients ; Sat amount =1.2 Sun amount ; Sat avg = 0.8 Sun avg ; total 880
qty_ratio=F(12,10)/F(8,10); sun=F(50)/(1+qty_ratio); sat=50-sun; sat_amt=F(880)*F(12,10)/(F(22,10)); sun_amt=880-sat_amt
out['V16']=(sat_amt/sat,'sun avg',sun_amt/sun,'overall',F(880,50),'sat,sun',sat,sun)
# V17 price down 20% -> +60 units ; original?
n=F(60)/(F(1)/F(8,10)-1); out['V17']=(n,'new',n+60,'wrong 60/0.2',F(60)/F(2,10))
# V18 big:mid:small counts 2:3:5, load 5:3:2, trips 3:4:6 ; small total 120 t
w=[2*5*3,3*3*4,5*2*6]; out['V18']=(F(120)*sum(w)/w[2],'parts',w,'no trips',F(120)*(2*5+3*3+5*2)/(5*2))
# V19 last yr p:n=1:4 ; p+10, n-2 -> 1:2 ; this yr p?
for k in range(1,100):
    if (k+10)*2==(4*k-2): out['V19']=(k+10,'last p',k,'this n',4*k-2,'this total',5*k+8)
# V20 A:B=5:3 ; each +40 -> 7:5
for k in range(1,200):
    if (5*k+40)*5==(3*k+40)*7: out['V20']=(5*k,'B',3*k,'A now',5*k+40)
# V21 out 20% then 30% of remaining -> 280 left
o=F(280)/(F(8,10)*F(7,10)); out['V21']=(o,'wrong additive',F(280)/F(5,10),'280/0.7',F(280)/F(7,10),'280/0.8',F(280)/F(8,10))
# V22 50 shots ; first30 80% ; first20 == last20 rate ; mid10 (21-30) hit 7
f30=30*F(8,10); f20=f30-7; out['V22']=(f20+7+f20,'50*80%',40)
# V23 each 6 -> +50 ; each 8 -> +10 ; then add people, each 5 exactly
n=F(50-10,8-6); T=6*n+50; out['V23']=(T/5-n,'n',n,'T',T,'T/5',T/5)
# V24 prices 80,60,50 ; 200 boxes ; 12100 ; A=2B
for b in range(1,100):
    a=2*b; c=200-3*b
    if c>=0 and 80*a+60*b+50*c==12100: out['V24']=(c,'a,b',a,b)
for k,v in out.items(): print(k,v)
