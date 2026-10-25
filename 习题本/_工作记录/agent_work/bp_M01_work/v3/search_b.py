from fractions import Fraction as F
import itertools, math
print("== 15-5-2 check (7,5,3,2) y=10 r=3")
for k in range(1,100):
    A,B,C,D=7*k,5*k,3*k,2*k; x=A-B-10
    if x>0 and C+x==3*(D-10): print('k',k,'A',A,'x',x,'after',A-x,B+10,C+x,D-10)
# distractor: forget B received 10 -> A-x=B
for k in range(1,100):
    A,B,C,D=7*k,5*k,3*k,2*k; x=A-B
    if C+x==3*(D-10): print('forget +10 ->A',A)
print("== 15-7-2 reservoir: -p1, +p2 (cancel), -p3 -> final V ; original")
for p1,p2 in [(F(1,4),F(1,3)),(F(1,5),F(1,4)),(F(1,10),F(1,9)),(F(1,3),F(1,2))]:
    assert (1-p1)*(1+p2)==1
    for p3 in [F(1,10),F(1,5),F(1,4),F(2,5),F(3,10)]:
        for V in [F(x,10) for x in range(5,40)]:
            orig=V/(1-p3)
            if orig.denominator==1 or (orig*10).denominator==1:
                if orig*10 % 1==0 and orig<5:
                    add=V/(1-p1+p2-p3); only1=V/(1-p1); seq=V*(1-p3)
                    print(p1,p2,p3,'V',float(V),'orig',float(orig),'distr add',float(add),'only first',float(only1),'seqmul',float(seq))
