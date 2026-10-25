import itertools, math
def pts(A,B,C,p,q,r):
    D=(B[0]+p*(B[0]-A[0]), B[1]+p*(B[1]-A[1]))
    E=(C[0]+q*(C[0]-B[0]), C[1]+q*(C[1]-B[1]))
    F=(A[0]+r*(A[0]-C[0]), A[1]+r*(A[1]-C[1]))
    return D,E,F
def area(P,Q,R):
    return abs((Q[0]-P[0])*(R[1]-P[1])-(R[0]-P[0])*(Q[1]-P[1]))/2
def minangle(P,Q,R):
    def ang(X,Y,Z):
        v=(Y[0]-X[0],Y[1]-X[1]); w=(Z[0]-X[0],Z[1]-X[1])
        c=(v[0]*w[0]+v[1]*w[1])/math.hypot(*v)/math.hypot(*w)
        return math.degrees(math.acos(max(-1,min(1,c))))
    return min(ang(P,Q,R),ang(Q,R,P),ang(R,P,Q))
best=[]
for (p,q,r) in set(itertools.permutations((1,2,4))):
    for ax in [x/10 for x in range(-10,21)]:
        for ay in [y/10 for y in range(3,21)]:
            A=(ax,ay); B=(0,0); C=(1,0)
            D,E,F=pts(A,B,C,p,q,r)
            s=area(A,B,C); T=area(D,E,F)
            ma=minangle(D,E,F); mb=minangle(A,B,C)
            xs=[P[0] for P in (D,E,F)]; ys=[P[1] for P in (D,E,F)]
            w=max(xs)-min(xs); h=max(ys)-min(ys)
            aspect=max(w,h)/min(w,h)
            best.append((-(ma+0.5*mb)+5*abs(aspect-1.3),p,q,r,A,round(ma,1),round(mb,1),round(aspect,2),round(T/s,3)))
best.sort()
for b in best[:15]: print(b)
