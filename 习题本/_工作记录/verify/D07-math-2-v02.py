# D07-math-2-v02: equilateral stage of side 4 m with one vertex pointing due north, tiled by
# equilateral tiles of side 0.5 m (no cutting, tile edges parallel to the stage edges).
# Count the tiles that have a vertex pointing due south, by enumerating the triangular lattice.
from fractions import Fraction as F
import math

side, tile = F(4), F(1, 2)
n = side / tile
assert n.denominator == 1
n = int(n)
s3 = math.sqrt(3) / 2


def pt(i, j):                     # lattice point -> Euclidean (x east, y north), unit = tile side
    return (i + 0.5 * j, s3 * j)


big = [pt(0, 0), pt(n, 0), pt(0, n)]          # apex pt(0, n) is the northernmost vertex
assert max(big, key=lambda p: p[1]) == pt(0, n)


def inside(p, tri=big, eps=1e-9):
    (x1, y1), (x2, y2), (x3, y3) = tri

    def cr(ax, ay, bx, by, cx, cy):
        return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    d1 = cr(x1, y1, x2, y2, *p)
    d2 = cr(x2, y2, x3, y3, *p)
    d3 = cr(x3, y3, x1, y1, *p)
    return (d1 >= -eps and d2 >= -eps and d3 >= -eps) or (d1 <= eps and d2 <= eps and d3 <= eps)


north = south = 0
for i in range(-2, n + 3):
    for j in range(-2, n + 3):
        for tri in ([pt(i, j), pt(i + 1, j), pt(i, j + 1)],            # one orientation
                    [pt(i + 1, j), pt(i, j + 1), pt(i + 1, j + 1)]):    # the other one
            if all(inside(p) for p in tri):
                ys = sorted(p[1] for p in tri)
                if ys[2] - ys[1] > 1e-9:      # a single top vertex -> points north
                    north += 1
                elif ys[1] - ys[0] > 1e-9:    # a single bottom vertex -> points south
                    south += 1
total = north + south
assert total == (side / tile) ** 2            # area ratio = (side ratio)^2
opts = {'A': 28, 'B': 32, 'C': 36, 'D': 64}
hit = [k for k, v in opts.items() if v == south]
assert len(hit) == 1, (south, hit)
print('total', total, 'north-pointing', north, 'south-pointing', south)
print(hit[0])
