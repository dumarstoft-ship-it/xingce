# D06-math-h-v05：初评通过 40%；初评未通过的均修改后复评 1 次，复评通过 30%；初评或复评通过者进入终评，
# 终评被采纳 50%。已知某方案最终被采纳，求它是经复评才进入终评的概率。
# 枚举整棵流程树的全部叶子（路径概率逐段相乘），在"被采纳"的叶子里算"经复评"的占比。
from fractions import Fraction as F

OPTIONS = {'A': F(9, 50), 'B': F(9, 29), 'C': F(3, 7), 'D': F(9, 20)}
P_FIRST, P_RETRY, P_FINAL = F(40, 100), F(30, 100), F(50, 100)

leaves = []   # (经过复评?, 被采纳?, 概率)
for first_ok, w1 in ((True, P_FIRST), (False, 1 - P_FIRST)):
    if first_ok:
        branches = [(False, True, w1)]
    else:
        branches = [(True, ok, w1 * w) for ok, w in ((True, P_RETRY), (False, 1 - P_RETRY))]
    for via_retry, in_final, w in branches:
        if in_final:
            for adopted, w3 in ((True, P_FINAL), (False, 1 - P_FINAL)):
                leaves.append((via_retry, adopted, w * w3))
        else:
            leaves.append((via_retry, False, w))
assert sum(w for *_, w in leaves) == 1

p_adopt = sum(w for v, a, w in leaves if a)
p_retry_adopt = sum(w for v, a, w in leaves if a and v)
ans = p_retry_adopt / p_adopt

hits = [k for k, v in OPTIONS.items() if v == ans]
assert len(hits) == 1, (ans, hits)

# 自检：干扰项对应的错误路径
assert (1 - P_FIRST) * P_RETRY == OPTIONS['A']                                  # 不缩小样本空间
assert P_RETRY / (P_FIRST + P_RETRY) == OPTIONS['C']                            # 路径漏乘"初评未通过"0.6
assert p_retry_adopt / (p_adopt - p_retry_adopt) == OPTIONS['D']                # 只除以另一条路径
print('P(采纳) =', p_adopt, ' P(经复评且采纳) =', p_retry_adopt, ' P =', ans, float(ans))
print(hits[0])
