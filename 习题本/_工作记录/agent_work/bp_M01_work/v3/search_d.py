from fractions import Fraction as F
out=[]
for a in [F(1,5),F(1,4),F(1,2),F(1,3)]:
    for b in [F(1,5),F(1,4),F(1,6),F(1,3)]:
        if (a,b)==(F(2,5),F(1,8)): continue
        # s1 = 1 unit base: s2=(1+a)s1, s3=s2/(1-b)
        for m in [F(1,1),F(3,2),F(2,1),F(5,2)]:
            for c in [F(1,4),F(1,3),F(1,2),F(1,5)]:
                s1=F(1); s2=(1+a)*s1; s3=s2/(1-b)
                front=s1+s2+s3; back=m*front
                s4=back/(2+c); s5=s4*(1+c)
                for D in [F(x) for x in range(10,100)]:
                    # s5 - s3 = D  -> unit
                    if s5-s3<=0: continue
                    u=D/(s5-s3)
                    vals=[v*u for v in (s1,s2,s3,s4,s5)]
                    if all(v.denominator==1 for v in vals) and all(v<400 for v in vals):
                        ask=vals[3]-vals[0]
                        out.append((a,b,m,c,D,[int(v) for v in vals],'s4-s1',ask,'s5-s3',vals[4]-vals[2],'s5-s1',vals[4]-vals[0]))
for o in out[:60]: print(o)
print(len(out))
