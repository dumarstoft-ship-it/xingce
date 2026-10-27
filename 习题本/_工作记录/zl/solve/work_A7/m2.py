# MK2718X-M3 domestic tourism
yrs=[2019,2020,2021,2022,2023]
tour=dict(zip(yrs,[6006,2879,3246,2530,4891]))  # 百万人次
nat=dict(zip(yrs,[953.3,774.1,899.3,808.1,1004.6]))
urb=dict(zip(yrs,[1062.6,870.3,1009.6,875.6,1111.8]))
rur=dict(zip(yrs,[634.7,530.5,613.6,592.8,649.0]))
print("check text: 2023 tourist growth", tour[2023]/tour[2022]-1, "per cap growth", nat[2023]/nat[2022]-1)
avg=sum(tour.values())/5
print("Q1 avg", avg, [y for y in yrs if tour[y]>avg])
# Q2
u_cnt=4891*0.768; r_cnt=4891*0.232   # 百万人次
u_sp=u_cnt*1e6*1111.8/1e12; r_sp=r_cnt*1e6*649.0/1e12  # 万亿元
print("Q2 urban count",u_cnt,"rural count",r_cnt,"urban spend(万亿)",u_sp,"rural spend",r_sp,"diff",u_sp-r_sp)
tot23=4891e6*1004.6/1e12
print("  total 2023 spend 万亿", tot23, "u+r", u_sp+r_sp)
# Q3
g=(1+0.933)*(1+0.243)-1
print("Q3 growth", g, "check via data", tour[2023]*nat[2023]/(tour[2022]*nat[2022])-1)
# Q4
for name,d in [("tour",tour),("nat",nat),("urb",urb),("rur",rur)]:
    print("Q4",name, d[2022]/d[2021]-1)
# Q5
for name,d in [("tour",tour),("nat",nat),("urb",urb),("rur",rur)]:
    incs=[round(d[y]-d[y-1],1) for y in range(2020,2024)]
    print("Q5",name,incs)
