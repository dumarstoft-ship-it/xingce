# real 2026ZJA-96  酒店升级提星：要求 升级 → 设施完备 ∧ 通过考核。哪些情形说明"没有遵守要求"？
from itertools import product

def rule_ok(up, fac, chk):
    # 要求：升级提星 → (基本设施完备 ∧ 通过卫生考核)
    return (not up) or (fac and chk)

# 三个情形（未提及的变量任意取值）
SCEN = {
    1: lambda up, fac, chk: up and not chk,             # 升级了，但没通过考核
    2: lambda up, fac, chk: up and not fac,             # 升级了，但设施不完备
    3: lambda up, fac, chk: fac and chk and not up,     # 设施完备且通过考核，但没升级
}

def shows_violation(s):
    worlds = [w for w in product([True, False], repeat=3) if SCEN[s](*w)]
    assert worlds
    # "说明没有遵守要求"：该情形下要求必然被违反
    return all(not rule_ok(*w) for w in worlds)

viol = {s for s in SCEN if shows_violation(s)}
print('能说明违反要求的情形：', sorted(viol))
OPTS = {'A': {1, 2}, 'B': {2, 3}, 'C': {3}, 'D': {1, 2, 3}}
hits = [k for k, v in OPTS.items() if v == viol]
assert len(hits) == 1, hits
print(hits[0])
