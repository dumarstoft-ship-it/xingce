import math
def finish_day(W, k, first_seg=None):
    # machines on day d: ceil(d/k) (days 1..k ->1, k+1..2k ->2 ...); first_seg shifts nodes
    cum, d = 0, 0
    while cum < W:
        d += 1
        if first_seg is None:
            m = (d - 1) // k + 1
        else:  # misaligned: first segment has first_seg days, then k days each
            m = 1 if d <= first_seg else (d - first_seg - 1) // k + 2
        cum += m
    return d
for k in (3, 4, 5, 6):
    for W in range(100, 401, 10):
        # full segments
        m = 0
        while k * (m + 1) * (m + 2) // 2 <= W: m += 1
        cum = k * m * (m + 1) // 2      # after m full segments (day k*m)
        R = W - cum
        if R == 0: continue
        corr = finish_day(W, k)
        whole = k * (m + 1)
        floor_ = k * m + R // (m + 1) if R % (m + 1) else None
        prev = k * m + math.ceil(R / m)
        mis = finish_day(W, k, first_seg=k - 1)
        stop = k * m
        if floor_ is None: continue
        opts = {corr, whole, floor_, stop}
        print(f"k={k} W={W} m={m} cum={cum} R={R} next={m+1}: correct={corr} whole={whole} floor={floor_} prev={prev} mis={mis} stop={stop}")
