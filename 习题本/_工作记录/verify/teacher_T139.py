# teacher T139（2019联考）计划20天完工，从第三天起每天比前一天多完成1倍，至少几天完工
OPTS = {'A': 5, 'B': 6, 'C': 7, 'D': 8}
PLAN = 20
total = PLAN * 1                 # 赋值原效率为1
done, day, rate = 0, 0, 1
log = []
while done < total:
    day += 1
    if day >= 3:
        rate *= 2                 # 多完成1倍 = 前一天的2倍
    done += rate
    log.append(done)
print('累计', log, '-> 天数', day)
hits = [k for k, v in OPTS.items() if v == day]
assert len(hits) == 1, hits
print(hits[0])
