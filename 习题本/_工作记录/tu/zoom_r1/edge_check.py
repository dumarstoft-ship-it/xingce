import json, sys
from PIL import Image
import numpy as np
d = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/tu/batch_r1.json'))
for x in d:
    for key in ('q_img', 'j_img'):
        p = x.get(key)
        if not p:
            continue
        a = np.array(Image.open(p).convert('L'))
        h, w = a.shape
        dark = a < 128
        rows = np.where(dark.any(axis=1))[0]
        cols = np.where(dark.any(axis=0))[0]
        # margin from ink to each edge
        top = rows.min(); bot = h - 1 - rows.max(); left = cols.min(); right = w - 1 - cols.max()
        flag = []
        if top <= 2: flag.append('TOP')
        if bot <= 2: flag.append('BOTTOM')
        if left <= 2: flag.append('LEFT')
        if right <= 2: flag.append('RIGHT')
        print(f"{x['id']:16s} {key} {w}x{h} margins t{top} b{bot} l{left} r{right} {' '.join(flag)}")
