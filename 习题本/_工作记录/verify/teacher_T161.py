# teacher T161（2017河南）周一到周五锻炼，某年每季度锻炼天数相同，国庆节星期几
OPTS = {'A': '一', 'B': '五', 'C': '六', 'D': '日'}
WD = ['一', '二', '三', '四', '五', '六', '日']
res = set()
for leap in (False, True):
    mdays = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for jan1 in range(7):
        k, cal = jan1, []
        for m in range(12):
            for d in range(1, mdays[m] + 1):
                cal.append((m, d, k % 7))
                k += 1
        q = [0] * 4
        for m, d, w in cal:
            if w < 5:                             # 周一至周五
                q[m // 3] += 1
        if len(set(q)) == 1:
            oct1 = next(w for m, d, w in cal if m == 9 and d == 1)
            res.add(WD[oct1])
            print('闰年' if leap else '平年', '1月1日周' + WD[jan1], '各季度', q, '国庆周' + WD[oct1])
assert len(res) == 1
hits = [k for k, v in OPTS.items() if v in res]
assert len(hits) == 1, hits
print(hits[0])
