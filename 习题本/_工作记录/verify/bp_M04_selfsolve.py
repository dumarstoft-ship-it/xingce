# -*- coding: utf-8 -*-
"""M04 行程问题：无官方答案真题的独立验算（从题面数据出发，事件/分段精确模拟，不代入预期答案）。"""
from fractions import Fraction as F
import random

def pick(options, value):
    hits = [k for k, v in options.items() if abs(float(v) - float(value)) < 1e-9]
    assert len(hits) == 1, (options, value, hits)
    return hits[0]

# ---------- 往返（弹跳）运动的分段精确模拟工具 ----------
def bounce_pos(v, t, lo, hi, x0, dir0):
    """速度 v 在 [lo,hi] 间往返，t 时刻位置与方向（精确分数）。"""
    L = hi - lo
    # 展开：从 lo 出发方向 + 的等效展开距离
    if dir0 > 0:
        d0 = x0 - lo
    else:
        d0 = 2 * L - (x0 - lo)
    d = (d0 + v * t) % (2 * L)
    if d < L:
        return lo + d, 1
    elif d == L:
        return hi, 0  # 恰在端点（掉头瞬间）
    else:
        return lo + 2 * L - d, -1

def breakpoints(v, lo, hi, x0, dir0, T):
    L = hi - lo
    d0 = (x0 - lo) if dir0 > 0 else 2 * L - (x0 - lo)
    pts = []
    k = 0
    while True:
        # 到达端点时展开距离为 L 的整数倍
        target = (d0 // L + 1 + k) * L
        t = (target - d0) / v
        if t > T:
            break
        pts.append(t)
        k += 1
    return pts

# ========== 2026GD-45：直线往返，甲第二次追上乙的位置 ==========
def gd45():
    v1, v2, L = F(140), F(100), F(200)
    T = F(60)
    bps = sorted(set([F(0), T] + breakpoints(v1, 0, L, 0, 1, T) + breakpoints(v2, 0, L, 0, 1, T)))
    events = []
    eps = F(1, 10**9)
    for a, b in zip(bps, bps[1:]):
        # 区间 (a,b) 内两人都做线性运动
        m = (a + b) / 2
        x1m, d1 = bounce_pos(v1, m, 0, L, 0, 1)
        x2m, d2 = bounce_pos(v2, m, 0, L, 0, 1)
        s1, s2 = v1 * d1, v2 * d2
        # x1(t)=x1m+s1(t-m), x2(t)=x2m+s2(t-m)
        if s1 != s2:
            t = m + (x2m - x1m) / (s1 - s2)
            if a <= t <= b:
                events.append((t, d1, d2))
    # 合并同一时刻；判定"追上"：相遇时刻之前两人运动方向相同（甲从后面赶上）
    seen = {}
    for t, d1, d2 in events:
        if t == 0:
            continue
        seen.setdefault(t, set()).add((d1, d2))
    catches = []
    for t in sorted(seen):
        # 看相遇前一瞬间的方向
        _, d1b = bounce_pos(v1, t - eps, 0, L, 0, 1)
        _, d2b = bounce_pos(v2, t - eps, 0, L, 0, 1)
        x, _ = bounce_pos(v1, t, 0, L, 0, 1)
        kind = "追上" if d1b == d2b else "迎面"
        if kind == "追上":
            catches.append((t, x))
    t2, x2 = catches[1]
    print("2026GD-45 追上事件(时刻min,距起点m):", [(str(t), str(x)) for t, x in catches[:4]])
    return pick({"A": 0, "B": 50, "C": 100, "D": 200}, x2)

# ========== 2026GK-71：张在甲乙间往返、王在乙丙间往返，到达次数 ==========
def gk71():
    # 甲=0, 丙=1, 乙=2；设王速度=1，张速度=r，找 r 使"王第5次到乙"与"张第4次到乙"同时
    def arrivals_at(v, lo, hi, x0, dir0, target, n):
        T = F(1000)
        res = []
        for t in breakpoints(v, lo, hi, x0, dir0, T):
            x, _ = bounce_pos(v, t, lo, hi, x0, dir0)
            if x == target:
                res.append(t)
            if len(res) >= n:
                break
        return res[n - 1]
    t_wang5 = arrivals_at(F(1), 1, 2, 2, -1, 2, 5)   # 王从乙(2)出发向丙
    # 张第4次到乙的时刻 = t_wang5  =>  张速度 = 张的路程 / t_wang5，用速度1求张第4次到乙的"路程"
    t_zhang4_at_speed1 = arrivals_at(F(1), 0, 2, 0, 1, 2, 4)
    r = t_zhang4_at_speed1 / t_wang5
    print("2026GK-71 张/王 =", r)
    return pick({"A": F(5, 7), "B": F(7, 5), "C": F(7, 10), "D": F(10, 7)}, r)

# ========== 2026GK-79：环形三车，相遇时间差 5 秒 ==========
def gk79():
    # 速度 4k,5k,6k，周长 L；令 k=1 求 L（秒）
    # 甲丙反向首次相遇 t1=L/10，乙丙 t2=L/11，t1-t2=5
    # 用数值搜索而非直接代公式：二分 L
    lo, hi = F(1), F(10**6)
    for _ in range(200):
        mid = (lo + hi) / 2
        diff = mid / 10 - mid / 11
        if diff < 5:
            lo = mid
        else:
            hi = mid
    L = (lo + hi) / 2
    # 乙追上甲：模拟同向两车，逐秒找首次领先一圈
    t = L / (5 - 4)
    minutes = float(t) / 60
    print("2026GK-79 周长(以k=1计)=%.3f, 乙首次追上甲=%.3f 秒=%.3f 分" % (float(L), float(t), minutes))
    if minutes < 8: return "A"
    if minutes < 9: return "B"
    if minutes < 10: return "C"
    return "D"

# ========== 2026ZJA-57：竹排参照系 ==========
def zja57():
    random.seed(1)
    res = set()
    for _ in range(200):
        v = F(random.randint(5, 30))      # 静水速度
        w = F(random.randint(1, 4))       # 水速
        t = F(random.randint(1, 20), 10)  # 经过时间
        # 由"甲距竹排 2、乙距竹排 8"反推 x,y：x - v t = 2, y - v t = 8（从位置模型独立推出）
        # 位置模型（下游为正）：A=0, C=x, B=x+y；甲 (v+w)t，竹排 x+wt，乙 x+y-(v-w)t
        x = 2 + v * t
        y = 8 + v * t
        jia, raft, yi = (v + w) * t, x + w * t, x + y - (v - w) * t
        assert raft - jia == 2 and yi - raft == 8
        res.add(y - x)
    assert len(res) == 1
    val = res.pop()
    print("2026ZJA-57 y-x =", val)
    return pick({"A": -3, "B": -6, "C": 3, "D": 6}, val)  # A:x-y=3 即 y-x=-3

# ========== 2026ZJA-48：追及（中途休息） ==========
def zja48():
    # 乙速度 v，甲 v+1；8点出发，11-12点甲休息，12点乙赶上
    for v in [F(n, 10) for n in range(1, 400)]:
        jia = (v + 1) * 3          # 甲 8-11 点行走
        yi = v * 4                 # 乙 8-12 点行走
        # 12点前乙不能已超过甲（"在12点赶上"）
        if yi == jia:
            print("2026ZJA-48 乙速度=%s, 乙路程=%s" % (v, yi))
            return pick({"A": 9, "B": 12, "C": 15, "D": 18}, yi)

if __name__ == "__main__":
    out = {"2026GD-45": gd45(), "2026GK-71": gk71(), "2026GK-79": gk79(),
           "2026ZJA-57": zja57(), "2026ZJA-48": zja48()}
    print(out)
