# teacher T160（2020深圳）撕下的最近10页日历数字和为244，当天日历显示几日
OPTS = {'A': 29, 'B': 30, 'C': 1, 'D': 2}
TORN, TOTAL = 10, 244
res = set()
for prev_len in (28, 29, 30, 31):                 # 上个月天数
    for cur_len in (28, 29, 30, 31):              # 本月天数
        for today in range(1, cur_len + 1):
            pages = [today - k if today - k >= 1 else today - k + prev_len for k in range(1, TORN + 1)]
            if sum(pages) == TOTAL:
                res.add((today, prev_len))
print('(今天, 上月天数) =', res)
todays = {t for t, _ in res}
assert len(todays) == 1
hits = [k for k, v in OPTS.items() if v in todays]
assert len(hits) == 1, hits
print(hits[0])
