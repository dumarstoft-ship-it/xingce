gdp=266.02; v=[28.66,82.29,155.07]; g=[5.8,2.7,3.6]; pull=[0.4,0.8,2.3]
print("Q1 sum pull", sum(pull))
print("Q1 check: sum v", sum(v), "base", sum(x/(1+r/100) for x,r in zip(v,g)), "growth", gdp/sum(x/(1+r/100) for x,r in zip(v,g))-1)
print("Q2")
inc=[x/(1+r/100)*r/100 for x,r in zip(v,g)]
print("inc", inc, [round(i/sum(inc)*100,1) for i in inc])
print("pull ratio", [round(p/sum(pull)*100,1) for p in pull])
print("structure", [round(x/gdp*100,2) for x in v])
pies = {'A':[63.4,150.4],'B':[70.0,238.9],'C':[39.0,150.2],'D':[133.8,277.4]}
for k,(b1,b2) in pies.items():
    print(k, [round(b1/3.6,1), round((b2-b1)/3.6,1), round((360-b2)/3.6,1)])
print("Q3")
sep = 183.37-158.65
print("sep", sep, "Q4", 3*sep, "total", 183.37+3*sep)
print("Q4")
s19=[3.8,28.6,67.6]; s18=[4.2,28.4,67.4]
for i in range(3):
    a = 183.37*s19[i]/100 - 158.65*s18[i]/100
    print(i+1, a, a/sep*100, "vs", s19[i])
print("Q5")
print("A", [round(x/gdp*100,1) for x in v])
print("B", 82.29/1.027)
print("C", (183.37/158.65-1)*100)
print("D", 158.65*(28.4-4.2)/100, "trap 1-9:", 183.37*(28.6-3.8)/100)
print("1-8 growth", -2.4+3.5)
