import math
# MK2735D-M3
p,s,t=317.78,7775.71,22262.24
gp,gs,gt=0.035,0.026,0.053
gdp=30355.73
print("check 2023 sum:", p+s+t, gdp, " shares:", [round(x/gdp*100,2) for x in (p,s,t)])
b=[p/(1+gp), s/(1+gs), t/(1+gt)]
tot=sum(b)
print("Q1 base vals:", b, "sum", tot, " gdp/1.046:", gdp/1.046)
print("   shares on sum:", [round(x/tot*100,3) for x in b])
print("   shares on gdp base:", [round(x/(gdp/1.046)*100,3) for x in b])
# Q2
inds={"wholesale":(4248.59,0.074),"transport":(2029.96,0.122),"hotel":(515.99,-0.105),"finance":(2736.74,0.075)}
for k,(v,g) in inds.items():
    print("Q2",k, v*g/(1+g))
# Q3
r=18994.25
for y in range(2024,2031):
    r*=1.103
    print("Q3",y,r)
print("   n=", math.log(27000/18994.25)/math.log(1.103))
# Q4
m23=1729.68/18994.25
m22=(1729.68/1.307)/(18994.25/1.103)
print("Q4 margin23:",m23*100," margin22:",m22*100," diff pp:",(m23-m22)*100)
# Q5
print("Q5 (1):", 13.2-(-3.9))
print("Q5 (2): ratio", 2736.74/515.99, " more-times:", 2736.74/515.99-1)
print("Q5 (3): gdp22", gdp/1.046)
