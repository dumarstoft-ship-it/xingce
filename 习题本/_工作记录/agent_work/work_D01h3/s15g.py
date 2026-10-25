exec(open('s15f.py').read().split("print(len(res))")[0])
out=[]
for r in res:
    s1,s2,(p,q),W,N,t3,x,ds=r
    if (p,q) in ((2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1)): continue
    for combo in (('rev','small','div'),('rev','ign','small'),('rev','ign','div'),('ign','small','div')):
        vals=[ds[k] for k in combo]
        if None in vals or len(set(vals))<3 or x in vals: continue
        allv=sorted(vals+[x]); pos=allv.index(x)
        if pos in (0,3):
            out.append((pos,s1,s2,(p,q),W,N,t3,x,dict(zip(combo,vals))))
for o in sorted(out,key=lambda o:(o[3],o[5])): print(o)
print(len(out))
