from fractions import Fraction as F
print('--- V17 (fast)')
cands=[]
for p1,p2 in [(F(1,3),F(1,4)),(F(2,5),F(1,3)),(F(1,2),F(1,3)),(F(3,5),F(1,2)),(F(1,4),F(1,5)),(F(2,3),F(1,2)),(F(3,5),F(3,4))]:
  for q1,q2 in [(F(1,2),F(2,3)),(F(1,2),F(1,3)),(F(1,3),F(1,2)),(F(3,4),F(1,2)),(F(1,4),F(1,2)),(F(2,3),F(1,4)),(F(1,2),F(3,4)),(F(1,3),F(2,3))]:
    for d in [2,3,4,5,6]:
      for tr in range(20,61):
        a=q1*(1-p1); b=q2*(1-p2)
        det=p1*b+p2*a
        x=(d*b+p2*tr)/det; y=(p1*tr-a*d)/det
        if x>0 and y>0 and x==int(x) and y==int(y):
          vals=[p1*x,p2*y,a*x,b*y]
          if all(v==int(v) for v in vals) and 30<=x<=150 and 30<=y<=150:
            cands.append((p1,p2,q1,q2,d,tr,int(x),int(y),int(x-y)))
seen=set()
for c in cands:
    key=c[:4]
    if key in seen: continue
    seen.add(key); print([str(v) for v in c])
