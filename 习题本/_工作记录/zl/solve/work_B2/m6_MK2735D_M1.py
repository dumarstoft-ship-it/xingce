# MK2735D-M1 freight supervision; "同比增长" column = absolute increase
T = {
 'imp':(30853,1018,270710,11001),
 'exp':(16271,-55,143487,5999),
 'tools':(3555116,451265,31896977,7531496),
 'cross':(3283126,413997,29466855,7163173),
 'car':(2795972,360315,25089654,6432622),
 'train':(378361,29772,3436394,423331),
 'ship':(32287,565,296517,24108),
 'plane':(76506,23345,644290,283112),
}
print("check sums", sum(T[k][0] for k in ['car','train','ship','plane']), sum(T[k][1] for k in ['car','train','ship','plane']))
print("Q1 2023 Sep imp+exp", T['imp'][0]+T['exp'][0], T['imp'][1]+T['exp'][1], T['imp'][0]+T['exp'][0]-(T['imp'][1]+T['exp'][1]))
print("Q2 1-9 growth")
for k in ['car','train','ship','plane']:
    c,i = T[k][2],T[k][3]
    print(k, round(i/(c-i)*100,2))
print("Q3 Sep vs 1-8 avg")
for k in ['imp','exp','ship','plane']:
    s,_,c,_ = T[k]
    print(k, s, round((c-s)/8,1), round(c/9,1), s<(c-s)/8)
print("Q4 2023 1-9 imp/exp", (270710-11001), (143487-5999), (270710-11001)/(143487-5999))
print("Q5")
print("A 2023 Sep car/cross", (2795972-360315)/(3283126-413997)*100)
print("B 1-8 increase tools", 7531496-451265)
print("C train contribution", 29772/451265*100)
print("D non-cross 1-9", 31896977-29466855)
