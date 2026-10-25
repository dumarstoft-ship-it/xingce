# D03-math-2-v08: patrol boat going upstream drops a lifebuoy (it drifts with the current); noticed 15 min later,
# boat turns at once and chases downstream. Still-water speed 16 km/h, current 4 km/h. How far had the buoy
# drifted when caught?
# Method: bank frame (upstream = +), exact meeting time of two linear motions; cross-check with a fine time step.
from fractions import Fraction as F

V, W, T = F(16), F(4), F(15, 60)
OPTIONS = {'A': F(1), 'B': F(7, 4), 'C': F(9, 5), 'D': F(2)}

# phase 1 (0..T): boat +(V-W), buoy -W ; phase 2: boat -(V+W)
boat_T = (V - W) * T
buoy_T = -W * T
gap = boat_T - buoy_T
t_chase = gap / ((V + W) - W)          # closing speed in bank frame
t_total = T + t_chase
drift = W * t_total
# fine-step cross-check (1/3600 h = 1 s)
dt = F(1, 3600)
t, xb, xu = F(0), F(0), F(0)
while True:
    t += dt
    xb += ((V - W) if t <= T else -(V + W)) * dt
    xu += -W * dt
    if t > T and xb <= xu:
        break
assert t == t_total and xu == -drift
hits = [k for k, v in OPTIONS.items() if v == drift]
assert len(hits) == 1, (drift, hits)
# distractors: only the first 15 min; forgot the buoy's first drift (gap 3 km, closing 16);
# forgot the buoy moves during the chase (gap 4 km, closing 20)
assert W * T == OPTIONS['A']
assert W * (T + boat_T / V) == OPTIONS['B']
assert W * (T + gap / (V + W)) == OPTIONS['C']
print('chase time', t_chase * 60, 'min; drift', drift, 'km')
print(hits[0])
