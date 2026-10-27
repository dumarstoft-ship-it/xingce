"""图推专项本: the crop repairs found by the check (tu/check_*.json) and by tu_pagegap.py, in one re-runnable place.
- REGIONS: new question / 解析 regions (through fix_crops, so they are recorded in db/overrides.json)
- Q_FROM_J: 2023 江苏 prints its 图推 questions as phone photos; its 解析 PDF reprints each question as a clean
  redrawing, and the answer and 解析 belong to that redrawing (87's photo even differs from it), so the question is
  cropped from the 解析 PDF
- SPLIT: a 解析 too long for one page, cropped page by page (rendered one after another)
- LABELS: option panels printed without letters get an A–D row under them; BOTTOM_RULE / RIGHT_RULE: stray rules
- BLUE: 解析 with yellow strokes, cropped from the darkest colour channel
- TEXT: 解析 whose scanned text is unusable (lost glyphs, "SEP" boxes): the crop keeps the figure, the text comes
  from the PDF text layer; notes where the original 解析 itself lacks a figure or a 解析
Writes the per-question decisions into tu/fixes.json (merged). Usage: tu_jfix.py"""
import json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop import crop
import mask_qnum
from rescale_crops import rescale_one
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
CR = S + '/crops/real2'

REGIONS = {
    # a figure at the top of the next page was skipped (tu_pagegap.py)
    '2020JSA-87': {'jiexi_regions': {'15': [749.9, 764.3], '16': [25.1, 294.4]}},
    '2021JSA-84': {'jiexi_regions': {'19': [563.4, 727.3], '20': [25.1, 140.1]}},
    '2021JSA-87': {'jiexi_regions': {'20': [710.0, 775.7], '21': [25.1, 324.4]}},
    '2021JSA-89': {'jiexi_regions': {'21': [682.9, 748.5], '22': [25.1, 504.4]}},
    '2019JSA-84': {'regions': {'8': [746.3, 760.7], '9': [25.1, 104.9]}},
    # the next question's figure placed before its number: give it to the right question
    '2017ZJA-55': {'jiexi_regions': {'9': [364.3, 609.3]}},
    '2017ZJA-56': {'jiexi_regions': {'9': [609.3, 743.8], '10': [46.1, 88.4]}},
    '2018GK-81': {'jiexi_regions': {'15': [594.5, 806.4], '16': [31.9, 45.2]}},
    '2018GK-82': {'jiexi_regions': {'16': [45.3, 275.7]}},
    # cut short / running into the next item
    '2022SC1-61': {'jiexi_regions': {'22': [662.0, 741.3], '23': [55.8, 251.0]}},
    '2015JSA-60': {'jiexi_regions': {'14': [63.5, 486.0]}},  # drop the 拓展 note: its 图1、图2 are not in the PDF
    '2024ZJA-79': {'jiexi_regions': {'25': [141.7, 576.0]}},
    '2022GK-80': {'jiexi_regions': {'24': [602.3, 653.5], '25': [34.0, 333.5]}},
    '2022JSA-84': {'jiexi_regions': {'25': [410.7, 609.5]}},
    '2017JSA-85': {'regions': {'10': [561.5, 684.0]}},
    # figures right of the text column were cut at the text's right edge
    '2021SD-48': {'jiexi_regions': {'13': [746.5, 811.7], '14': [26.8, 404.0]}, 'j_full_width': True},
    '2021SD-49': {'jiexi_regions': {'14': [402.5, 611.0]}, 'j_full_width': True},
    '2021GK-82': {'jiexi_regions': {'21': [129.0, 369.7]}, 'j_full_width': True},
    # figure only; the text is typeset from the text layer (TEXT)
    '2016GK-78': {'jiexi_regions': {'12': [110.9, 219.5]}},
    '2018ZJA-4': {'jiexi_regions': {'1': [192.5, 353.8]}},
    '2018ZJA-5': {'jiexi_regions': {'1': [489.5, 585.2]}},
    '2018ZJA-7': {'jiexi_regions': {'2': [51.5, 200.0]}},
    # 2023 江苏: the 解析 starts at 【答案】 (the reprinted question becomes the question crop, Q_FROM_J)
    '2023JSA-85': {'jiexi_regions': {'45': [687.5, 720.8], '46': [71.8, 255.4]}},
    '2023JSA-86': {'jiexi_regions': {'46': [574.5, 761.1], '47': [74.5, 446.5]}},
    '2023JSA-87': {'jiexi_regions': {'47': [590.0, 628.3], '48': [73.5, 372.4]}},
    '2023JSA-88': {'jiexi_regions': {'48': [516.0, 748.1], '49': [74.5, 154.0]}},
    '2023JSA-90': {'jiexi_regions': {'50': [231.5, 559.5]}},  # stops before 三、逻辑判断
}
Q_FROM_J = {'2023JSA-85': {'45': [429.4, 687.5]}, '2023JSA-86': {'46': [253.9, 574.5]}, '2023JSA-87': {'47': [445.0, 590.0]},
            '2023JSA-88': {'48': [370.9, 516.0]}, '2023JSA-90': {'49': [690.7, 731.8], '50': [74.2, 231.5]}}
SPLIT = {'2021JSA-90': [{'22': [502.9, 713.8]}, {'23': [25.1, 784.1]}, {'24': [25.1, 324.5]}]}
LABELS = {'2022JSA-84': 'right'}  # the four answer panels are the right-hand frame
BOTTOM_RULE = ['2017JSA-85']  # a rule inside the scanned figure, under the option letters
RIGHT_RULE = ['2017JSA-88']  # a thin scan edge right of the frame

def paras(t):
    """the 解析 text layer as paragraphs: drop U+2028, rejoin wrapped lines, new paragraph at A项/故正确答案/因此"""
    out = []
    for ln in t.replace(' ', '\n').split('\n'):
        ln = ln.strip()
        if not ln: continue
        if out and not re.match(r'[A-D]\s*项|故正确答案|因此', ln): out[-1] += ln
        else: out.append(ln)
    return out

def text_fixes(raw):
    p = {i: paras(raw[i]['jiexi_raw'] or '') for i in ('2016GK-78', '2018ZJA-4', '2018ZJA-5', '2018ZJA-7')}
    strip_no = lambda s: re.sub(r'^\d+、', '', s)
    return {
        '2016GK-78': {'extra': '\n'.join(p['2016GK-78'][1:])},  # the crop keeps the first line and the figure
        '2018ZJA-4': {'jiexi_pre': strip_no(p['2018ZJA-4'][0]), 'extra': '\n'.join(p['2018ZJA-4'][1:])},
        '2018ZJA-5': {'jiexi_pre': strip_no(p['2018ZJA-5'][0]), 'extra': '\n'.join(p['2018ZJA-5'][1:])},
        '2018ZJA-7': {'jiexi_pre': strip_no(p['2018ZJA-7'][0]), 'extra': '\n'.join(p['2018ZJA-7'][1:])},
        '2021SC0327-62': {'j_ok': True, 'extra': '（原卷解析此处缺少拼合后的示意图。）'},
        '2016JSA-88': {'extra': '（原卷解析此处缺图。）'},
        '2026CQ-74': {'j_ok': False, 'jiexi_text': '（原卷只给答案，没有解析。）'},
    }

def add_labels(path, side):
    """write A B C D under the four panels of the left/right frame; the frame's vertical lines are the columns whose
    longest dark run spans (nearly) the whole frame height, unlike the grid lines inside the figures"""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    js = json.load(open(path + '.json')) if os.path.exists(path + '.json') else {}
    if js.get('labels_added'): return False
    im = Image.open(path).convert('L'); a = np.asarray(im) < 128; H, W = a.shape
    def run(x):
        best = cur = 0
        for v in a[:, x]:
            cur = cur + 1 if v else 0; best = max(best, cur)
        return best
    runs = [run(x) for x in range(W)]; full = max(runs)
    xs = [x for x in range(W) if runs[x] >= 0.9 * full]
    groups = []  # adjacent line columns -> one vertical line each
    for x in xs:
        if groups and x - groups[-1][-1] <= 3: groups[-1].append(x)
        else: groups.append([x])
    lines = [sum(g) / len(g) for g in groups]
    frame = lines[-5:] if side == 'right' else lines[:5]
    assert len(lines) >= 5, lines
    x0 = int(frame[0]); bottom = max(y for y in range(H) if a[y, x0])
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 34)
    out = Image.new('L', (W, bottom + 60), 255); out.paste(im.crop((0, 0, W, min(H, bottom + 4))), (0, 0))
    d = ImageDraw.Draw(out)
    for k, ch in enumerate('ABCD'):
        cx = (frame[k] + frame[k + 1]) / 2; w = d.textlength(ch, font=font)
        d.text((cx - w / 2, bottom + 12), ch, fill=0, font=font)
    out.save(path); js['labels_added'] = True; json.dump(js, open(path + '.json', 'w'))
    print('  frame lines', [round(x) for x in frame])
    return True

def strip_bottom_rule(path, rows=16, ink=200):
    """remove a thin rule printed across the foot of a figure (below its last row of content)"""
    import numpy as np
    from PIL import Image
    im = Image.open(path); a = np.asarray(im.convert('L')) < ink; H, W = a.shape
    dark = a.sum(axis=1)
    for y in range(H - 1, max(0, H - rows), -1):
        if dark[y] > 0.6 * W:  # a rule: find its band and the blank gap above it
            y0 = y
            while y0 > 0 and dark[y0 - 1] > 0.6 * W: y0 -= 1
            if y - y0 <= 4 and dark[max(0, y0 - 4):y0].sum() == 0:
                im.crop((0, 0, W, y0 - 2)).save(path); return True
    return False

def strip_right_rule(path, cols=60, ink=200):
    """remove a thin vertical line printed just right of a figure's frame (a scan edge)"""
    import numpy as np
    from PIL import Image
    js = json.load(open(path + '.json')) if os.path.exists(path + '.json') else {}
    if js.get('right_rule_removed'): return False  # once only: the frame's own edge must not go next time
    im = Image.open(path); a = np.asarray(im.convert('L')) < ink; H, W = a.shape
    dark = a.sum(axis=0); xs = [x for x in range(W) if dark[x] > 0]
    if not xs: return False
    x1 = xs[-1]; x0 = x1
    while x0 > 0 and dark[x0 - 1] > 0: x0 -= 1
    if x1 - x0 <= 4 and W - x1 <= cols and dark[max(0, x0 - 5):x0].sum() == 0 and dark[x0:x1 + 1].max() > 0.3 * H:
        im.crop((0, 0, x0 - 2, H)).save(path)
        js['right_rule_removed'] = True; json.dump(js, open(path + '.json', 'w')); return True
    return False

BLUE = ['2024SC-59']  # yellow strokes in the 解析 figure vanish in grey: crop from the darkest colour channel instead

def crop_blue(stem, regions, out):
    """crop() on a page rendered in colour and reduced to its darkest channel (yellow, blue and black all come out dark)"""
    import subprocess, crop as C
    from PIL import Image
    orig = C.page_png
    def blue_png(st, page, dpi=200):
        W = C.page_lines(st, page)['width']
        if W > 700: dpi = max(60, int(dpi * 595 / W))
        base = os.path.join(C.CACHE, f'{st}__p{page}_{dpi}_rgb')
        if not os.path.exists(base + '_blue.png'):
            subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', str(dpi), '-png', '-singlefile',
                            os.path.join(C.SRC, st + '.pdf'), base], check=True)
            from PIL import ImageChops
            r, g, b = Image.open(base + '.png').convert('RGB').split()
            ImageChops.darker(ImageChops.darker(r, g), b).save(base + '_blue.png')  # darkest channel: any colour shows
        return base + '_blue.png'
    C.page_png = blue_png
    try: C.crop(stem, regions, out)
    finally: C.page_png = orig

def main():
    import fix_crops
    raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    fix_crops.main(REGIONS)
    for qid, regs in Q_FROM_J.items():
        out = f'{CR}/{qid}_q.png'
        crop(raw[qid]['jfile'], regs, out)
        if mask_qnum.mask(qid, raw[qid].get('text'), shift=True) != 'ok':
            shutil.copy(out, f'{CR}_nonum/{qid}_q.png'); shutil.copy(out + '.json', f'{CR}_nonum/{qid}_q.png.json')
        for p in (out, f'{CR}_nonum/{qid}_q.png'): rescale_one(p)
        print(qid, 'q from 解析 PDF')
    for qid in BLUE:
        crop_blue(raw[qid]['jfile'], raw[qid]['jiexi_regions'], f'{CR}/{qid}_j.png'); rescale_one(f'{CR}/{qid}_j.png')
        print(qid, 'j from the darkest colour channel')
    fixes = json.load(open(S + '/tu/fixes.json'))
    for qid, parts in SPLIT.items():
        paths = []
        for k, regs in enumerate(parts):
            p = f'{CR}/{qid}_p{k}_j.png'; crop(raw[qid]['jfile'], regs, p); rescale_one(p); paths.append(p)
        fixes.setdefault(qid, {}).update({'j_parts': paths, 'j_ok': True})
        print(qid, 'split', len(paths))
    for qid, side in LABELS.items():
        print(qid, 'labels', add_labels(f'{CR}_nonum/{qid}_q.png', side))
    for qid in BOTTOM_RULE:
        print(qid, 'bottom rule removed', strip_bottom_rule(f'{CR}_nonum/{qid}_q.png'))
    for qid in RIGHT_RULE:
        print(qid, 'right rule removed', strip_right_rule(f'{CR}_nonum/{qid}_q.png'))
    for qid in list(LABELS) + BOTTOM_RULE + RIGHT_RULE:
        fixes.setdefault(qid, {})['q_ok'] = True
    for qid in BLUE + ['2025SC-60']:  # 2025SC-60: a 3px sliver of text above its figure, inside the original image
        fixes.setdefault(qid, {})['j_ok'] = True
    for qid, f in text_fixes(raw).items():
        fixes.setdefault(qid, {}).update(f)
    for qid in list(REGIONS) + list(Q_FROM_J) + list(SPLIT):  # repaired: the check's verdict on the old crop no longer holds
        fixes.setdefault(qid, {}).update({'q_ok': True} if 'regions' in REGIONS.get(qid, {}) or qid in Q_FROM_J else {})
        if 'jiexi_regions' in REGIONS.get(qid, {}) and 'j_ok' not in text_fixes(raw).get(qid, {}): fixes[qid]['j_ok'] = True
    json.dump(fixes, open(S + '/tu/fixes.json', 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
