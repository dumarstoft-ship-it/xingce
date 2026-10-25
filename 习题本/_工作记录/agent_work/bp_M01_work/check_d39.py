from fractions import Fraction as F
import math, itertools
P=print
out={}
# V1 desalination: fresh 0.45, brine 0.55 per m3 ; brine - fresh = 1802 -> fresh?
sea=F(1802)/F(10,100); fresh=sea*F(45,100); out['V1']=(fresh,'approx 1800 ->',F(1800)/F(10,100)*F(45,100))
# V2 carbon points with caps
walk=min(15,10)*30; metro=min(3*2,4)*22; bike=6*F(1,2)*8; pts=walk+metro+bike
out['V2']=(pts//100*5,'pts',pts,'nocap',(15*30+6*22+bike)//100*5,'only metro cap',(15*30+4*22+bike)//100*5,'no 100 rule',pts*F(5,100))
# V5 trip split
oil=F(840,4); room=F(600,4)  # two rooms 300 each, 2 people each -> 150
out['V5']=(oil+room,)
# V6 elevator: floors2-6 coef1..5, 2 households each, 54 wan ; prepaid 3 each
unit=F(54)/(2*sum(range(1,6))); out['V6']=(5*unit-3,'unit',unit,'6F share',5*unit)
# V7 rotation 4 companies brute force
hits=set()
for Bn in range(3,25):
    A=Bn+2; C=A+3; D=A-1; avg=F(A+Bn+C+D,4)
    if avg!=int(avg): continue
    for a in range(0,A+1):
        for b in range(0,Bn+1):
            for c in range(0,C+1):
                for d in range(0,D+1):
                    if A-a+d==avg and Bn-b+a==avg and C-c+b==avg and D-d+c==avg: hits.add(c-b)
out['V7']=('c-b',hits)
# V8 warehouses 600: step1 甲 gives 1/4 of itself to 乙 ; step2 乙 gives 1/3 of current to 丙 ; final 3:4:5
for a in range(4,600,4):
    for b in range(0,600-a):
        c=600-a-b
        a1=a-a//4; b1=b+a//4
        if b1%3: continue
        b2=b1-b1//3; c2=c+b1//3
        if a1*4==b2*3 and b2*5==c2*4: out['V8']=(b,'a,c',a,c)
# V10 industry
out['V10']=(1000*F(108,100)-800*F(105,100),)
# V11 MOP 2781 -> HKD -> CNY + 1% fee
hkd=F(2781)/F(103,100); cny=hkd*100/108; out['V11']=(cny*F(101,100),'hkd',hkd,'cny',cny)
# V12
B=60; A=B/20; Bp=B/30; C=(B-8*A-12*Bp)/10; out['V12']=(B/C,)
# V13
cl=[15,20,25]; am=[F(1200)*x/12 for x in [4,5,3]]; out['V13']=(am[2]/cl[2],'avgs',[a/c for a,c in zip(am,cl)])
# V14 n,p : 1.25n(p-30)=np ; (n-6)(p+50)=np
for n in range(7,200):
    for p_ in range(31,1000):
        if F(5,4)*n*(p_-30)==n*p_ and (n-6)*(p_+50)==n*p_: out['V14']=(n*p_,'n,p',n,p_)
# V15
s24=F(22)/(F(125,100)*F(88,100)); orders24=s24*10**8/200; out['V15']=(orders24*F(125,100)/10**4,'sales24',s24,'orders24(wan)',orders24/10**4)
# V16
for k in range(1,200):
    if (3*k-20)*6==(2*k+20)*7: tot=5*k; a1,b1=3*k-20,2*k+20; out['V16']=(a1-tot*6//13,'k',k,'after1',a1,b1,'tot',tot)
# V17
for k in range(1,100):
    last_m,last_f=5*k,4*k; this_tot=F(5,4)*9*k; this_m=this_tot*F(4,9); this_f=this_tot*F(5,9)
    if this_f-last_f==36 and this_m==int(this_m): out['V17']=(this_m,'last',last_m,last_f,'this f',this_f)
# V18
a=F(2); Am,Af,Bm,Bf=4*a,a,2*a,3*a; Ap=F(2,5)*5*a; Apm,Apf=Ap*F(3,4),Ap*F(1,4); Bpf=4*Apf; Bpm=Bpf/2
out['V18']=((Apm+Bpm)/(Apf+Bpf),'check B female party<=B female',Bpf<=Bf)
# V19
for k in range(1,1000):
    if (5*k-160)*5==(4*k-200)*7: tot=9*k; out['V19']=(200-80,'total',tot,'fail m,f',5*k-160,4*k-200)
# V20
B=F(36+4,10)/(1-F(3,10)-F(2,10)-F(3,10)) # 0.2B = 4 -> B in wan
books=F(3,10)*B*10000/30; out['V20']=(books*F(5,4),'B',B,'bought',books)
# V21
f30=30*F(9,10); l30=30*F(8,10); out['V21']=((f30+l30-10)/50,)
# V23
share_exp=F(6,12); r=(8-12*share_exp)/(1-share_exp); out['V23']=(r,)
# V25
for n in range(1,60):
    if 45*n+30==48*(n-1)+33: st=45*n+30; out['V25']=(math.ceil(st/40)-n,'n',n,'students',st)
# V26
a=F(1); b=F(3,2)*a; c=3*a-b; assert 3*a+2*b==4*c
out['V26']=(F(2400)*b/(a+b+c),'ratio',(a,b,c))
# V28
for b in range(2,40,2):
    # need b(p-30)=400 with integer p
    p_=F(400,b)+30
    a1=40-b
    if p_==int(p_) and b%2==0:
        c2=30*(50-F(b,2))+p_*F(b,2); c3=30*(60-F(3*b,2))+p_*F(3*b,2)
        out.setdefault('V28',set()).add((c2,c3))
# V29
post=F(500)/F(20,100); pre=post-500; val=post*F(15,10); jia_val=val*F(80,100); post2=jia_val/F(60,100); out['V29']=(post2-val,'post1',post,'val',val)
for k,v in out.items(): P(k,v)

P('=== V22 harder live chain: 6 sessions, mixed relations, range options')
# s2 = s1*(1+a); s2 = s3*(1-b); back3 = k*front3; s5 = tot*share; s5 = s4*(1+c); s6 - s5 = D ; ask s6 - s3
for a,b in [(F(1,4),F(1,5)),(F(1,5),F(1,6)),(F(3,5),F(1,5)),(F(1,2),F(1,4))]:
  for k in [2,3]:
    for share in [F(1,5),F(1,4),F(3,10)]:
      for c in [F(1,4),F(1,5),F(1,10),F(1,8)]:
        s3=F(1); s2=s3*(1-b); s1=s2/(1+a); front=s1+s2+s3; back=k*front; tot=front+back
        s5=tot*share; s4=s5/(1+c); s6=back-s4-s5
        if s6<=0 or s6<=s5: continue
        D=s6-s5; t=F(20)/D  # scale so that s6-s5=20
        vals=[x*t for x in [s1,s2,s3,s4,s5,s6]]
        if all(v.denominator<=10 for v in vals):
          P('a',a,'b',b,'k',k,'share',share,'c',c,'vals',[float(v) for v in vals],'ask s6-s3',float(vals[5]-vals[2]))
P('=== V24 two goods (milk m, eggs e) per home ; n homes')
for (m1,e1,rem_diff) in [(6,4,18),(6,4,20),(5,3,16),(8,5,15)]:
  for (m2,e2,sm,se) in [(8,5,6,3),(8,5,5,4),(7,5,10,8),(9,6,8,2),(10,6,7,9)]:
    for n in range(5,60):
        M=m2*n-sm; E=e2*n-se
        if M-m1*n-(E-e1*n)==rem_diff and M>0 and E>0:
            best=None
            for kk in range(1,100):
                # ratio milk:eggs = 3:2 per home: 3kk milk, 2kk eggs
                if 3*kk*n>=M and 2*kk*n>=E:
                    buy=3*kk*n-M+2*kk*n-E; best=(buy,kk); break
            P('m1,e1,diff',m1,e1,rem_diff,'m2,e2,short',m2,e2,sm,se,'n',n,'M,E',M,E,'best (buy,k)',best)
P('=== V27 elder beds: x self-care 1:10, y assisted 1:5, z disabled 1:2 ; total beds N ; caregivers C ; next year: self-care all converted to assisted, disabled +50%, total beds increases accordingly, caregivers C2')
for N in range(100,401,20):
  for z in range(10,N,2):
    for y in range(10,N-z,5):
        x=N-y-z
        if x<10 or x%10: continue
        C=F(x,10)+F(y,5)+F(z,2)
        if C!=int(C): continue
        C2=F(x+y,5)+F(3*z,4)
        if C2!=int(C2): continue
        # ask z given N, C, C2: unique? linear system x+y+z=N ; x/10+y/5+z/2=C ; (x+y)/5+3z/4=C2
        # det check
        import numpy as np
        A=np.array([[1,1,1],[0.1,0.2,0.5],[0.2,0.2,0.75]]);
        if abs(np.linalg.det(A))<1e-9: continue
        if N==200 and C in (40,45,50,55,60):
            P('N',N,'x,y,z',x,y,z,'C',C,'C2',C2)
P('=== V30 coop dividend')
for total_shares in [2000,2500,4000,5000]:
  for cash_shares in [400,500,800,1000]:
    for guarantee in [10,20,25,50]:
      for profit in [400000,500000,600000]:
        dist=F(profit)*F(8,10)
        rest=dist-cash_shares*guarantee
        per=rest/total_shares
        zhang=4*guarantee+10*per   # 6 mu land=6 shares, 4000 cash=4 shares -> total 10 shares; cash 4 get guarantee
        if per==int(per) and zhang==int(zhang):
            P(total_shares,cash_shares,guarantee,profit,'per',per,'zhang',zhang,'no guarantee',dist/total_shares*10)
