import itertools, math
from math import comb
print("2021HB-75: 201 boxes, guarantee some shop>=8 regardless; max shops:", max(n for n in range(1,300) if 7*n<201))
print("2021ZJA-66: signals", 2*2*4*4, "x min", -(-250//64))
print("2022HB-74:", min(49,70)+min(49,60)+min(49,50)+min(49,20)+1)
print("2023SD-38:", min(9,50)+min(9,5)+min(9,30)+min(9,50)+1)
print("2020SZ1-50:", comb(7,2)+7+1)
print("2024SZ-52:", comb(6,2)+6+1)
print("2020SZS-21:", sum(comb(10,k) for k in range(1,5))*4+1)
print("2024SC-46:", 3**3*2+1)
print("2023ZJA-56:", 20*2+1)
print("2025GD-36:", 9*5+1)
print("2020HB-71:", 40+1)
# 2022SD-39
rem=89-58
for x in range(0,rem+1):
    a=34+x
    if a>15+(rem-x) and a>9+(rem-x):
        print("2022SD-39: x",x);break
# T191, T192
for x in range(0,9):
    if 17+x>16+(8-x) and 17+x>11+(8-x): print("T191:",x);break
for x in range(0,31):
    if 15+x>10+(30-x) and 15+x>5+(30-x): print("T192:",x);break
# T186
cls=set(); 
print("T186: classes", len(set(i%6 for i in range(1,26))), "->", len(set(i%6 for i in range(1,26)))+1)
# 2022ZJA-66
for N in range(50,60):
    if N%13==0:
        F=(N-4)//2; M=F+4
        print("2022ZJA-66: N",N,"M",M,"F",F,"25%M",M*0.25)
        # women w: any 6 must include a man -> w<=5 ; guarantee one point with women>1 -> w>=5 (4 points)
        for w in range(0,F+1):
            if w<=5 and w>4: print("   women",w,"total",int(M*0.25)+w)
# 2022SC1-55
best=None
inst=[(5,3,2),(5,3,2),(7,4,3),(7,4,3)]  # total, male, female
for g in itertools.product(range(1,5),range(1,5),range(1,7),range(1,7)):
    o=(5-g[0],5-g[1],7-g[2],7-g[3])
    if len(set(g))<4 or len(set(o))<4: continue
    for grp in (g,o):
        males=sum(max(0,grp[i]-inst[i][2]) for i in range(4))
        if best is None or males<best: best=males; arg=(grp, g, o)
print("2022SC1-55: min males in one group",best,arg)
# 2022JSA-56
print("2022JSA-56:", 1000-(130+250+310))
# T188/T189/T190
print("T188:",100-(32+42+22)," T189:",1600-(420+240+350+560)," T190 excellent>=",100-130/2)
