tot = 7377
print("Q1", tot*(0.599-0.385-0.016), tot*0.599, tot*(0.385+0.016))
print("Q2", tot/1.099)
print("Q3")
d = {'东':(780.4,15.7),'中':(441.8,16.7),'西':(534.3,15.4),'东北':(110.3,25.8)}
s = sum(v[0] for v in d.values())
for k,(v,g) in d.items():
    print(k, v/(1+g/100)*g/100, v/s*100)
print("sum", s)
print("Q4")
p = {'东':(61.5,4.8),'中':(62.6,5.4),'西':(61.5,5.1),'东北':(61.9,5.7)}
r = {k: a-b for k,(a,b) in p.items()}
print(sorted(r.items(), key=lambda x: x[1]))
print("Q5")
print("A", 201.9/(3022-201.9)*100)
print("B", 29.8/6)
print("C", 454.9/0.357)
print("D", 3244-3264)
