exec(open('s15.py').read().split("print(len(res))")[0])
cnt=0
seen=set()
for r in res:
    s1,s2,ratio,W,cd,q,ans,fl,rv,ig=r
    if rv in (ans,fl) or rv>ans+5 or rv<2: continue
    if not ig: continue
    igv=set(ig)
    if any(v in (ans,fl,rv) for v in igv) or max(igv)>ans+5: continue
    if ratio not in [(3,2),(5,2),(5,3),(7,4),(7,3),(5,4),(7,5),(8,5),(9,4),(9,5),(3,1),(2,1),(4,3)]: continue
    cnt+=1
    print(s1,s2,'B:S',ratio,'W',W,'ask',cd,'W/cap',q,round(float(q),3),'ans',ans,'floor',fl,'rev',rv,'ignore',ig)
print(cnt)
