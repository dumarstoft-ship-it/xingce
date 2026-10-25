# D07-math-1-v01: 矩形绿地长、宽各缩短 2 米，面积减少 44 平方米，求原周长
from fractions import Fraction as F

CUT, DEC = 2, 44
perims = set()
# 在 0.5 米网格上穷举原来的长 l、宽 w（都须大于 2 米），收集所有满足条件的周长
for l2 in range(5, 600):
    for w2 in range(5, l2 + 1):
        l, w = F(l2, 2), F(w2, 2)
        if l * w - (l - CUT) * (w - CUT) == DEC:
            perims.add(2 * (l + w))
assert len(perims) == 1, perims          # 周长被唯一确定（长、宽本身不唯一）
P = perims.pop()
opts = {'A': 24, 'B': 40, 'C': 44, 'D': 48}
hit = [k for k, v in opts.items() if v == P]
assert len(hit) == 1, (P, hit)
print('原周长 =', P)
print(hit[0])
