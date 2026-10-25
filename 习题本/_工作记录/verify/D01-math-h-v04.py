# D01-math-h-v04  企业用工＝合同制职工＋劳务派遣人员，派遣人员占15%。先将10名派遣人员转为合同制职工
# （仍在企业，用工总量不变），再将20名派遣人员退回派遣单位（用工总量减少），此外无其他变动；
# 此时派遣人员占用工总量的10%。求原来的用工总量。
from fractions import Fraction as F

OPTS = {'A': 360, 'B': 400, 'C': 540, 'D': 560}
P0 = F(15, 100)    # 原派遣占比
CONV = 10          # 转为合同制职工的派遣人员：派遣人数减少，总量不变
OUT = 20           # 退回派遣单位的人员：派遣人数、总量都减少
P1 = F(10, 100)    # 变动后派遣占比
N = 200000


def solve(dispatch_drop, total_drop):
    """穷举原总量t（派遣人数须为整数且够减），返回满足“变动后占比＝P1”的全部t。"""
    out = []
    for t in range(1, N + 1):
        d = P0 * t
        if d.denominator != 1 or d < dispatch_drop or t <= total_drop:
            continue
        if F(d - dispatch_drop, t - total_drop) == P1:
            out.append(t)
    return out


# 正确建模：派遣人数共减少 10＋20，用工总量只减少退回的 20
sols = solve(CONV + OUT, OUT)
assert len(sols) == 1, sols
t = sols[0]
hits = [k for k, v in OPTS.items() if v == t]
assert len(hits) == 1, hits
vals = [OPTS[k] for k in 'ABCD']
assert vals == sorted(vals)

# 干扰项来源核对
r = solve(OUT, OUT)                    # 照搬“其余部分不变”，漏掉转正的10人（合同制职工其实多了10人）
assert r == [OPTS['A']], r
assert OUT / (P0 - P1) == OPTS['B']    # 把下降的5个百分点直接对应退回的20人
r = solve(CONV + OUT, CONV + OUT)      # 把转正的10人也算成用工总量减少
assert r == [OPTS['C']], r
assert t - OUT == OPTS['C']            # 也等于“答成变动后的用工总量”
d0 = P0 * t
print('original total', t, 'dispatched', d0, '-> after', d0 - CONV - OUT, '/', t - OUT)
print(hits[0])
