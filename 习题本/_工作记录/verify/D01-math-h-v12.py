# D01-math-h-v12  三所乡镇中学教师交流轮岗（修订版：给三组总数）：
# 甲校小组→丙校，丙校小组→乙校，乙校小组→甲校，其余教师不动；交流期间三校在岗人数相等。
# 原来甲校比乙校少12人，丙校比乙校少9人；三个交流小组共30人。求丙校小组人数。
OPTS = {'A': 7, 'B': 10, 'C': 11, 'D': 13}
TOTAL = 30
DEST = {'jia': 'bing', 'bing': 'yi', 'yi': 'jia'}       # 各校小组的去向


def balanced(c, g, dest, sign=1):
    inc = {s: 0 for s in c}
    for s in c:
        inc[dest[s]] += g[s]
    now = {s: c[s] + sign * (inc[s] - g[s]) for s in c}
    return now['jia'] == now['yi'] == now['bing']


def solutions(dest, total=TOTAL, sign=1, cap=None):
    """穷举乙校原有人数 n 及三个小组人数；total=None 时不加“共30人”这一条件"""
    found = set()
    for n in range(13, 201):
        c = {'yi': n, 'jia': n - 12, 'bing': n - 9}
        top = cap if cap else total
        for gj in range(1, min(c['jia'], top) + 1):
            for gy in range(1, min(c['yi'], top) + 1):
                gbs = [total - gj - gy] if total else range(1, min(c['bing'], top) + 1)
                for gb in gbs:
                    if gb < 1 or gb > c['bing']:
                        continue
                    if balanced(c, {'jia': gj, 'yi': gy, 'bing': gb}, dest, sign):
                        found.add((gj, gy, gb))
    return found


sols = solutions(DEST)
assert len(sols) == 1, sols
gj, gy, gb = next(iter(sols))
hits = [k for k, v in OPTS.items() if v == gb]
assert len(hits) == 1, hits

# 不给“三组共30人”时，丙组人数定不下来（只盯一校、甚至三校全列也不够）
free = solutions(DEST, total=None, cap=20)
assert len({s[2] for s in free}) > 1

# 干扰项来源核对
assert TOTAL // 3 == OPTS['B']                                          # 三组平均分
rev = solutions({'jia': 'yi', 'yi': 'bing', 'bing': 'jia'})             # 轮换方向弄反
assert len(rev) == 1 and next(iter(rev))[2] == OPTS['C']
sgn = solutions(DEST, sign=-1)                                          # 净变化正负弄反
assert len(sgn) == 1 and next(iter(sgn))[2] == OPTS['D']
print('groups (jia, yi, bing) =', (gj, gy, gb))
print(hits[0])
