# 2-11-2: 甲每次做p小时, 乙每次做q小时, 甲先, 反复. 找"尾巴跨到乙"的情形(甲做满p小时后还要乙做一部分)
from fractions import Fraction as F
from math import lcm
def sim(W,a,b,p,q):
    t=F(0); done=F(0)
    while True:
        # 甲 turn
        if done + a*p >= W:
            return t + (W-done)/a
        done += a*p; t += p
        if done + b*q >= W:
            return t + (W-done)/b
        done += b*q; t += q
for T1 in range(4,31):
    for T2 in range(4,41):
        if T1==T2: continue
        W=lcm(T1,T2); a=W//T1; b=W//T2
        for p,q in [(2,1),(1,2),(3,1),(2,3),(3,2)]:
            R=a*p+b*q
            k,r=divmod(W,R)
            if r==0: continue
            spill = r > a*p
            ans=sim(W,a,b,p,q)
            if (ans*60).denominator!=1: continue
            # errors
            e_tail_A = k*(p+q) + F(r,a)            # 尾巴全按甲
            e_avg = F(W*(p+q),R)                  # 平均效率
            e_up = (k+1)*(p+q)                    # 取整轮
            if spill:
                print(f"T1={T1} T2={T2} W={W} a={a} b={b} p={p} q={q} R={R} k={k} r={r} ans={float(ans):.4f}h={ans} tailA={e_tail_A} avg={e_avg} up={e_up}")
