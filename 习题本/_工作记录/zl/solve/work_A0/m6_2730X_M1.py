# MK2730X-M1 空调累计产量
cum22={8:15722,9:17492,10:18960,11:20449,12:22247}
gr22={8:1.9,9:3.5,10:3.2,11:2.0,12:1.8}
cum23={2:3331,3:6260,4:8870,5:11425,6:14060,7:16348}
gr23={2:10.8,3:12.6,4:12.2,5:14.2,6:16.6,7:17.9}
print("Q1")
h1_22=cum23[6]/(1+gr23[6]/100)
print("2022 H1", h1_22, "2022 H2", cum22[12]-h1_22)
print("alt: 2022 1-7", cum23[7]/(1+gr23[7]/100), "H2 via 1-7?", cum22[12]-cum23[7]/(1.179))
print("Q2")
sep=cum22[9]-cum22[8]; octo=cum22[10]-cum22[9]
print("sep", sep, "oct", octo, "mom", (octo/sep-1)*100)
print("Q3")
jun23=cum23[6]-cum23[5]
jun22=cum23[6]/(1+gr23[6]/100)-cum23[5]/(1+gr23[5]/100)
print("jun23", jun23, "jun22", jun22, "yoy", (jun23/jun22-1)*100)
print("Q4")
print("unit price growth", ((1-0.154)/(1+0.013)-1)*100, "trap", ((1+0.013)/(1-0.154)-1)*100)
print("unit price 2023-07 $/unit", 500028*1000/(308*1e4))
print("Q5")
m={}
for k in [9,10,11,12]: m[k]=cum22[k]-cum22[k-1]
print("monthly", m)
inc={k:m[k]-m[k-1] for k in [10,11,12]}
print("mom increments", inc)
