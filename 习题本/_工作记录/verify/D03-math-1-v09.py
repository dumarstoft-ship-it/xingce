# D03-math-1-v09: 8:00出发，上行75分到补给站，休息15分，再上行到山顶；下行：山顶→补给站30分，补给站→山脚45分；求到顶时刻
from fractions import Fraction as F

START = 8 * 60
UP_LOW, REST, DOWN_HIGH, DOWN_LOW = 75, 15, 30, 45   # 分钟
OPTS = {'A': '9:48', 'B': '10:00', 'C': '10:05', 'D': '10:20'}

def clock(m):
    m = F(m)
    assert m.denominator == 1
    m = int(m)
    return f'{m // 60}:{m % 60:02d}'

arrivals = set()
# 穷举两段路长：山脚—补给站 x、补给站—山顶 y（10米步长），上、下行速度由已知用时确定
for x10 in range(10, 501):
    x = F(x10 * 10)
    up = x / UP_LOW               # 上行速度（米/分）
    down = x / DOWN_LOW           # 下行速度
    for y10 in range(10, 501):
        y = F(y10 * 10)
        if y / down != DOWN_HIGH:  # 山顶→补给站下行 30 分钟
            continue
        t_top = START + UP_LOW + REST + y / up
        arrivals.add(clock(t_top))
assert len(arrivals) == 1, arrivals
ans = arrivals.pop()
hit = [k for k, v in OPTS.items() if v == ans]
assert len(hit) == 1, (ans, hit)
# 干扰项来源
assert clock(START + UP_LOW + REST + DOWN_HIGH) == OPTS['B']                         # 直接用下行30分钟
assert clock(START + UP_LOW + F(DOWN_HIGH * UP_LOW, DOWN_LOW)) == OPTS['C']          # 忘了休息
assert clock(START + UP_LOW + REST + F(DOWN_HIGH * DOWN_LOW, UP_LOW)) == OPTS['A']   # 比例用反
print('到顶时刻', ans)
print(hit[0])
