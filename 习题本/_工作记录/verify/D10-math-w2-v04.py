# D10-math-w2-v04: six purchase points on a T-shaped road network.
#   main road: A - B - C - D with lengths 2, 4, 5 km;  branch from C: C - E - F with lengths 5, 3 km
#   goods (t): A 6, B 4, C 3, D 7, E 8, F 14;  transport only along these roads, 2 yuan per t per km
# Question: gather everything at one of the six points; the minimum freight (yuan).
# Method: all-pairs shortest road distances (Floyd-Warshall), total freight for every candidate point,
# take the minimum (check the best point is unique), then match the options.
from fractions import Fraction as Fr

NODES = 'ABCDEF'
ROADS = {('A', 'B'): 2, ('B', 'C'): 4, ('C', 'D'): 5, ('C', 'E'): 5, ('E', 'F'): 3}
GOODS = {'A': 6, 'B': 4, 'C': 3, 'D': 7, 'E': 8, 'F': 14}
PRICE = 2

INF = float('inf')
d = {(u, v): (0 if u == v else INF) for u in NODES for v in NODES}
for (u, v), l in ROADS.items():
    d[(u, v)] = d[(v, u)] = l
for k in NODES:
    for i in NODES:
        for j in NODES:
            if d[(i, k)] + d[(k, j)] < d[(i, j)]:
                d[(i, j)] = d[(i, k)] + d[(k, j)]

freight = {v: PRICE * sum(GOODS[u] * d[(u, v)] for u in NODES) for v in NODES}
best = min(freight.values())
best_pts = [v for v in NODES if freight[v] == best]
assert len(best_pts) == 1, best_pts

opts = {'A': 458, 'B': 478, 'C': 542, 'D': 654}
hit = [k for k, v in opts.items() if v == best]
assert len(hit) == 1, (best, hit)

# cross-check with the "lighter side crosses each road" formula (valid on a tree)
total = sum(GOODS.values())


def side(u, v):                        # goods on u's side when road u-v is cut
    seen, stack = {u}, [u]
    while stack:
        x = stack.pop()
        for (a, b) in ROADS:
            for p, q in ((a, b), (b, a)):
                if p == x and q not in seen and {p, q} != {u, v}:
                    seen.add(q)
                    stack.append(q)
    return sum(GOODS[x] for x in seen)


lighter = PRICE * sum(l * min(side(u, v), side(v, u)) for (u, v), l in ROADS.items())
assert lighter == best

# where the distractors come from (documentation only)
heaviest = max(GOODS, key=GOODS.get)                      # point with the most goods
junction = 'C'                                            # the fork in the road
assert best_pts[0] not in (heaviest, junction)
assert [freight[junction], freight[heaviest], freight['B']] == [opts['B'], opts['C'], opts['D']]

print({v: freight[v] for v in NODES}, 'best point', best_pts[0])
print(hit[0])
