# T191（2008山东）52人投票，某时刻甲17、乙16、丙11，得票最多者当选，甲最少再得几票能保证当选。
TOTAL, VOTES = 52, {'甲': 17, '乙': 16, '丙': 11}
OPTS = {'A': 1, 'B': 2, 'C': 4, 'D': 8}
remain = TOTAL - sum(VOTES.values())


def guaranteed(x):
    for b in range(remain - x + 1):          # 其余票任意分给乙、丙
        c = remain - x - b
        if not (VOTES['甲'] + x > VOTES['乙'] + b and VOTES['甲'] + x > VOTES['丙'] + c):
            return False
    return True


ans = next(x for x in range(remain + 1) if guaranteed(x))
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('remaining =', remain, 'need =', ans)
print(hits[0])
