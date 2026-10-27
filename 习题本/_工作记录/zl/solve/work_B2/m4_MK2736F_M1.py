# MK2736F-M1 Zhongguancun
zgc = 13922.8; zg = 0.071
gx = 5280.0; gg = 0.058
s25 = gx/zgc
s24 = (gx/(1+gg))/(zgc/(1+zg))
print("Q1 share 2025", s25*100, "2024", s24*100, "diff pp", (s25-s24)*100)
print("   formula", s25*(gg-zg)/(1+gg)*100)
print("Q2 elec share base", 5.1/11.4*100)
print("Q3 per-capita R&D growth", (1.025/(1-0.019)-1)*100)
rd = [3.7,4.3,2.8,3.4,3.0,3.0,2.6,2.2,1.9,2.0]  # 1-2..1-11 (2024)
labels = ['1-2','1-3','1-4','1-5','1-6','1-7','1-8','1-9','1-10','1-11']
print("Q4 monthly > cumulative iff cum rises")
cnt=0
for i in range(1,len(rd)):
    up = rd[i] > rd[i-1]
    print(labels[i], rd[i-1], '->', rd[i], 'month', i+2, 'yes' if up else ('equal' if rd[i]==rd[i-1] else 'no'))
    cnt+=up
print("count", cnt)
print("Q5 ③ 2023 1-2 total revenue", zgc/1.071/1.089)
print("   2024 1-2 R&D", 611.9/1.025)
