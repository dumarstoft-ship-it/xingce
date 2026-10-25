# teacher T157（2015江苏B）3月有5个星期一、4个星期二，国庆节星期几
OPTS = {'A': '二', 'B': '三', 'C': '四', 'D': '五'}
WD = ['一', '二', '三', '四', '五', '六', '日']
MONTH = [31, None, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]   # 3~9月与闰年无关
res = set()
for start in range(7):                            # 3月1日的星期
    cnt = [0] * 7
    for d in range(31):
        cnt[(start + d) % 7] += 1
    if cnt[0] == 5 and cnt[1] == 4:
        offset = sum(MONTH[2:9])                  # 3月1日 -> 10月1日
        res.add(WD[(start + offset) % 7])
print(res)
assert len(res) == 1
hits = [k for k, v in OPTS.items() if v in res]
assert len(hits) == 1, hits
print(hits[0])
