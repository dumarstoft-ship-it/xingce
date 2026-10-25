from itertools import permutations
P=['发改','教育','交通','文旅']; T=['单丛','普洱','红茶','绿茶']
L=lambda i:(i+1)%4; R=lambda i:(i-1)%4; O=lambda i:(i+2)%4
def run(conds, fix_first=True):
    S=[]
    for seat in permutations(range(4)):
        st=dict(zip(P,seat))
        if fix_first and st['发改']!=0: continue   # 消去旋转对称
        at={v:k for k,v in st.items()}
        for tea in permutations(T):
            t=dict(zip(P,tea)); w={v:k for k,v in t.items()}
            if all(c(st,at,t,w) for c in conds): S.append((st,t))
    return S
conds=[
 lambda st,at,t,w: at[R(st['发改'])]=='交通',
 lambda st,at,t,w: st[w['普洱']]==O(st['教育']),
 lambda st,at,t,w: at[L(st[w['单丛']])]=='文旅',
 lambda st,at,t,w: t['发改']!='绿茶' and t['教育']!='单丛',
]
S=run(conds)
for st,t in S:
    at={v:k for k,v in st.items()}
    print([ (at[i],t[at[i]]) for i in range(4)])
