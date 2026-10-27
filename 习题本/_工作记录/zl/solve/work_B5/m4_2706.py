# MK2706X-M2
dep22=31935.05; wd22=21363.27; bal22=92454.82; cum22=256927.26
print("Q1 bal21:", bal22-(dep22-wd22), " wrong-dir:", bal22+(dep22-wd22))
print("Q2 dep20:", dep22/1.0953/1.1124)
dep=[12.61,10.55,11.24,9.53]; wd=[10.46,13.94,9.51,5.15]
print("Q3 years up:", [y for y,a,b in zip(range(2019,2023),dep,wd) if b>a])
s21=79.2+3.0
print("Q4 2021 share:", s21, " ratio:", s21/(100-s21), " more:", s21/(100-s21)-1)
print("   2022 ratio:", 79.2/20.8, " more:", 79.2/20.8-1)
print("Q5 A:", 6782.63/16979.57)
print("Q5 B (wan yuan/person):", 21363.27*1e4/6782.63)
print("Q5 C:", 452.72/1.088, " trap:", 452.72-75.22)
print("Q5 D:", cum22-bal22)
