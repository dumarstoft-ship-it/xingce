# T204x2 由两个正三角形拼成的菱形ABCD周长800米，道路为四条边、对角线AC、BD以及DE⊥AB、BF⊥CD（如图）。
# 从任一点出发走完每一段道路，最少行进多少米。
# 做法：按坐标求出所有交点、把道路切成段，统计各点度数；奇点两两之间用最短路配对（留2个奇点作起终点）。
import math
from itertools import combinations

S = 800 / 4                                      # 边长
h = S * math.sqrt(3) / 2                         # 正三角形的高
P = {'A': (-h, 0.0), 'B': (0.0, S / 2), 'C': (h, 0.0), 'D': (0.0, -S / 2)}


def foot(p, a, b):                               # p 到直线ab的垂足
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    return (ax + t * dx, ay + t * dy)


P['E'] = foot(P['D'], P['A'], P['B'])
P['F'] = foot(P['B'], P['C'], P['D'])
ROADS = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('A', 'C'), ('B', 'D'), ('D', 'E'), ('B', 'F')]


def inter(s1, s2):
    (x1, y1), (x2, y2) = P[s1[0]], P[s1[1]]
    (x3, y3), (x4, y4) = P[s2[0]], P[s2[1]]
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-12:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / den
    if -1e-9 <= t <= 1 + 1e-9 and -1e-9 <= u <= 1 + 1e-9:
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None


def key(pt):
    for name, q in P.items():
        if math.dist(pt, q) < 1e-6:
            return name
    name = 'X%d' % len(P)
    P[name] = pt
    return name


pts_on = {r: {r[0], r[1]} for r in ROADS}
for r1, r2 in combinations(ROADS, 2):
    q = inter(r1, r2)
    if q is not None:
        k = key(q)
        pts_on[r1].add(k)
        pts_on[r2].add(k)
edges = []
for r, names in pts_on.items():
    a = P[r[0]]
    seq = sorted(names, key=lambda n: math.dist(a, P[n]))
    edges += [(seq[i], seq[i + 1], math.dist(P[seq[i]], P[seq[i + 1]])) for i in range(len(seq) - 1)]
total = sum(w for _, _, w in edges)
deg = {}
for u, v, _ in edges:
    deg[u] = deg.get(u, 0) + 1
    deg[v] = deg.get(v, 0) + 1
odd = sorted(n for n, d in deg.items() if d % 2)
# Floyd 求各点间沿道路的最短距离
nodes = sorted(deg)
D = {(i, j): (0 if i == j else math.inf) for i in nodes for j in nodes}
for u, v, w in edges:
    D[u, v] = D[v, u] = min(D[u, v], w)
for k in nodes:
    for i in nodes:
        for j in nodes:
            if D[i, k] + D[k, j] < D[i, j]:
                D[i, j] = D[i, k] + D[k, j]


def best_pairing(vs):
    if not vs:
        return 0.0
    a, rest = vs[0], vs[1:]
    return min(D[a, b] + best_pairing([x for x in rest if x != b]) for b in rest)


extra = min(best_pairing([v for v in odd if v not in ends]) for ends in combinations(odd, 2)) if len(odd) > 2 else 0.0
best = total + extra
r3 = math.sqrt(3)
OPTS = {'A': 1000 + 400 * r3, 'B': 1100 + 400 * r3, 'C': 1100 + 500 * r3, 'D': 1000 + 600 * r3}
hits = [k for k, v in OPTS.items() if abs(v - best) < 1e-6]
assert len(hits) == 1, (best, hits)
print('odd vertices =', odd, 'road total =', round(total, 3), 'extra =', round(extra, 3), 'answer =', round(best, 3))
print(hits[0])
