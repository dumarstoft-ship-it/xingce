# -*- coding: utf-8 -*-
"""M04 行程问题验算工具：分段线性轨迹（精确分数）+ 相遇事件检测。
所有改编 idea 与自解真题都用它从题面数据出发独立计算（模拟运动过程），不代入预期答案。"""
from fractions import Fraction as F
import math

def Fr(x):
    return x if isinstance(x, F) else F(x).limit_denominator(10**9) if isinstance(x, float) else F(x)

class Traj:
    """轨迹 = 首尾相接的线性段 (t0, t1, x0, x1)；t1 之后停在最后位置。"""
    def __init__(self, t0=0, x0=0):
        self.segs = []
        self.t = Fr(t0)
        self.x = Fr(x0)
    def move_to(self, x, v):
        x = Fr(x); v = Fr(v)
        dt = abs(x - self.x) / v
        self.segs.append((self.t, self.t + dt, self.x, x))
        self.t += dt; self.x = x
        return self
    def move_for(self, dt, v_signed):
        dt = Fr(dt); v = Fr(v_signed)
        nx = self.x + v * dt
        self.segs.append((self.t, self.t + dt, self.x, nx))
        self.t += dt; self.x = nx
        return self
    def wait(self, dt):
        dt = Fr(dt)
        self.segs.append((self.t, self.t + dt, self.x, self.x))
        self.t += dt
        return self
    def pos(self, t):
        t = Fr(t)
        if not self.segs or t <= self.segs[0][0]:
            return self.segs[0][2] if self.segs else self.x
        for a, b, x0, x1 in self.segs:
            if a <= t <= b:
                return x0 if b == a else x0 + (x1 - x0) * (t - a) / (b - a)
        return self.segs[-1][3]
    def vel(self, t, side=+1):
        """t 时刻左(side=-1)/右(side=+1)速度"""
        t = Fr(t)
        for a, b, x0, x1 in self.segs:
            if b == a:
                continue
            if (side > 0 and a <= t < b) or (side < 0 and a < t <= b):
                return (x1 - x0) / (b - a)
        return F(0)
    def end(self):
        return self.t
    def breakpoints(self):
        s = set()
        for a, b, *_ in self.segs:
            s.add(a); s.add(b)
        return s

def bounce(L, v, T, x0=0, dir0=+1, t0=0, stay=0, trips=None):
    """在 [0,L] 间往返，速度 v，从 x0 出发方向 dir0，t0 时刻开始(之前停在 x0)，
    每到端点停留 stay；trips=往返次数(到达出发端算一次来回)，None 表示一直跑到 T。"""
    L, v, T = Fr(L), Fr(v), Fr(T)
    tr = Traj(0, x0)
    if Fr(t0) > 0:
        tr.wait(t0)
    d = dir0
    legs = 0
    while tr.t < T:
        target = L if d > 0 else F(0)
        tr.move_to(target, v)
        legs += 1
        if trips is not None and legs >= 2 * trips:
            break
        if stay:
            tr.wait(stay)
        d = -d
    return tr

def meetings(A, B, tmin=None, tmax=None, eps=F(1, 10**7)):
    """返回 A、B 位置相同的时刻（孤立点）及类型：
    head-on 迎面（相遇前后速度方向相反）/ catch 追上（同向，一方从后面赶上）/ touch 接触 / other。"""
    ts = set()
    for a1, b1, p1, q1 in A.segs:
        for a2, b2, p2, q2 in B.segs:
            lo, hi = max(a1, a2), min(b1, b2)
            if lo > hi:
                continue
            # A(t) = p1 + s1 (t-a1), B(t)= p2 + s2 (t-a2)
            s1 = (q1 - p1) / (b1 - a1) if b1 > a1 else F(0)
            s2 = (q2 - p2) / (b2 - a2) if b2 > a2 else F(0)
            c1 = p1 - s1 * a1
            c2 = p2 - s2 * a2
            if s1 == s2:
                if c1 == c2:
                    ts.add(('interval', lo, hi))
                continue
            t = (c2 - c1) / (s1 - s2)
            if lo <= t <= hi:
                ts.add(('pt', t))
    pts = sorted(set(x[1] for x in ts if x[0] == 'pt'))
    out = []
    for t in pts:
        if tmin is not None and t <= tmin:
            continue
        if tmax is not None and t > tmax:
            continue
        x = A.pos(t)
        if B.pos(t) != x:
            continue
        dA_before = A.pos(t) - A.pos(t - eps); dB_before = B.pos(t) - B.pos(t - eps)
        before = (A.pos(t - eps) - B.pos(t - eps))
        after = (A.pos(t + eps) - B.pos(t + eps))
        va, vb = A.vel(t, -1), B.vel(t, -1)
        if va * vb < 0:
            kind = 'head-on'
        elif va * vb > 0:
            kind = 'catch'
        else:
            kind = 'one-still'
        crossing = (before > 0 > after) or (before < 0 < after)
        out.append(dict(t=t, x=x, kind=kind, cross=crossing, before=before, after=after))
    return out

def ring_pos(v, t, L, start=0, direction=+1):
    return (Fr(start) + direction * Fr(v) * Fr(t)) % Fr(L)

def pick(options, value, tol=1e-9):
    """恰好一个选项与 value 相等，返回其字母；否则抛错"""
    hits = []
    for k, v in options.items():
        try:
            if abs(float(v) - float(value)) < tol:
                hits.append(k)
        except TypeError:
            if v == value:
                hits.append(k)
    assert len(hits) == 1, ("选项匹配异常", options, value, hits)
    return hits[0]

def solve_linear(f, lo, hi, it=200):
    """单调函数二分求根（浮点，仅作交叉核对）"""
    flo = f(lo)
    for _ in range(it):
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0):
            lo = m
        else:
            hi = m
    return (lo + hi) / 2
