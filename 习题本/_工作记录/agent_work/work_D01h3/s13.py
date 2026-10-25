# search data for need 13: three-way doubling, final C:A ratio, integrality pins answer
from fractions import Fraction as F
from math import gcd

def reverse(a,b,c):
    """final -> list of states from initial to final; None if non-integer/non-positive"""
    T=a+b+c
    st=[(a,b,c)]
    # undo step3 (C gave to A,B doubling them)
    a,b,c=a/2,b/2,c+a/2+b/2; st.append((a,b,c))
    # undo step2 (B gave to A,C)
    a,b,c=a/2,b+a/2+c/2,c/2; st.append((a,b,c))
    # undo step1 (A gave to B,C)
    a,b,c=a+b/2+c/2,b/2,c/2; st.append((a,b,c))
    st=st[::-1]
    for s in st:
        for v in s:
            if v<=0 or v!=int(v): return None
    return [tuple(int(v) for v in s) for s in st]

def sols(T, r):  # r = C/A in final (Fraction)
    out=[]
    for a in range(1,T):
        c=r*a
        if c.denominator!=1: continue
        c=int(c); b=T-a-c
        if b<=0 or c<=0: continue
        st=reverse(F(a),F(b),F(c))
        if st: out.append(st)
    return out

for T in range(120,361,2):
    for q in range(2,33):
        for p in range(1,2*q):
            if gcd(p,q)!=1 or p==q: continue
            r=F(p,q)
            s=sols(T,r)
            if len(s)!=1: continue
            s2=sols(T,1/r)
            print(T,f"C/A={p}/{q}",s[0],'rev:',[x[0][0] for x in s2])
