"""D03-logic-2-v03 数据验算（图书馆纸质书借阅量与市民阅读量）。

从题面数据出发：前年纸质书借阅 60 万册次，去年下降 30%，有人据此认为市民阅读量明显下降。
逐项读取各选项给出的、纸质书借阅之外的阅读渠道增量，计算借阅总量是否仍然下降，
找出能用数量推翻“明显下降”的选项，并确认恰好一项。
"""
from fractions import Fraction as F

paper_before = 60                          # 万册次（题面）
drop_rate = F(30, 100)                     # 题面：下降 30%
paper_after = paper_before * (1 - drop_rate)
decrease = paper_before - paper_after
assert paper_after == 42 and decrease == 18, (paper_after, decrease)

# 各选项给出的口径外增量（万册次）：
#   None = 有增长但没有数量（只能部分抵消，无法确定能否抵消 18 万册次的降幅）
#   0    = 没有提供增量（支持或无关）
offsets = {
    'A': None,      # 书店图书零售量“略有增长”，无数量
    'B': 0,         # 不少市民没时间读书：支持观点
    'C': 50 - 0,    # 电子书平台去年上线，当年借阅 50 万册次；上线前为 0
    'D': 0,         # 部分老年读者不会用电子书平台：偏支持
}

refuters = []
for letter, inc in offsets.items():
    if not inc:
        continue
    total_before = paper_before + 0
    total_after = paper_after + inc
    print(letter, 'library borrowing total', total_before, '->', total_after, '(paper drop', decrease, ')')
    if inc >= decrease and total_after >= total_before:
        refuters.append(letter)

assert len(refuters) == 1, refuters
assert paper_after + offsets[refuters[0]] == 92   # 与解析一致：总量 60 → 92 万册次
print(refuters[0])
