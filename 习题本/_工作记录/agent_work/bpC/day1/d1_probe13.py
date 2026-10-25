from itertools import permutations
P=['甲','乙','丙','丁','戊','己']
n=6
L=lambda i,k=1:(i+k)%n   # 面向圆心：左手边=俯视顺时针下一位
R=lambda i,k=1:(i-k)%n
O=lambda i:(i+3)%n
adj=lambda a,b:(a-b)%n in (1,n-1)
S=[]
for p in permutations(range(1,6)):
    st=dict(zip(P,(0,)+p))
    at={v:k for k,v in st.items()}
    if st['乙']!=O(st['甲']): continue
    if st['丙']!=L(st['甲'],2): continue
    if not adj(st['丁'],st['丙']): continue
    if adj(st['戊'],st['甲']): continue
    S.append(st)
for st in S:
    at={v:k for k,v in st.items()}
    print([at[i] for i in range(6)])
# 检查若干候选结论
cand={
 '己与甲相邻':lambda st:adj(st['己'],st['甲']),
 '丁坐在乙的右手边':lambda st:st['丁']==R(st['乙']),
 '戊坐在丙的对面':lambda st:st['戊']==O(st['丙']),
 '丁与甲相邻':lambda st:adj(st['丁'],st['甲']),
 '己坐在甲的右手边':lambda st:st['己']==R(st['甲']),
 '戊与乙相邻':lambda st:adj(st['戊'],st['乙']),
}
for k,f in cand.items(): print(k,[f(st) for st in S])
