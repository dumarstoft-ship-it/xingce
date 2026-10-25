import json, os, sys
import numpy as np
from PIL import Image
S = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(S, 'cls/new_batch.jsonl'))]
def boxfilter(m, k):
    # integral image mean filter
    p = k // 2
    a = np.pad(m.astype(float), p, mode='constant')
    c = a.cumsum(0).cumsum(1)
    c = np.pad(c, ((1,0),(1,0)))
    H, W = m.shape
    s = c[k:k+H, k:k+W] - c[0:H, k:k+W] - c[k:k+H, 0:W] + c[0:H, 0:W]
    return s / (k*k)
def components(m):
    H, W = m.shape
    lab = np.zeros((H, W), int); n = 0; boxes = []
    for y in range(H):
        for x in range(W):
            if m[y, x] and not lab[y, x]:
                n += 1; st = [(y, x)]; lab[y, x] = n
                x0 = x1 = x; y0 = y1 = y; cnt = 0
                while st:
                    cy, cx = st.pop(); cnt += 1
                    x0 = min(x0, cx); x1 = max(x1, cx); y0 = min(y0, cy); y1 = max(y1, cy)
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n; st.append((ny, nx))
                boxes.append((cnt, x0, y0, x1, y1))
    return boxes
for r in rows:
    if not r['id'].startswith('2026JS'): continue
    g = np.asarray(Image.open(os.path.join(S, r['q_crop'])).convert('L'))
    gray = (g >= 120) & (g <= 205)
    nonwhite = g < 250
    d = boxfilter(gray, 9)
    dense = d > 0.45
    boxes = [b for b in components(dense) if b[0] > 150]
    boxes.sort(reverse=True)
    print(r['id'], g.shape, [(b[0], b[1], b[2], b[3], b[4]) for b in boxes[:5]])
    rgb = np.stack([g, g, g], -1).copy()
    rgb[dense] = [255, 0, 0]
    Image.fromarray(rgb.astype(np.uint8)).save(os.path.join(S, 'js_enh', r['id'] + '_dense.png'))
