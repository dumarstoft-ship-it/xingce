prod = {2014:12089,2015:11215,2016:11176,2017:11379,2018:11937,2019:12169,2020:12014,2021:11454,2022:11236,2023:11376,2024:11457}
area = {2014:2606,2015:2359,2016:2333,2017:2318,2018:2434,2019:2416,2020:2353,2021:2187,2022:2180,2023:2123,2024:2220}
print("Q1 unit yield (吨/亩 *1):")
for y in range(2016,2021):
    print(y, prod[y]/area[y])
print("Q2")
g = prod[2024]/prod[2023]-1
print("g2024", g)
p2025 = prod[2024]*(1+g)
print("2025", p2025)
tot = sum(prod[y] for y in range(2021,2025)) + p2025
print("total 2021-2025", tot)
print("total 2021-2024", sum(prod[y] for y in range(2021,2025)))
print("total 2016-2020", sum(prod[y] for y in range(2016,2021)))
print("Q3")
top3 = 6929.81+1687.15+1227.16
r68 = 80.77+77.18+59.79
print(top3, r68, top3/r68)
print("Q4")
yn = 1687.15
inc = yn/1.063*0.063
nat = prod[2024]-prod[2023]
print(inc, nat, inc/nat)
print("Q5 area growth")
for y in range(2015,2025):
    print(y, (area[y]/area[y-1]-1)*100)
