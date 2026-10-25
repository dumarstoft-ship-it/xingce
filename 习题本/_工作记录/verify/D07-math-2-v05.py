# D07-math-2-v05: 46 straight 1-m fence pieces (no bending, no cutting, laid end to end without
# overlap; leftovers allowed). Two separate rectangles with equal perimeters, every side made of
# whole pieces, so all side lengths are positive integers. Maximise the total area (brute force).
N = 46
best = None
for l1 in range(1, N):
    for w1 in range(1, N):
        p = 2 * (l1 + w1)              # perimeter = pieces used by one rectangle
        if 2 * p > N:                  # both rectangles together must not exceed N pieces
            continue
        for l2 in range(1, N):
            w2 = p // 2 - l2
            if w2 < 1:
                continue
            tot = l1 * w1 + l2 * w2
            if best is None or tot > best[0]:
                best = (tot, (l1, w1), (l2, w2), p)
tot = best[0]
opts = {'A': 30, 'B': 60, 'C': 60.5, 'D': 72}
hit = [k for k, v in opts.items() if v == tot]
assert len(hit) == 1, (best, hit)
print('best (total, rect1, rect2, perimeter):', best)
print(hit[0])
