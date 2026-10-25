# T105 2016山东：1~100号，1号拿三色旗；每隔2人拿红、每隔3人拿蓝、每隔6人拿黄；求拿两种及以上颜色的人数
N = 100
GAP = {'red': 2, 'blue': 3, 'yellow': 6}       # "每隔k个学生有1人" → 周期 k+1
OPTS = {'A': 13, 'B': 14, 'C': 15, 'D': 16}

flags = {i: set() for i in range(1, N + 1)}
for color, k in GAP.items():
    i = 1
    while i <= N:
        flags[i].add(color)
        i += k + 1
cnt = sum(1 for s in flags.values() if len(s) >= 2)
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('students with >=2 colors:', cnt, sorted(i for i, s in flags.items() if len(s) >= 2))
print(hits[0])
