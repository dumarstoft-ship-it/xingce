# MK2731X-M2 travel
years = list(range(2015, 2024))
ren = [39.9, 44.4, 50.0, 55.4, 60.1, 28.8, 32.5, 25.3, 48.9]  # 亿人次
hua = [3.4, 3.9, 4.6, 5.1, 5.7, 2.2, 2.9, 2.0, 4.9]  # 万亿元
R = dict(zip(years, ren)); H = dict(zip(years, hua))

print("Q1 avg spend growth (text rates):", (1+1.403)/(1+0.933)-1)
print("Q1 avg spend growth (chart values):", (4.9/48.9)/(2.0/25.3)-1, 4.9e12/48.9e8, 2.0e12/25.3e8)

# Q2
c22 = 4.2/(1+1.475); n22 = 0.7/(1+1.064)
print("Q2 2022 urban", c22, "rural", n22, "ratio", c22/n22, "多几倍", c22/n22-1)

# Q3
a23 = 4.2e12/37.6e8
a22 = (4.2e12/2.475)/(37.6e8/1.949)
print("Q3 urban avg 2023", a23, "2022", a22, "diff", a23-a22)

# Q4
for y in range(2018, 2024):
    print("Q4", y, H[y], H[y-1], H[y]/H[y-1]-1)
print("Q4 2023 text rate 140.3%")

# Q5
print("Q5A profit per agency (万元)", 37.4e8/56275/1e4)
print("Q5B urban share 2023", 37.6/48.9, "2022", (37.6/1.949)/(48.9/1.933))
s = sum(R[y] for y in range(2016, 2021))
print("Q5C 13th FYP sum", s, "monthly", s/60)
for y in range(2018, 2023):
    print("Q5D", y, H[y], "incr", round(H[y]-H[y-1], 3))
