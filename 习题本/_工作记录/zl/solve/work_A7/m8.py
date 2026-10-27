# MK2732X-M1 X region real estate 2023 (value, growth%)
D = {
 'inv':   ((1168.53,0.8),(823.05,-0.6)),
 'cons':  ((15375.68,-4.4),(10467.79,-4.3)),
 'comp':  ((1297.88,13.7),(950.00,22.1)),
 'sarea': ((1903.23,25.5),(1711.29,24.2)),
 'samt':  ((1167.46,32.1),(989.70,29.4)),
}
def base(v,g): return v/(1+g/100)
# Q1
(T,gt),(R,gr)=D['inv']
s23=R/T; s22=base(R,gr)/base(T,gt)
print("Q1 share23",s23,"share22",s22,"diff pp",(s23-s22)*100, "formula", s23*(gr-gt)/100/(1+gr/100)*100)
# Q2
(T,gt),(R,gr)=D['cons']
T22=base(T,gt); R22=base(R,gr)
print("Q2 total22",T22,"res22",R22,"nonres22",T22-R22," nonres23",T-R)
# Q3
cnt=0
for k,((T,gt),(R,gr)) in D.items():
    T22=base(T,gt); R22=base(R,gr); N=T-R; N22=T22-R22; gn=(N/N22-1)*100
    print("Q3",k,"res g",gr,"total g",gt,"nonres g",round(gn,3),"res faster?",gr>gn)
    cnt+= gr>gn
print("Q3 count",cnt)
# Q4
(T,gt),(R,gr)=D['samt']
T22=base(T,gt); R22=base(R,gr)
print("Q4 nonres23",T-R,"nonres22",T22-R22,"inc",(T-R)-(T22-R22)," total inc",T-T22,"res inc",R-R22)
# Q5
(TA,gta),(RA,gra)=D['sarea']
TA22=base(TA,gta); RA22=base(RA,gra)
print("Q5-1 2022 nonres sales area share", (TA22-RA22)/TA22)
print("Q5-2 2022 unit sales (元/m2)", base(*D['samt'][0])/TA22*1e4)
print("Q5-3 needs 2021 residential sales amount & area -> not given")
