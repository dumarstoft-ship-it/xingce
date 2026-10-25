# D02-math-1-v06  甲单独18天、乙单独36天；甲周日休、乙周六周日休；周一开工，求完工星期
from fractions import Fraction as F
WD = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
OPTS = {'A': '星期一', 'B': '星期二', 'C': '星期五', 'D': '星期六'}
jia, yi = F(1, 18), F(1, 36)


def finish(jia_rest, yi_rest):
    """逐日累加工作量，返回完工是第几天及星期几（0=周一）。"""
    done, day = F(0), 0
    while done < 1:
        wd = day % 7
        done += (0 if wd in jia_rest else jia) + (0 if wd in yi_rest else yi)
        day += 1
    return day, WD[(day - 1) % 7]


day, wd = finish({6}, {5, 6})
hits = [k for k, v in OPTS.items() if v == wd]
assert len(hits) == 1, (day, wd, hits)

# 干扰项来源核对
assert finish(set(), set())[1] == OPTS['C']           # 不考虑休息
assert finish({5, 6}, {5, 6})[1] == OPTS['B']         # 忽略甲周六施工
assert finish({6}, {6})[1] == OPTS['D']               # 以为乙周六也施工
print('day', day, wd)
print(hits[0])
