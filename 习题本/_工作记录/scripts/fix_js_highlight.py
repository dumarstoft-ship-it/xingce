"""2026JS papers mark the correct option with a gray highlight. Remove large mid-gray areas from those crops
(keeps dark text strokes), so the question page does not reveal the answer. Run after crop/mask steps."""
import glob, os, sys, shutil
import numpy as np
from PIL import Image, ImageFilter
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def clean(path):
    im = Image.open(path).convert('L'); a = np.asarray(im).astype(np.int16)
    mid = ((a >= 135) & (a <= 225)).astype(np.uint8) * 255
    # large mid-gray blobs = highlight background (text anti-aliasing is thin and gets removed by the opening)
    blob = Image.fromarray(mid).filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(23))
    b = np.asarray(blob) > 0
    if not b.any(): return False
    out = a.copy(); out[b & (a > 110)] = 255; out[b & (a <= 110)] = (a[b & (a <= 110)] * 0.55).astype(np.int16)
    Image.fromarray(out.astype(np.uint8)).save(path)
    return True

if __name__ == '__main__':
    n = 0
    for d in ('crops/real2', 'crops/real2_nonum'):
        for p in sorted(glob.glob(f'{S}/{d}/2026JS-*_q.png')):
            n += clean(p)
    print('cleaned', n)
