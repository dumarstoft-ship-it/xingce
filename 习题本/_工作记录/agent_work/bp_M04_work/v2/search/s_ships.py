from fractions import Fraction as F
import math
res=[]
for a in range(10, 101, 5):
    for b in range(10, 101, 5):
        for p in range(5, 41, 5):
            for q in range(5, 41, 5):
                if p*b == q*a: continue      # 同时到港（成比例）太简单
                # d^2 = (a-pt)^2+(b-qt)^2 = (p^2+q^2)t^2 - 2(ap+bq)t + a^2+b^2
                A_ = p*p+q*q; B_ = -2*(a*p+b*q); C0 = a*a+b*b
                for D in range(5, 101, 5):
                    disc = B_*B_ - 4*A_*(C0-D*D)
                    if disc <= 0: continue
                    r = math.isqrt(disc)
                    if r*r != disc: continue
                    t1 = F(-B_ - r, 2*A_); t2 = F(-B_ + r, 2*A_)
                    if t1 <= 0: continue
                    if t1.denominator > 2 or t2.denominator > 2: continue
                    # 两船都在到港前（t2 < min(a/p, b/q)）
                    if True:
                        tmin = F(a*p+b*q, A_)
                        dmin2 = (a-p*tmin)**2+(b-q*tmin)**2
                        res.append((a,b,p,q,D,t1,t2,tmin,dmin2))
print(len(res))
for r in res[:40]: print(r)
