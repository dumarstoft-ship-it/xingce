# MK2740X-M2 数字阅读
users={2018:4.30,2019:4.68,2020:4.94,2021:5.06,2022:5.30}
ug={2018:13.76,2019:8.84,2020:5.56,2021:2.43,2022:4.74}
share={2018:(79.90,12.33,7.77),2019:(60.83,28.90,10.27),2020:(58.69,11.90,29.41),2021:(52.70,15.80,31.50),2022:(48.73,21.02,30.25)}
print("Q1")
cnt=0
for y in range(2018,2023):
    inc=users[y]*ug[y]/100/(1+ug[y]/100)
    alt=users[y]-users.get(y-1,float('nan'))
    print(y, "inc(by rate)", round(inc,4), "inc(by diff)", round(alt,4), "check growth", (users[y]/users[y-1]-1)*100 if y>2018 else None)
    if inc>0.3: cnt+=1
print("count >0.3", cnt)
print("share sums", {y:round(sum(v),2) for y,v in share.items()})
print("Q2")
rev22=463.52; rev21=rev22/1.115
print("rev21", rev21, "copyright21", rev21*0.158, "trap (2022 rev*15.8%)", rev22*0.158, "2022 copyright", rev22*0.2102)
print("Q3")
w22=5271.86; w21=w22-1825.00; w20=w22-2168.26
print("w21", w21, "w20", w20, "growth21", (w21/w20-1)*100, "growth22", (w22/w21-1)*100)
print("Q4")
net=3458.84*0.0793/1.0793; eb=206.92*0.1461/1.1461; oth=87.49*0.418/1.418
print("net inc", net, "ebook inc", eb, "ratio", net/eb, "other inc", oth)
print("Q5")
print("1: min overlap", 36.60+30.55+55.87-100)
cs=[share[y][1] for y in range(2018,2023)]
print("2: copyright shares", cs, "max-min", max(cs)-min(cs), "trap 28.90-12.33", 28.90-12.33)
for y in range(2019,2023):
    a=share[y][2]; b=share[y-1][2]
    print("3:", y, "ad share", b, "->", a, "total growth > ad growth?" , a<b)
print("age sum", 16.93+36.60+30.55+13.23+2.74, "sex sum", 55.87+44.13)
