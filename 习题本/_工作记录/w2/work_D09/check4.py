import itertools, math
from fractions import Fraction as F
def max_fail(wrong, N, k):
    # max number of people with >=k wrong, given per-item wrong counts (people can be wrong at most once per item)
    best=0
    for x in range(0,N+1):
        if sum(min(w,x) for w in wrong)>=k*x: best=x
    return best
w=[8,4,12,18,30]; N=60
x=max_fail(w,N,3); print("2022SZ-58 max fail",x,"min pass",N-x)
w=[18,22,27,10,43]; 
for N in (100,200):
    ww=[v*N//100 for v in w]; x=max_fail(ww,N,3); print("2020SZS-30 N",N,"min qualified rate",(N-x)/N)
w=[5,15,25,35,50]; x=max_fail(w,100,2); print("T190 min excellent", 100-x)
# 2018GK-67: ballots choose 1..5 works; valid if <=2; vote rates 69,63,44,58,56 of ballots (N=100)
r=[69,63,44,58,56]; N=100
best=0
for v in range(0,N+1):
    inv=N-v
    # each work gets: votes from invalid ballots <= inv (each invalid ballot picks 3..5 works), valid picks 1..2
    # feasibility: need to distribute. invalid ballots: each picks between 3 and 5 works; valid: 1..2.
    # total selections 290 must lie in [v*1+inv*3, v*2+inv*5], and per work r_i <= v+inv, plus a per-work cap for valid part
    tot=sum(r)
    if not (v+3*inv<=tot<=2*v+5*inv): continue
    # check a constructive condition: invalid give min(r_i,inv) to each work? use LP-ish: votes from invalid to work i: y_i in [max(0,r_i-v), min(r_i,inv)], sum y_i in [3inv,5inv];
    # remaining r_i-y_i from valid ballots must satisfy sum in [v,2v] and each <= v
    lo=sum(max(0,ri-v) for ri in r); hi=sum(min(ri,inv) for ri in r)
    Ylo=max(lo,3*inv, tot-2*v); Yhi=min(hi,5*inv, tot-v)
    if Ylo<=Yhi: best=v
print("2018GK-67 max valid rate", best)
# 2024GK-69
best=None
for c1 in range(21):
  for w1 in range(21-c1):
    u1=20-c1-w1
    if not w1>c1: continue
    for c2 in range(21):
      for w2 in range(21-c2):
        u2=20-c2-w2
        if 3*(c1+c2)+u1+u2==82:
          if best is None or c2<best: best=c2; arg=(c1,w1,u1,c2,w2,u2)
print("2024GK-69 min c2",best,arg)
# 2020GKD-67
from fractions import Fraction as Fr
days=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
keep={'Mon':Fr(1,2),'Tue':Fr(2,3),'Wed':Fr(1,2),'Thu':Fr(2,3),'Fri':Fr(1,2),'Sat':Fr(2,3),'Sun':Fr(1,2)}
res=[]
for s in range(7):
    p=Fr(1)
    for i in range(6): p*=keep[days[(s+i)%7]]
    res.append((Fr(1,72)/p,days[s]))
print("2020GKD-67 initial amounts by start day", sorted(res,reverse=True)[:3])
# 2019ZJA-75
best=None
for n1 in range(1,40):
  for n2 in range(n1+1,40):
    for n3 in range(n2+1,40):
      n4=40-n1-n2-n3
      if n4>n3:
        H=n1+2*n2+3*n3+4*n4
        if best is None or H<best: best=H; arg=(n1,n2,n3,n4)
print("2019ZJA-75 minH",best,arg,"diff",2*best-205)
# 2016JSA-65
for r in (0,1,2,3):
    print("2016JSA-65 r",r,"x",33-r)
# 2024GD-42
best=0
for t in range(11):
    rest=10-t
    for w in itertools.product(range(1,11),repeat=3):
        if sum(w)==rest and len(set(w))==3: best=max(best,t)
print("2024GD-42 max all-correct", best)
# 2024JSA-63: maximize length L with 9 occupied, every empty has exactly one occupied neighbour
best=0
for L in range(9,33):
    # DP over positions: state (prev occupied?, prev-prev occupied?, count occ) -- brute force by DP
    from functools import lru_cache
    @lru_cache(None)
    def ok(i,p2,p1,cnt,need_check):
        # need_check: whether position i-1 is empty and still needs its right neighbour checked (count of occupied neighbors so far)
        if cnt>9: return False
        if i==L:
            if need_check is not None and need_check!=1: return False
            return cnt==9
        for cur in (0,1):
            # verify position i-1 if it was empty
            if need_check is not None:
                c=need_check+cur
                if c!=1: continue
            nc = None if cur==1 else (p1)  # left neighbour occupied count for position i
            if not ok(i+1,p1,cur,cnt+cur,nc): continue
            return True
        return False
    if ok(0,0,0,0,None): best=L
print("2024JSA-63 max points", best)
# 2023ZJA-57
for n in range(2,20):
    if 18+5*(n-2)>=6*n: m=n
print("2023ZJA-57 max files", m*10)
# 2024GD-45
for x in range(1,30):
    if 8*(x+2)>=10*x+5: mx=10*x+5
print("2024GD-45 max elderly", mx)
