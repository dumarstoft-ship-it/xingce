"""D06-math-h-v07  多层楼 40 栋×24 户（80% 楼栋已改造）、高层楼 20 栋×72 户（95% 楼栋已改造），
随机抽 1 户，其所在楼栋已改造的概率。
独立求解：按题面把每一栋楼、每一户都列出来（已改造楼栋数 = 栋数×比例），逐户计数，得精确分数；
再把四个百分数选项解析成分数，确认恰好一个相等，打印该选项字母。
"""
from fractions import Fraction as F

# ---- 题面数据 ----
TYPES = [  # (栋数, 每栋户数, 已完成改造的楼栋比例)
    (40, 24, F(80, 100)),
    (20, 72, F(95, 100)),
]
OPTIONS = {"A": "85.0%", "B": "86.0%", "C": "87.5%", "D": "89.0%"}

households = []  # 每户记录其所在楼栋是否已改造
for n_bld, per, rate in TYPES:
    done = rate * n_bld
    assert done.denominator == 1  # 楼栋数必须是整数
    for k in range(n_bld):
        renovated = k < done
        households += [renovated] * per
P = F(sum(households), len(households))
print("住户总数", len(households), "所在楼栋已改造的户数", sum(households), "P =", P, float(P))

# 对照：按楼栋数加权（随机抽一栋楼）只用于展示干扰项来源
bld = F(sum(int(r * n) for n, _, r in TYPES), sum(n for n, _, _ in TYPES))
print("若随机抽一栋楼：", bld, float(bld))

def parse(s):
    return F(s.rstrip("%")) / 100

hits = [k for k, v in OPTIONS.items() if parse(v) == P]
assert len(hits) == 1, hits
print(hits[0])
