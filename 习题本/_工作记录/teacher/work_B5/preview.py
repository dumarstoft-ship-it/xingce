# 生成含 KaTeX 的预览页，检查公式与图形显示
import json, html, re, sys
R = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/render'
bank = json.load(open(sys.argv[1]))
pick = set(sys.argv[3].split(','))


def rich(s):
    parts = re.split(r'(\$[^$]+\$)', s or '')
    return ''.join(p if p.startswith('$') and p.endswith('$') and len(p) > 2 else html.escape(p) for p in parts).replace('\n', '<br>')


h = [f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{R}/node_modules/katex/dist/katex.min.css">'
     f'<script src="file://{R}/node_modules/katex/dist/katex.min.js"></script><script src="file://{R}/node_modules/katex/dist/contrib/auto-render.min.js"></script>'
     '<style>body{width:1000px;font-family:"Noto Sans SC",sans-serif;font-size:14px;margin:12px} .q{border-bottom:1px solid #ccc;padding:8px 0} .fig svg{max-width:70%} .j{color:#444;font-size:13px}</style></head><body>']
for b in bank:
    if b['tid'] not in pick or not b['keep']:
        continue
    h.append(f'<div class="q"><b>{b["tid"]}</b> [{b["module"]}·{b["level"]}] {rich(b["stem"])}')
    if b['figure']:
        h.append(f'<div class="fig">{b["figure"]["svg"]}</div>')
    h.append('<div>' + '　'.join(f'{k}. {rich(v)}' for k, v in b['options'].items()) + f'　【{b["answer"]}】</div>')
    h.append(f'<div class="j">{rich(b["jiexi"])}</div><div class="j">学到：{rich(b["learn"])}</div></div>')
h.append('<script>renderMathInElement(document.body,{delimiters:[{left:"$",right:"$",display:false}]});</script></body></html>')
open(sys.argv[2], 'w').write(''.join(h))
