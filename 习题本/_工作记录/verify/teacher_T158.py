# teacher T158（2023深圳）周二至周六上班，31天的月工作22天，4号星期几
OPTS = {'A': {'一'}, 'B': {'二'}, 'C': {'一', '四'}, 'D': {'四', '日'}}
WD = ['一', '二', '三', '四', '五', '六', '日']
WORK = {'二', '三', '四', '五', '六'}
res = set()
for start in range(7):                            # 1号的星期
    if sum(WD[(start + d) % 7] in WORK for d in range(31)) == 22:
        res.add(WD[(start + 3) % 7])
print('4号可能是周', res)
hits = [k for k, v in OPTS.items() if v == res]
assert len(hits) == 1, hits
print(hits[0])
