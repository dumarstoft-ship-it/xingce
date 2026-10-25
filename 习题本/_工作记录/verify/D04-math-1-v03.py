# D04-math-1-v03  利润率口径：进价120，甲店"进价加价25%"，乙店"利润占售价25%"
from fractions import Fraction as F

COST = F(120)
RATE = F(25, 100)

jia = COST * (1 + RATE)
# 乙店：在 0.01 元精度上穷举满足 (P-进价)/P = 25% 的售价
yi_list = [F(c, 100) for c in range(12001, 100000) if (F(c, 100) - COST) / F(c, 100) == RATE]
assert len(yi_list) == 1
yi = yi_list[0]

STATEMENTS = {
    'A': ('两店售价相同', lambda: jia == yi),
    'B': ('甲店比乙店高6元', lambda: jia - yi == 6),
    'C': ('乙店比甲店高7.5元', lambda: yi - jia == F(15, 2)),
    'D': ('乙店比甲店高10元', lambda: yi - jia == 10),
}
hits = [L for L, (_, f) in STATEMENTS.items() if f()]
assert len(hits) == 1, hits

# 干扰项来源核对
w_conv = COST * (1 + RATE / (1 + RATE))     # 换算记反 s/(1+s)=20% -> 144
assert jia - w_conv == 6
w_base = COST + RATE * jia                  # 用甲店售价150作基数 -> 157.5
assert w_base - jia == F(15, 2)
# 换算式核对：销售利润率 s 对应成本利润率 s/(1-s)
assert (yi - COST) / COST == RATE / (1 - RATE)

print('jia', jia, 'yi', yi)
print(hits[0])
