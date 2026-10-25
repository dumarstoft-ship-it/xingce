from fractions import Fraction as F
import math, itertools
out={}
# V1 honey biscuits
honey_g=1500*F(14,10); per=15*F(3,100); biscuits=honey_g/per; out['V1']=(math.floor(biscuits/20),'biscuits',biscuits)
# V2 宣讲: singles 2t+4, pairs 2t, triples t ; total 39
for t in range(1,20):
    if 5*t+4==39: s1,s2,s3=2*t+4,2*t,t
p=None
for pp in range(0,15):
    if pp+(pp+2)+2*pp==s2: p=pp
ab,ac,bc=p,p+2,2*p
for s in range(0,20):
    if 3*s+3==s1: sa=s
out['V2']=('jia appearances',sa+ab+ac+s3,'renci',s1+2*s2+3*s3,'singles/pairs/triples',(s1,s2,s3),'pairs',(ab,ac,bc),'singles',(sa,sa,sa+3))
# V3
out['V3']=(60*F(7-3,(7-3)+(5-3)),)
# V4
out['V4']=(F(3600)*20/(30+30+20+10),)
# V5 symbolic check by brute force: B's patrol m, answer a-m
hits=set()
for B in range(3,30):
    A=B+3; C=A+6; avg=F(A+B+C,3)
    for a in range(0,A+1):
        for b in range(0,B+1):
            for c in range(0,C+1):
                if A-a+c==avg and B-b+a==avg and C-c+b==avg: hits.add(a-b)
out['V5']=('a-b',hits)
# V6 reverse doubling
def fwd(a,b,c):
    # 甲 gives so 乙,丙 double
    a=a-b-c; b,c=2*b,2*c
    b=b-a-c; a,c=2*a,2*c
    c=c-a-b; a,b=2*a,2*b
    return a,b,c
for a in range(1,96):
    for b in range(1,96-a):
        c=96-a-b
        if fwd(a,b,c)==(32,32,32): out['V6']=(a,b,c)
# V7
for j in range(4,300,4):
    for y in range(6,300,6):
        if F(j,4)+F(y,6)==26 and (F(j,2)+F(y,3))-(F(j,4)+F(y,2))==4: out['V7']=(j,y)
# V8 tools: T ; (jia-10) = 1/4 (others) ; (yi-10)=1/3 others
for T in range(20,1000):
    j=F(T-10,5)+10; y=F(T-10,4)+10; c=T-j-y
    if j==int(j) and y==int(y) and c>0 and T==210: out['V8']=(c,'j,y',j,y)
# V9
B=90; A=B/30; Bp=B/45; C=A*F(2,3); out['V9']=((B-18*A-9*C)/Bp,)
# V11
for s in range(0,19):
    d=18-s
    if 4*d==2*(2*s): boys=(2*s-10)+30; girls=10+(4*d-30); out['V11']=(boys-girls,'s,d',s,d,boys,girls)
# V12
n=F(15)/(F(1)/F(8,10)-1); x=(n/48-1)*100; out['V12']=(x,'n',n)
# V13
for t in range(1,100):
    k=1
    # 7k - t : 3k - t = 5:1  -> with k scaled
for k in range(1,50):
    for t in range(1,7*k):
        if (7*k-t)*1==(3*k-t)*5: out['V13']=(F(2*t,10*k),'k,t',k,t)
# V14
for k in range(1,100):
    if (7*k-6)*7==(5*k+6)*9: tot=12*k; out['V14']=((7*k-6)-tot//2,'k',k,'after',7*k-6,5*k+6)
# V15 ratio
k=F(1); jm,jf=6*k,4*k; jpm,jpf=jm/3,jf/2; jp=jpm+jpf; yp=F(12,10)*jp; ypm,ypf=yp*F(3,4),yp*F(1,4)
out['V15']=((jpm+ypm)/(jpf+ypf),)
# V16
for b in range(1,100):
    a=2*b
    if 5*a-4*b==30: out['V16']=(5*a+4*b,'a,b',a,b)
# V18
B=F(6+2)/(1-F(45,100)-F(45,100)*F(6,10)-F(45,100)*F(6,10)/F(135,100)); out['V18']=(F(45,100)*F(6,10)*B,'B',B,'decor',F(45,100)*F(6,10)/F(135,100)*B)
# V19
for x in range(0,801):
    y=800-x
    if F(1,10)*x+F(1,4)*y==140: out['V19']=(F(9,10)*x-F(3,4)*y,'x,y',x,y)
# V21
T=F(240); a=T/20; b=T/30; c=T/8-a-b; out['V21']=(T/c,)
# V22
for n in range(1,200):
    T=6*n+30
    if F(5,4)*T==8*n+10: T2=F(16,10)*T; per=T2/(n+5); out['V22']=(math.floor(per),'n,T',n,T,'T2',T2,'per',per)
# V25
out['V25']=(F(176+276,5),)
# V26
out['V26']=(F(14)/(50*F(7,10)),)
# V27
tech=F(8,10)*300-100; out['V27']=((100+tech)/360,'tech',tech)
for k,v in out.items(): print(k,v)

print('--- V10 search cross-border')
for usd in [1000,1500,2000,2500,3000,4000,5000]:
  for fee in [F(1,100),F(2,100),F(25,1000),F(3,100),F(4,100),F(5,100)]:
    for rate in [F(71,10),F(72,10),F(70,10),F(715,100),F(725,100)]:
      for part in [F(1,4),F(1,3),F(2,5),F(1,2),F(3,5),F(3,4)]:
        for hk in [F(108,100),F(109,100),F(110,100),F(107,100)]:
          cny=usd*(1-fee)*rate; h=cny*part*hk
          if cny==int(cny) and h==int(h) and usd*(1-fee)==int(usd*(1-fee)):
              print(usd,fee,rate,part,hk,'cny',cny,'hkd',h)
