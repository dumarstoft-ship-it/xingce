import datetime as dt
# 2016GK-62: side1 "每隔3棵银杏种1棵梧桐" -> period (Y,Y,Y,W); side2 "每隔4棵梧桐种1棵银杏" -> (W,W,W,W,Y); 35 each; max ginkgo
def best(pattern, n=35):
    L=len(pattern); return max(sum(1 for i in range(n) if pattern[(i+s)%L]=='Y') for s in range(L))
print('2016GK-62 max ginkgo =', best('YYYW')+best('WWWWY'), '(B=34)')

# 2026ZJA-65: Jan 1 on Wednesday, min count over any 10 consecutive years (Gregorian 1901-2400)
mins=[]
for y0 in range(1901, 2391):
    c=sum(1 for y in range(y0,y0+10) if dt.date(y,1,1).weekday()==2)
    mins.append((c,y0))
print('2026ZJA-65 min count =', min(mins)[0], 'e.g. start', [y for c,y in mins if c==min(mins)[0]][:5], '| max', max(mins)[0])
# also restricted to 1901-2099 (no century exception)
m2=min(sum(1 for y in range(y0,y0+10) if dt.date(y,1,1).weekday()==2) for y0 in range(1901,2091))
print('   within 1901-2099:', m2)

# 2026ZJA-49: rest every 5th day; A,B,C,D rest Sep1..4 -> all on duty days in September
print('2026ZJA-49 =', sum(1 for d in range(1,31) if all((d-r)%5!=0 for r in (1,2,3,4))), '(D=6)')

# 2026ZJA-54: 51 baskets; make 1 every 2 days, sell 2/day -> first sold-out day, two production timings
def sold_out(timing):
    s=51
    for day in range(1,100):
        if timing=='start' and day%2==1: s+=1
        if timing=='mid' and day%2==0: s+=1
        sell=min(2,s); s-=sell
        if timing=='end' and day%2==0: s+=1
        if s==0 or sell<2: return day
for t in ('start','mid','end'):
    print('2026ZJA-54', t, sold_out(t))
