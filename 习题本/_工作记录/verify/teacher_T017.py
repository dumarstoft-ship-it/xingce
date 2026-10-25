# teacher_T017  2023广东-33：去年党员:非党员=1:3；今年总人数+20%，比为1:2，党员多6人。今年党员人数
from fractions import Fraction as F

OPTS = {'A': 16, 'B': 24, 'C': 32, 'D': 48}
sols = []
for p in range(1, 2000):                     # 去年党员
    total_last = 4 * p
    total_now = F(6, 5) * total_last
    if total_now.denominator != 1 or total_now % 3:
        continue
    party_now = total_now / 3
    if party_now - p == 6:
        sols.append(int(party_now))
assert len(sols) == 1, sols
ans = sols[0]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('今年党员 =', ans)
print(hits[0])
