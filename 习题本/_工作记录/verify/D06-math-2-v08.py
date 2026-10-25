# D06-math-2-v08: prevalence 2%, sensitivity 95%, false-positive rate 5%;
# P(infected | positive), pick the closest option.
from fractions import Fraction as F

prev, sens, fpr = F(2, 100), F(95, 100), F(5, 100)
tp = prev * sens
fp = (1 - prev) * fpr
P = tp / (tp + fp)

opts = {'A': F(28, 100), 'B': F(39, 100), 'C': F(50, 100), 'D': F(95, 100)}
dist = sorted((abs(v - P), k) for k, v in opts.items())
# the closest option must be clearly closest
assert dist[1][0] - dist[0][0] > F(5, 100), dist
print('P =', float(P))
print(dist[0][1])
