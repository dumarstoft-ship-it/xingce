# D01-math-h-v13 三个分拣台共200件包裹，A→(B,C)、B→(A,C)、C→(A,B)三次"使另两台都翻倍"的调配，
# 末态C台是A台的7/8，求调配前A台的包裹数。
# 独立求解：枚举所有初始分配(a,b,c)，按题意正向模拟三次调配（分出的一台包裹不够即不可行），
# 筛出末态 C/A = 7/8 的情形，确认唯一；再用"带字母倒推"做交叉验证，并逐一复核干扰项的错误路径。
from fractions import Fraction as Fr

OPTS = {'A': 104, 'B': 107, 'C': 108, 'D': 116}
TOTAL = 200
RATIO = Fr(7, 8)          # 末态 C 台 / A 台


def run(a, b, c, strict=True):
    """正向模拟三次调配，返回各阶段状态；分出的一台包裹不足（或 strict 时出现 0 件）返回 None。"""
    lo = 1 if strict else 0
    states = [(a, b, c)]
    give = b + c                       # 第一次：A 调出，使 B、C 都翻倍
    if a - give < lo: return None
    a, b, c = a - give, 2 * b, 2 * c
    states.append((a, b, c))
    give = a + c                       # 第二次：B 调出，使 A、C 都翻倍
    if b - give < lo: return None
    a, b, c = 2 * a, b - give, 2 * c
    states.append((a, b, c))
    give = a + b                       # 第三次：C 调出，使 A、B 都翻倍
    if c - give < lo: return None
    a, b, c = 2 * a, 2 * b, c - give
    states.append((a, b, c))
    return states


def solve(ratio, strict=True):
    out = []
    lo = 1 if strict else 0
    for a in range(lo, TOTAL + 1):
        for b in range(lo, TOTAL - a + 1):
            c = TOTAL - a - b
            if c < lo: continue
            st = run(a, b, c, strict)
            if st is None: continue
            fa, fb, fc = st[-1]
            if fa > 0 and Fr(fc, fa) == ratio:
                out.append(st)
    return out


sols = solve(RATIO)
assert len(sols) == 1, sols
assert solve(RATIO, strict=False) == sols          # 允许中途出现 0 件也不改变唯一解
states = sols[0]
ans = states[0][0]
assert states[-1][2] * 8 == states[-1][0] * 7


# 交叉验证：设末态 A=8x、C=7x、B=200-15x，逐步倒推（被翻倍的两台减半，分出的一台加回）
def back(x):
    a, b, c = Fr(8 * x), Fr(TOTAL - 15 * x), Fr(7 * x)
    chain = [(a, b, c)]
    a, b, c = a / 2, b / 2, c + a / 2 + b / 2; chain.append((a, b, c))   # 撤销第三次
    a, b, c = a / 2, b + a / 2 + c / 2, c / 2; chain.append((a, b, c))   # 撤销第二次
    a, b, c = a + b / 2 + c / 2, b / 2, c / 2; chain.append((a, b, c))   # 撤销第一次
    return chain[::-1]


ok_x = [x for x in range(1, 40)
        if all(v.denominator == 1 and v > 0 for s in back(x) for v in s)]
assert ok_x == [8], ok_x
assert back(8)[0][0] == ans and all(back(x)[0][0] == 100 + x for x in range(1, 14))

# 干扰项的错误路径
rev = solve(1 / RATIO)                              # 把比例看反：A 是 C 的 7/8
assert len(rev) == 1 and rev[0][0][0] == OPTS['B']
# 只验到"第二次之前 C=50+7x/4 为整数"（x 是 4 的倍数）就停：x=4 → 104
x4 = [x for x in range(1, 14) if back(x)[1][2].denominator == 1 and x % 8]
assert 100 + x4[0] == OPTS['A']
# x=16 也让各步为整数，但末态 B=200-240<0，正向模拟时第二次 B 台包裹不够
assert 100 + 16 == OPTS['D'] and all(v.denominator == 1 for s in back(16) for v in s)
assert run(116, 45, 39) is None and back(16)[0] == (116, 45, 39)

# 解析中的正推快法：每次分出包裹的那一台，新数＝2×原数−200（另两台翻倍，正好拿走 200−原数）
(a0, b0, c0), s1, s2, s3 = states
assert s1[0] == 2 * a0 - TOTAL and s2[1] == 2 * s1[1] - TOTAL and s3[2] == 2 * s2[2] - TOTAL
assert s3[0] == 4 * (2 * a0 - TOTAL) and s3[2] == 8 * c0 - TOTAL
# 末态C＝7/8×末态A → 8c＝7a−500：选项中只有 a 除以8余4 的108、116能使 c 为整数
assert sorted(v for v in OPTS.values() if (7 * v - 500) % 8 == 0) == [108, 116]
c116 = (7 * 116 - 500) // 8
assert (c116, TOTAL - 116 - c116) == (39, 45) and run(116, 45, 39) is None   # 116：第二次B台不够分

hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits
print('states', states)
print(hits[0])
