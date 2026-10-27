# MK2734X-M2 sugar crops
years = list(range(2014, 2025))
prod = [12089,11215,11176,11379,11937,12169,12014,11454,11236,11376,11457]  # 万吨
area = [2606,2359,2333,2318,2434,2416,2353,2187,2180,2123,2220]  # 万亩
P = dict(zip(years, prod)); A = dict(zip(years, area))
print("Q1 unit yield (吨/亩 = 万吨/万亩) 2016-2020:")
for y in range(2016, 2021):
    print(y, P[y]/A[y])
print()
# Q2
g24 = P[2024]/P[2023]-1
p25 = P[2024]*(1+g24)
print("Q2 g24=", g24, "p25=", p25)
tot = sum(P[y] for y in range(2021,2025)) + p25
print("total 2021-2025:", tot, "sum 2021-2024:", sum(P[y] for y in range(2021,2025)))
print()
# Q3
top3 = 6929.81+1687.15+1227.16
r68 = 80.77+77.18+59.79
print("Q3 top3=", top3, "r6-8=", r68, "ratio=", top3/r68)
print()
# Q4
yn = 1687.15
inc_yn = yn/1.063*0.063
inc_nat = P[2024]-P[2023]
print("Q4 inc_yn=", inc_yn, "inc_nat=", inc_nat, "contrib=", inc_yn/inc_nat)
print()
# Q5 area yoy growth
gA = {y: A[y]/A[y-1]-1 for y in range(2015, 2025)}
for y in gA: print(y, round(gA[y]*100, 3))
for s,e in [(2015,2018),(2017,2020),(2019,2022),(2021,2024)]:
    seq = [gA[y] for y in range(s,e+1)]
    diffs = [seq[i+1]-seq[i] for i in range(len(seq)-1)]
    print(s,e,[round(x*100,3) for x in seq], "diffs", [round(d*100,3) for d in diffs])
