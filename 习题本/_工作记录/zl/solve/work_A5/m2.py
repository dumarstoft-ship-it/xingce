# MK2723X-M3  H省 2023
gdp=43944.1; g=5.5; g_prev = 5.5-1.7
p1,p2,p3 = 4466.2,16435.3,23042.6
grain=3809.9; grain_g=-1.4
xia=1498.6; xia_g=0.8; qiu=2311.3
meat=491.1; meat_g=3.3; egg=404.6; egg_g=1.6; milk=571.9; milk_g=4.6
print("Q1 2022夏粮比重:", xia/grain*(1+grain_g/100)/(1+xia_g/100)*100)
print("   2023 current share", xia/grain*100, " check xia+qiu", xia+qiu)
print("   2022 xia, grain:", xia/1.008, grain/0.986)
print("Q2 2022 growth rates: 规上", 6.9-1.4, "制造业", 6.4-2.4, "采矿业", 13.0+4.5, "电力等", 5.8+1.9)
for n,v,gg in [('粮食',grain,grain_g),('肉',meat,meat_g),('蛋',egg,egg_g),('奶',milk,milk_g)]:
    print("Q3", n, "change %.3f" % (v*gg/(100+gg)))
print("Q4 2022 growth", g_prev, " 2021 GDP:", gdp/(1+g/100)/(1+g_prev/100))
print("Q5 shares:", p1/gdp*100, p2/gdp*100, p3/gdp*100, " sum", p1+p2+p3)
