# MK2730X-M3
tot22=64931; tot21=tot22/1.04
print('tot21', tot21)
print('Q1 east21 via share', tot21*0.475, ' via 2022 share/growth', tot22*0.468/1.025)
print('check shares 2022', 18685/tot22*100, 3328/tot22*100)
print('sum shares', 47.5+18.5+28.7+5.3, 46.8+19.3+28.8+5.1)
print('Q2 west growth via actual', (18685/(tot21*0.287)-1)*100, ' via shares', (1.04*28.8/28.7-1)*100)
print('Q3', (1.214/1.135-1)*100)
a=6793; ar=0.023; b=31580; br=0.006
cur=a/b; base=(a/(1+ar))/(b/(1+br))
print('Q4 cur', cur*100, 'base', base*100, 'diff pp', (cur-base)*100, 'formula', cur*(ar-br)/(1+ar)*100)
# Q5
third_inc = 11379*0.049/1.049; tot_inc = tot22*0.04/1.04
print('Q5 2: third inc', third_inc, 'tot inc', tot_inc, 'ratio', third_inc/tot_inc*100)
print('Q5 3:', 17163/4121, (17163-4121)/4121, 4121*5)
# check sum of industry
print('sum industries', 858+42364+11379+10331)
print('mfg parts sum', 17163+6793+4121+3503)
