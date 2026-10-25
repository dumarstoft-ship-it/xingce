"""D06-math-h-v08  甲箱 3 本科普 + 2 本历史，乙箱 2 本科普 + 3 本历史；从甲箱随机取 2 本放入乙箱，
再从乙箱随机借走 1 本，求借走科普读物的概率。
独立求解：给每本书编号，穷举"从甲箱取哪 2 本"（无序、等可能）×"从乙箱借哪 1 本"（等可能）的全部结果，
逐一计数，得精确分数；另按"移入几本科普"分类复核一遍。再解析四个选项，确认恰好一个相等，打印该选项字母。
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import re

# ---- 题面数据 ----
BOX_JIA = ["科普"] * 3 + ["历史"] * 2
BOX_YI = ["科普"] * 2 + ["历史"] * 3
MOVE = 2
OPTIONS = {"A": r"$\frac{2}{5}$", "B": r"$\frac{3}{7}$", "C": r"$\frac{16}{35}$", "D": r"$\frac{1}{2}$"}

# 方法 1：逐本穷举
total = F(0)
picks = list(combinations(range(len(BOX_JIA)), MOVE))
for pick in picks:                       # 每种取法概率 1/len(picks)
    new_yi = BOX_YI + [BOX_JIA[i] for i in pick]
    for book in new_yi:                  # 每本书被借走的概率 1/len(new_yi)
        if book == "科普":
            total += F(1, len(picks)) * F(1, len(new_yi))
print("穷举 P(借到科普) =", total, float(total))

# 方法 2：按移入科普本数 j 分类（超几何权重）
a, b = BOX_JIA.count("科普"), BOX_JIA.count("历史")
c, n2 = BOX_YI.count("科普"), len(BOX_YI)
by_class = sum(F(comb(a, j) * comb(b, MOVE - j), comb(a + b, MOVE)) * F(c + j, n2 + MOVE) for j in range(MOVE + 1))
print("分类 P =", by_class)
assert by_class == total

def parse(s):
    m = re.search(r"\\frac\{(\d+)\}\{(\d+)\}", s)
    return F(int(m.group(1)), int(m.group(2)))

hits = [k for k, v in OPTIONS.items() if parse(v) == total]
assert len(hits) == 1, hits
print(hits[0])
