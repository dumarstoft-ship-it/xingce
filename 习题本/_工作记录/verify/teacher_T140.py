# teacher T140（2017联考）“股神”每天对上一天收到正确信息的人一半报涨一半报跌，保证有人连续6天都正确，最初至少几人
OPTS = {'A': 8, 'B': 64, 'C': 32, 'D': 16}
DAYS = 6

def guaranteed(n):
    g = n
    for _ in range(DAYS):
        g //= 2                   # 分成两半，结果只有一半正确；人数为奇数时最坏只保证较少的那一半
    return g

need = min(n for n in range(1, 100000) if guaranteed(n) >= 1)
print('最少', need)
hits = [k for k, v in OPTS.items() if v == need]
assert len(hits) == 1, hits
print(hits[0])
