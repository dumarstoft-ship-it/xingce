from fractions import Fraction as F
import itertools, math

def solve3(M, rhs):
    def det(m):
        return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    D = det(M)
    if D == 0: return None
    out=[]
    for i in range(3):
        Mi=[row[:] for row in M]
        for r in range(3): Mi[r][i]=rhs[r]
        out.append(F(det(Mi),D))
    return out

print("== D16-四-深化: 甲p1+乙q1 = 乙p2+丙q2 = 甲p3+丙q3 = 全部 ==")
cnt=0
for p1,q1,p2,q2,p3,q3 in itertools.product(range(2,9),range(2,11),range(2,9),range(2,11),range(2,9),range(2,13)):
    s = solve3([[p1,q1,0],[0,p2,q2],[p3,0,q3]],[1,1,1])
    if not s or any(v<=0 for v in s): continue
    a,b,c = s
    days = 1/(a+b+c); singles=[1/a,1/b,1/c]
    if days.denominator==1 and all(x.denominator==1 for x in singles) and days<=12 and max(singles)<=60 and len(set(singles))==3:
        cnt+=1
        if cnt<=10: print(dict(甲p1=p1,乙q1=q1,乙p2=p2,丙q2=q2,甲p3=p3,丙q3=q3,三人合作=int(days),单独=[int(x) for x in singles]))

print("== D16-九-深化 ==")
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

print("== D16-十-巩固: 技术支持型 ==")
for ja,yr in [(30,F(6,5)),(30,F(3,2)),(24,F(3,2)),(20,F(3,2)),(30,F(4,3)),(36,F(4,3))]:
    tot = 120*ja
    J = F(tot,ja); Y = J*yr
    for m,n in [(F(1),F(3,2)),(F(1),F(2)),(F(6,5),F(2)),(F(1,2),F(1)),(F(1),F(1))]:
        for t0 in range(1,5):
            for tl in range(1,4):
                rem = tot - (J+Y)*t0 - J*(1+m)*tl
                x = rem/((J+Y)*(1+n))
                if x.denominator==1 and 1<=x<=10:
                    print(dict(甲单独=ja,乙比甲=str(yr),单支持=str(m),双支持=str(n),t0=t0,x=int(x),tl=tl,总=t0+int(x)+tl))

print("== D16-十-深化: 依次投入等间隔 ==")
for L in [40,45,50,60,70,80,90]:
    for single in [100,110,120,125,130,140,150,160,180]:
        W = 4*single
        d = F(18*L - W, 22)
        if d.denominator==1 and 0< d < F(L,2):
            print(dict(甲共工作=L,单台=single,间隔=int(d)))

print("== D16-十-拓展: 效率逐日递增 ==")
for start,inc,total,old in itertools.product([150,200,240],[10,20,30],[3000,3600,4000,4500,5000,5600,6000],[250,280,300,320,350]):
    s=0;n=0
    while s<total:
        n+=1; s+= start+inc*(n-1)
    oldd = math.ceil(total/old)
    if s==total and abs(oldd-n) in (1,2,3) and total % old !=0:
        print(dict(首日=start,每天增=inc,总量=total,新线天数=n,老线日产=old,老线天数=oldd))

print("== D16-十二-深化 ==")
for N in range(600,3001,10):
    for (fa,ta),(fb,tb),(fc,tc,delay) in [((150,1),(120,2),(100,1,2)),((200,2),(150,1),(120,2,1)),((180,1),(120,3),(90,2,1)),((160,2),(120,1),(100,3,1))]:
        for n in range(3,15):
            tot = fa*max(0,n-ta)+fb*max(0,n-tb)+fc*max(0,n-tc-delay)
            if tot==N:
                if n-tc-delay>0 and N%100==0:
                    print(dict(N=N,A=(fa,ta),B=(fb,tb),C=(fc,tc,delay),n=n))
