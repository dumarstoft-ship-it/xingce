# T204（2018江苏B）6栋楼F、A、B、C、D、E间可铺管道的线路及长度（百米）如图，连通所有楼的管道最短多长（米）。
# 最小生成树：穷举所有5条边的组合，取能连通全部6个点的最小总长（不依赖贪心算法的正确性）。
from fractions import Fraction as F
from itertools import combinations

NODES = 'FABCDE'
EDGES = [('F', 'A', F(3)), ('A', 'B', F(10)), ('A', 'C', F(4)), ('B', 'C', F(8)), ('B', 'D', F(6)),
         ('C', 'D', F(5, 2)), ('F', 'C', F(13, 2)), ('F', 'E', F(15, 2)), ('C', 'E', F(3)), ('D', 'E', F(5))]
UNIT = 100
OPTS = {'A': 1800, 'B': 1850, 'C': 1950, 'D': 2000}


def connected(es):
    adj = {n: set() for n in NODES}
    for u, v, _ in es:
        adj[u].add(v)
        adj[v].add(u)
    seen, stack = {NODES[0]}, [NODES[0]]
    while stack:
        for w in adj[stack.pop()] - seen:
            seen.add(w)
            stack.append(w)
    return len(seen) == len(NODES)


best = min(sum(w for _, _, w in es) for k in range(len(NODES) - 1, len(EDGES) + 1)
           for es in combinations(EDGES, k) if connected(es))
length = best * UNIT
hits = [k for k, v in OPTS.items() if v == length]
assert len(hits) == 1, (length, hits)
print('min total =', float(best), 'hundred metres =', float(length), 'm')
print(hits[0])
