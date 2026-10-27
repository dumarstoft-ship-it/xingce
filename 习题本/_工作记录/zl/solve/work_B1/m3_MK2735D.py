# MK2735D-M2 power generation 2023
tot = 89090
months = ['1-2','3','4','5','6','7','8','9','10','11','12']
days = {'1-2':59,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31}
daily = {'1-2':228.8,'3':231.4,'4':219.5,'5':222.1,'6':246.6,'7':273.0,'8':272.6,'9':248.5,'10':227.2,'11':243.7,'12':267.4}
yoy = {'2022-12':3.0,'1-2':0.7,'3':5.1,'4':6.1,'5':5.6,'6':2.8,'7':3.6,'8':1.1,'9':7.7,'10':5.2,'11':8.4,'12':8.0}
monthly = {m: daily[m]*days[m] for m in months}
print('sum of monthly from daily*days:', sum(monthly.values()), 'vs', tot)
print("Q1: Dec share", monthly['12'], monthly['12']/tot*100)
print("   alt (30 days)", daily['12']*30/tot*100)
print("Q2: Jun - May", monthly['6'], monthly['5'], monthly['6']-monthly['5'])
print("   traps: (246.6-222.1)*30 =", (246.6-222.1)*30, " (246.6-222.1)*31 =", (246.6-222.1)*31)
d2212 = daily['12']/(1+yoy['12']/100)
print("Q3: 2022-12 daily", d2212, " 2021-12 daily", d2212/(1+yoy['2022-12']/100))
avg = tot/12
print("Q4: monthly avg", avg)
for m in ['7','8','9','10','11','12']:
    print('  ', m, monthly[m], '<=avg' if monthly[m] <= avg else '>avg')
print("   daily-avg compare: annual daily", tot/365)
print("Q5")
print(" A thermal share", 62318/tot*100, ' 70% of total =', 0.7*tot)
print(" B 6->10 daily dir vs yoy dir")
seq = ['6','7','8','9','10']
for i in range(1,len(seq)):
    a, b = seq[i-1], seq[i]
    print('  ', b, 'daily', 'up' if daily[b]>daily[a] else 'down', ' yoy', 'up' if yoy[b]>yoy[a] else 'down')
print(" C MoM daily increases:")
prev = d2212; cnt = 0
for m in months:
    up = daily[m] > prev
    print('  ', m, daily[m], 'vs', round(prev,1), 'up' if up else 'down')
    cnt += up; prev = daily[m]
print('   count (incl. Mar vs 1-2):', cnt)
print(" D hydro decrease", 11409*0.056/(1-0.056))
