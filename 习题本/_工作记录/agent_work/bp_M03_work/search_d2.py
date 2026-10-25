from fractions import Fraction as F
import itertools

print("== 多块草地（单位面积化）: n*t = a*(y + g*t) ==")
sols=[]
for a1,n1,t1,a2,n2,t2 in itertools.product([10,12,15,20],[12,15,16,18,20,24],[6,8,10,12,15,20],[15,20,24,30],[18,20,24,30,36],[4,5,6,8,10,12]):
    if a2<=a1 or t2>=t1: continue
    # per area: n1*t1/a1 = y + g t1 ; n2*t2/a2 = y + g t2
    p1=F(n1*t1,a1); p2=F(n2*t2,a2)
    if p1==p2: continue
    g=(p1-p2)/(t1-t2); y=p1-g*t1
    if g<=0 or y<=0: continue
    if g.denominator!=1 or y.denominator!=1: continue
    for a3,t3 in itertools.product([24,30,36,40,45,48,50,60],[5,6,8,9,10,12,15,18]):
        n3=F(a3)*(y+g*t3)/t3
        if n3.denominator==1 and 10<=n3<=80:
            sols.append((a1,n1,t1,a2,n2,t2,int(y),int(g),a3,t3,int(n3)))
print(len(sols)); 
for s in sols[:12]: print(s)

print("== 中途人员变动：求提前天数 ==")
# plan T together; a days together, then 乙 alone b days -> half; 丙=k*甲 joins; after c days 甲 returns
out=[]
for T in [18,20,24,30,36]:
    for a in range(2,8):
        for b in range(4,20):
            # T(j+y)/2 = a(j+y) + b*y  -> (T/2 - a) j = (b - T/2 + a) y
            L=F(T,2)-a; R=b-F(T,2)+a
            if L<=0 or R<=0: continue
            j=R; yv=L  # ratio j:y = R:L
            tot=T*(j+yv); half=tot/2
            for k in [F(1),F(3,2),F(2),F(5,2),F(3)]:
                c_=k*j
                for c in range(1,6):
                    w=c*(yv+c_)
                    if w>=half: continue
                    rest=(half-w)/(j+yv+c_)
                    if rest.denominator!=1: continue
                    total=a+b+c+rest
                    if total<T and (T-total)>=1:
                        g=__import__('math').gcd(int(j),int(yv))
                        out.append((T,a,b,f'{int(j)//g}:{int(yv)//g}',str(k),c,int(rest),int(T-total)))
for o in out[:20]: print(o)

print("== 故障维修：反推维修时长 ==")
out=[]
for ta,tb in [(12,20),(10,15),(12,18),(15,20),(10,20),(12,24),(9,18),(8,12)]:
    tot=ta*tb//__import__('math').gcd(ta,tb); A=F(tot,ta); B=F(tot,tb)
    plan=tot/(A+B)
    for t0 in range(1,6):
        for p in [F(1,5),F(1,4),F(1,2),F(1,3)]:
            for r in [F(1,2),F(1),F(3,2),F(2),F(5,2),F(3)]:
                done=(A+B)*t0 + A*r
                if done>=tot: continue
                rest=(tot-done)/(A+B*(1-p))
                actual=t0+r+rest
                delay=actual-plan
                if delay.denominator in (1,2,3,4,6) and delay>0 and rest.denominator in (1,2,3,4,6):
                    out.append((ta,tb,t0,str(p),str(r),str(plan),str(actual),str(delay)))
for o in out[:25]: print(o)
