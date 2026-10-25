from itertools import permutations, product
P=['发改','教育','交通','文旅']; T=['单丛','普洱','红茶','绿茶']
L=lambda i:(i+1)%4; R=lambda i:(i-1)%4; O=lambda i:(i+2)%4
def allsol(conds):
    S=[]
    for seat in permutations(range(4)):
        st=dict(zip(P,seat))
        if st['发改']!=0: continue
        at={v:k for k,v in st.items()}
        for tea in permutations(T):
            t=dict(zip(P,tea)); w={v:k for k,v in t.items()}
            if all(c(st,at,t,w) for c in conds): S.append((st,t))
    return S
base=[lambda st,at,t,w: at[R(st['发改'])]=='交通', lambda st,at,t,w: st[w['普洱']]==O(st['教育'])]
found=[]
for side in ('左','右'):
    for X in P:
        for (e1p,e1t) in product(P,T):
            for (e2p,e2t) in product(P,T):
                if (e1p,e1t)>=(e2p,e2t): continue
                c3 = (lambda X=X: (lambda st,at,t,w: at[L(st[w['单丛']])]==X))() if side=='左' else (lambda X=X: (lambda st,at,t,w: at[R(st[w['单丛']])]==X))()
                c4 = (lambda a=e1p,b=e1t,c=e2p,d=e2t: (lambda st,at,t,w: t[a]!=b and t[c]!=d))()
                S=allsol(base+[c3,c4])
                if len(S)==1: found.append((side,X,(e1p,e1t),(e2p,e2t),S[0]))
print(len(found))
for f in found[:40]:
    st,t=f[4]; at={v:k for k,v in st.items()}
    print(f[0],f[1],f[2],f[3],[(at[i],t[at[i]]) for i in range(4)])
