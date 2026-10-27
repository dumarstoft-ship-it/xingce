# MK2733X-M2 energy production/consumption
prod = {2018:(378859,262170,27278,20458,68953),2019:(397317,272162,27415,22250,75490),2020:(407295,274924,27696,24438,80237),2021:(427115,284886,28617,25627,87985),2022:(463808,314084,29358,27494,92872)}
cons = {2018:(471925,278436,89194,35866,68429),2019:(487488,281281,92623,38999,74585),2020:(498314,283541,93683,41858,79232),2021:(525896,293976,97817,46279,87824),2022:(540956,304042,96839,45444,94631)}
# check sums
for y in prod:
    print(y, 'prod sum', sum(prod[y][1:]), prod[y][0], 'cons sum', sum(cons[y][1:]), cons[y][0])
print('Q1 other energy production growth')
for y in range(2019,2023):
    print(y, prod[y][4]/prod[y-1][4]-1, prod[y][4]-prod[y-1][4])
print('Q2')
dc = cons[2021][1]-cons[2020][1]; do = cons[2021][2]-cons[2020][2]
print(dc, do, dc/do)
print('Q3 shares 2022 consumption')
t = cons[2022][0]
for name, v in zip(['coal','oil','gas','other'], cons[2022][1:]):
    print(name, v, v/t, v/t*360)
print('Q4 gas production avg')
s = sum(prod[y][3] for y in prod); print(s, s/5)
print('Q5')
for y in prod:
    print(y, 'coal cons-prod', cons[y][1]-prod[y][1])
for y in range(2019,2023):
    print(y, 'coal', cons[y][1]-cons[y-1][1], 'oil', cons[y][2]-cons[y-1][2], 'gas', cons[y][3]-cons[y-1][3])
print('C', (cons[2021][1]+cons[2021][2]+cons[2021][3])/cons[2021][0], 1-cons[2021][4]/cons[2021][0])
print('D', cons[2022][0]/cons[2020][0]-1, cons[2020][0]*1.1)
