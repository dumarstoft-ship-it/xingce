# MK2726X-M2 再生资源 & 废弃电器电子产品
w23=3.76; wg23=1.5; wg22=1.5-4.1
amt23=1.3; ag23=-1.2; ag22=-(1.2+2.8)
tab = {2020:(18500,426,155.5),2021:(20200,463,222.4),2022:(18800,415,227.4),2023:(19000,420,231.0)}
wr = (1+wg23/100)*(1+wg22/100); ar = (1+ag23/100)*(1+ag22/100)
print("Q1 2022 weight g", wg22, " 2022 amount g", ag22)
print("   weight 2yr ratio", wr, " amount 2yr ratio", ar, " per-ton change %.4f%%" % ((ar/wr-1)*100))
n21,t21,m21 = tab[2021]; n22,t22,m22 = tab[2022]
print("Q2 2022 growth: 数量 %.3f%%  重量 %.3f%%  金额 %.3f%%" % ((n22/n21-1)*100,(t22/t21-1)*100,(m22/m21-1)*100))
pc = {y:(v[2]*1e8)/(v[0]*1e4) for y,v in tab.items()}
print("Q3 per-unit (yuan/台):", {y:round(v,3) for y,v in pc.items()}, " 2021-2020 diff", pc[2021]-pc[2020])
pt = {y:(v[2]*1e8)/(v[1]*1e4) for y,v in tab.items()}
print("Q4 per-ton (yuan/吨):", {y:round(v,1) for y,v in pt.items()}, " >5000:", [y for y,v in pt.items() if v>5000])
print("Q5 A total weight", sum(v[1] for v in tab.values()))
print("   B min count year", min(tab, key=lambda y: tab[y][0]), " min weight year", min(tab, key=lambda y: tab[y][1]))
print("   C 2021 total weight (亿吨)", w23/wr)
print("   D e-waste amount growth 2023 %.3f%% vs total %.1f%%" % ((tab[2023][2]/tab[2022][2]-1)*100, ag23))
print("     share 2023 %.4f%%  share 2022 %.4f%%" % (tab[2023][2]/(amt23*1e4)*100, tab[2022][2]/(amt23*1e4/(1+ag23/100))*100))
