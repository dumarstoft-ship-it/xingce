# D03-math-2-v10: 小周's intercity train (250 m long, 120 km/h); a 350 m high-speed train at 300 km/h overtakes it
# on the next track. Time from the HSR head to its tail passing 小周's window (window width ignored)?
# Method: positions in metres (ground frame), window = a point moving with 小周's train; solve exactly for the
# instants the HSR head and tail reach the window; cross-check with 0.01 s stepping.
from fractions import Fraction as F

v_c = F(120 * 1000, 3600)       # m/s
v_h = F(300 * 1000, 3600)
L_h, L_c = F(350), F(250)
OPTIONS = {'A': F(3), 'B': F(21, 5), 'C': F(7), 'D': F(12)}

x_win0 = F(1000)                 # window somewhere ahead of the HSR head at t = 0
head = lambda t: v_h * t
win = lambda t: x_win0 + v_c * t
t_head = x_win0 / (v_h - v_c)                    # head reaches window
t_tail = (x_win0 + L_h) / (v_h - v_c)            # tail (head - L_h) reaches window
dur = t_tail - t_head
assert head(t_head) == win(t_head) and head(t_tail) - L_h == win(t_tail)
# stepping check
dt, t, s = F(1, 100), F(0), None
while True:
    t += dt
    if s is None and head(t) >= win(t):
        s = t
    if head(t) - L_h >= win(t):
        break
assert abs((t - s) - dur) <= 2 * dt
hits = [k for k, v in OPTIONS.items() if v == dur]
assert len(hits) == 1, (dur, hits)
# distractors: speed sum; HSR speed only; both lengths (complete overtaking)
assert L_h / (v_h + v_c) == OPTIONS['A'] and L_h / v_h == OPTIONS['B'] and (L_h + L_c) / (v_h - v_c) == OPTIONS['D']
print('duration', dur, 's')
print(hits[0])
