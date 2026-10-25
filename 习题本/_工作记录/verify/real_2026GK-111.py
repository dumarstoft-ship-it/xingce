# real 2026GK-111  "三医"协同：由题干条件链可以推出哪项？
# T 提高卫生事业发展水平  H 相关部门密切合作、同向发力  S 促进"三医"协同发展和治理
# D 深化医改领导体制和工作推进机制  G 强化两个规划的刚性约束
# M 更好满足人民群众对美好生活的新期待  F 提高获得感、幸福感和安全感
from itertools import product

def imp(a, b):
    return (not a) or b

def premises(v, jin_er='F->M'):
    T, H, S, D, G, M, F = v
    ok = imp(S, T and H) and imp(S, D) and imp(D, G) and imp(M, D)
    # "只有D，才能M，进而F"：F 要靠 M 实现，即 F→M（标准译法）
    ok = ok and (imp(F, M) if jin_er == 'F->M' else imp(M, F))
    return ok

OPTS = {
    'A': lambda T, H, S, D, G, M, F: imp(T, H),          # 只要T就H
    'B': lambda T, H, S, D, G, M, F: imp(F, G),          # 只有G才F
    'C': lambda T, H, S, D, G, M, F: imp(D, S),          # 要D就必须S
    'D': lambda T, H, S, D, G, M, F: imp(not M, not S),  # 不M就不S
}

def valid_opts(jin_er):
    W = [v for v in product([True, False], repeat=7) if premises(v, jin_er)]
    assert W
    return [k for k, f in OPTS.items() if all(f(*v) for v in W)]

print('对照：若把"进而"译成 M→F，可推出的选项', valid_opts('M->F'))
hits = valid_opts('F->M')
assert len(hits) == 1, hits
print(hits[0])
