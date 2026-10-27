# MK2705X-M3 employee medical insurance
years = list(range(2015, 2023))
n = [28893, 29532, 30322, 31681, 32924, 34455, 35430, 36243]
N = dict(zip(years, n))
# Q1
for name, v, inc in [("企业", 24400, 356), ("机关事业", 6572, 37), ("灵活就业等其他", 5272, 420)]:
    print("Q1", name, "growth", inc/(v-inc))
# Q2
print("Q2 13th FYP avg annual increase", (N[2020]-N[2015])/5, "wrong-base", (N[2020]-N[2016])/5)
print("Q2 avg level 2016-2020", sum(N[y] for y in range(2016, 2021))/5)
# Q3
inc21 = 13160.17/1.109; exp21 = 9558.40/1.025
print("Q3 2021 income", inc21, "expense", exp21, "ratio", inc21/exp21, "opts", 5/2, 7/2, 3/2, 4/3)
# Q4
for y in range(2018, 2022):
    print("Q4", y, "increment", N[y]-N[y-1])
# Q5
a1 = sum(N[y] for y in (2020, 2021, 2022))/3; a2 = sum(N[y] for y in (2016, 2017, 2018))/3
print("Q5-1 avg 2020-22", a1, "avg 2016-18", a2, "ratio", a1/a2)
print("Q5-2 in-service share 2022", 26604/36243, "2021", (26604/1.019)/(36243/1.023))
cum21 = 21393.11 - 3601.77
bal21 = inc21 - exp21
cum20 = cum21 - bal21
print("Q5-3 check 2022 balance", 13160.17-9558.40, "cum2021", cum21, "bal2021", bal21, "cum2020", cum20)
