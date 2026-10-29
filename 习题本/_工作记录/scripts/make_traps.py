"""易错陷阱记录: the traps the user fell into while working through the days, one card per question (how it went
wrong, the right working, which wrong option each slip leads to, and the habit that guards against it), with an index
on top. Entries live in traps.json and are appended as new traps come up. Usage: make_traps.py <traps.json> <out.pdf>"""
import html, json, os, re, subprocess, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
R = S + '/render'
NOWRAP = re.compile(r'\d+(?: : \d+)+|min\([^)]*\)')  # ratios and min(...) stay on one line

def esc(s):
    return NOWRAP.sub(lambda m: f'<span class="nw">{m.group(0)}</span>', html.escape(s))

def card(k, e):
    rows = [('题目', esc(e['q'])), ('我怎么错的', esc(e['wrong']))]
    if e['points']:
        rows.append(('坑在哪', '<ol>' + ''.join(f'<li>{esc(p)}</li>' for p in e['points']) + '</ol>'))
    rows.append(('正确做法', esc(e['right'])))
    if e['options']:
        rows.append(('选项对照', ''.join(f'<span class="opt"><b>{esc(o)}</b>{esc(how)}</span>' for o, how in e['options'])))
    rows.append(('以后怎么防', '<ul>' + ''.join(f'<li>{esc(g)}</li>' for g in e['guard']) + '</ul>'))
    body = ''.join(f'<tr><th>{t}</th><td>{c}</td></tr>' for t, c in rows)
    return (f'<section class="card"><div class="head"><span class="no">{k}</span><span class="where">{esc(e["where"])}</span>'
            f'<span class="kind">{esc(e["kind"])}</span><span class="src">{esc(e["src"])}</span></div>'
            f'<div class="trap">{esc(e["trap"])}</div><table>{body}</table></section>')

def page(data):
    es = data['entries']
    index = ''.join(f'<li><b>{esc(e["trap"])}</b><span>{esc(e["where"])}</span></li>' for e in es)
    return (f'<h1>易错陷阱记录</h1><div class="sub">{esc(data["note"])}</div>'
            f'<ol class="index">{index}</ol>' + ''.join(card(k, e) for k, e in enumerate(es, 1)))

CSS = """
@page { size: A4; margin: 14mm 14mm 12mm 14mm; }
body { font-family: 'Noto Sans SC', sans-serif; color: #111; margin: 0; font-size: 10.5pt; line-height: 1.6; }
h1 { font-size: 18pt; margin: 0 0 1.5mm 0; }
.sub { color: #555; font-size: 9.5pt; margin-bottom: 3mm; }
ol.index { margin: 0 0 5mm 0; padding: 2.5mm 4mm 2.5mm 9mm; background: #f5f5f5; border-radius: 2px; }
ol.index li { margin: 0.6mm 0; }
ol.index li span { color: #666; margin-left: 3mm; font-size: 9.5pt; }
.card { border: 1px solid #bbb; border-radius: 3px; margin: 0 0 5mm 0; break-inside: avoid; }
.head { display: flex; align-items: baseline; gap: 3mm; background: #eee; padding: 1.5mm 3mm; border-bottom: 1px solid #ccc; }
.head .no { font-weight: 700; background: #333; color: #fff; border-radius: 2px; padding: 0 1.8mm; font-size: 9.5pt; }
.head .where { font-weight: 700; }
.head .kind { color: #333; }
.head .src { color: #777; font-size: 9pt; margin-left: auto; }
.trap { padding: 1.8mm 3mm 0 3mm; font-weight: 700; color: #b00; }
table { border-collapse: collapse; width: 100%; margin: 0.5mm 0 1.5mm 0; }
th { width: 21mm; text-align: left; vertical-align: top; color: #555; font-weight: 600; padding: 1.2mm 0 1.2mm 3mm; font-size: 9.5pt; white-space: nowrap; }
td { padding: 1.2mm 3mm 1.2mm 2mm; vertical-align: top; }
ol, ul { margin: 0; padding-left: 5mm; }
li { margin: 0.4mm 0; }
.opt { display: inline-block; margin-right: 6mm; }
.opt b { margin-right: 2mm; }
.nw { white-space: nowrap; }
"""

if __name__ == '__main__':
    src, out_pdf = sys.argv[1], sys.argv[2]
    data = json.load(open(src))
    fonts = ''.join(f'<link rel="stylesheet" href="file://{R}/node_modules/@fontsource/noto-sans-sc/{w}.css">' for w in (400, 700))
    doc = (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>易错陷阱记录</title>{fonts}'
           f'<style>{CSS}</style></head><body>{page(data)}</body></html>')
    hp = S + '/traps.html'
    open(hp, 'w').write(doc)
    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)), exist_ok=True)
    subprocess.run(['node', R + '/print.js', hp, os.path.abspath(out_pdf)], check=True, cwd=R)
    print('ok', out_pdf, len(data['entries']), '条')
