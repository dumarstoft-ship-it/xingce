"""Review crops of each teacher example (question + the teacher's worked solution, as on the page)."""
import json, os, subprocess
from PIL import Image
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SRC = '/home/user/xingce/忧郁牛牛丨26数量关系笔记（一期+二期）.pdf'
DPI = 150; PW, PH = 455.04, 587.52

def page_png(p):
    out = f'{S}/teacher/pages/p{p:03d}'
    if not os.path.exists(out + '.png'):
        os.makedirs(f'{S}/teacher/pages', exist_ok=True)
        subprocess.run(['pdftoppm', '-f', str(p), '-l', str(p), '-r', str(DPI), '-png', '-singlefile', SRC, out], check=True)
    return out + '.png'

def main():
    exs = json.load(open(S + '/teacher/examples.json'))
    for k, e in enumerate(exs):
        nxt = exs[k + 1] if k + 1 < len(exs) else None
        parts = []
        for j, p in enumerate(e['pages']):
            im = Image.open(page_png(p)); sc = im.height / PH
            top = e['top'] - 8 if j == 0 else 0
            end = PH
            if nxt and nxt['page'] == p: end = nxt['top'] - 4
            parts.append(im.crop((0, int(max(0, top) * sc), im.width, int(end * sc))))
        H = sum(x.height for x in parts); W = max(x.width for x in parts)
        c = Image.new('RGB', (W, H), 'white'); y = 0
        for x in parts: c.paste(x, (0, y)); y += x.height
        if c.height > 2400: c = c.crop((0, 0, W, 2400))
        out = f"{S}/teacher/crops/{e['tid']}.png"; c.save(out); e['review_crop'] = out
    json.dump(exs, open(S + '/teacher/examples.json', 'w'), ensure_ascii=False, indent=1)
    print('crops', len(exs))

if __name__ == '__main__':
    main()
