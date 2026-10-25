"""D06-math-h-v09  从 6 家超市中随机抽 3 家；已知甲、乙两家至少有一家被抽中，求甲、乙两家都被抽中的概率。
独立求解：穷举全部 C(6,3) 种等可能的抽法，筛出满足"甲或乙被抽中"的结果（缩小样本空间），
数其中甲、乙都在的个数，得精确分数；再解析四个选项，确认恰好一个相等，打印该选项字母。
"""
from fractions import Fraction as F
from itertools import combinations
import re

# ---- 题面数据 ----
N, K = 6, 3
JIA, YI = 0, 1
OPTIONS = {"A": r"$\frac{1}{5}$", "B": r"$\frac{1}{4}$", "C": r"$\frac{1}{3}$", "D": r"$\frac{2}{5}$"}

outcomes = list(combinations(range(N), K))
cond = [s for s in outcomes if JIA in s or YI in s]
fav = [s for s in cond if JIA in s and YI in s]
P = F(len(fav), len(cond))
only_jia = sum(1 for s in cond if JIA in s and YI not in s)
only_yi = sum(1 for s in cond if YI in s and JIA not in s)
print("全部", len(outcomes), "满足条件", len(cond), "只甲/只乙/都中", only_jia, only_yi, len(fav), "P =", P)

def parse(s):
    m = re.search(r"\\frac\{(\d+)\}\{(\d+)\}", s)
    return F(int(m.group(1)), int(m.group(2)))

hits = [k for k, v in OPTIONS.items() if parse(v) == P]
assert len(hits) == 1, hits
print(hits[0])
