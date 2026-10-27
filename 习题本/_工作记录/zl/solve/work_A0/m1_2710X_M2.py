# MK2710X-M2 南昌人口
print("Q1")
u22=516.01; r22=137.80; tot22=653.81
u21=u22-9.78; r21=r22-0.28; tot21=u21+r21
rate22=u22/tot22*100; rate21=u21/tot21*100
print("tot22 check", u22+r22, "rate22 calc", rate22, "given 78.92")
print("u21",u21,"r21",r21,"tot21",tot21,"rate21",rate21,"diff",78.92-rate21, rate22-rate21)

print("Q2")
b21=4.58; br21=7.21; ng21=2.19
dr21=br21-ng21
print("death rate 21", dr21, "deaths21", b21*dr21/br21)
# check 2022
print("2022 check: deaths", 4.01*(6.19-0.73)/6.19, "given 3.54")

print("Q3")
p60_22=tot22*0.1521; p65_22=tot22*0.1118
p60_21=p60_22-4.75; p65_21=p65_22-4.20
print("p60_22",p60_22,"p65_22",p65_22,"p60_21",p60_21,"p65_21",p65_21,"ratio",p65_21/p60_21)
print("via shares", (11.18-0.48)/(15.21-0.50))
print("2022 ratio", 11.18/15.21)
# check tot21 from share change
# 60+ 2021 share 14.71% -> tot21 = p60_21/0.1471
print("tot21 implied by 60+", p60_21/0.1471, "by 65+", p65_21/0.1070)

print("Q4")
d={'东湖区':(41.89,94.43),'西湖区':(49.17,100.00),'青云谱区':(36.04,100.00),'青山湖区':(68.84,95.12),
'新建区':(61.28,71.61),'红谷滩区':(64.45,91.92),'南昌县':(123.86,63.25),'安义县':(26.77,55.11),
'进贤县':(65.07,52.78),'经开区':(57.30,87.01),'高新区':(47.58,82.51),'湾里管理局':(11.56,52.66)}
u={k:v[0]*v[1]/100 for k,v in d.items()}
for k,v in sorted(u.items(), key=lambda x:-x[1]): print(k, round(v,3))
print("sum pop", sum(v[0] for v in d.values()), "sum urban", sum(u.values()))
opts=['西湖区','青山湖区','红谷滩区','经开区']
print("options ranking:", sorted(opts, key=lambda k:-u[k]))

print("Q5")
nc_f=123.86*100/(100+109.46)
gx_m=47.58*111.87/(100+111.87)
print("nanchang county female", nc_f, "gaoxin male", gx_m, "ratio", nc_f/gx_m)
