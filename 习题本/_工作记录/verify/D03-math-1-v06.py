# D03-math-1-v06: 绕行路程是通道的3倍，通道车速是绕行的4/3倍，节省1小时；求走通道用时（分钟）
from fractions import Fraction as F

PATH_RATIO, SPEED_RATIO, SAVE = 3, F(4, 3), 60   # 节省 60 分钟
OPTS = {'A': 20, 'B': 30, 'C': 48, 'D': 80}

new_times = set()
# 穷举通道路程 d（1~200千米）和绕行车速 u（1~150千米/时），找出所有满足“节省1小时”的情形
for d in range(1, 201):
    for u in range(1, 151):
        old = F(PATH_RATIO * d, u) * 60           # 绕行用时（分钟）
        new = F(d) / (u * SPEED_RATIO) * 60       # 走通道用时（分钟）
        if old - new == SAVE:
            new_times.add(new)
assert len(new_times) == 1, new_times              # 路程、车速不唯一，但用时唯一
ans = new_times.pop()
hit = [k for k, x in OPTS.items() if x == ans]
assert len(hit) == 1, (ans, hit)
# 干扰项来源
assert F(SAVE) / (PATH_RATIO - 1) == OPTS['B']                  # 只看路程
r = F(1, PATH_RATIO) * SPEED_RATIO                               # 把车速倍数乘到用时上
assert SAVE / (1 - r) * r == OPTS['C']
assert ans + SAVE == OPTS['D']                                   # 求成绕行用时
print('new time =', ans)
print(hit[0])
