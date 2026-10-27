# MK2726X-M2
w23=0.015; w22=0.015-0.041
a23=-0.012; a22=-(0.012+0.028)
print("2022 weight g", w22, " 2022 amount g", a22)
r=((1+a23)*(1+a22))/((1+w23)*(1+w22))
print("Q1 per-ton 2023 vs 2021 %:", (r-1)*100)
n={2020:18500,2021:20200,2022:18800,2023:19000}
wt={2020:426,2021:463,2022:415,2023:420}
am={2020:155.5,2021:222.4,2022:227.4,2023:231.0}
print("Q2 2022 count g%", (n[2022]/n[2021]-1)*100, " weight g%", (wt[2022]/wt[2021]-1)*100, " amount g%", (am[2022]/am[2021]-1)*100)
pu={y:am[y]*1e8/(n[y]*1e4) for y in n}
print("Q3 yuan per unit:", pu, " diff 2021-2020:", pu[2021]-pu[2020])
pt={y:am[y]*1e8/(wt[y]*1e4) for y in n}
print("Q4 yuan per ton:", pt, " >5000:", [y for y in pt if pt[y]>5000])
print("Q5 A total weight:", sum(wt.values()))
print("Q5 B min count year:", min(n,key=n.get), " min weight year:", min(wt,key=wt.get))
t22=3.76/(1+w23); t21=t22/(1+w22)
print("Q5 C total weight 2022:", t22, " 2021:", t21)
print("Q5 D e-waste amount g%:", (am[2023]/am[2022]-1)*100, " vs total -1.2%")
print("   shares: 2023", am[2023]/13000*100, " 2022", am[2022]/(13000/(1+a23))*100)
