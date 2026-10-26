"""QA montage for one material: stem chunks + question crops, stacked with separators, downscaled."""
import sys, os, json
from PIL import Image, ImageDraw
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = S + '/crops/zl'
def montage(mat, recs, path, width=900):
    ims = []
    first = [r for r in recs if r['mat'] == mat and r['pos'] == 1][0]
    k = 1
    while os.path.exists(f"{OUT}/{first['id']}_p{k}.png"):
        ims.append(Image.open(f"{OUT}/{first['id']}_p{k}.png").convert('RGB')); k += 1
    for r in sorted([r for r in recs if r['mat'] == mat], key=lambda r: r['pos']):
        ims.append(Image.open(f"{OUT}/{r['id']}_q.png").convert('RGB'))
    W = max(i.width for i in ims)
    H = sum(i.height for i in ims) + 14 * len(ims)
    c = Image.new('RGB', (W, H), (255, 160, 160)); y = 0
    for i in ims:
        c.paste(i, (0, y)); y += i.height + 14
    sc = width / W
    c = c.resize((width, int(H * sc)))
    c.save(path)
    return path
if __name__ == '__main__':
    raw = json.load(open(S + '/db/zl_raw.json'))
    for m in sys.argv[1:]:
        print(montage(m, raw, f"{S}/zl/m_{m}.png"))
