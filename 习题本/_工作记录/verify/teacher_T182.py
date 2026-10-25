# T182（2014北京）20人百分制，平均79分，得分为互不相同的整数；前5名平均分=第16~20名平均分的2倍。
# 求第6名与第15名分差的最大值。
# 判定"从[lo,hi]中取k个互不相同的整数和为s"：可达的和恰为[最小和,最大和]内全部整数（逐个+1调整可证）。
N, AVG, FULL = 20, 79, 100
OPTS = {'A': 34, 'B': 37, 'C': 40, 'D': 43}


def can(k, lo, hi, s):
    if k == 0:
        return s == 0
    if hi - lo + 1 < k:
        return False
    mn = sum(range(lo, lo + k))
    mx = sum(range(hi - k + 1, hi + 1))
    return mn <= s <= mx


total = N * AVG
best = None
for sb in range(0, 5 * FULL + 1):           # 第16~20名总分
    st = 2 * sb                              # 第1~5名总分（平均分2倍，人数相同）
    if st > 5 * FULL:
        break
    for a6 in range(FULL + 1):
        if not can(5, a6 + 1, FULL, st):
            continue
        for a15 in range(a6 - 9, -1, -1):    # 第7~14名8人严格介于两者之间
            if best is not None and a6 - a15 <= best:
                continue
            mid = total - st - sb - a6 - a15
            if can(5, 0, a15 - 1, sb) and can(8, a15 + 1, a6 - 1, mid):
                best = a6 - a15
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('max gap =', best)
print(hits[0])
