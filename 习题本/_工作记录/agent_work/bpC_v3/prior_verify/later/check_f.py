from itertools import product
n=8
res={}
for P in range(3,8):
    for W in range(2,6):
        ks=set()
        for seq in product(['MP','MN','WP','WN'],repeat=n):
            if seq[0]!='MP' and seq[0]!='WP' and seq[0]!='MN' and seq[0]!='WN': continue
            if sum(s[1]=='P' for s in seq)!=P or sum(s[0]=='W' for s in seq)!=W: continue
            ok=all(seq[(i-1)%n][1]=='P' and seq[(i+1)%n][1]=='P' for i in range(n) if seq[i][0]=='W')
            if ok: ks.add(sum(1 for s in seq if s=='WP'))
        if ks: res[(P,W)]=sorted(ks)
for k,v in sorted(res.items()): print('党员',k[0],'女性',k[1],'可能的女党员数',v)
