# MK2734X-M1
tot24=73439; urb24=47345; rur24=26094
urb20=urb24-1074; rur20=rur24+2699
tot20=urb20+rur20
print("check sum 2024:", urb24+rur24, tot24)
print("Q1 2020 total:", tot20, " growth%:", (tot24/tot20-1)*100)
# Q2
pop=94350/0.67
print("Q2 total pop:", pop, " female emp share%:", 31900/pop*100)
print("   trap: 43.4% * 73439/pop", 43.4*tot24/pop)
# Q3
print("Q3 increase:", 29973*0.049/1.049)
# Q4
s20=(35866-60)/tot20*100
s24=35866/tot24*100
print("Q4 2020 share:", s20, " 2024 share:", s24, " diff:", s24-s20, " using 48.8:", 48.8-s20)
# Q5
U=urb24*0.051/(1-0.051)
print("Q5 A unemployed:", U, " trap 94350*5.1%:", 94350*0.051)
male=tot24-31900
print("Q5 B male/female:", male/31900, " via pct:", 56.6/43.4, " 4/3=", 4/3)
print("Q5 C 2020 rate:", 5.1+0.5)
mw20=29973/1.049
print("Q5 D 2020 migrant workers:", mw20, " 13000/mw20:", 13000/mw20*100)
