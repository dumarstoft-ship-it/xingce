import math
# MK2739X-M3: 2024 tea domestic sales & exports
vol = {"总":(241.27,0.35),"绿茶":(131.72,2.15),"红茶":(38.36,1.31),"黑茶":(36.78,-2.69),"乌龙茶":(24.74,-3.48),"白茶":(7.37,-10.75),"黄茶":(2.30,19.09)}
val = {"总":(3257.55,-2.66),"绿茶":(1950.46,-1.41),"红茶":(578.49,3.13),"黑茶":(359.97,0.37),"乌龙茶":(270.63,-12.98),"白茶":(72.03,-33.00),"黄茶":(25.98,-14.51)}
# Q1 domestic average price growth
for k in ["黑茶","乌龙茶","白茶","黄茶"]:
    g = (1+val[k][1]/100)/(1+vol[k][1]/100)-1
    print("Q1 %s price growth=%.4f%%" % (k, g*100))
# Q2 total sales volume growth
dom, domg = 241.27, 0.0035
ex, exg = 37.41, 0.0179
now = dom+ex; base = dom/(1+domg)+ex/(1+exg)
print("Q2 now=%.3f base=%.4f growth=%.4f%%" % (now, base, (now/base-1)*100))
# Q3 pie shares
tot = val["总"][0]
cum = 0
for k in ["绿茶","红茶","黑茶","乌龙茶","白茶","黄茶"]:
    sh = val[k][0]/tot
    cum += sh*360
    print("Q3 %s share=%.4f%% angle=%.2f cum=%.2f" % (k, sh*100, sh*360, cum))
# measured boundaries in pie C/D (enlarged x3 coordinates) -> angle clockwise from 12 o'clock
def ang(cx, cy, x, y):
    dx = x-cx; up = cy-y
    a = math.degrees(math.atan2(dx, up))
    return a % 360
for name, c, pts in [("C",(465,455),[(212,803),(35,385),(185,130),(385,30),(440,20)]),
                     ("D",(470,462),[(215,803),(40,480),(190,140),(390,45),(450,30)])]:
    print("Q3 pie", name, [round(ang(c[0],c[1],x,y),1) for x,y in pts])
# Q4 export unit price vs overall: value share / volume share
for k, vs, es in [("绿茶",86.57,75.59),("红茶",6.62,12.11),("乌龙茶",4.13,7.00),("茉莉花茶",2.00,3.95)]:
    print("Q4 %s ratio=%.4f" % (k, es/vs))
# Q5
p24 = 14.19e8/(37.41e7)   # USD per kg
p23 = (14.19e8/(1-0.1839))/((37.41e7)/(1+0.0179))
print("Q5A price24=%.4f USD/kg price23=%.4f diff=%.4f" % (p24, p23, p23-p24))
print("Q5B 红茶/茉莉 export value=%.4f" % (12.11/3.95))
r23 = 578.49/1.0313; w23 = 270.63/(1-0.1298)
print("Q5C 2023 red=%.3f oolong=%.3f diff=%.3f ; 2024 diff=%.2f" % (r23, w23, r23-w23, 578.49-270.63))
print("Q5D 白茶降幅10.75 vs 乌龙茶3.48 -> diff=%.2f pp (白茶降幅更高)" % (10.75-3.48))
