# teacher_T034  2020浙江B-17：排队购票，3个窗口90分钟，5个窗口45分钟，6个窗口几分钟
from fractions import Fraction as F

(W1, T1), (W2, T2), W3 = (3, 90), (5, 45), 6
OPTS = {'A': 36, 'B': 38, 'C': 40, 'D': 42}
r = F(W1 * T1 - W2 * T2, T1 - T2)        # 每分钟新增乘客需占用的窗口数
Q = (W1 - r) * T1                        # 原有排队量（窗口·分钟）
assert Q == (W2 - r) * T2 and Q > 0
t = Q / (W3 - r)
hits = [k for k, v in OPTS.items() if v == t]
assert len(hits) == 1, (t, hits)
print('r =', r, ' Q =', Q, ' t =', t)
print(hits[0])
