import json, os, sys
import numpy as np
from PIL import Image
S = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(S, 'cls/new_batch.jsonl'))]
out = []
for r in rows:
    if not r['id'].startswith('2026JS'): continue
    g = np.asarray(Image.open(os.path.join(S, r['q_crop'])).convert('L'))
    mask = (g >= 140) & (g <= 200)
    rgb = np.stack([g, g, g], -1).copy()
    rgb[mask] = [255, 0, 0]
    # bounding info of dense gray regions: row/col profile
    ys, xs = np.nonzero(mask)
    print(r['id'], 'graypix', mask.sum(), 'bbox', (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else None)
    out.append(Image.fromarray(rgb.astype(np.uint8)))
    Image.fromarray(rgb.astype(np.uint8)).save(os.path.join(S, 'js_enh', r['id'] + '_mark.png'))
