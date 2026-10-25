from fractions import Fraction as F
import math
out={}
# V1 rice 116/100g x200, broccoli 34/100g x300, chicken 132/100g x g ; jog 76 kcal per 10 min, 70 min
need=76*7; g=(need-F(116*200,100)-F(34*300,100))/F(132,100); out['V1']=(g,'kcal need',need)
# V2
for x in range(1,100):
    mon=4*x; tue=5*x; wed=mon+tue-30
    if mon+tue+wed==150:
        thu=F(7,4)*mon; fri=thu-15; d=[mon,tue,wed,thu,fri]; out['V2']=(max(d)-min(d),d,'first3 diff',max(d[:3])-min(d[:3]))
# V3 8 big ; +12 small -> +75% ; 10 big equivalent small
big_in_small=F(12)/(F(75,100)*8); out['V3']=(10*big_in_small,'big=',big_in_small,'small')
# V4
for x in range(1,200):
    orig=[x-6,x+4,F(2*x,3),F(3*x,2),x]
    if sum(orig)-3==5*x and all(o==int(o) and o>0 for o in orig): out['V4']=(max(orig)-min(orig),orig)
# V5 forward check
def ops(a,b,c):
    a,b=a-b,2*b; b,c=b-c,2*c; c,a=c-a,2*a; return a,b,c
for a in range(1,180):
    for b in range(1,180-a):
        c=180-a-b
        if ops(a,b,c)==(40,60,80): out['V5']=(a,b,c)
# V6
edu=F(36)/F(25,100); ms=edu/F(30,100); tot=ms/F(60,100); out['V6']=(tot+36,'orig total',tot,'edu',edu,'new edu share',(edu+36)/(tot+36))
# V7
T=F(2)/(F(1,3)-F(1,5)); done=T/5; done2=done+4; out['V7']=(done2/(T-done2),'T',T)
# V8
k=F(75,15); out['V8']=(k*3000+4*k*1500+10*k*500,'k',k)
# V9
x=(45-F(120,5))*2; out['V9']=(x,'new nurses',45-30)
# V10
for k in range(1,50):
    if 3*k+4==2*(2*k-1): out['V10']=(9*k,'k',k,[4*k-3,3*k+4,2*k-1])
# V11
for B in range(1,500):
    A=F(5,4)*B
    if A==int(A) and (B+10)==F(6,5)*(A-10): out['V11']=(A,'B',B)
# V12 cross
pa=F(3,5); pb=F(1,4); pt=F(1,2); out['V12']=((pt-pb)/(pa-pt),)
# V13
for k in range(1,100):
    if 4*(7*k-80)==5*(8*k-100): tot=15*k
opts=[225,240,255,300]; out['V13']=(tot,[o for o in opts if (o-180)%9==0 and o%15==0])
# V14
for a in range(1,50):
    for b in range(1,50):
        if (5*a+3*b)*5==(3*a+2*b)*8: rel=(a,b); break
out['V14']=('a=b' if rel[0]==rel[1] else rel, 'jia huji', F(25,10)/5*5*F(1,1)*F(1,1) )
a=F(25,10)/5; out['V14']=('a=b',rel,'甲户籍(万)',5*a,'甲总',8*a,'乙总',5*a)
# V15
o=F(54)/(F(75,100)*F(12,10)*F(6,10)); out['V15']=(o,'ignore night',F(54)/(F(75,100)*F(6,10)),'skip day1',F(54)/F(6,10)/F(12,10))
# V16
pub=F(35000); pri=F(15000); newtot=pri/F(25,100); out['V16']=(newtot-50000,)
# V17
r=(F(15)-9)/(9-6); jia=F(90)*r/(1+r); yi=90-jia; out['V17']=(yi*F(115,100),'jia,yi base',jia,yi)
# V19
r=(F(12)-6)/(15-12); share=r/(1+r); out['V19']=(15*share,'share export',share)
# V20
L=(3*120-2*105)/F(5); S_=(120-3*L)/2; out['V20']=(math.floor(200/L),'L,S',L,S_)
# V21
T=F(186+170+175+165,3); out['V21']=(T-186,'T',T,[T-186,T-170,T-175,T-165])
# V22 general solution check
sols=[]
for A in range(1,100):
    C=A-40; B=150-2*A
    if B>0 and C>0: sols.append((A,B,C,A+B+C))
out['V22']=(set(s[3] for s in sols),sols[:3])
# V23
out['V23']=(F(750,5)+F(400,5),'all/5',F(900+750+400,5))
# V24
k=F(1140,38); out['V24']=(4*k-3*k,'rice,flour',4*k,3*k)
# V25
duck=6*F(5,2)+9; out['V25']=(duck*F(7,3),'forgot 9 ducks',6*F(5,2)*F(7,3),'ducks only',9*F(7,3))
for k,v in out.items(): print(k,v)
# --- search for V18: A,B,C firms
print('--- V18 search')
res=[]
for total_g in [F(20,100),F(25,100),F(30,100)]:
  for dA in [100,200,300,400,500,600]:
    for pB in [F(10,100),F(20,100),F(25,100)]:
      for qC in [F(20,100),F(25,100),F(30,100),F(40,100),F(50,100)]:
        for b25 in range(10,3000,10):
            a25=2*b25; a24=a25-dA; b24=b25/(1-pB); c24=a24+b24; c25=c24*(1+qC)
            if a24<=0: continue
            if b24!=int(b24) or c25!=int(c25): continue
            if a25+b25+c25==(1+total_g)*(a24+b24+c24):
                res.append((total_g,dA,pB,qC,b25,a24,b24,c24,c25,a24-b24))
for r in res[:40]: print([str(x) for x in r])
