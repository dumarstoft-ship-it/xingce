# D07-math-2-v03: 4G radius 1.2 km; 5G radius 400 m; one 5G station costs 1/6 of one 4G station.
# Stations needed = city area / single-station coverage area (pi r^2).
# By what percent is the total 5G cost higher than the total 4G cost?
import math

city = 100.0                       # km^2, arbitrary (it cancels)
r4, r5 = 1.2, 0.4                  # km
c4 = 1.0
c5 = c4 / 6
n4 = city / (math.pi * r4 ** 2)
n5 = city / (math.pi * r5 ** 2)
ratio = (n5 * c5) / (n4 * c4)
pct = (ratio - 1) * 100
opts = {'A': 50, 'B': 150, 'C': 350, 'D': 800}
hit = [k for k, v in opts.items() if abs(v - pct) < 1e-6]
assert len(hit) == 1, (pct, hit)
print('5G/4G total cost ratio', round(ratio, 9), '-> higher by %', round(pct, 6))
print(hit[0])
