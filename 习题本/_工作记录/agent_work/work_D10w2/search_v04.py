import itertools
# T network: A-B-C-D main road, C-E-F branch
nodes = 'ABCDEF'
edges_t = [('A','B'),('B','C'),('C','D'),('C','E'),('E','F')]

def dists(L):
    # L: dict edge->len ; compute all-pairs via Floyd
    INF = 10**9
    d = {(u,v): (0 if u==v else INF) for u in nodes for v in nodes}
    for (u,v),l in L.items():
        d[(u,v)] = d[(v,u)] = l
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if d[(i,k)] + d[(k,j)] < d[(i,j)]:
                    d[(i,j)] = d[(i,k)] + d[(k,j)]
    return d

res = []
for lens in itertools.product(range(2, 8), repeat=5):
    L = dict(zip(edges_t, lens))
    if len(set(lens)) < 4: continue
    d = dists(L)
    for gw in itertools.permutations(range(2, 16), 6):
        g = dict(zip(nodes, gw))
        W = sum(gw)
        if W % 2 == 0 and False: pass
        cost = {v: sum(g[u]*d[(u,v)] for u in nodes) for v in nodes}
        best = min(cost.values())
        bs = [v for v in nodes if cost[v] == best]
        if bs != ['E']: continue
        mx = max(gw)
        if g['F'] != mx: continue
        if sorted(gw)[-2] == mx: continue
        # C second best
        order = sorted(nodes, key=lambda v: cost[v])
        if order[1] != 'C': continue
        if len(set(cost.values())) < 6: continue
        # balance: {E,F} vs rest margin small (2)
        ef = g['E'] + g['F']
        if ef - (W - ef) != 2: continue
        res.append((lens, gw, cost, W))
        break
    if len(res) > 4000: break

print(len(res))
import random
random.seed(1)
for r in res[:40]:
    lens, gw, cost, W = r
    print(lens, gw, 'W', W, {k: cost[k] for k in 'ABCDEF'})
