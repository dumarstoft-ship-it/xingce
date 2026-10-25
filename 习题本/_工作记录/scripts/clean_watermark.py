"""Remove the light outline watermark ("…老师的资料铺子") from the 2022 浙江 A 解析 crops: that PDF prints crisp
black text, so anything lighter than mid-gray is watermark. (Scanned papers with gray text are left alone.)"""
import glob, os, shutil, sys
import numpy as np
from PIL import Image
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
PATTERNS = ['2022ZJA-101_j.png', '2022ZJA-103_j.png', '2022ZJA-105_j.png', '2022ZJA-107_j.png', '2022ZJA-109_j.png', '2022ZJA-110_j.png']  # plain-text 解析 only: formula images are light gray too

# crops whose 解析 has formula images: clean only a box in the margin that holds a watermark fragment (x0, y0, x1, y1 px)
BOXES = {'2022ZJA-69_j.png': [(1040, 945, 1177, 1095)]}

def main():
    n = 0
    for name, boxes in BOXES.items():
        p = f'{S}/crops/real2/{name}'
        if not os.path.exists(p): continue
        b = f'{S}/crops/wm_backup/{name}'
        if not os.path.exists(b): shutil.copy(p, b)
        a = np.asarray(Image.open(b).convert('L')).astype(int)
        for x0, y0, x1, y1 in boxes:
            sub = a[y0:y1, x0:x1]
            a[y0:y1, x0:x1] = np.where(sub >= 125, 255, sub)
        Image.fromarray(a.astype(np.uint8)).save(p)
        n += 1
    for pat in PATTERNS:
        for p in glob.glob(f'{S}/crops/real2/{pat}'):
            b = f'{S}/crops/wm_backup/{os.path.basename(p)}'
            if not os.path.exists(b): shutil.copy(p, b)
            a = np.asarray(Image.open(b).convert('L')).astype(int)
            Image.fromarray(np.where(a >= 125, 255, a).astype(np.uint8)).save(p)
            n += 1
    print('cleaned', n)

if __name__ == '__main__':
    main()
