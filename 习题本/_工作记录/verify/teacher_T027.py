# teacher_T027  2023国考-66：10000份样本；甲200份/小时、100元/份，乙500份/小时、200元/份。15小时内比18小时内最低费用高多少万元
TOTAL = 10000
RATE = {'甲': 200, '乙': 500}
COST = {'甲': 100, '乙': 200}
OPTS = {'A': 3, 'B': 4, 'C': 5, 'D': 6}

def min_cost(hours):
    best = None
    for x in range(0, min(TOTAL, RATE['甲'] * hours) + 1):     # 甲检验份数
        y = TOTAL - x
        if y > RATE['乙'] * hours:
            continue
        c = COST['甲'] * x + COST['乙'] * y
        best = c if best is None else min(best, c)
    return best

diff = min_cost(15) - min_cost(18)
assert diff % 10000 == 0
ans = diff // 10000
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('15h:', min_cost(15), ' 18h:', min_cost(18), ' 差(万元):', ans)
print(hits[0])
