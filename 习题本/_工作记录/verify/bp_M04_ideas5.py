from fractions import Fraction as F
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/verify')
def unfold_pos(d, L):
    p = d % (2 * L)
    if p == 0: return F(0), 0
    if p < L: return p, 1
    if p == L: return L, 0
    return 2 * L - p, -1
def head_on_meets(v1, v2, L, n):
    """两端出发（甲在A，乙在B），返回前 n 次迎面相遇距A的位置"""
    res = []
    cand = set()
    for k in range(0, 200):
        t = (2 * L * k + L) / (v1 + v2)  # 展开：d1 + d2' ≡ 0 (mod 2L)，乙展开初值 L
        cand.add(t)
        if v1 != v2:
            t2 = (2 * L * k - L) / (v1 - v2)
            if t2 > 0: cand.add(t2)
            t3 = (2 * L * k + L) / (v1 - v2)
            if t3 > 0: cand.add(t3)
    eps = F(1, 10**9)
    for t in sorted(cand):
        if t <= 0: continue
        x1, _ = unfold_pos(v1 * t, L); x2, _ = unfold_pos(L + v2 * t, L)
        if x1 != x2: continue
        _, a = unfold_pos(v1 * (t - eps), L); _, b = unfold_pos(L + v2 * (t - eps), L)
        if a != b:
            res.append((t, x1))
        if len(res) >= n: break
    return res
# D31-G8-V1：首次迎面距A 30，第三次迎面距A 50 -> 扫描 S
sols = []
for S10 in range(310, 3001):  # S 从 31 到 300，步长 0.1
    S = F(S10, 10)
    v1, v2 = F(30), S - 30   # 时间同 -> 速度比 = 路程比
    m = head_on_meets(v1, v2, S, 3)
    if len(m) == 3 and m[0][1] == 30 and m[2][1] == 50:
        sols.append(float(S))
print("满足条件的 S:", sols)
# 三批接送占比公式核对
for n, k in [(2, 8), (3, 5), (3, 4)]:
    print("n=%d k=%d 乘车占比公式 (k+1)/(k+1+2(n-1)) =" % (n, k), F(k + 1, k + 1 + 2 * (n - 1)))
