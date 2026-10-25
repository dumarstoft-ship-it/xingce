from fractions import Fraction as F
# reviewer v09: 2025 Sep vs Aug -25%, 2024 Sep vs Aug -20%, 2025 Aug+Sep total +40% YoY; ask Sep YoY
e1,e3,G=F(-25,100),F(-20,100),F(40,100)
a24,s24=F(100),100*(1+e3)
T25=(a24+s24)*(1+G)
a25=T25/(2+e1); s25=a25*(1+e1)
print('2025 Aug',a25,'Sep',s25,'Sep YoY',s25/s24-1,'Aug YoY',a25/a24-1)
print('naive additive G+(e1-e3) =',G+(e1-e3))
# reviewer v07: 80(w-1)+40(13-w)=2.5*240
for w in range(1,13):
    if 80*(w-1)+40*(13-w)==F(5,2)*80*3: print('v07 w =',w)
