from math import *
# 2021SD-36: c+2.1 = 4a/3, c^2 = a^2 + 2.1^2
a = 5.6*9/7; c = sqrt(a*a+2.1**2); print('2021SD-36 a=',a,'c=',c,'check',c+2.1, 4*a/3)
# 2020SC0725-54 frustum: full water 7u, half-height water 1.5^3-1
full = 8-1; half = 1.5**3-1; u = 4.5/(full-half); print('2020SC0725-54 x=', 9-full*u)
# 2021HB-66
r = (50/(2*sqrt(3)))/(1+2/sqrt(3)); print('2021HB-66 r=',r,'path=',5*pi*r, '25(2-sqrt3)=',25*(2-sqrt(3)))
# T255x1
print('T255x1 ratio=', 2/3 - sqrt(3)/(2*pi))
# 2022SC1-53 gray-black
print('2022SC1-53 gray-black=', 20*pi-64, 'gray=',8*pi-16,'black=',48-12*pi)
# 2023GK-75
print('2023GK-75 above ratio', (1-0.729/1.5)**(1/3))
# T251
print('T251', (100-100/sqrt(3))/11 / ((100*sqrt(3)-100)/17))
# 2022ZJA-69
print('2022ZJA-69 n=', floor((20-1.5)/sqrt(1.5**2-0.5**2))+1)
# 2024SD-60
print('2024SD-60 BC=', 90/sqrt(7))
# T249x1
print('T249x1 total=', 200+10*sqrt(2))
# 2026GK-72: a+b=1.5n, a:b=3:2 -> b=0.6n
n=1; a_=0.9; b_=0.6; tot=(2+4*a_)+(2+4*b_); print('2026GK-72 reduction share', 2/tot, 'b/n', b_)
# 2025JSA-59
d = 200*22/(110-22); print('2025JSA-59 d=', d, ' aim-top error d=', 200*22/(132-22))
# Variant birdhead: A(0,0) B(1,0) C(0,1); D=B+(B-A), E=C+2(C-B), F=A+3(A-C)
A=(0,0);B=(1,0);C=(0,1)
D=(2*B[0]-A[0],2*B[1]-A[1]); E=(C[0]+2*(C[0]-B[0]),C[1]+2*(C[1]-B[1])); F=(A[0]+3*(A[0]-C[0]),A[1]+3*(A[1]-C[1]))
area=lambda P,Q,R: abs(P[0]*(Q[1]-R[1])+Q[0]*(R[1]-P[1])+R[0]*(P[1]-Q[1]))/2
print('birdhead DEF/ABC =', area(D,E,F)/area(A,B,C))
# Variant boundary: xy=600, y<=20 -> min 2x+y
best=min((2*600/y+y, y) for y in [i/100 for i in range(100,2001)]); print('boundary min new wall', best, ' unconstrained', 40*sqrt(3), ' x+y wrong', 2*sqrt(600))
