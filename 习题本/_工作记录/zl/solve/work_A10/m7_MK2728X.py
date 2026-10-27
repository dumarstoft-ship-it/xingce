# MK2728X-M3 civil aviation airports 2024
years = [2020, 2021, 2022, 2023, 2024]
pax = [8.57, 9.07, 5.20, 12.60, 14.60]; pax_g = [-36.6, 5.8, -42.7, 142.3, 15.9]
cargo = [1607.49, 1782.80, 1453.05, 1683.31, 2006.19]; cargo_g = [-6.0, 10.9, -18.5, 15.8, 19.2]
# Q1
p2019 = pax[0]/(1+pax_g[0]/100)
s = p2019 + sum(pax)
print("Q1 2019 pax", p2019, "sum 2019-2024", s, "avg", s/6, "(2020-24 avg", sum(pax)/5, ")")
# Q2
reg = {"东部": (7.57, 18.6, 1376.68, 14.1), "中部": (1.61, 12.8, 240.19, 58.5),
       "西部": (4.49, 12.6, 325.27, 21.9), "东北": (0.93, 15.8, 64.05, 10.0)}
tp = sum(v[0] for v in reg.values()); tc = sum(v[2] for v in reg.values())
print("Q2 sums", tp, tc)
for k, v in reg.items():
    print("Q2", k, "pax share %", round(v[0]/14.60*100, 2), "angle", round(v[0]/14.60*360, 1))
# Q3
e = 1376.68; mw = 240.19 + 325.27
print("Q3 east", e, "mid+west", mw, "ratio", e/mw, "多倍", e/mw - 1)
# Q4
for k, v in reg.items():
    ps24 = v[0]/14.60; ps23 = (v[0]/(1+v[1]/100))/(14.60/1.159)
    cs24 = v[2]/2006.19; cs23 = (v[2]/(1+v[3]/100))/(2006.19/1.192)
    print("Q4", k, "pax share up", ps24 > ps23, round(ps24*100, 4), round(ps23*100, 4),
          "| cargo share up", cs24 > cs23, round(cs24*100, 3), round(cs23*100, 3))
# Q5
print("Q5A sorted cargo", sorted(cargo), "median", sorted(cargo)[2])
print("Q5B max pax growth year", years[pax_g.index(max(pax_g))], "max cargo growth year", years[cargo_g.index(max(cargo_g))])
c2019 = cargo[0]/(1+cargo_g[0]/100)
print("Q5C 2019 cargo", c2019, "2021 vs 2019", cargo[1]/c2019 - 1, "via rates", (1-0.06)*(1+0.109)-1)
print("Q5D 2022 pax g - cargo g", pax_g[2] - cargo_g[2])
