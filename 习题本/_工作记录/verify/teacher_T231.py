# T231 10x10x24 长方体挖去两个圆锥（底面为上下底面内切圆，高为长方体高的一半）
import math
a, b, H = 10, 10, 24
r = a / 2
h = H / 2
remain = a * b * H - 2 * (1/3) * math.pi * r**2 * h
options = {"A": 2400 - 100*math.pi, "B": 2400 - 200*math.pi, "C": 2400 - 300*math.pi, "D": 2400 - 600*math.pi}
hits = [k for k, v in options.items() if abs(v - remain) < 1e-9]
assert len(hits) == 1, hits
print(hits[0])
