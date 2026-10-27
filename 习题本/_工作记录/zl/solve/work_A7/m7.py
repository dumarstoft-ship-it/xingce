# MK2713X-M1 Shanghai finance
t={2018:1645.78,2019:1934.31,2020:2274.83,2021:2511.07,2022:2932.98}
print("check 2022 growth", t[2022]/t[2021]-1)
print("Q1 securities growth", 3121/(30110-3121), " (wrong base 30110:", 3121/30110, ") stocks growth", 134/(2213-134))
print("Q2 avg 2019-2022", sum(t[y] for y in range(2019,2023))/4, " avg 2018-2022", sum(t.values())/5, " avg 2018-2021", sum(t[y] for y in range(2018,2022))/4)
p21=663.05/1.049; l21=1431.96/1.07
print("Q3 sum22", 663.05+1431.96, "2021", p21+l21, "growth", 2095.01/(p21+l21)-1)
inc=t[2022]-t[2021]
f={2023:t[2022]+inc,2024:t[2022]+2*inc,2025:t[2022]+3*inc}
cum=t[2021]+t[2022]+sum(f.values())
print("Q4 inc",inc,f,"cum 2021-2025",cum)
incs={y:t[y]-t[y-1] for y in range(2019,2023)}
print("Q5A incs", incs)
print("Q5B claims ratio", 654.55/2095.01, "1/3 of premium", 2095.01/3)
print("Q5C 2023", t[2022]*1.168, "2x2018", 2*t[2018], "ratio", t[2022]*1.168/t[2018])
print("Q5D stock decrease", 96.26/(1-0.156)*0.156, " (wrong 96.26*0.156", 96.26*0.156, ")")
