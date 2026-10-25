from fractions import Fraction as F
from math import gcd, lcm
print("== 2-4-1 (c != 3) ==")
res=[]
for z in range(2,10):
  for l in range(1,z):
    if gcd(z,l)!=1 or (z,l)==(3,2): continue
    for a in range(3,12):
      for b in range(3,14):
        W=z*a+l*b
        for c in range(1,a):
          if c==3: continue
          rem=W-(z+l)*c
          if rem<=0 or rem%l: continue
          d=rem//l
          if d<=0 or d>15: continue
          Tz=F(W,z); Tl=F(W,l)
          if Tz.denominator!=1: continue
          if d-b<=0 or c+d-b<=0: continue
          z1,l1=d-b,a-c; g=gcd(z1,l1); z1//=g; l1//=g; T1=F(z1*a+l1*b,z1)
          z2,l2=c+d-b,a; g=gcd(z2,l2); z2//=g; l2//=g; T2=F(z2*a+l2*b,z2)
          vals=[Tz,Tl,T1,T2]
          if len(set(vals))<4: continue
          if not all(v.denominator==1 for v in vals): continue
          if not Tz<min(Tl,T1,T2): continue
          if max(vals)>2.2*Tz: continue
          res.append((z,l,a,b,c,d,W,[str(v) for v in vals]))
for r in res: print(r)

print("== 2-3-3 weekday ==")
W7=['一','二','三','四','五','六','日']
def finish(p,q,Wt,mode):
    done=0; day=0
    while True:
        wd=day%7  # 0=Mon
        if mode=='correct': r=(p+q) if wd<5 else (p if wd==5 else 0)
        elif mode=='norest': r=p+q
        elif mode=='bothweekend': r=(p+q) if wd<5 else 0
        elif mode=='bothsat': r=(p+q) if wd<6 else 0
        done+=r; day+=1
        if done>=Wt: return day, W7[(day-1)%7], done==Wt
for A in range(10,40):
  for B in range(A+1,61):
    if (A,B)==(20,30): continue
    Wt=lcm(A,B); p=Wt//A; q=Wt//B
    out={m:finish(p,q,Wt,m) for m in ['correct','norest','bothweekend','bothsat']}
    wds=[out[m][1] for m in out]
    if len(set(wds))<4: continue
    if '日' in wds: continue
    if out['correct'][0]>24 or out['correct'][0]<9: continue
    print(A,B,Wt,p,q,out)
