# teacher T155（2015上海B）某年2月有5个星期日、4个星期六，2月1日星期几
OPTS = {'A': '四', 'B': '五', 'C': '六', 'D': '日'}
WD = ['一', '二', '三', '四', '五', '六', '日']
res = set()
for days in (28, 29):
    for start in range(7):                       # 2月1日的星期
        cnt = [0] * 7
        for d in range(days):
            cnt[(start + d) % 7] += 1
        if cnt[WD.index('日')] == 5 and cnt[WD.index('六')] == 4:
            res.add((days, WD[start]))
print(res)
starts = {w for _, w in res}
assert len(starts) == 1
hits = [k for k, v in OPTS.items() if v in starts]
assert len(hits) == 1, hits
print(hits[0])
