import itertools, math
from functools import lru_cache

print("== 2026ZJA-60: 10 distinct integer ages, mean 35, max-min=25; max sum of youngest 3")
# a1<...<a10, a10=a1+25, sum=350. maximize a1+a2+a3.
best=None; arg=None
for a1 in range(1,60):
    a10=a1+25
    # middle a2..a9 strictly between a1 and a10, distinct, 8 values chosen from (a1+1..a1+24)
    rest=350-a1-a10
    pool=list(range(a1+1,a10))
    if len(pool)<8: continue
    # maximize a2+a3 where a2<a3 are the two smallest chosen among 8; others a4..a9 >a3
    for a2 in pool:
        for a3 in pool:
            if a3<=a2: continue
            # a4..a9: 6 distinct values from (a3+1..a10-1)
            cand=list(range(a3+1,a10))
            if len(cand)<6: continue
            mn=sum(cand[:6]); mx=sum(cand[-6:])
            need=rest-a2-a3
            if mn<=need<=mx:
                s=a1+a2+a3
                if best is None or s>best: best=s; arg=(a1,a2,a3,need)
print(best,arg)

print("== 2026GK-74: 30 people distinct ints 0..100, those >=90 avg 93.8, Xiao Jiang 92; worst rank")
worst=0; ex=None
vals=list(range(90,101))
for k in range(1,12):
    for comb in itertools.combinations(vals,k):
        if 92 not in comb: continue
        if abs(sum(comb)-93.8*k)<1e-9:
            above=sum(1 for v in comb if v>92)
            if above+1>worst: worst=above+1; ex=comb
print("worst rank",worst,ex)

print("== 2026ZJA-52: 10 days, total 41, any two days differ <=2, max days with exactly 5")
best=0;ex=None
for m in range(0,10):
    # values in [m,m+2]
    for a in range(11):
        for b in range(11-a):
            c=10-a-b
            if a*m+b*(m+1)+c*(m+2)==41:
                cnt5=(a if m==5 else 0)+(b if m+1==5 else 0)+(c if m+2==5 else 0)
                if cnt5>best: best=cnt5; ex=(m,a,b,c)
print(best,ex)

print("== 2025JSA-67: N%8==3, N%9==5; 3 distinct bouquets using all; min of the largest")
Ns=[n for n in range(1,400) if n%8==3 and n%9==5]
print(Ns[:4])
for N in Ns[:2]:
    best=None
    for x in range(1,N):
        for y in range(x+1,N):
            z=N-x-y
            if z>y:
                if best is None or z<best: best=z
    print(N,best)

print("== 2026JS-58: 23 zones, 77 events, each <=5 (>=0); min number of zones with >=4")
best=None
for k in range(24):
    # k zones with 4..5, 23-k zones with 0..3
    lo=4*k; hi=5*k+3*(23-k)
    if lo<=77<=hi:
        best=k;break
print(best)

print("== 2025JSA-66: 7 scores multiples of 0.5 in [0,10], middle-3 sum=22; max avg")
best=None
H=[i/2 for i in range(21)]
for s3 in H:
    for s4 in H:
        if s4<s3: continue
        s5=22-s3-s4
        if s5<s4 or s5>10 or (s5*2)%1!=0: continue
        tot=2*s3+22+20  # s1=s2=s3 max, s6=s7=10
        if best is None or tot>best: best=tot; ex=(s3,s4,s5)
print(best, best/7, ex)
