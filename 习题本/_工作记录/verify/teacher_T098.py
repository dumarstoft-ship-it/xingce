# T098 2021国考副省级73：96人分四区，专业62人；机场人数最多；车站64%、超市65%专业；学校非专业比专业少30%
from fractions import Fraction as F

TOTAL, PRO = 96, 62
P_STATION, P_MARKET = F(64, 100), F(65, 100)
RANK = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}

answers = set()
for s in range(1, TOTAL):
    if (s * P_STATION).denominator != 1:
        continue
    for m in range(1, TOTAL - s):
        if (m * P_MARKET).denominator != 1:
            continue
        for x in range(1, TOTAL - s - m):
            # 学校：非专业 = 专业 × (1-30%)
            for xp in range(1, x + 1):
                if F(x - xp) != F(xp) * F(7, 10):
                    continue
                a = TOTAL - s - m - x
                if not (a > s and a > m and a > x):
                    continue           # 机场人数最多
                ap = PRO - s * P_STATION - m * P_MARKET - xp
                if not (0 <= ap <= a):
                    continue
                shares = {'station': s * P_STATION / s, 'market': P_MARKET,
                          'school': F(xp, x), 'airport': F(ap) / a}
                order = sorted(shares.values(), reverse=True)
                rank = order.index(shares['airport']) + 1
                answers.add((rank, (s, m, x, a), float(shares['airport'])))
assert len({r for r, _, _ in answers}) == 1, answers
rank, sizes, share = answers.pop()
print('sizes (station, market, school, airport) =', sizes, 'airport share =', round(share, 4))
print(RANK[rank])
