# D07-math-2-v01: lamp at the top of a pole, 4.5 m above the ground; a 1.8 m tall person walks
# straight away from the pole, from 3 m to 9 m from its foot. How far does the tip of the shadow move?
# Solve geometrically: the tip is where the ray lamp -> head meets the ground.
from fractions import Fraction as F

H, h = F(45, 10), F(18, 10)      # lamp height, person height
d1, d2 = F(3), F(9)              # person's distance from the pole foot, before / after


def tip(d):
    # lamp L=(0,H), head P=(d,h); point L + t(P-L) has y = H + t(h-H) = 0
    t = H / (H - h)
    return t * d                 # x-coordinate of the shadow tip


move = tip(d2) - tip(d1)
growth = (tip(d2) - d2) - (tip(d1) - d1)     # change of the shadow length (a distractor)
opts = {'A': F(4), 'B': F(6), 'C': F(84, 10), 'D': F(10)}
hit = [k for k, v in opts.items() if v == move]
assert len(hit) == 1, (move, hit)
print('tip moves', move, '| shadow length grows by', growth)
print(hit[0])
