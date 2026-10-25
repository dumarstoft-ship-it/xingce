import json, os, sys
import numpy as np
from PIL import Image
S = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(S, 'cls/new_batch.jsonl'))]
for r in rows:
    if not r['id'].startswith('2026JS'): continue
    im = np.asarray(Image.open(os.path.join(S, r['q_crop'])).convert('L')).astype(float)
    # histogram of light pixels
    h = np.histogram(im, bins=[0,100,150,200,220,230,240,245,250,253,256])[0]
    print(r['id'], im.shape, h.tolist())
    # stretch: 200..255 -> 0..255 to reveal faint gray
    e = np.clip((im - 215) / (255 - 215) * 255, 0, 255).astype(np.uint8)
    Image.fromarray(e).save(os.path.join(S, 'js_enh', r['id'] + '.png'))
