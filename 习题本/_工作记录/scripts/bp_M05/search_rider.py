"""为 D32 骑手分段计酬巩固题找干净数据：a 为整数；超过基础量 k 的单每单 a+1.5；超过健康临界 h 的单每单 a-1。
第一日 n1 单（k<n1<=h），第二日 n2 单（n2>h）。要求：由 (n1,d1,n2,d2) 反推 (a,k,h) 唯一，且 a 在 6~9。"""
from collections import defaultdict
idx = defaultdict(set)
for a in range(3, 15):
    for k in range(1, 40):
        for h in range(k + 1, 60):
            for n1 in range(k + 1, h + 1):
                for n2 in range(h + 1, 61):
                    d1 = n1 * a + 1.5 * (n1 - k)
                    d2 = n2 * a + 1.5 * (h - k) - (n2 - h)
                    idx[(n1, d1, n2, d2)].add((a, k, h))
good = []
for (n1, d1, n2, d2), v in idx.items():
    if len(v) != 1: continue
    a, k, h = next(iter(v))
    if not (6 <= a <= 9 and 8 <= k <= 20 and 30 <= h <= 40 and n1 in (30, 32, 35) and n2 in (40, 42, 45, 48)): continue
    if d1 == int(d1): continue          # 第一日均价需非整数，才能用"居中"锁定 a
    avg = d1 / n1
    cand = [x for x in range(1, 20) if x < avg < x + 1.5]
    good.append((n1, d1, n2, d2, a, k, h, round(avg, 3), cand))
good.sort(key=lambda t: (len(t[8]), t[0], t[2]))
for g in [g for g in good if g[0] in (32, 35) and g[2] in (45, 48) and g[4] in (7, 8) and len(g[8]) == 1][:12]: print(g)
print(len(good))
