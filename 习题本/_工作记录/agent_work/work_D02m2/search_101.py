# 2-10-1: 甲T1h, 乙T2h, 计划同时; 同时t1小时后乙停机维修r小时(甲继续), 修后乙效率降低q, 之后一起直到完成; 比计划晚L小时. 求r.
from fractions import Fraction as F
from math import lcm
seen=set()
for T1 in range(6,25):
    for T2 in range(6,31):
        if (T1,T2) in [(12,20),(20,12)]: continue
        W=lcm(T1,T2); e1=F(W,T1); e2=F(W,T2)
        T0=W/(e1+e2)
        for t1 in range(1,6):
            if t1>=T0: continue
            for q in [F(1,5),F(1,4),F(2,5),F(1,2),F(1,3)]:
                e2n=e2*(1-q)
                for L4 in range(1,13):   # L in quarter hours
                    L=F(L4,4)
                    T=T0+L
                    # t1(e1+e2)+e1 r+(e1+e2n)(T-t1-r)=W
                    r=(t1*(e1+e2)+(e1+e2n)*(T-t1)-W)/(e2n)
                    if r<=0 or T-t1-r<=0: continue
                    if (r*4).denominator!=1: continue
                    if r==2: continue
                    # error paths
                    # E1 甲维修期间也停: t1(e1+e2)+(e1+e2n)(T-t1-r)=W
                    E1=(T-t1)-(W-t1*(e1+e2))/(e1+e2n)
                    # E2 乙修后效率按q计(降低到q): 
                    e2w=e2*q
                    E2=(t1*(e1+e2)+(e1+e2w)*(T-t1)-W)/(e2w)
                    # E3 乙修后不降效
                    E3=(t1*(e1+e2)+(e1+e2)*(T-t1)-W)/(e2)
                    key=(T1,T2,t1,q,L)
                    print(f"T1={T1} T2={T2} W={W} e1={e1} e2={e2} T0={T0} t1={t1} q={q} L={L} r={r} | E1={E1} E2={E2} E3={E3}")
