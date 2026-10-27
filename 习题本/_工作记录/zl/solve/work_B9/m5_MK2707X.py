# MK2707X-M3
yrs = list(range(2016,2023))
qty = [2267,2325,2443,2658,2408,2646,2818]
qg  = [-2.7,2.6,5.1,8.8,-9.4,9.9,6.5]
val = [210.92,202.01,205.64,235.15,200.48,215.72,229.00]
vg  = [-12.6,-4.2,1.8,14.4,-14.7,7.6,6.2]
# Q1
print("Q1 by rates", (1.062/1.065-1)*100, " by values", ((val[6]/qty[6])/(val[5]/qty[5])-1)*100)
print("  actual growth qty", (qty[6]/qty[5]-1)*100, "val", (val[6]/val[5]-1)*100)
# Q2
print("Q2 sum 2018-2022", sum(qty[2:]))
# Q3
for i in range(4):
    print("Q3", yrs[i], val[i]/qty[i]*1e4, "万美元/架")
# Q4
base2015 = val[0]/(1+vg[0]/100)
incs = [val[0]-base2015] + [val[i]-val[i-1] for i in range(1,7)]
for y,inc in zip(yrs,incs):
    print("Q4", y, round(inc,2))
# Q5
base2015q = qty[0]/(1+qg[0]/100)
qincs = [qty[0]-base2015q] + [qty[i]-qty[i-1] for i in range(1,7)]
for y,inc in zip(yrs,qincs):
    print("Q5", y, round(inc,1))
