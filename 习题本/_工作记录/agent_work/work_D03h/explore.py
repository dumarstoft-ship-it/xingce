from fractions import Fraction as F
# Q1: a,b,c,t
a,b,c,t=60,75,65,6
S=F((a+c)*(b+c)*t,(b-a)); T=F((a+c)*t,(b-a))
print('Q1 S',S,'T',T,'E1',F((b+c)**2*t,b-a),'E2',F(c*(b+c)*t,b-a),'E3',(a+c)*T,'gap',(a+c)*t)
# Q2
S2,v,k=18,4,9
x=F(2*S2,k+3); T2=x/v+(S2-x)/(k*v)
xa=F(S2,k+1); Ta=xa/v+(S2-xa)/(k*v)
xb=F(2*S2,k+1); Tb=xb/v+(S2-xb)/(k*v)
print('Q2 x',x,'T',T2*60,'Ta',Ta*60,'Tb',Tb*60,'pick',x/v*60,'loaded only',2*(S2-x)/(k*v)*60,'shuttle',F(3*S2,k*v)*60,'car dist',3*S2-4*x)
# Q3
FIRST,GAP,TRIP=390,8,48
D=FIRST+2*GAP
lo,hi=D-TRIP,D+TRIP
cnt=[s for s in range(FIRST,FIRST+400,GAP) if lo<s<hi]
print('Q3 dep',D,'count',len(cnt),[f'{s//60}:{s%60:02d}' for s in cnt])
# Q4
Dd,u,w=100,32,24
ts=F(Dd*u,u*u+w*w)
d2=(Dd-u*ts)**2+(w*ts)**2
print('Q4 t*',ts,'d2',d2,'legs',Dd-u*ts,w*ts,'E_int',F(w*Dd,u),'proj',F(Dd*u,(u*u+w*w))*40)
