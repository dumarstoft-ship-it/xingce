import itertools
# x: left->right (1..4), y: front(1)/back(2), z: bottom->top (1..3)
S={(x,y,z) for x in range(1,5) for y in (1,2) for z in range(1,4)} - {(3,1,2),(3,1,3),(4,1,3)}
assert len(S)==21
opts={
 'A':{(1,1,1),(2,1,1),(2,1,2),(1,2,1),(2,2,1),(1,2,2),(2,2,2)},
 'B':{(1,1,1),(2,1,1),(3,1,1),(2,1,2),(1,2,1),(2,2,1),(1,2,2)},
 'C':{(1,1,1),(2,1,1),(3,1,1),(1,2,1),(2,2,1),(2,2,2),(2,2,3)},
 'D':{(1,1,1),(2,1,1),(1,2,1),(2,2,1),(3,2,1),(1,2,2),(2,2,2)},
}
def mats(allow_reflect):
    res=[]
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1,-1),repeat=3):
            M=[[0]*3 for _ in range(3)]
            for i in range(3): M[i][perm[i]]=signs[i]
            det=(M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
            if det==1 or allow_reflect: res.append(M)
    return res
def orients(shape, allow_reflect):
    out=set()
    for M in mats(allow_reflect):
        pts=[tuple(sum(M[i][j]*p[j] for j in range(3)) for i in range(3)) for p in shape]
        mn=[min(p[i] for p in pts) for i in range(3)]
        out.add(frozenset(tuple(p[i]-mn[i] for i in range(3)) for p in pts))
    return out
def placements(shape, allow_reflect):
    pl=[]
    for o in orients(shape, allow_reflect):
        for dx in range(0,5):
            for dy in range(0,3):
                for dz in range(0,4):
                    p=frozenset((a+dx,b+dy,c+dz) for a,b,c in o)
                    if p<=S: pl.append(p)
    return list(set(pl))
def tilings(pl):
    sols=[]
    cells=sorted(S)
    def rec(rem, chosen):
        if not rem: sols.append(list(chosen)); return
        c=min(rem)
        for p in pl:
            if c in p and p<=rem:
                chosen.append(p); rec(rem-p, chosen); chosen.pop()
    rec(frozenset(S), [])
    return sols
for refl in (False, True):
    print('allow_reflect', refl)
    for k,v in opts.items():
        pl=placements(v, refl)
        sols=tilings(pl)
        print(' ',k,'placements',len(pl),'tilings',len(sols))
        if sols:
            for p in sols[0]: print('    ',sorted(p))
