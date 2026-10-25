# T263 两人离地 1 米、相距 2 米，分身经地面反弹一次到达对方，最短路程（数值最小化反弹点）
import math
h, d = 1.0, 2.0
best = min(math.hypot(x, h) + math.hypot(d - x, h) for x in [i * d / 200000 for i in range(200001)])
options = {"A": 2*math.sqrt(2), "B": math.sqrt(3), "C": math.sqrt(2), "D": 2*math.sqrt(3)}
hits = [k for k, v in options.items() if abs(v - best) < 1e-6]
assert len(hits) == 1, (best, hits)
print(hits[0])
