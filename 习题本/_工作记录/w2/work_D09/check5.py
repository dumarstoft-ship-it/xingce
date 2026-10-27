# teacher items
# T177: 4 bids avg 380 (sum 1520); only Jia >400; pairwise diff in [10,100]; max Jia (step 0.5)
best=None
vals=[x/2 for x in range(600,1000)]  # 300..499.5
for j in [v for v in vals if v>400]:
    # others: three values <=400, pairwise diff>=10 and <=100 incl. with j; minimize their sum: lowest possible j-100, j-90, j-80
    o=[j-100,j-90,j-80]
    if max(o)<=400 and sum(o)+j<=1520:
        # can we raise others to reach exactly 1520 while keeping constraints? others max: up to 400 with spacing
        hi=[400-20,400-10,400]
        hi=[min(h, j-10-10*(2-i)) for i,h in enumerate(hi)]
        if sum(hi)+j>=1520:
            best=j
print("T177 max Jia", best)
# T178
for x in range(1,100):
    if x+2*x+sum(2*x-i for i in range(1,5))>=500 and 2*x-4>x: print("T178 A min",x);break
# T180
for x in range(80,101):
    if 100+77+x+(x-1)+(x-2)>=450 and x-2>77: print("T180 2nd min",x);break
# T181
for y in range(1,10):
    pass
best=max(y for y in range(1,10) if 13+12+11+10+(y+3)+(y+2)+(y+1)+y<=76 and y+3<10)
print("T181 last max",best)
# T182 brute-ish: maximize s6 - s15 under constraints; search over top-5 consecutive block start a and bottom block
best=0
import itertools
for a in range(60,97):
    top=[a+i for i in range(5)]
    T=sum(top)
    if T%2: continue
    B=T//2
    # bottom 5 distinct ints >=0 sum B: minimize their max -> as equal as possible
    m=-(-(B-10)//5)+4 if B>=10 else None  # min possible max of 5 distinct with sum B
    # compute exact min max
    mm=None
    for mx in range(4,101):
        if 5*mx-10>=B: mm=mx;break
    s6=a-1; s15=mm+1
    mid=1580-T-B-s6-s15
    lo=sum(range(s15+1,s15+9)); hi=sum(range(s6-8,s6))
    if lo<=mid<=hi and s6-s15>best: best=s6-s15; arg=(a,mm)
print("T182 max diff",best,arg)
# T183
for k in range(15,0,-1):
    low=sum(range(60-k,60)); high=sum(range(100-(30-k)+1,101))
    if low+high>=2400: print("T183 max below60",k);break
# 2017JSA-68
for x in range(100,121):
    if 120+119+x+(x-1)+(x-2)>=575: print("2017JSA-68 3rd min",x);break
