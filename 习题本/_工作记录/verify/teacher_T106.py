# T106 2011安徽：卡片面积A60、B170、C150，共盖住280；A∩B=22、B∩C=60、C∩A=35；求三者公共（阴影）面积
A, B, C, COVER = 60, 170, 150, 280
AB, BC, CA = 22, 60, 35
OPTS = {'A': 15, 'B': 16, 'C': 17, 'D': 18}

sols = []
for x in range(0, min(AB, BC, CA) + 1):        # 三张卡片的公共部分
    # 由公共部分推出七个区域面积，检验是否非负且总覆盖面积吻合
    ab, bc, ca = AB - x, BC - x, CA - x        # 仅两张重叠
    a, b, c = A - ab - ca - x, B - ab - bc - x, C - bc - ca - x
    regions = [a, b, c, ab, bc, ca, x]
    if min(regions) >= 0 and sum(regions) == COVER:
        sols.append(x)
assert len(sols) == 1, sols
x = sols[0]
print('shaded =', x)
print([k for k, v in OPTS.items() if v == x][0])
