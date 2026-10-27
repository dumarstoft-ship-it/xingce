"""资料分析 print booklet: each set = 4 passages (20 questions, numbered 1–20), colour crops from the original papers,
no sources on the page. Usage: zl_render.py <sets.json> <first_day> <last_day> <out.pdf>"""
import json, os, sys, html, subprocess
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
R = S + '/render'
CR = S + '/crops/zl'
DPI = 200
CN = '一二三四五六七八九十'
CHECKLINE = os.environ.get('ZL_CHECKLINE', '')  # e.g. 读题圈：时间｜主体｜指标｜问法　选前：回看圈词、核单位
CSS = r"""
@page { size: A4; margin: 13mm 14mm 14mm 14mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Noto Serif SC', serif; font-size: 10.5pt; line-height: 1.55; color: #111; margin: 0; background: #fff; }
.sans, h1 { font-family: 'Noto Sans SC', sans-serif; }
.cover h1 { font-size: 22pt; margin: 0 0 2mm 0; }
.cover .sub { color: #555; font-size: 10pt; margin-bottom: 6mm; }
.cover table { width: 100%; border-collapse: collapse; font-size: 10pt; font-family: 'Noto Sans SC', sans-serif; }
.cover td, .cover th { border: 1px solid #999; padding: 1.8mm 2.5mm; text-align: center; }
.cover th { background: #eee; font-weight: 600; }
.cover .note { font-size: 9.5pt; color: #333; margin: 5mm 0; line-height: 1.7; }
.set { page-break-before: always; }
.set-h { font-family: 'Noto Sans SC', sans-serif; display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #111; padding-bottom: 1.2mm; margin-bottom: 1.5mm; }
.set-h .t { font-size: 15pt; font-weight: 700; }
.set-h .m { font-size: 9.5pt; color: #333; }
.rec { font-family: 'Noto Sans SC', sans-serif; font-size: 9pt; color: #333; text-align: right; margin-bottom: 3mm; }
.mat-h { font-family: 'Noto Sans SC', sans-serif; font-size: 10pt; font-weight: 600; margin: 3.5mm 0 1.5mm 0; break-after: avoid; }
img.chunk { display: block; break-inside: avoid; margin: 0 0 1.2mm 0; }
.q { display: flex; align-items: flex-start; gap: 1.6mm; margin: 1.6mm 0 2.2mm 0; break-inside: avoid; }
.q .no { flex: 0 0 auto; min-width: 6.2mm; text-align: center; font-family: 'Noto Sans SC', sans-serif; font-weight: 700; font-size: 9.5pt; border: 1.2px solid #111; border-radius: 2px; margin-top: 0.4mm; line-height: 1.35; }
.chk { font-family: 'Noto Sans SC', sans-serif; font-size: 9pt; color: #222; border: 1px dashed #888; padding: 0.8mm 2mm; margin: 0 0 2mm 0; }
.card { break-inside: avoid; margin: 0 0 2mm 0; font-family: 'Noto Sans SC', sans-serif; font-size: 9pt; }
.card table { border-collapse: collapse; }
.card td { border: 1px solid #888; width: 8.4mm; height: 6.5mm; text-align: center; }
.card tr.n td { height: 4.5mm; background: #f0f0f0; color: #444; font-size: 8pt; }
"""
def img(path, sc, cls):
    w, h = Image.open(path).size
    return f'<img class="{cls}" src="file://{path}" style="width:{w / DPI * sc:.3f}in">'

def chunk_img(path, sc):
    """a tall table or chart that fills little of the column (small print in the original) is trimmed and enlarged"""
    import numpy as np
    im = Image.open(path); w, h = im.size
    cols = np.flatnonzero((np.asarray(im.convert('L')) < 200).any(axis=0))
    if h > 400 and len(cols) and (cols[-1] - cols[0] + 1) < 0.55 * w:
        x0 = max(0, cols[0] - 10); x1 = min(w, cols[-1] + 11)
        f = min(1.35, 0.9 * w / (x1 - x0), 240 / (h / DPI * 25.4 * sc))
        if f > 1.05:
            t = path[:-4] + '_t.png'
            im.crop((x0, 0, x1, h)).save(t)
            return img(t, sc * f, 'chunk')
    return img(path, sc, 'chunk')

def chunks(first_id):
    from zl_crop import chunk_files
    return [f for f in chunk_files(first_id) if Image.open(f).size[1] >= 20]  # skip stray rule lines

def render(sets, raw, meta, title, out_html):
    by = {}
    for r in raw: by.setdefault(r['mat'], []).append(r)
    fonts = ''.join(f'<link rel="stylesheet" href="file://{R}/node_modules/@fontsource/{f}/{w}.css">' for f in ('noto-serif-sc', 'noto-sans-sc') for w in (400, 700))
    h = [f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{html.escape(title)}</title>{fonts}<style>{CSS}</style></head><body>']
    mats = [m for s in sets for m in s['mats']]; n_mock = sum(1 for m in mats if m.startswith('MK'))
    src_note = ('题目都选自历年真题中正确率低、计算量大的篇目，' if not n_mock else
                f'题目选自历年真题和 2027 国考模考大赛题本（本册 {len(mats)} 篇中模考 {n_mock} 篇）中难度大、计算量大的篇目，')
    rows = ''.join(f'<tr><td>第 {s["day"]} 天</td><td>第 {s["set"]} 套</td><td>{sum(len(by[m]) for m in s["mats"])}</td><td></td><td></td></tr>' for s in sets)
    h.append(f'<div class="cover"><h1>{html.escape(title)}</h1><div class="sub">广东省考 42 天专项训练 · 资料分析（每天两套）</div>'
             '<div class="note">每套 4 篇材料、20 道题，按考场节奏一口气做完，不跳题、不放弃，做完再对答案。'
             + src_note +
             '按篇挑选后重新组卷，题号是本册自己的编号。'
             + ('模考题没有官方答案，答案和解析由两人分别独立求解、核对一致后写成。' if n_mock else '') +
             '答案和解析在当天的电子版习题本里。图表保留了原卷颜色，彩印最清楚，黑白打印也能看。</div>'
             f'<table><tr><th>日期</th><th>套</th><th>题量</th><th>用时</th><th>正确数</th></tr>{rows}</table></div>')
    for s in sets:
        n = sum(len(by[m]) for m in s['mats'])
        cells = ''.join(f'<td>{i}</td>' for i in range(1, n + 1))
        h.append(f'<section class="set"><div class="set-h"><span class="t">第 {s["set"]} 套</span><span class="m">第 {s["day"]} 天 · {len(s["mats"])} 篇 {n} 题</span></div>'
                 '<div class="rec">开始 ______　结束 ______　用时 ______　正确 ______ / ' + str(n) + '</div>'
                 + (f'<div class="chk">{html.escape(CHECKLINE)}</div>' if CHECKLINE else '')
                 + f'<div class="card"><table><tr class="n">{cells}</tr><tr>' + '<td></td>' * n + '</tr></table></div>')
        q = 0
        for k, m in enumerate(s['mats']):
            rs = sorted(by[m], key=lambda r: r['pos'])
            sc = meta[rs[0]['paper']]['scale']
            h.append(f'<div class="mat-h">（{CN[k]}）根据以下资料，回答 {q + 1}～{q + len(rs)} 题。</div>')
            for c in chunks(rs[0]['id']):
                h.append(chunk_img(c, sc))
            for r in rs:
                q += 1
                h.append(f'<div class="q"><span class="no">{q}</span>{img(f"{CR}/{r["id"]}_q.png", sc, "qi")}</div>')
        h.append('</section>')
    h.append('</body></html>')
    open(out_html, 'w').write('\n'.join(h))

if __name__ == '__main__':
    sets_all = json.load(open(sys.argv[1])); d0, d1 = int(sys.argv[2]), int(sys.argv[3]); out = sys.argv[4]
    sets = [s for s in sets_all if d0 <= s['day'] <= d1]
    raw = json.load(open(S + '/db/zl_raw.json'))
    meta = {}
    for f in [S + '/db/zl_meta_all.json']:
        if os.path.exists(f): meta.update(json.load(open(f)))
    title = f'资料分析打印册 · 第 {d0}–{d1} 天'
    hp = out[:-4] + '.html'
    render(sets, raw, meta, title, hp)
    subprocess.run(['node', R + '/print.js', os.path.abspath(hp), os.path.abspath(out)], check=True, cwd=R)
    print('ok', out)
