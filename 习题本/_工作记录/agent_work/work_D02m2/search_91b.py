from fractions import Fraction as F
out=[]
for N in range(15,37):
    for a in range(2,9):
        for b in range(2,16):
            for p in [F(2,5),F(1,3),F(3,5)]:
                den = a+b-p*N
                if den==0: continue
                r = (p*N-a)/den   # 乙/甲
                if r<=0 or r==2: continue
                if r.denominator>2 or r.numerator>4: continue
                # scale so that 甲,乙 integers
                s = r.denominator
                e1, e2 = s, int(r*s)
                W = N*(e1+e2)
                for d in range(1,4):
                    rem = N-d-a-b
                    if rem<4: continue
                    for c in range(1,13):   # 丙 efficiency in same units
                        x = F(rem*(e1+e2+c) - (1-p)*W, e1)
                        if x.denominator!=1 or x<2 or rem-x<2 or x==3: continue
                        if W % c: continue
                        Tc = W//c
                        if (e1,e2,c) in [(1,2,3)]: continue
                        out.append(dict(N=N,a=a,b=b,p=str(p),e1=e1,e2=e2,c=c,Tc=Tc,W=W,d=d,x=int(x),rem=rem))
print(len(out))
for o in out:
    if o['p']=='2/5' and o['Tc']<=60:
        print(o)
