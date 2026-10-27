"""Fit sector boundary directions for pie charts.
For each pie: sample along circles at many radii, find class transitions (K = dark
line/black fill vs others), convert transition points to x,y, and fit straight lines
through the transition points of each boundary. Report boundary angles clockwise from 12 o'clock.
"""
import sys
import math
import numpy as np
from PIL import Image

path = sys.argv[1]
boxes = eval(sys.argv[2])
im = np.array(Image.open(path).convert('L')).astype(float)


def sample(x, y):
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    dx, dy = x - x0, y - y0
    return (im[y0, x0] * (1 - dx) * (1 - dy) + im[y0, x0 + 1] * dx * (1 - dy)
            + im[y0 + 1, x0] * (1 - dx) * dy + im[y0 + 1, x0 + 1] * dx * dy)


def pt(cx, cy, r, th):
    return cx + r * math.sin(math.radians(th)), cy - r * math.cos(math.radians(th))


def dark_runs(cx, cy, r, step=0.02, thr=90):
    ths = np.arange(-20, 340, step)
    vals = np.array([sample(*pt(cx, cy, r, t)) for t in ths])
    d = vals < thr
    runs = []
    i = 0
    n = len(d)
    while i < n:
        if d[i]:
            j = i
            while j + 1 < n and d[j + 1]:
                j += 1
            runs.append((ths[i], ths[j]))
            i = j + 1
        else:
            i += 1
    return runs


def fit_dir(points, cx, cy):
    P = np.array(points)
    m = P.mean(axis=0)
    U, S, Vt = np.linalg.svd(P - m)
    d = Vt[0]
    # orient outward from center
    if np.dot(d, m - np.array([cx, cy])) < 0:
        d = -d
    ang = math.degrees(math.atan2(d[0], -d[1])) % 360
    # distance of line from center
    nrm = np.array([-d[1], d[0]])
    off = np.dot(np.array([cx, cy]) - m, nrm)
    return ang, off


for idx, (r0, r1, c0, c1) in enumerate(boxes):
    cx = (c0 + c1) / 2.0
    cy = (r0 + r1) / 2.0
    R = ((c1 - c0) + (r1 - r0)) / 4.0
    print('pie', 'ABCD'[idx], 'center', cx, cy, 'R', R)
    per_r = []
    for frac in np.arange(0.35, 0.86, 0.025):
        r = R * frac
        runs = dark_runs(cx, cy, r)
        per_r.append((r, runs))
    # print run structure at a middle radius
    r, runs = per_r[len(per_r) // 2]
    print('  runs at r=%.1f:' % r, ['(%.2f,%.2f)' % (a, b) for a, b in runs])
    # number of runs should be consistent; collect run endpoints across radii
    nr = [len(rr) for _, rr in per_r]
    print('  run counts', nr)
    common = max(set(nr), key=nr.count)
    sel = [(r, rr) for r, rr in per_r if len(rr) == common]
    for k in range(common):
        starts = [pt(cx, cy, r, rr[k][0]) for r, rr in sel]
        ends = [pt(cx, cy, r, rr[k][1]) for r, rr in sel]
        mids = [pt(cx, cy, r, (rr[k][0] + rr[k][1]) / 2) for r, rr in sel]
        a_s, o_s = fit_dir(starts, cx, cy)
        a_e, o_e = fit_dir(ends, cx, cy)
        a_m, o_m = fit_dir(mids, cx, cy)
        print('  run%d start-edge %.2f (off %.2f) end-edge %.2f (off %.2f) mid %.2f (off %.2f)' % (k, a_s, o_s, a_e, o_e, a_m, o_m))
