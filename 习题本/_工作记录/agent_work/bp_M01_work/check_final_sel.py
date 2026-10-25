from fractions import Fraction as F
import itertools
# D29-V24 ordering: (a+b)/2-c=5 ; (b+c)/2-d=2 ; a-d=9  -> order
d=F(0); 
for c in [F(i,2) for i in range(-40,41)]:
    a=d+9; b=2*c+10-a
    if (b+c)/2-d==2: print('D29-V24 a,b,c,d',a,b,c,d)
# D15-V18 final
a25=1600; b25=800; a24=a25-200; b24=F(b25)/F(8,10); c24=a24+b24; c25=c24*F(3,2)
print('D15-V18', a24,b24,c24,c25,'total growth',(a25+b25+c25)/(a24+b24+c24)-1,'ask c25-a25',c25-a25)
# D39-V3 photos selection T=55 h=2s-2 fam=1/2 h ; fm==mc ; child single = dad+mom single+1 ; dad single = mom single + 1
s=19; h=36; fam=18; pairs=18
sol=set()
for fm in range(0,19):
    for fc in range(0,19-fm):
        mc=pairs-fm-fc
        cg=fam+fc+mc; dg=fam+fm+fc; mg=fam+fm+mc
        if 2*cg==dg+mg and fm==mc:
            for cs in range(0,s+1):
                for ds in range(0,s-cs+1):
                    ms=s-cs-ds
                    if cs==ds+ms+1 and ds==ms+1: sol.add((dg+ds,cg+cs,mg+ms,fm,fc,mc,cs,ds,ms))
print('D39-V3',sol)
# D39-V4 subsidy
zk=2; bk=F(3,2)*zk; ss=bk+1; bs=2*ss; ppl=[100,200,80,20]
print('D39-V4 total',sum(p*v for p,v in zip(ppl,[zk,bk,ss,bs])),'doc',bs)
# D39-V9 shopping
T=960; x,y,z=288,360,312
print('D39-V9',x-120==F(1,4)*(y+z), y-120==F(2,5)*(x+z), z-96==F(1,3)*(x+y), [o for o in [900,960,1000,1020] if (o-120)%35==0 and (o-96)%4==0])
# D39-V22
v=[40,60,80,160,180,200]
print('D39-V22', v[1]==v[0]*F(3,2), v[1]==v[2]*F(3,4), sum(v[3:])==3*sum(v[:3]), v[4]==F(1,4)*sum(v), v[4]==v[3]*F(9,8), v[3]-v[0])
# D39-V24
n=21; M=162; E=102
print('D39-V24', M-6*n-(E-4*n), 8*n-M, 5*n-E)
# D39-V27
x,y,z=80,60,60
print('D39-V27', x+y+z, F(x,10)+F(y,5)+F(z,2), F(x+y,5)+F(3*z,4))
# D39-V30
dist=500000*F(8,10); rest=dist-400*20; per=rest/2000; print('D39-V30',4*20+10*per)
