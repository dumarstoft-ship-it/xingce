# teacher T128（2023江西/河北联考）L形道路网最短路线经过丙地的概率
from fractions import Fraction as F
from functools import lru_cache

OPTS = {'A': F(11, 15), 'B': F(12, 53), 'C': F(11, 36), 'D': F(16, 53)}
# 按原图建坐标：x=0..4 自左向右，y=0..4 自下向上
# 下部 x0~4、y0~2 为完整网格；上部只有 x2~4、y2~4（左上角缺一块）
def node(x, y):
    return (0 <= x <= 4 and 0 <= y <= 2) or (2 <= x <= 4 and 2 <= y <= 4)
JIA, YI, BING = (4, 4), (0, 0), (3, 1)    # 甲右上角，乙左下角，丙为右数第2列、下数第2行的交点

@lru_cache(None)
def paths(a, b):
    """从a到b的最短路线数：只能向左或向下，且只能走网格上的路"""
    if a == b:
        return 1
    x, y = a
    return sum(paths((nx, ny), b) for nx, ny in ((x - 1, y), (x, y - 1))
               if nx >= b[0] and ny >= b[1] and node(nx, ny))

total = paths(JIA, YI)
via = paths(JIA, BING) * paths(BING, YI)
P = F(via, total)
print('甲→乙', total, '| 甲→丙', paths(JIA, BING), '| 丙→乙', paths(BING, YI), '| P =', P)
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
