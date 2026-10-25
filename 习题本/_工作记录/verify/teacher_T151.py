# teacher T151（2015四川上）立方体堆垛：1层共1个，2层共4个，3层共10个，求7层共几个
OPTS = {'A': 60, 'B': 64, 'C': 80, 'D': 84}
GIVEN = {1: 1, 2: 4, 3: 10}           # 摆n层时的总数

def layer_count(k):
    """第k层是边长为k的三角形阵：位置(i,j)满足 i+j<k"""
    return sum(1 for i in range(k) for j in range(k) if i + j < k)

cum = lambda n: sum(layer_count(k) for k in range(1, n + 1))
assert all(cum(n) == v for n, v in GIVEN.items())   # 与题给数据吻合
total = cum(7)
print('各层', [layer_count(k) for k in range(1, 8)], '合计', total)
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits
print(hits[0])
