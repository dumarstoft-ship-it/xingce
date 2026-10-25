# teacher_T026  第一次定制甲乙共50个花1150元，甲单价15元；第二次共70个，乙个数是第一次的1/4。第二次花费
from fractions import Fraction as F

N1, COST1, P_JIA, N2, SHRINK = 50, 1150, 15, 70, F(1, 4)
OPTS = {'A': 1150, 'B': 1725, 'C': 2300, 'D': 2875}
costs = set()
for b in range(1, N1):                       # 第一次乙的个数
    a = N1 - b
    p_yi = F(COST1 - P_JIA * a, b)           # 乙单价（未知，由第一次反推）
    b2 = SHRINK * b
    if p_yi <= 0 or b2.denominator != 1 or b2 > N2:
        continue
    costs.add(P_JIA * (N2 - b2) + p_yi * b2)
assert len(costs) == 1, costs                # 无论乙单价、个数如何，第二次花费唯一
ans = costs.pop()
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('第二次花费 =', ans)
print(hits[0])
