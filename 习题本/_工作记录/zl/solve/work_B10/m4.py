# MK2728X-M3 民航机场吞吐量
pax = {2020:(8.57,-0.366),2021:(9.07,0.058),2022:(5.20,-0.427),2023:(12.60,1.423),2024:(14.60,0.159)}
crg = {2020:(1607.49,-0.060),2021:(1782.80,0.109),2022:(1453.05,-0.185),2023:(1683.31,0.158),2024:(2006.19,0.192)}
# Q1 2019-2024 年均旅客
p2019 = pax[2020][0]/(1+pax[2020][1])
s = p2019 + sum(v[0] for v in pax.values())
print("Q1 2019", p2019, "sum6", s, "avg", s/6, " trap 5yr avg", sum(v[0] for v in pax.values())/5, " trap sum5/6", sum(v[0] for v in pax.values())/6)
# Q2 2024 旅客分地区占比
reg_p = {"东部":(7.57,0.186),"中部":(1.61,0.128),"西部":(4.49,0.126),"东北":(0.93,0.158)}
reg_c = {"东部":(1376.68,0.141),"中部":(240.19,0.585),"西部":(325.27,0.219),"东北":(64.05,0.100)}
print("Q2 sum", sum(v[0] for v in reg_p.values()))
for k,v in reg_p.items(): print("  ", k, round(100*v[0]/14.60,2))
print("  西/中", 4.49/1.61)
# Q3 东部 / (中+西) 货邮
zx = 240.19+325.27
print("Q3 中+西", zx, "ratio", 1376.68/zx, " 多几倍", 1376.68/zx-1)
# Q4 比重均高于上年
Tp, Tc = (14.60,0.159), (2006.19,0.192)
for k in reg_p:
    sp_now = reg_p[k][0]/Tp[0]; sp_prev = (reg_p[k][0]/(1+reg_p[k][1]))/(Tp[0]/(1+Tp[1]))
    sc_now = reg_c[k][0]/Tc[0]; sc_prev = (reg_c[k][0]/(1+reg_c[k][1]))/(Tc[0]/(1+Tc[1]))
    print("Q4", k, "pax", round(100*sp_prev,3), "->", round(100*sp_now,3), sp_now>sp_prev, "| cargo", round(100*sc_prev,3), "->", round(100*sc_now,3), sc_now>sc_prev)
# Q5
vals = sorted(v[0] for v in crg.values()); print("Q5A sorted", vals, "median", vals[2])
print("Q5B max pax growth year", max(pax, key=lambda y: pax[y][1]), " max cargo growth year", max(crg, key=lambda y: crg[y][1]))
c2019 = crg[2020][0]/(1+crg[2020][1])
print("Q5C 2019 cargo", c2019, "2021/2019-1", crg[2021][0]/c2019-1, " 间隔增速", (1+crg[2020][1])*(1+crg[2021][1])-1)
print("Q5D", crg[2022][1]*100 - pax[2022][1]*100)
