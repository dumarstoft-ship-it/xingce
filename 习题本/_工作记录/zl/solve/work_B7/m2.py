print("Q1")
g_send_2022 = 1.0+3.4
g_conv_2022 = 20.4-21.1
print(g_send_2022, g_conv_2022, g_send_2022-g_conv_2022)
print("Q2")
tab = {'煤':(278101,1.9),'冶炼物资':(90986,-5.3),'石油':(13050,5.4),'粮食':(6847,-8.0),'化肥及农药':(5027,-7.2),'集装箱':(79111,7.4)}
mx = max(tab, key=lambda k: tab[k][1]); mn = min(tab, key=lambda k: tab[k][1])
print(mx, mn, tab[mx][0]/tab[mn][0], 23/2, 55, 1/40, 2/7)
print("Q3")
inc = 190/1.18*0.18
print("inc", inc)
v = 190; y = 2023
while v <= 300:
    v += inc; y += 1
    print(y, v)
print("Q4")
conv23 = 51189.74; fr23 = 36460.39
conv22 = conv23/1.204; fr22 = fr23/1.014
p23 = conv23-fr23; p22 = conv22-fr22
print("p23", p23, "p22", p22, "inc", p23-p22, "growth", p23/p22-1)
print("conv inc", conv23-conv22, "fr inc", fr23-fr22)
print("Q5")
print("A", (1.002*1.048-1)*100)
oth = fr23-32638.50
print("B other share", oth, oth/fr23*100)
print("C grain 2022", 6847/0.92, "fert 2022", 5027/0.928)
print("D avg dist 2023 vs 2022 ratio", (1-0.001)/(1+0.002))
print("D 2023 avg", 32638.50/39.11, "2022 avg", (32638.50/0.999)/(39.11/1.002))
