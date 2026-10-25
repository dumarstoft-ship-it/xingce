from fractions import Fraction as F
print("== 29-8-1 three towns")
sol=[]
for a in range(1,3000):
    j25=a+100; y25=F(j25,2); y24=y25/F(3,4); b24=a+y24; b25=F(14,10)*b24
    if (j25+y25+b25)==F(12,10)*(a+y24+b24): sol.append((a,y24,b24,j25,y25,b25))
print(sol)
a,y24,b24,j25,y25,b25=sol[0]
tot25=j25+y25+b25; tot24=a+y24+b24
print('share25',float(b25/tot25),'share24',float(b24/tot24),'b25/tot24',float(b25/tot24),'b24/tot25',float(b24/tot25))
# error: 乙 2024 computed as y25*1.25 (下降25% misapplied)
for a in range(1,3000):
    j25=a+100; y25=F(j25,2); y24=y25*F(5,4); b24=a+y24; b25=F(14,10)*b24
    if (j25+y25+b25)==F(12,10)*(a+y24+b24): print('err y24=1.25*y25 ->',a,float(b25/(j25+y25+b25)))
print("== 29-10-2 rotation")
for B in range(5,40):
    A,Bc,C=B+2,B,B+4; avg=B+2
    b=9
    # correct: B gives b to C, receives a from A : B - b + a = avg
    a=avg-B+b
    # C gives c to A, receives b: C - c + b = avg -> c
    c=C+b-avg
    # check A: A - a + c = avg
    assert A-a+c==avg
    # reversed direction (A<-B, B<-C, C<-A): B gives b to A, receives c from C: B-b+c=avg -> c ; C gives c to B, receives a from A: C-c+a = avg -> a
    c2=avg-B+b; a2=avg-C+c2
    print('B',B,'a',a,'c',c,'reversed a',a2,'c',c2); break
