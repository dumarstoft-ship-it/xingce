exec(open('s15.py').read().split("print(len(res))")[0])
for r in res:
    s1,s2,ratio,W,cd,q,ans,fl,rv,ig=r
    if ratio not in [(3,2),(5,2),(5,3),(7,4),(7,3),(8,3),(9,4),(9,5),(3,1),(2,1)]: continue
    if cd[1]!=0: continue
    if rv in (ans,fl) or rv>ans+4: continue
    vals={ans,fl,rv}
    if ig and ig[0]==ig[1] and ig[0] not in vals and ig[0]<=ans+4:
        tag='IGOK'
    else:
        tag=''
    if not tag: continue
    print(s1,s2,'B:S',ratio,'W',W,'ask',cd,'W/cap',q,round(float(q),3),'ans',ans,'floor',fl,'rev',rv,'ignore',ig,tag)
