# MK2723X-M1 catering / takeaway
mkt={2016:1663,2017:2741,2018:4250,2019:5779,2020:6646,2021:8117,2022:9417}
# Q1
per_year=8117/5.44   # 元/人/年 (亿元/亿人)
print("Q1 per year",per_year,"per month",per_year/12)
# Q2
print("Q2 sum 2016-2020", sum(mkt[y] for y in range(2016,2021)))
print("   other sums: 2017-2020",sum(mkt[y] for y in range(2017,2021)),"2016-2019",sum(mkt[y] for y in range(2016,2020)),"2018-2022",sum(mkt[y] for y in range(2018,2023)))
# Q3
r20=(1-0.005)**2/(1+0.186)-1
c20=46895/1.186; c19=46895/(0.995**2)
print("Q3 2020 growth",r20,"c20",c20,"c19",c19)
# Q4
share20=0.106-0.005
print("Q4 retail 2020 (万亿)", c20/share20/1e4, " wrong: using 10.6%:",c20/0.106/1e4," using 11.1%:",c20/0.111/1e4, " 2021 retail:",46895/0.106/1e4)
# Q5
inc={y:mkt[y]-mkt[y-1] for y in range(2017,2023)}
print("Q5 increments",inc)
for s in [2020,2019,2018,2017]:
    print(s,s+2,[inc[y] for y in range(s,s+3)])
