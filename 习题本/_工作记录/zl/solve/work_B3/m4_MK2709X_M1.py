# MK2709X-M1
yrs = [2018,2019,2020,2021,2022,2023,2024]
users = [4.1,4.0,4.2,5.4,5.2,5.5,5.9]
share = [49.0,44.0,42.3,52.7,48.8,49.9,53.4]
net = {y: u/(s/100) for y,u,s in zip(yrs,users,share)}
print("网民:", {y: round(v,4) for y,v in net.items()})
print("Q1: 2024-2020 =", net[2024]-net[2020])

ug = {yrs[i]: (users[i]/users[i-1]-1)*100 for i in range(1,7)}
print("Q2 外卖用户增速:", {y: round(v,3) for y,v in ug.items()})

print("Q3:")
inc_rate = 2.7*0.148/1.148
print("  增量(增速法) =", inc_rate, "  增量(作差法) =", 2.7-2.4)
for inc,label in [(inc_rate,"增速法"),(0.3,"作差法")]:
    v = 2.7; y = 2024
    seq=[]
    while v <= 4:
        y += 1; v += inc; seq.append((y, round(v,4)))
    print("  ", label, seq)
print("  (4-2.7)/inc:", (4-2.7)/inc_rate, (4-2.7)/0.3)
# consistency check of chart chain
v = 2.7
for y,g in [(2024,0.148),(2023,0.151),(2022,0.152),(2021,0.163),(2020,-0.019)]:
    v = v/(1+g); print("   back-chain value of", y-1, "=", round(v,4))

ng = {y: (net[y]/net[y-1]-1)*100 for y in yrs[1:]}
print("Q4 网民增速:", {y: round(v,3) for y,v in ng.items()})

print("Q5:")
g = {2020:-0.019,2021:0.163,2022:0.152,2023:0.151,2024:0.148}
val = {2020:1.5,2021:1.8,2022:2.1,2023:2.4,2024:2.7}
print(" A 增量(增速法,亿元):", {y: round(val[y]*g[y]/(1+g[y])*1e4,1) for y in g})
v19 = 1.5/(1-0.019)
print(" B 2019 =", v19, " 2024/2019-1 =", (2.7/v19-1)*100, " chained growth =", (0.981*1.163*1.152*1.151*1.148-1)*100)
print(" C share up years:", [y for i,y in enumerate(yrs) if i>0 and share[i]>share[i-1]], " compare growth:", {y: (round(ug[y],2), round(ng[y],2), ug[y]>ng[y]) for y in yrs[1:]})
print(" D sum =", sum(val.values()))
