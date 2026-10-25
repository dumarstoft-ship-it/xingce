# D02-math-h-v01  三条分拣线各分拣210件，8:00同时开工、速度不变。11:30丙线完成，此时乙线还剩35件；
# 乙线完成时，甲线还剩42件。次日690件分给三线：甲、乙8:00开工，丙9:00开工，要求同时完成。求丙应分配的件数。
from fractions import Fraction as F

OPTS = {'A': 216, 'B': 240, 'C': 276, 'D': 300}
Q = 210
START = F(8)
C_DONE = F(23, 2)          # 11:30
B_LEFT_AT_C_DONE = 35
A_LEFT_AT_B_DONE = 42


def day1_matches(a, b, c):
    """按题面第一天的观测逐条核对速度 (a, b, c)（件/小时）。"""
    if START + F(Q, c) != C_DONE:                      # 丙 11:30 恰好完成
        return False
    if Q - b * (C_DONE - START) != B_LEFT_AT_C_DONE:  # 此时乙还剩35件
        return False
    tb = F(Q, b)                                       # 乙完成所用时长
    if not (tb > C_DONE - START):                      # 乙在丙之后完成
        return False
    return Q - a * tb == A_LEFT_AT_B_DONE              # 乙完成时甲还剩42件


# 由第一天的三条观测直接解出速度（允许分数），再逐条回代核对
c = F(Q) / (C_DONE - START)                         # 丙：8:00~11:30 完成 Q
b = F(Q - B_LEFT_AT_C_DONE) / (C_DONE - START)      # 乙：同一时段完成 Q-35
a = F(Q - A_LEFT_AT_B_DONE) / (F(Q) / b)            # 甲：乙完成所用的时段内完成 Q-42
assert day1_matches(a, b, c) and a < b < c

# ---- 第二天：甲乙8:00、丙9:00开工，在同一时刻 T 完成，三线完成量之和=690 ----
M = 690
AB_START, C_START = F(8), F(9)


def done_by(T):
    return a * (T - AB_START) + b * (T - AB_START) + c * (T - C_START)


sols = [F(s, 3600) for s in range(9 * 3600 + 1, 24 * 3600) if done_by(F(s, 3600)) == M]   # 按秒扫描
assert len(sols) == 1, sols
T = sols[0]
share_c = c * (T - C_START)


def option_ok(v):
    """若丙分到 v 件：丙从9:00干 v/c 小时；甲乙干到同一时刻，三者之和须恰为 M。"""
    t_end = C_START + F(v, c)
    return a * (t_end - AB_START) + b * (t_end - AB_START) + v == M


hits = [k for k, v in OPTS.items() if option_ok(v)]
assert len(hits) == 1 and OPTS[hits[0]] == share_c, hits

# ---- 干扰项来源核对 ----
S = a + b + c
late = C_START - AB_START
assert F(M * c, S) == OPTS['C']                       # 直接按速度比 4:5:6 分 690
assert F((M + c * late) * c, S) == OPTS['D']          # “补齐”成 750 后忘了减去丙缺的 60
assert F(M * c, S) - c * late == OPTS['A']            # 按比例分后直接扣掉丙 1 小时的 60
wrong = F((M - c * late) * c, S)                      # 总量先扣丙 1 小时再按比例分（不在选项中，核对它不会碰巧等于答案）
assert wrong != share_c and wrong not in OPTS.values()

print('speeds', a, b, c, 'finish', T, 'C share', share_c)
print(hits[0])
