from itertools import product
n=8
alt=True; wp=set()
for seq in product(['MP','MN','WP','WN'],repeat=n):
    if sum(s[1]=='P' for s in seq)!=5 or sum(s[0]=='W' for s in seq)!=4: continue
    if all(seq[(i-1)%n][1]=='P' and seq[(i+1)%n][1]=='P' for i in range(n) if seq[i][0]=='W'):
        wp.add(sum(s=='WP' for s in seq))
        if any(seq[i][0]==seq[(i+1)%n][0] for i in range(n)): alt=False
print('D11 女党员数',wp,'男女必相间?',alt)
# D17 6人：党员5 女4 硕士5，每人至少一项，丙只具备一项；三项都具备至少几人
P=6
best=None
for prof in product(range(1,8),repeat=6):   # bitmask: 1党 2女 4硕
    if sum(1 for x in prof if x&1)!=5 or sum(1 for x in prof if x&2)!=4 or sum(1 for x in prof if x&4)!=5: continue
    if bin(prof[2]).count('1')!=1: continue   # 丙=index2
    if prof[0]!=prof[1]: continue             # 甲乙三项情况都相同
    t=sum(1 for x in prof if x==7)
    best=t if best is None else min(best,t)
print('D17 三项都具备至少',best)
