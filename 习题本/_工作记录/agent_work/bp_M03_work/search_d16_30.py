from fractions import Fraction as F
import itertools, math

print("== D16-一-深化: 支援一分为二 (甲d天完成后一半支援乙、一半支援丙；乙p天、丙q天完成；乙每天比丙多k) ==")
for d,p,q in itertools.product(range(6,13),range(8,20),range(8,22)):
    if not (d<p<q): continue
    # Q = d*a ; Q = p*b + (p-d)*a/2 ; Q = q*c + (q-d)*a/2  -> b = a*(d-(p-d)/2)/p ; c = a*(d-(q-d)/2)/q
    bb = F(d) - F(p-d,2); cc = F(d) - F(q-d,2)
    if bb<=0 or cc<=0: continue
    b = bb/p; c = cc/q   # in units of a
    diff = b - c
    if diff<=0: continue
    for k in [2,3,4,5,6]:
        a = F(k)/diff
        if a.denominator==1 and (b*a).denominator==1 and (c*a).denominator==1 and a<=80:
            print(dict(d=d,p=p,q=q,k=k,a=int(a),b=int(b*a),c=int(c*a),Q=int(d*a)))
            break

print("== D16-三-深化: 甲a天完成p1；乙b天完成剩余的p2；之后合作x天完成 ==")
for a,b in itertools.product(range(2,7),range(2,9)):
    for p1 in [F(1,5),F(1,4),F(1,3),F(3,10),F(2,5)]:
        for p2 in [F(1,4),F(1,3),F(3,8),F(2,5),F(1,2)]:
            ja = p1/a; yi = (1-p1)*p2/b
            rest = (1-p1)*(1-p2)
            x = rest/(ja+yi)
            if x.denominator==1 and 2<=x<=10 and (1/ja).denominator==1 and (1/yi).denominator==1:
                print(dict(a=a,p1=str(p1),b=b,p2=str(p2),x=int(x),甲单独=int(1/ja),乙单独=int(1/yi)))

print("== D16-四-深化: 三方案等量 4a+6b = 3b+8c = 2a+?c ... 求三人合作天数 ==")
cnt=0
for p1,q1,p2,q2,p3,q3 in itertools.product(range(2,9),range(2,11),range(2,9),range(2,11),range(2,9),range(2,13)):
    # 甲p1+乙q1 = T ; 乙p2+丙q2 = T ; 甲p3+丙q3 = T  (three eq, unknown a,b,c with T)
    # solve with T=1 via linear algebra
    import numpy as np
    M = np.array([[p1,q1,0],[0,p2,q2],[p3,0,q3]],dtype=float)
    if abs(np.linalg.det(M))<1e-9: continue
    sol = np.linalg.solve(M,[1,1,1])
    if (sol<=0).any(): continue
    a_,b_,c_=[F(v).limit_denominator(1000) for v in sol]
    if any(abs(float(fv)-v)>1e-9 for fv,v in zip((a_,b_,c_),sol)): continue
    days = 1/(a_+b_+c_)
    singles = [1/a_,1/b_,1/c_]
    if days.denominator==1 and all(s.denominator==1 for s in singles) and days<=12 and max(singles)<=60:
        cnt+=1
        if cnt<=12: print(dict(甲p1=p1,乙q1=q1,乙p2=p2,丙q2=q2,甲p3=p3,丙q3=q3,三人合作=int(days),单独=[int(s) for s in singles]))

print("== D16-九-深化: 合作T天; a天后乙退出x天; 回归时完成p; 丙加入后y天完工且按期 -> 求x (甲:乙已知) ==")
for T in [20,24,30]:
    for rj,ry in [(1,1),(2,1),(1,2),(3,2),(2,3)]:
        tot = T*(rj+ry)
        for a in range(2,8):
            for x in range(2,10):
                done = a*(rj+ry) + x*rj
                p = F(done,tot)
                if p.denominator not in (2,3,4,5,10): continue
                y = T - a - x
                if y<=0: continue
                c = F(tot-done, y) - rj - ry
                if c>0 and c.denominator==1:
                    print(dict(T=T,ratio=f'{rj}:{ry}',a=a,x=x,完成=str(p),y=y,丙=int(c)))

print("== D16-十-巩固: 技术支持型（丙支持一队+m%，支持两队+n%） ==")
for ja,yr in [(30,F(6,5)),(30,F(3,2)),(24,F(3,2)),(20,F(3,2)),(30,F(4,3))]:
    tot = ja*12  # assign
    J = F(tot,ja); Y = J*yr
    for m,n in [(F(1),F(3,2)),(F(1),F(2)),(F(6,5),F(2)),(F(1,2),F(1)),(F(1),F(1))]:
        for t0 in range(1,5):
            for tl in range(1,4):
                # 甲乙 t0 天, 三队 x 天, 最后 tl 天 乙休息 (甲+丙)
                rem = tot - (J+Y)*t0 - J*(1+m)*tl
                x = rem/((J+Y)*(1+n))
                if x.denominator==1 and 1<=x<=10:
                    print(dict(甲单独=ja,乙比甲=str(yr),单支持=str(m),双支持=str(n),t0=t0,x=int(x),tl=tl,总=t0+int(x)+tl))

print("== D16-十-深化: 依次投入等间隔 d, 甲共工作 L 分钟; 单台效率4, 两台各+25%(5), 三台各+50%(6) ==")
for L in [40,45,50,60,70,80,90]:
    for single in [100,110,120,125,130,140,150]:
        W = 4*single
        # 4d + 10d + 18(L-2d) = W -> 14d +18L -36d = W -> d = (18L - W)/22
        d = F(18*L - W, 22)
        if d.denominator==1 and 0< d < F(L,2):
            print(dict(甲共工作=L,单台=single,间隔=int(d)))

print("== D16-十-拓展: 效率逐日递增 ==")
for start,inc,total,old in itertools.product([150,200,240],[10,20,30],[3000,3600,4000,4500,5000,5600,6000],[250,280,300,320,350]):
    s=0;n=0
    while s<total:
        n+=1; s+= start+inc*(n-1)
    exact = (s==total)
    oldd = math.ceil(total/old)
    if exact and abs(oldd-n) in (1,2,3) and total % old !=0:
        print(dict(首日=start,每天增=inc,总量=total,新线天数=n,老线日产=old,老线天数=oldd))

print("== D16-十二-深化: 多出口疏散 + 某出口延迟开启 ==")
for N in range(600,3000,10):
    for (fa,ta),(fb,tb),(fc,tc,delay) in [((150,1),(120,2),(100,1,2)),((200,2),(150,1),(120,2,1)),((180,1),(120,3),(90,2,1)),((160,2),(120,1),(100,3,1))]:
        # exit c opens 'delay' minutes late; total time n: people through a = fa*(n-ta), b = fb*(n-tb), c = fc*(n-tc-delay)
        for n in range(3,15):
            tot = fa*max(0,n-ta)+fb*max(0,n-tb)+fc*max(0,n-tc-delay)
            if tot==N:
                prev = fa*max(0,n-1-ta)+fb*max(0,n-1-tb)+fc*max(0,n-1-tc-delay)
                if prev<N and n-tc-delay>0 and N%100==0:
                    print(dict(N=N,A=(fa,ta),B=(fb,tb),C=(fc,tc,delay),n=n))
