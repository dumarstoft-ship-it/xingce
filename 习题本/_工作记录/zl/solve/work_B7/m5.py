yrs = [2019,2020,2021,2022,2023]
tour = dict(zip(yrs,[6006,2879,3246,2530,4891]))
nat = dict(zip(yrs,[953.3,774.1,899.3,808.1,1004.6]))
urb = dict(zip(yrs,[1062.6,870.3,1009.6,875.6,1111.8]))
rur = dict(zip(yrs,[634.7,530.5,613.6,592.8,649.0]))
avg = sum(tour.values())/5
print("Q1 avg", avg, [y for y in yrs if tour[y]>avg])
print("Q2")
U = 4891e6*0.768*1111.8; R = 4891e6*0.232*649.0
print(U/1e12, R/1e12, (U-R)/1e12, "万亿")
print("check total", 4891e6*1004.6/1e12, (U+R)/1e12)
print("Q3", (1.933*1.243-1)*100)
print("Q3 chart", (tour[2023]*nat[2023])/(tour[2022]*nat[2022])-1)
print("Q4")
for nm,d in [('tour',tour),('nat',nat),('urb',urb),('rur',rur)]:
    print(nm, (d[2022]/d[2021]-1)*100)
print("Q5 increments")
pix = [-112,90,-22,62]
for nm,d in [('tour',tour),('nat',nat),('urb',urb),('rur',rur)]:
    inc = [round(d[y]-d[y-1],1) for y in yrs[1:]]
    sc = [i/abs(inc[0])*112 for i in inc]
    print(nm, inc, [round(s,1) for s in sc])
print("pix", pix)
