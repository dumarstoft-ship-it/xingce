from fractions import Fraction as F
from math import ceil, floor, gcd
res=[]
for a1 in range(1,7):
 for b1 in range(1,9):
  for t1 in range(2,7):
   for a2 in range(1,7):
    for b2 in range(1,9):
     for t2 in range(2,7):
      if t1==t2: continue
      if (a1,b1)==(a2,b2): continue
      x=a1*t1-a2*t2; y=b2*t2-b1*t1   # x B = y S
      if x<=0 or y<=0: continue
      g=gcd(x,y); Bp,Sp=y//g,x//g    # B:S = y:x
      if not (Bp>Sp): continue
      if Bp>6: continue
      W=t1*(a1*Bp+b1*Sp)
      assert W==t2*(a2*Bp+b2*Sp)
      # reversed ratio
      Br,Sr=Sp,Bp; Wr=t1*(a1*Br+b1*Sr)
      # ignore trips: a1 B + b1 S = a2 B + b2 S
      xi=a1-a2; yi=b2-b1
      ign=None
      if xi>0 and yi>0:
          gi=gcd(xi,yi); Bi,Si=yi//gi,xi//gi
          ign=(Bi,Si)
      for c in range(1,9):
        for d in range(0,9):
          if c+d==0: continue
          if (c,d) in ((a1,b1),(a2,b2)): continue
          cap=c*Bp+d*Sp
          q=F(W,cap)
          if q.denominator==1: continue
          ans=ceil(q)
          if not (3<=ans<=9): continue
          fl=floor(q)
          rv=ceil(F(Wr,c*Br+d*Sr))
          ig=None
          if ign:
              Bi,Si=ign
              ig1=ceil(F(t1*(a1*Bi+b1*Si),c*Bi+d*Si)); ig2=ceil(F(t2*(a2*Bi+b2*Si),c*Bi+d*Si))
              ig=(ig1,ig2)
          res.append(((a1,b1,t1),(a2,b2,t2),(Bp,Sp),W,(c,d),q,ans,fl,rv,ig))
print(len(res))
# want: rv distinct from ans and fl, plausible (<= ans+4); ig present with value distinct
cnt=0
for r in res:
    s1,s2,ratio,W,cd,q,ans,fl,rv,ig=r
    if rv in (ans,fl) or rv>ans+4 or rv<2: continue
    if not ig or ig[0]!=ig[1] or ig[0] in (ans,fl,rv) or ig[0]>ans+4: continue
    if cd[1]!=0: continue
    cnt+=1
    print(s1,s2,'B:S',ratio,'W',W,'ask',cd,'W/cap',q,float(q),'ans',ans,'floor',fl,'rev',rv,'ignore',ig)
print(cnt)
