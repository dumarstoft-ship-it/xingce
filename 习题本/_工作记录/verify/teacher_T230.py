# T230 沙漏：上锥尖朝下，沙堆始终是与容器相似的小圆锥；高度降一半所需时间
from fractions import Fraction as F
total_minutes = 60
remain_ratio = F(1, 2) ** 3            # 体积比 = 相似比的立方
t = total_minutes * (1 - remain_ratio) # 匀速流沙
options = {"A": F(30), "B": F(45), "C": F(475, 10), "D": F(525, 10)}
hits = [k for k, v in options.items() if v == t]
assert len(hits) == 1, (t, hits)
print(hits[0])
