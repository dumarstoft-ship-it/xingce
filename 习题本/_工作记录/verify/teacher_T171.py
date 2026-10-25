# teacher T171（2019北京）100辆单车，7点起每20秒骑走1辆，7点起每15分钟补30辆，哪个时段会无车
OPTS = {'A': (8, 21, 8, 25), 'B': (8, 36, 8, 40), 'C': (8, 41, 8, 45), 'D': (8, 46, 8, 50)}
START, RIDE, PERIOD, ADD = 100, 20, 15 * 60, 30
sec = lambda h, m: (h - 7) * 3600 + m * 60          # 距7:00的秒数

def empty_seconds(first_ride_at_zero, ride_before_add):
    bikes, empty = START, set()
    for t in range(0, 2 * 3600 + 1):
        add = (t % PERIOD == 0)
        ride = (t % RIDE == 0) and (t > 0 or first_ride_at_zero)
        if ride_before_add and ride and bikes > 0:
            bikes -= 1
        if add:
            bikes += ADD
        if not ride_before_add and ride and bikes > 0:
            bikes -= 1
        if bikes == 0:
            empty.add(t)
    return empty

answers = set()
for z in (False, True):                             # 第一辆在7:00还是7:00:20被骑走
    for rb in (False, True):                         # 同一时刻先骑走还是先补车
        e = empty_seconds(z, rb)
        hit = tuple(k for k, (h1, m1, h2, m2) in OPTS.items()
                    if any(sec(h1, m1) <= t <= sec(h2, m2) for t in e))
        first = min(e)
        print('约定', z, rb, '首次无车 7:00+%d秒 = %d:%02d:%02d' % (first, 7 + first // 3600, first % 3600 // 60, first % 60), '->', hit)
        answers.add(hit)
assert len(answers) == 1 and len(next(iter(answers))) == 1, answers
print(next(iter(answers))[0])
