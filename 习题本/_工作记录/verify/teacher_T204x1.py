# T204x1（2012广州）M到N的线路图（边上数字为电量损耗），求M到N架设电缆的最低损耗。
# 结点按图中位置命名：上排 M,T1,T2,T3；中排 L,ML,C,MR,R；下排 BL,B2,B3,N。
import heapq

EDGES = [
    ('M', 'T1', 3), ('T1', 'T2', 5), ('T2', 'T3', 2),            # 上边
    ('M', 'L', 4), ('L', 'BL', 2),                               # 左斜边
    ('T3', 'R', 3), ('R', 'N', 6),                               # 右斜边
    ('BL', 'B2', 7), ('B2', 'B3', 9), ('B3', 'N', 4),            # 下边
    ('L', 'ML', 1), ('ML', 'C', 3), ('C', 'MR', 5), ('MR', 'R', 4),  # 中间横线
    ('T1', 'ML', 2), ('ML', 'BL', 4), ('T2', 'C', 3), ('C', 'B2', 5),
    ('T3', 'MR', 1), ('MR', 'B3', 3),                            # 竖线
    ('T1', 'C', 7), ('BL', 'C', 8), ('C', 'T3', 6), ('C', 'B3', 2),  # 斜线
]
OPTS = {'A': 14, 'B': 16, 'C': 17, 'D': 18}
adj = {}
for u, v, w in EDGES:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))
dist, pq = {'M': 0}, [(0, 'M')]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]:
        continue
    for v, w in adj[u]:
        if d + w < dist.get(v, float('inf')):
            dist[v] = d + w
            heapq.heappush(pq, (d + w, v))
ans = dist['N']
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('labels =', dict(sorted(dist.items(), key=lambda kv: kv[1])))
print(hits[0])
