# T192（2013辽宁）60张票，前30张甲15、乙10、丙5，得票最多者当选，甲至少再得多少票一定当选。
TOTAL, VOTES = 60, {'甲': 15, '乙': 10, '丙': 5}
OPTS = {'A': 15, 'B': 13, 'C': 10, 'D': 8}
remain = TOTAL - sum(VOTES.values())


def guaranteed(x):
    for b in range(remain - x + 1):
        c = remain - x - b
        if not (VOTES['甲'] + x > VOTES['乙'] + b and VOTES['甲'] + x > VOTES['丙'] + c):
            return False
    return True


ans = next(x for x in range(remain + 1) if guaranteed(x))
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('remaining =', remain, 'need =', ans)
print(hits[0])
