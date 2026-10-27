# MK2704X-M2 电力市场交易
print("Q1")
t23=46578; g=0.081; s23=0.613; ds=0.012
t22=t23/(1+g); s22=s23-ds
print("t22", t22, "s22", s22, "use22", t22/s22, "use23 (trap)", t23/s23, "other", t22/s23, t23/s22)
print("Q2")
prov=35454.3+1480.5+113.2
print("prov sum", prov, "total-inter", t23-9530, "inter sum", 1059.4+8370+100.6)
print("traps", 35454.3+1480.5+113.2-414.3, 35454.3-7201.4+1480.5+113.2)
print("Q3")
a=35454.3/prov*100; b=1059.4/9530*100
print("prov direct share", a, "inter direct share", b, "diff", a-b)
print("Q4")
bj22=8878/1.147; nm22=2571.2/1.322
print("bj22", bj22, "nm22", nm22, "diff", bj22-nm22, "2023 diff", 8878-2571.2)
print("Q5")
sw=7690.9/0.587
print("south grid use", sw, "monthly", sw/10)
