"""D06-math-h-v06  网球"平分"后须领先 2 分才赢下该局，甲每分得分概率 2/3，求甲赢下该局的概率。
独立求解：
  方法 1：按分差建吸收马尔可夫链（分差 -1/0/+1 为过渡态，±2 吸收），用分数做高斯消元精确求解；
  方法 2：逐分动态规划把前 400 分内结束的概率累加（浮点），确认与方法 1 一致。
然后把四个选项解析成分数，确认恰好一个与精确解相等，打印该选项字母。
"""
from fractions import Fraction as F
import re

# ---- 题面数据 ----
p = F(2, 3)          # 甲每分得分概率
q = 1 - p
LEAD = 2             # 须领先 2 分
OPTIONS = {"A": r"$\frac{2}{3}$", "B": r"$\frac{20}{27}$", "C": r"$\frac{4}{5}$", "D": r"$\frac{8}{9}$"}

# ---- 方法 1：吸收链精确解 ----
states = list(range(-(LEAD - 1), LEAD))          # 分差 -1, 0, 1
idx = {s: i for i, s in enumerate(states)}
n = len(states)
# 方程：x_s - p*x_{s+1} - q*x_{s-1} = 吸收项（到 +2 记 1，到 -2 记 0）
A = [[F(0)] * n for _ in range(n)]
b = [F(0)] * n
for s in states:
    i = idx[s]
    A[i][i] += 1
    for nxt, pr in ((s + 1, p), (s - 1, q)):
        if nxt >= LEAD:
            b[i] += pr
        elif nxt <= -LEAD:
            pass
        else:
            A[i][idx[nxt]] -= pr
# 高斯消元
for c in range(n):
    piv = next(r for r in range(c, n) if A[r][c] != 0)
    A[c], A[piv] = A[piv], A[c]
    b[c], b[piv] = b[piv], b[c]
    for r in range(n):
        if r != c and A[r][c] != 0:
            f = A[r][c] / A[c][c]
            A[r] = [x - f * y for x, y in zip(A[r], A[c])]
            b[r] -= f * b[c]
x = {s: b[idx[s]] / A[idx[s]][idx[s]] for s in states}
exact = x[0]
print("exact P(甲胜 | 平分) =", exact)

# ---- 方法 2：逐分 DP 累加 ----
dist = {0: 1.0}
win = 0.0
for _ in range(400):
    nd = {}
    for d, pr in dist.items():
        for nxt, pp in ((d + 1, float(p)), (d - 1, float(q))):
            if nxt >= LEAD:
                win += pr * pp
            elif nxt <= -LEAD:
                pass
            else:
                nd[nxt] = nd.get(nxt, 0.0) + pr * pp
    dist = nd
print("DP (400 分内) =", round(win, 12))
assert abs(win - float(exact)) < 1e-12

# ---- 对照选项 ----
def parse(s):
    m = re.search(r"\\frac\{(\d+)\}\{(\d+)\}", s)
    return F(int(m.group(1)), int(m.group(2)))

hits = [k for k, v in OPTIONS.items() if parse(v) == exact]
assert len(hits) == 1, hits
print(hits[0])
