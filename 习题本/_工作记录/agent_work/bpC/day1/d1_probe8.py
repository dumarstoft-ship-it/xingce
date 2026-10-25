from itertools import permutations
P=['甲','乙','丙','丁','戊']; C=['广州','深圳','佛山','东莞','珠海']
S=[]
for pos in permutations(range(1,6)):
    s=dict(zip(P,pos)); at={v:k for k,v in s.items()}
    for cs in permutations(C):
        c=dict(zip(P,cs)); w={v:k for k,v in c.items()}
        if s['甲']!=3: continue
        if s[w['深圳']]!=s['甲']-1: continue
        if not ({s['乙'], s[w['佛山']]}=={1,5} and w['佛山']!='乙'): continue
        if c['丙']=='东莞' or s['丙']!=s['丁']+1: continue
        if s[w['珠海']]!=4: continue
        S.append((s,c))
for s,c in S:
    at={v:k for k,v in s.items()}
    print([ (at[i], c[at[i]]) for i in range(1,6)])
