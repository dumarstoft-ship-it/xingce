# MK2707X-M3 general aviation
yrs=list(range(2016,2023))
n=dict(zip(yrs,[2267,2325,2443,2658,2408,2646,2818]))
gn=dict(zip(yrs,[-2.7,2.6,5.1,8.8,-9.4,9.9,6.5]))
v=dict(zip(yrs,[210.92,202.01,205.64,235.15,200.48,215.72,229.00]))
gv=dict(zip(yrs,[-12.6,-4.2,1.8,14.4,-14.7,7.6,6.2]))
for y in yrs[1:]:
    print(y,"n growth calc",round((n[y]/n[y-1]-1)*100,2),"given",gn[y]," v growth calc",round((v[y]/v[y-1]-1)*100,2),"given",gv[y])
print("Q1 via rates", (1.062/1.065-1)*100, " via raw", ((v[2022]/n[2022])/(v[2021]/n[2021])-1)*100)
print("Q2 sum 2018-2022", sum(n[y] for y in range(2018,2023)))
avg={y:v[y]/n[y]*1e4 for y in yrs}  # 万美元/架
print("Q3", {y:round(avg[y],2) for y in range(2016,2020)}, sorted(range(2016,2020), key=lambda y:-avg[y]))
v15=v[2016]/(1+gv[2016]/100)
dec={2016:v[2016]-v15}
dec.update({y:v[y]-v[y-1] for y in yrs[1:]})
print("Q4 v15",v15, {y:round(d,2) for y,d in dec.items()}, "years dec>10:", [y for y,d in dec.items() if d< -10])
n15=n[2016]/(1+gn[2016]/100)
inc={2016:n[2016]-n15}
inc.update({y:n[y]-n[y-1] for y in yrs[1:]})
print("Q5 increments", {y:round(d,1) for y,d in inc.items()})
for s in [2016,2017,2018,2019]:
    print(s,s+3,[round(inc[y],1) for y in range(s,s+4)])
