# MK2735D-M3 Z市经济
import math
print("Q1")
gdp=30355.73; g=0.046
p=[(317.78,0.035),(7775.71,0.026),(22262.24,0.053)]
print("2023 sum", sum(x for x,_ in p), "2023 shares", [round(x/gdp*100,3) for x,_ in p])
b=[x/(1+r) for x,r in p]; sb=sum(b)
print("2022 bases", b, "sum", sb, "gdp22", gdp/(1+g))
print("2022 shares (sum)", [round(x/sb*100,3) for x in b])
print("2022 shares (gdp22)", [round(x/(gdp/(1+g))*100,3) for x in b])
print("Q2")
ind={'批发零售':(4248.59,0.074),'交通运输':(2029.96,0.122),'住宿餐饮':(515.99,-0.105),'金融':(2736.74,0.075)}
inc={k:v*r/(1+r) for k,(v,r) in ind.items()}
for k,v in sorted(inc.items(), key=lambda x:-x[1]): print(k, v)
print("Q3")
rev=18994.25; r=0.103
x=rev; y=2023
while x<=27000:
    y+=1; x*=1+r; print(y, x)
print("n", math.log(27000/rev)/math.log(1+r))
print("Q4")
pr=1729.68
m23=pr/rev*100; m22=(pr/1.307)/(rev/1.103)*100
print("margin23", m23, "margin22", m22, "diff", m23-m22)
print("formula", m23*(0.307-0.103)/1.307)
print("Q5")
print("1:", 13.2-(-3.9))
print("2: ratio", 2736.74/515.99, "more by", 2736.74/515.99-1)
print("3: gdp22", gdp/1.046)
