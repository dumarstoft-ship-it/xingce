import itertools, math
from fig2_gen import pts
def area(P,Q,R): return abs((Q[0]-P[0])*(R[1]-P[1])-(R[0]-P[0])*(Q[1]-P[1]))/2
def angs(P,Q,R):
    def ang(X,Y,Z):
        v=(Y[0]-X[0],Y[1]-X[1]); w=(Z[0]-X[0],Z[1]-X[1])
        c=(v[0]*w[0]+v[1]*w[1])/math.hypot(*v)/math.hypot(*w)
        return math.degrees(math.acos(max(-1,min(1,c))))
    return (ang(P,Q,R),ang(Q,R,P),ang(R,P,Q))
res=[]
p,q,r=2,1,4
for ax in [x/20 for x in range(-20,41)]:
    for ay in [y/20 for y in range(4,41)]:
        A=(ax,ay); B=(0,0); C=(1,0)
        D,E,F=pts(A,B,C,p,q,r)
        a1=min(angs(D,E,F)); a2=min(angs(A,B,C))
        # side length ratios of ABC (avoid near-degenerate)
        res.append((round(a1+0.8*a2,1),A,round(a1,1),round(a2,1)))
res.sort(reverse=True)
for x in res[:12]: print(x)
