# D05-math-h-v01：12 棵果树栽成 3 行 4 列（横向、纵向相邻间距相等），
# 以其中 3 棵树为顶点围三角形，问能围出多少个不同的三角形。
# 暴力枚举：把果树放在坐标网格上，枚举全部 3 棵树的组合，用叉积判断三点是否共线。
from itertools import combinations

OPTIONS = {'A': 196, 'B': 200, 'C': 204, 'D': 209}

ROWS, COLS, GAP = 3, 4, 4  # 3 行 4 列，相邻间距 4 米（间距只要相等，结果与具体数值无关）
trees = [(c * GAP, r * GAP) for r in range(ROWS) for c in range(COLS)]


def collinear(p, q, s):
    return (q[0] - p[0]) * (s[1] - p[1]) - (q[1] - p[1]) * (s[0] - p[0]) == 0


count = sum(1 for t in combinations(trees, 3) if not collinear(*t))

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('trees =', len(trees), 'triangles =', count)
print(hits[0])
