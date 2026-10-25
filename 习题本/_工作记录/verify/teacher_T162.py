# teacher T162（2021广东县级）周一至周五晚读书，每晚20页到7月28日读完、每晚30页到7月20日读完，7月1日周三，求制定计划的日期
OPTS = {'A': 2, 'B': 3, 'C': 5, 'D': 7}
JUL1 = 2                                           # 0=周一，7月1日周三
read = lambda d: (JUL1 + d - 1) % 7 <= 4          # 周一至周五读书
END_SLOW, END_FAST, P_SLOW, P_FAST = 28, 20, 20, 30
assert read(END_SLOW) and read(END_FAST)          # 两个“刚好读完”的日子都是读书日
res = []
for s in range(1, END_FAST + 1):                   # 从制定当天开始读
    n_slow = sum(read(d) for d in range(s, END_SLOW + 1))
    n_fast = sum(read(d) for d in range(s, END_FAST + 1))
    if P_SLOW * n_slow == P_FAST * n_fast:
        res.append((s, n_slow, n_fast))
print('(制定日, 20页读书天数, 30页读书天数) =', res)
assert len(res) == 1
hits = [k for k, v in OPTS.items() if v == res[0][0]]
assert len(hits) == 1, hits
print(hits[0])
