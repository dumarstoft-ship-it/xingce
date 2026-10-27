# MK2712X-M1 支付体系运行
print("Q1")
unit=9517.38/10000; per=141.26; tot=142.21
print("sum now", unit+per)
base=unit/1.0293+per/1.0037
print("base", base, "growth % (using tot)", (tot/base-1)*100, "(using sum)", ((unit+per)/base-1)*100)

print("Q2")
print("debit per capita", 6.78*87.82/95.73)
print("population implied (亿)", 95.73/6.78)
print("card sum", 87.82+7.91)

print("Q3")
items={'商户':(2561.38,161.47),'POS':(3309.74,246.33),'ATM':(88.27,1.32)}
gr={}
for k,(now,dec) in items.items():
    gr[k]=-dec/(now+dec)*100
    print(k, "base", now+dec, "growth", gr[k])
print("max-min", max(gr.values())-min(gr.values()))

print("Q4")
print("avg per bill growth", ((1-0.0384)/(1-0.1593)-1)*100)
print("trap: ", ((1-0.1593)/(1-0.0384)-1)*100)

print("Q5")
print("A: 2022Q1 noncash count", 1145.87/1.1846)
print("B: basic share", 6689.88/9517.38*100, "sum unit", 6689.88+2324.42+483.12+19.96)
print("C: avg per bill (万元)", 23.63e12/2417.44e4/1e4)
print("D: counts", 1782.31, 628.50, 2.36, 4.27, "amounts(亿)", 17.81e4, 5.72e4, 316.25, 756.42)
print("bill sum count", 1782.31+628.50+2.36+4.27, "amount", 17.81+5.72+0.031625+0.075642)
