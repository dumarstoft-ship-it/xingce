from fractions import Fraction as F
# units: 1=甲, 2=乙(reference, n), 3=丙 ; counts c1=n+p, c2=n, c3=n+q
# rotation R: 甲->丙, 丙->乙, 乙->甲   (unit i sends g_i to dest[i]); reversed: 甲->乙, 乙->丙, 丙->甲
def solve(p,q,S,dest,avg_override=None):
    n=100
    c={1:n+p,2:n,3:n+q}
    m=F(sum(c.values()),3) if avg_override is None else avg_override(c)
    sols=[]
    for g1 in range(1,80):
      for g2 in range(1,80):
        g3=S-g1-g2
        if g3<1: continue
        g={1:g1,2:g2,3:g3}
        inc={1:0,2:0,3:0}
        for i in (1,2,3): inc[dest[i]]+=g[i]
        if all(c[i]-g[i]+inc[i]==m for i in (1,2,3)): sols.append((g1,g2,g3))
    return sols
R={1:3,3:2,2:1}
RV={1:2,2:3,3:1}
out=[]
for p in range(-12,13):
  for q in range(-12,13):
    if p==0 or q==0 or p==q or (p+q)%3: continue
    for S in range(24,61):
      s=solve(p,q,S,R)
      if len(s)!=1: continue
      g=s[0]
      if min(g)<4: continue
      rv=solve(p,q,S,RV)
      av=solve(p,q,S,R,avg_override=lambda c:c[2])          # avg mistaken as 乙(reference)
      for ask in (1,2,3):
        cand={'ok':g[ask-1]}
        if len(rv)==1: cand['rev']=rv[0][ask-1]
        if len(av)==1: cand['avg']=av[0][ask-1]
        if S%3==0: cand['S3']=S//3
        vals=list(cand.values())
        if len(cand)<4 or len(set(vals))<4: continue
        pos=sorted(vals).index(cand['ok'])
        if pos not in (0,3): continue
        out.append((p,q,S,ask,g,cand,'pos',pos))
for o in out[:80]: print(o)
print(len(out))
