import itertools
def rots():
    # all 24 proper rotation matrices
    mats=[]
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product([1,-1],repeat=3):
            m=[[0]*3 for _ in range(3)]
            for i in range(3): m[i][perm[i]]=signs[i]
            # determinant
            det=(m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
            if det==1: mats.append(m)
    return mats
R=rots()
def norm(cells):
    mx=min(c[0] for c in cells); my=min(c[1] for c in cells); mz=min(c[2] for c in cells)
    return tuple(sorted((x-mx,y-my,z-mz) for x,y,z in cells))
def orients(cells):
    out=set()
    for m in R:
        out.add(norm([tuple(sum(m[i][k]*c[k] for k in range(3)) for i in range(3)) for c in cells]))
    return out
X,Y,Z=3,3,2
box=[(x,y,z) for x in range(X) for y in range(Y) for z in range(Z)]
def placements(cells):
    pl=set()
    for o in orients(cells):
        for dx in range(X):
            for dy in range(Y):
                for dz in range(Z):
                    s=[(a+dx,b+dy,c+dz) for a,b,c in o]
                    if all(0<=a<X and 0<=b<Y and 0<=c<Z for a,b,c in s): pl.add(frozenset(s))
    return list(pl)
P={
 'L':[(0,0,0),(1,0,0),(2,0,0),(2,1,0)],
 'O':[(0,0,0),(1,0,0),(0,1,0),(1,1,0)],
 'S':[(0,0,0),(0,1,0),(1,1,0),(1,2,0)],
 'I2':[(0,0,0),(0,0,1)],
}
opts={
 'A_tripod':[(0,0,0),(1,0,0),(0,1,0),(0,0,1)],
 'B_T':[(0,0,0),(1,0,0),(2,0,0),(1,0,1)],
 'C_L':[(0,0,0),(0,1,0),(0,2,0),(1,2,0)],
 'D_O':[(0,0,0),(1,0,0),(0,1,0),(1,1,0)],
}
def solve(pieces):
    names=list(pieces)
    pls={n:placements(pieces[n]) for n in names}
    sols=[]
    def rec(i,used,chosen):
        if i==len(names):
            if len(used)==len(box): sols.append(dict(chosen))
            return
        n=names[i]
        for p in pls[n]:
            if used.isdisjoint(p):
                chosen[n]=p; rec(i+1,used|p,chosen); del chosen[n]
    rec(0,frozenset(),{})
    return sols
for k,v in opts.items():
    pcs=dict(P); pcs['X']=v
    s=solve(pcs)
    print(k, 'solutions:', len(s))
    if s:
        sol=s[0]
        for z in range(Z):
            print('  layer',z)
            for y in range(Y):
                print('   ', ' '.join(next(n for n,c in sol.items() if (x,y,z) in c).ljust(2) for x in range(X)))
