from fractions import Fraction as F
import itertools, math
P=print
P('=== D29-V20 live-stream chain (5 sessions)')
# s2 = s1*(1+a) ; s2 = s3*(1-b) ; back(s4+s5) = k*front ; s5 = s4*(1+c) ; s5 - s3 = D ; ask s4 - s1
found=0
for a,b in [(F(1,4),F(1,5)),(F(1,5),F(1,6)),(F(1,2),F(1,4)),(F(1,4),F(1,6)),(F(1,3),F(1,5)),(F(2,5),F(1,8))]:
  for k in [2,F(3,2),3]:
    for c in [F(1,4),F(1,5),F(1,3),F(1,2),F(1,10)]:
      # choose s3 = 1 unit t
      s3=F(1); s2=s3*(1-b); s1=s2/(1+a); front=s1+s2+s3; back=k*front; s4=back/(2+c); s5=s4*(1+c)
      # scale t so that all integers and D moderate
      den=math.lcm(*[x.denominator for x in [s1,s2,s3,s4,s5]])
      vals=[x*den for x in [s1,s2,s3,s4,s5]]
      D=vals[4]-vals[2]
      if D>0:
        # scale factor m so that D*m in [20,200]
        for m in range(1,20):
          if 20<=D*m<=300 and found<12:
            v=[int(x*m) for x in vals]
            P('a',a,'b',b,'k',k,'c',c,'sessions',v,'s5-s3',v[4]-v[2],'ask s4-s1',v[3]-v[0])
            found+=1; break
P('=== D29-V23 data center: x+y+z=N ; x*pa+y*pb+z*pc=P ; next: remove A, B*fb, C*fc, power P2')
res=[]
for pa,pb,pc in [(1,2,4),(1,2,5),(1,3,5),(2,3,5),(1,3,4)]:
  for fb,fc in [(F(3,2),F(3,2)),(2,2),(F(3,2),2),(2,F(3,2)),(F(5,4),F(3,2))]:
    for N in range(100,301,10):
      for z in range(1,N):
        for y in range(1,N-z):
          x=N-y-z
          P1=x*pa+y*pb+z*pc
          P2=fb*y*pb+fc*z*pc
          if P2==P1 and fb*y==int(fb*y) and fc*z==int(fc*z):
            res.append((pa,pb,pc,str(fb),str(fc),N,x,y,z,P1))
seen=set()
for r in res:
    if r[:6] in seen: continue
    seen.add(r[:6]); P(r)
