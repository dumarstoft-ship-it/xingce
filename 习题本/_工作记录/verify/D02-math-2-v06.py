# D02-math-2-v06：甲、乙、丙单独分别需20、30、15天。甲乙合作4天→甲调走，乙单独若干天→乙丙合作4天完工。
# 工程款75万元按工作量分配，求乙队应得。解法：枚举乙单独天数（以1/2天为步长），逐日累计各队工作量。
from fractions import Fraction as F

OPTIONS = {'A': 20, 'B': 25, 'C': 30, 'D': 40}
TA, TB, TC = 20, 30, 15
rA, rB, rC = F(1, TA), F(1, TB), F(1, TC)
MONEY = 75

sol = []
for half_days in range(0, 200):
    s = F(half_days, 2)                 # 乙单独施工天数
    work = {'甲': rA * 4, '乙': rB * (4 + s + 4), '丙': rC * 4}
    if sum(work.values()) == 1:
        sol.append((s, work))
assert len(sol) == 1, sol
s, work = sol[0]
pay_yi = MONEY * work['乙'] / sum(work.values())
hits = [k for k, v in OPTIONS.items() if v == pay_yi]
assert len(hits) == 1, (pay_yi, hits)
# 干扰项：丙的份额(或只算乙单独那几天)=20；平均分=25；漏算乙前4天=30；(按天数分=50不在选项)
assert MONEY * work['丙'] == OPTIONS['A'] and MONEY * rB * s == OPTIONS['A']
assert F(MONEY, 3) == OPTIONS['B']
assert MONEY * rB * (s + 4) == OPTIONS['C']
print('乙单独', s, '天；工作量', {k: str(v) for k, v in work.items()}, '乙得', pay_yi, '万元')
print(hits[0])
