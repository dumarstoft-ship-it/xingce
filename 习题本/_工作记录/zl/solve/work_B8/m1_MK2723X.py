# MK2723X-M1 外卖/餐饮
size = {2016:1663, 2017:2741, 2018:4250, 2019:5779, 2020:6646, 2021:8117, 2022:9417}
# Q1 人均月消费 = 8117亿/5.44亿人/12
print("Q1 annual per person", 8117/5.44, "monthly", 8117/5.44/12)
# Q2 十三五 2016-2020 sum
print("Q2 sum 2016-2020", sum(size[y] for y in range(2016,2021)))
print("   other sums: 2016-2019", sum(size[y] for y in range(2016,2020)), "2017-2021", sum(size[y] for y in range(2017,2022)), "2018-2022", sum(size[y] for y in range(2018,2023)))
# Q3 2020 growth: (1+r20)(1+18.6%) = (1-0.5%)^2
r20 = (1-0.005)**2/1.186 - 1
print("Q3 r2020", r20)
# Q4 2020 社零: 2020餐饮收入 = 46895/1.186; share2020 = 10.6%-0.5% = 10.1%
c20 = 46895/1.186
print("Q4 2020 catering", c20, "retail total (万亿)", c20/0.101/10000)
print("   wrong: 46895/0.101", 46895/0.101/10000, "c20/0.106", c20/0.106/10000, "46895/0.106", 46895/0.106/10000, "c20/0.111", c20/0.111/10000)
# Q5 increments
inc = {y: size[y]-size[y-1] for y in range(2017,2023)}
print("Q5 increments", inc)
# chart pixel positions: p1 y=197, p2 y=58, p3 y=97 -> rise 139, drop 39
print("   chart ratio drop/rise", 39/139)
for a,b,c in [(2020,2021,2022),(2019,2020,2021),(2018,2019,2020),(2017,2018,2019)]:
    print("  ", a, c, inc[a], inc[b], inc[c], "d1", inc[b]-inc[a], "d2", inc[c]-inc[b], "ratio", (inc[b]-inc[c])/(inc[b]-inc[a]) if inc[b]!=inc[a] else None)
