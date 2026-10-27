from fractions import Fraction as F
out = {}
# 2026ZJA-53: 160 invested, 200 back (25%); 甲 40%, 乙 16%
for a in range(0,161):
    if F(a)*F(140,100) + F(160-a)*F(116,100) == 200: out['2026ZJA-53'] = (a, {60:'A',70:'B',80:'C',90:'D'}.get(a))
# 2026ZJA-47: 200g c + 100g 30%, evaporate 150 water -> 40%
c = (F(150)*F(40,100) - 30) / 200
out['2026ZJA-47'] = (c, {F(15,100):'A',F(20,100):'B',F(25,100):'C',F(30,100):'D'}.get(c))
# 2020SZS-23: 20% 1000g + 甲 200 (3b) + 乙 400 (b) -> dry, weight = 1/4 * 1600 = 400 salt
b = (F(400) - 200) / (200*3 + 400)
out['2020SZS-23'] = (3*b, {F(60,100):'A',F(45,100):'B',F(20,100):'C',F(15,100):'D'}.get(3*b))
# 2018JSA-58: c/24 = 1%
c = F(24,100)
out['2018JSA-58'] = (c, 'D (24%)')
# 2021JSA-52: 5000, 5.6% & 6.2%, interest 295.6
for a in range(0,5001,50):
    if F(a)*F(56,1000) + F(5000-a)*F(62,1000) == F(2956,10): out['2021JSA-52'] = (a, {2250:'A',2400:'B',2650:'C',2800:'D'}.get(a))
# 2022SZ-56: avg 92.35 -> 96.85 after +90
n = F(90) / (F(9685,100) - F(9235,100))
out['2022SZ-56'] = (n, {18:'A',20:'B',25:'C',30:'D'}.get(int(n)))
# 2025GD-37: 41 + 28(n-1) = 29n
n = 41 - 28
out['2025GD-37'] = (n, {13:'A',14:'B',15:'C',16:'D'}.get(n))
# 2021GK-73 (T098): 车站 25k, 超市 20k, 学校 17k, 机场 most, total 96, prof 62
sols=[]
for a in range(1,4):
    for b in range(1,5):
        for c in range(1,6):
            st, cs, sc = 25*a, 20*b, 17*c
            ap = 96 - st - cs - sc
            if ap <= max(st,cs,sc): continue
            prof = 16*a + 13*b + 10*c
            apf = 62 - prof
            if 0 <= apf <= ap: sols.append((st,cs,sc,ap,apf, round(apf/ap,4)))
out['2021GK-73'] = (sols, 'A (第一)' if all(s[5] > 0.65 for s in sols) else '?')
for k,v in out.items(): print(k, v)
