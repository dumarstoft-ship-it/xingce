# MK2714X-M2 fixed asset investment / real estate 2025H1
# Q1
g25 = 0.028; g24 = 0.028 + 0.011
v23 = 248653/(1+g25)/(1+g24)
print("Q1 2023H1 FAI", v23, "2024H1", 248653/(1+g25))
# Q2
t25, tg = 46658, -0.112
z25, zg = 35770, -0.104
t24 = t25/(1+tg); z24 = z25/(1+zg)
f25 = t25 - z25; f24 = t24 - z24
print("Q2 non-res 2025", f25, "2024", f24, "growth", f25/f24 - 1)
# Q3
s2 = 88294/1.102; s3 = 155543/(1-0.011)
print("Q3 2024 secondary", s2, "tertiary", s3, "ratio", s2/s3, "options", 1/2, 2/3, 2/5, 3/7)
# Q4
p25 = 44241e8/45851e4
p24 = (44241e8/(1-0.055))/(45851e4/(1-0.035))
print("Q4 price 2025", p25, "2024", p24, "diff", p25-p24)
print("Q4 formula check: p25*(1 - (1-0.035)/(1-0.055))", p25*(1-(0.965/0.945)))
# Q5
print("Q5A foreign capital increment (亿元)", 17*0.254/1.254)
print("Q5C deposit/mortgage ratio", 14781/6847, "多倍", 14781/6847-1)
print("Q5D mortgage share", 6847/50202)
# self-raised share check
print("Q5B self-raised share 2025", 17544/50202, "2024", (17544/0.928)/(50202/0.938))
