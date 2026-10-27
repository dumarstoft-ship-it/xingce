"""Render one day's workbook (questions + answer key + 解析) to HTML, then PDF via Playwright."""
import json, os, re, sys, html, subprocess
from PIL import Image

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
R = S + '/render'
DPI = 200

CSS = r"""
@page { size: A4; margin: 14mm 14mm 14mm 14mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Noto Serif SC', serif; font-size: 10.5pt; line-height: 1.62; color: #111; margin: 0; background: #fff; }
h1, h2, h3, .sans { font-family: 'Noto Sans SC', sans-serif; }
.cover { border: 1.5px solid #222; border-radius: 6px; padding: 10mm 9mm; margin-bottom: 6mm; }
.cover h1 { font-size: 22pt; margin: 0 0 2mm 0; letter-spacing: 1px; }
.cover .sub { color: #555; font-size: 10pt; margin-bottom: 5mm; }
.cover table { width: 100%; border-collapse: collapse; font-size: 10.5pt; }
.cover td, .cover th { border: 1px solid #bbb; padding: 2.2mm 3mm; text-align: left; vertical-align: top; }
.cover th { background: #f1f1f1; font-family: 'Noto Sans SC', sans-serif; font-weight: 600; }
.cover .note { font-size: 9pt; color: #444; margin-top: 4mm; line-height: 1.55; }
.part { page-break-before: always; }
.part-h { font-family: 'Noto Sans SC', sans-serif; font-size: 14pt; font-weight: 700; border-bottom: 2px solid #222; padding-bottom: 1.5mm; margin: 0 0 4mm 0; display: flex; justify-content: space-between; align-items: baseline; }
.part-h .meta { font-size: 9.5pt; font-weight: 400; color: #444; }
.grp { font-family: 'Noto Sans SC', sans-serif; font-size: 9.5pt; color: #333; background: #f3f3f3; border-left: 3px solid #555; padding: 1mm 2.5mm; margin: 4mm 0 2.5mm 0; break-after: avoid; }
.q { margin: 0 0 4.2mm 0; break-inside: avoid; }
.q.shared { border-left: 2px solid #999; padding-left: 2mm; }
.mat-h { font-family: 'Noto Sans SC', sans-serif; font-size: 9.5pt; color: #333; margin-bottom: 1mm; }
.q .qh { font-family: 'Noto Sans SC', sans-serif; font-size: 9pt; margin-bottom: 0.8mm; display: flex; gap: 2mm; align-items: center; }
.q .no { display: inline-block; min-width: 7mm; padding: 0 1.4mm; background: #222; color: #fff; border-radius: 2px; text-align: center; font-weight: 700; font-size: 9.5pt; }
.tag { display: inline-block; padding: 0 1.5mm; border: 1px solid #888; border-radius: 2px; color: #333; font-size: 8.5pt; }
.tag.real { border-color: #1f5fa8; color: #1f5fa8; }
.tag.var { border-color: #8a5a00; color: #8a5a00; }
.q img.crop { display: block; max-width: 100%; }
.stem { white-space: normal; }
.stem p { margin: 0 0 0.8mm 0; }
.opts { display: grid; gap: 0.6mm 4mm; margin-top: 1mm; }
.opts.c4 { grid-template-columns: repeat(4, 1fr); }
.opts.c2 { grid-template-columns: repeat(2, 1fr); }
.opts.c1 { grid-template-columns: 1fr; }
.fig { margin: 1.5mm 0; }
.fig svg, .fig img { max-width: 70%; }
.keys { page-break-before: always; }
table.key { border-collapse: collapse; margin: 0 0 4mm 0; font-family: 'Noto Sans SC', sans-serif; font-size: 9pt; }
table.key td { border: 1px solid #aaa; width: 9.2mm; text-align: center; padding: 0.6mm 0; }
table.key tr.n td { background: #f1f1f1; color: #555; font-size: 8pt; }
.ana { margin: 0 0 4mm 0; break-inside: avoid-page; }
.ana .ah { font-family: 'Noto Sans SC', sans-serif; font-size: 9.5pt; font-weight: 600; margin-bottom: 0.8mm; break-after: avoid; }
.ana .ah .ans { color: #b00020; }
.ana .kf { font-weight: 400; color: #444; font-size: 8.8pt; }
.ana img.crop { display: block; max-width: 100%; }
.ana .txt { font-size: 10pt; }
.ana .txt p { margin: 0 0 0.8mm 0; }
.src-note { font-size: 8.5pt; color: #666; }
.intro { font-size: 9.5pt; line-height: 1.6; background: #f5f5f5; border-left: 3px solid #555; padding: 2mm 3mm; margin: 0 0 4.5mm 0; }
.intro p { margin: 0 0 1mm 0; }
"""

def esc(s):
    return html.escape(s or '', quote=False)

def rich(s):
    """Escape text but keep $...$ math for KaTeX; newlines -> paragraphs."""
    s = s or ''
    parts = re.split(r'(\$[^$]+\$)', s)
    math = lambda p: p.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')  # KaTeX reads the decoded text
    out = ''.join(math(p) if p.startswith('$') and p.endswith('$') and len(p) > 2 else esc(p) for p in parts)
    paras = [p for p in out.split('\n')]
    return ''.join(f'<p>{p}</p>' for p in paras if p.strip())

def img_tag(path, cls='crop', max_h=None):
    if not path or not os.path.exists(path):
        return '<div class="src-note">[图片缺失]</div>'
    w, h = Image.open(path).size
    sc = 1.0
    if os.path.exists(path + '.json'):
        sc = json.load(open(path + '.json')).get('scale', 1.0)
    if max_h and h / DPI * sc > max_h: sc = max_h * DPI / h  # a very long 解析 shrinks to one page, with its header
    return f'<img class="{cls}" src="file://{path}" style="width:{w / DPI * sc:.3f}in">'

def opt_cols(opts):
    m = max((len(re.sub(r'\$[^$]*\$', 'xx', v or '')) for v in opts.values()), default=0)
    return 'c4' if m <= 9 else ('c2' if m <= 22 else 'c1')

def zl_kind(items):
    m = sum(1 for it in items if it.get('mock'))
    return '真题' if not m else ('模考题' if m == len(items) else '真题和模考题')

def render_q(n, it):
    tag = ''
    if it['type'] == 'real' and not it.get('stem'):
        body = img_tag(it['q_img'])
    else:
        body = f'<div class="stem">{rich(it["stem"])}</div>'
        if it.get('figure'):
            body += f'<div class="fig">{it["figure"]}</div>'
        opts = {k: re.sub(r'(?<!d)\\frac', r'\\dfrac', str(v)) for k, v in it['options'].items()}
        body += f'<div class="opts {opt_cols(opts)}">' + ''.join(f'<div>{k}. {rich(v)[3:-4] if rich(v).startswith("<p>") else rich(v)}</div>' for k, v in opts.items()) + '</div>'
    return f'<div class="q"><div class="qh"><span class="no">{n}</span>{tag}</div>{body}</div>'

def render_ana(n, it):
    kf = ' ｜ '.join(x for x in [it.get('kaofa'), it.get('technique')] if x)
    src = f'{"模考" if it.get("mock") else "真题"} · {it["src_label"]}' if it['type'] == 'real' else (it['src_label'] if it['type'] == 'teacher' else '改编')
    head = f'<div class="ah">{n}. 答案 <span class="ans">{esc(it["answer"] or "?")}</span> <span class="kf">［{esc(src)}'
    if kf: head += f' ｜ {esc(kf)}'
    head += '］</span></div>'
    if it['type'] == 'real':
        if it.get('jiexi_imgs'):  # a 解析 too long for one page, cut at its page breaks
            body = ''.join(img_tag(p, max_h=9.9) for p in it['jiexi_imgs'])
        elif it.get('jiexi_img'):
            body = img_tag(it['jiexi_img'], max_h=9.9)
        elif it.get('jiexi_text'):
            body = f'<div class="txt">{rich(it["jiexi_text"])}</div>'
        else:
            body = '<div class="src-note">（解析待补）</div>'
        if it.get('extra'):
            body += f'<div class="txt">{rich(it["extra"])}</div>'
        if it.get('jiexi_pre'):  # the 解析's own text above its figure, when the scan of that text is unusable
            body = f'<div class="txt">{rich(it["jiexi_pre"])}</div>' + body
    else:
        body = f'<div class="txt">{rich(it["jiexi"])}</div>'
        if it.get('extra'): body += f'<div class="txt">{rich(it["extra"])}</div>'
    return f'<div class="ana">{head}{body}</div>'

def key_table(items, start=1):
    rows = []
    for i in range(0, len(items), 15):
        chunk = items[i:i + 15]
        rows.append('<tr class="n">' + ''.join(f'<td>{start + i + j}</td>' for j in range(len(chunk))) + '</tr>')
        rows.append('<tr>' + ''.join(f'<td>{esc(it["answer"] or "?")}</td>' for it in chunk) + '</tr>')
    return '<table class="key">' + ''.join(rows) + '</table>'

def render_day(day, out_html):
    fonts = ''.join(f'<link rel="stylesheet" href="file://{R}/node_modules/@fontsource/{f}/{w}.css">' for f in ('noto-serif-sc', 'noto-sans-sc') for w in (400, 700))
    katex = f'<link rel="stylesheet" href="file://{R}/node_modules/katex/dist/katex.min.css"><script src="file://{R}/node_modules/katex/dist/katex.min.js"></script><script src="file://{R}/node_modules/katex/dist/contrib/auto-render.min.js"></script>'
    h = [f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{esc(day.get("title") or "第" + str(day["day"]) + "天")}</title>{fonts}{katex}<style>{CSS}</style></head><body>']
    # cover
    def cnt(p):
        nr = sum(1 for i in p['items'] if i['type'] == 'real'); nt = sum(1 for i in p['items'] if i['type'] == 'teacher')
        nv = len(p['items']) - nr - nt
        return f'{len(p["items"])} 题（真题 {nr}' + (f'，老师精选 {nt}' if nt else '') + f'，改编 {nv}）'
    rows = ''.join(f'<tr><td>{esc(p["title"])}</td><td>{esc(p["module"])}</td><td>{p.get("count_text") or cnt(p) if not p.get("print_only") else str(len(p["items"])) + f" 题（{zl_kind(p['items'])}，题目在打印册）"}</td><td>{p.get("time_min", "")} 分钟</td></tr>' for p in day['parts'])
    cover_title = day.get('title') or f'第 {day["day"]} 天'
    h.append(f'<div class="cover"><h1>{esc(cover_title)}</h1><div class="sub">{esc(day.get("subtitle", "广东省考 42 天专项训练 · 数量关系 + 判断推理"))}</div>'
             f'<table><tr><th>部分</th><th>{esc(day.get("module_head", "今日模块"))}</th><th>题量</th><th>建议用时</th></tr>{rows}</table>'
             f'<div class="note">{esc(day.get("note", ""))}</div></div>')
    # parts
    for p in day['parts']:
        if p.get('print_only'):  # questions live in the printed booklet: this page only points to it
            continue
        h.append(f'<div class="part"><div class="part-h"><span>{esc(p["title"])} · {esc(p["module"])}</span><span class="meta">{len(p["items"])} 题 · 建议 {p.get("time_min", "")} 分钟</span></div>')
        cur_grp = None; last_stem = None
        for i, it in enumerate(p['items'], 1):
            st = it.get('stem_img'); sk = it.get('stem_key') or st
            if st and sk != last_stem and os.path.exists(st):
                k = i
                while k < len(p['items']) and (p['items'][k].get('stem_key') or p['items'][k].get('stem_img')) == sk: k += 1
                rng = f'第 {i}～{k} 题' if k > i else f'第 {i} 题'
                h.append(f'<div class="q shared"><div class="mat-h">根据以下材料，回答{rng}。</div>{img_tag(st)}</div>')
            last_stem = sk if st else None
            if it.get('shared_stem_text') and it.get('shared_stem_text') != (p['items'][i - 2].get('shared_stem_text') if i > 1 else None):
                h.append(f'<div class="q shared"><div class="stem">{rich(it["shared_stem_text"])}</div></div>')
            h.append(render_q(i, it))
        h.append('</div>')
    # answers
    h.append('<div class="keys"><div class="part-h"><span>答案速查</span><span class="meta">先对答案，再看解析</span></div>')
    for p in day['parts']:
        if p.get('print_only'):
            for sn in dict.fromkeys(it['set'] for it in p['items']):
                its = [it for it in p['items'] if it['set'] == sn]
                h.append(f'<h3 style="font-size:11pt;margin:2mm 0 1.5mm 0">{esc(p["title"])} · 打印册第 {sn} 套</h3>' + key_table(its))
            continue
        h.append(f'<h3 style="font-size:11pt;margin:2mm 0 1.5mm 0">{esc(p["title"])}</h3>' + key_table(p['items']))
    h.append('</div>')
    for p in day['parts']:
        h.append(f'<div class="part"><div class="part-h"><span>解析 · {esc(p["title"])}</span><span class="meta">{esc(p["module"])}</span></div>')
        if p.get('ana_intro'):  # a chapter's method summary, shown before its 解析 (the question pages stay bare)
            h.append(f'<div class="intro">{rich(p["ana_intro"])}</div>')
        cur_set = None
        for i, it in enumerate(p['items'], 1):
            if p.get('print_only') and it['set'] != cur_set:
                cur_set = it['set']
                h.append(f'<div class="grp">打印册第 {cur_set} 套</div>')
            h.append(render_ana(it['zl_no'] if p.get('print_only') else i, it))
        h.append('</div>')
    h.append('<script>document.addEventListener("DOMContentLoaded",function(){if(window.renderMathInElement)renderMathInElement(document.body,{delimiters:[{left:"$",right:"$",display:false}],throwOnError:false});});</script>')
    h.append('</body></html>')
    open(out_html, 'w').write('\n'.join(h))
    return out_html

def to_pdf(html_path, pdf_path):
    subprocess.run(['node', R + '/print.js', os.path.abspath(html_path), os.path.abspath(pdf_path)], check=True, cwd=R)
    return pdf_path

if __name__ == '__main__':
    day = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    hp = out[:-4] + '.html'
    render_day(day, hp)
    to_pdf(hp, out)
    print('ok', out)
