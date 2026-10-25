from itertools import permutations
import random
random.seed(11)
P=['甲','乙','丙','丁']; T=['A','B','C','D']
found=[]
for trial in range(300000):
    M=[[random.randint(3,9) for _ in range(4)] for _ in range(4)]
    vals=[]
    for p in permutations(range(4)):
        days=[M[i][p[i]] for i in range(4)]
        vals.append((max(days),sum(days),p))
    vals.sort()
    if vals[0][0]==vals[1][0]: continue
    opt=vals[0]
    # 最小总天数方案 与 最小最晚方案 不同（制造"总和最小"陷阱）
    s_sorted=sorted(vals,key=lambda x:(x[1],x[0]))
    if s_sorted[0][2]==opt[2]: continue
    if s_sorted[0][1]==s_sorted[1][1]: continue
    # 行最小值冲突（贪心不可行）
    rowmin=[min(r) for r in M]
    greedy=[r.index(min(r)) for r in M]
    if len(set(greedy))==4: continue
    found.append((M,opt,s_sorted[0]))
    if len(found)>=8: break
for M,opt,s in found:
    print(M, '最晚最早方案',opt, '总和最小方案',s)
