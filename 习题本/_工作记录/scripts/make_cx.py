"""复杂关系画表专练: 20 questions whose relations are easiest to untangle with a table (rows = objects or stages,
columns = quantities). Questions are the original crops (or the teacher-bank text), each followed by room to draw the
table; then an answer key; then a table-first 解析 per question. Content lives in cx_tables.json; every answer was
checked by program against the official one. Usage: make_cx.py <cx_tables.json> <out.pdf>"""
import glob, html, json, os, re, subprocess, sys
from PIL import Image
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
R = S + '/render'
DPI = 200

def esc(s):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(s))

def table(rows):
    head = ''.join(f'<th>{esc(c)}</th>' for c in rows[0])
    body = ''.join('<tr>' + ''.join(f'<{"th" if k == 0 else "td"}>{esc(c)}</{"th" if k == 0 else "td"}>' for k, c in enumerate(r)) + '</tr>'
                   for r in rows[1:])
    return f'<table class="t"><tr>{head}</tr>{body}</table>'

def crop(path):
    w, _ = Image.open(path).size
    sc = json.load(open(path + '.json')).get('scale', 1.0) if os.path.exists(path + '.json') else 1.0
    return f'<img class="q" src="file://{path}" style="width:{w / DPI * sc:.3f}in">'

def load():
    data = json.load(open(sys.argv[1]))
    raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    tb = {t['tid']: t for f in glob.glob(S + '/teacher/bank_B*.json') for t in json.load(open(f))}
    for it in data['items']:
        if 'tid' in it:
            t = tb[it['tid']]
            it['label'] = f'老师笔记精选 · {t["source"]}' if t.get('source') else '老师笔记精选'
            opts = ''.join(f'<span>{k}. {html.escape(v)}</span>' for k, v in t['options'].items())
            it['q'] = f'<div class="stem">{html.escape(t["stem"])}</div><div class="opts">{opts}</div>'
            assert t['answer'] == it['answer'], it['tid']
        else:
            r = raw[it['id']]
            it['label'] = f'真题 · {r["paper_name"]} 第{r["num"]}题'
            it['q'] = crop(f'{S}/crops/real2_nonum/{it["id"]}_q.png')
            assert r['answer_official'] == it['answer'], it['id']
    return data

def page(d):
    out = [f'<section class="cover"><h1>{d["title"]}</h1><div class="sub">共 {len(d["items"])} 题 · {esc(d["intro"])}</div>',
           '<div class="box"><div class="bt">画表三步</div><ol>' + ''.join(f'<li>{m}</li>' for m in d['method']) + '</ol></div>',
           f'<div class="box"><div class="bt">{esc(d["model"]["label"])}</div>{table(d["model"]["table"])}'
           + ''.join(f'<p>{esc(s)}</p>' for s in d['model']['steps']) + '</div></section>']
    out.append('<h2 class="sec">题目</h2>')
    for k, it in enumerate(d['items'], 1):
        out.append(f'<div class="qb"><div class="qn">{k}</div><div class="qc">{it["q"]}</div><div class="draw">画表</div></div>')
    out.append('<h2 class="sec brk">答案速查</h2><table class="key"><tr>'
               + ''.join(f'<th>{k}</th>' for k in range(1, 11)) + '</tr><tr>'
               + ''.join(f'<td>{it["answer"]}</td>' for it in d['items'][:10]) + '</tr><tr>'
               + ''.join(f'<th>{k}</th>' for k in range(11, 21)) + '</tr><tr>'
               + ''.join(f'<td>{it["answer"]}</td>' for it in d['items'][10:]) + '</tr></table>')
    out.append('<h2 class="sec">解析</h2>')
    for k, it in enumerate(d['items'], 1):
        out.append(f'<div class="ab"><div class="ah"><b>{k}. 答案 {it["answer"]}</b><span>［{esc(it["label"])}］</span></div>'
                   f'<div class="key-line">画表要点：{esc(it["key"])}</div>{table(it["table"])}'
                   + ''.join(f'<p>{esc(s)}</p>' for s in it['steps']) + '</div>')
    return ''.join(out)

CSS = """
@page { size: A4; margin: 14mm 14mm 14mm 14mm; }
body { font-family: 'Noto Sans SC', sans-serif; color: #111; margin: 0; font-size: 10.5pt; line-height: 1.6; }
h1 { font-size: 20pt; margin: 0 0 1.5mm 0; }
.sub { color: #444; margin-bottom: 4mm; }
.box { border: 1px solid #bbb; border-radius: 3px; padding: 2.5mm 4mm; margin-bottom: 4mm; break-inside: avoid; }
.bt { font-weight: 700; margin-bottom: 1.5mm; }
.box ol { margin: 0; padding-left: 5mm; }
.box li { margin: 0.8mm 0; }
.box p, .ab p { margin: 1.2mm 0; }
h2.sec { font-size: 14pt; border-bottom: 2px solid #333; padding-bottom: 1mm; margin: 0 0 3mm 0; }
.cover { break-after: page; }
.brk { break-before: page; }
.qb { display: grid; grid-template-columns: 8mm 1fr; column-gap: 2mm; break-inside: avoid; margin-bottom: 3mm; }
.qn { font-weight: 700; background: #333; color: #fff; border-radius: 2px; text-align: center; height: 6mm; line-height: 6mm; font-size: 10pt; }
.qc img.q { max-width: 100%; }
.stem { margin-bottom: 1.5mm; }
.opts { display: grid; grid-template-columns: repeat(4, 1fr); }
.draw { grid-column: 2; height: 58mm; border: 1px dashed #bbb; border-radius: 3px; margin-top: 2mm; color: #bbb; font-size: 9pt; padding: 1mm 2mm; }
table.key { border-collapse: collapse; margin-bottom: 6mm; }
table.key th, table.key td { border: 1px solid #aaa; width: 15mm; text-align: center; padding: 1mm 0; }
table.key th { background: #eee; font-weight: 600; }
.ab { break-inside: avoid; border-top: 1px solid #ddd; padding-top: 2mm; margin-bottom: 3mm; }
.ah { display: flex; gap: 3mm; align-items: baseline; }
.ah span { color: #666; font-size: 9.5pt; }
.key-line { color: #8a3b00; font-size: 10pt; margin: 1mm 0 1.5mm 0; }
table.t { border-collapse: collapse; margin: 1mm 0 1.5mm 0; font-size: 10pt; }
table.t th, table.t td { border: 1px solid #999; padding: 0.8mm 2.5mm; text-align: center; }
table.t tr:first-child th { background: #eee; }
table.t td b { color: #b00; }
table.t th:first-child { background: #f6f6f6; text-align: left; }
"""

if __name__ == '__main__':
    d = load()
    fonts = ''.join(f'<link rel="stylesheet" href="file://{R}/node_modules/@fontsource/noto-sans-sc/{w}.css">' for w in (400, 700))
    doc = (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{d["title"]}</title>{fonts}'
           f'<style>{CSS}</style></head><body>{page(d)}</body></html>')
    hp = S + '/cx/cx.html'
    open(hp, 'w').write(doc)
    subprocess.run(['node', R + '/print.js', hp, os.path.abspath(sys.argv[2])], check=True, cwd=R)
    print('ok', sys.argv[2], len(d['items']), '题')
