# 用书稿渲染器的 render_q / render_ana 生成本批预览页（只读导入，不改动 scripts/）
import json, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
sys.path.insert(0, S + '/scripts')
import render_day as rd
V = json.load(open(S + '/gen/D07_math_1.json'))
items = [{'type': 'var', 'stem': v['stem'], 'options': v['options'], 'answer': v['answer'], 'jiexi': v['jiexi'],
          'kaofa': v['kaofa'], 'technique': v['technique'], 'figure': v.get('figure_svg')} for v in V]
fonts = ''.join(f'<link rel="stylesheet" href="file://{rd.R}/node_modules/@fontsource/{f}/{w}.css">' for f in ('noto-serif-sc', 'noto-sans-sc') for w in (400, 700))
katex = f'<link rel="stylesheet" href="file://{rd.R}/node_modules/katex/dist/katex.min.css"><script src="file://{rd.R}/node_modules/katex/dist/katex.min.js"></script><script src="file://{rd.R}/node_modules/katex/dist/contrib/auto-render.min.js"></script>'
h = [f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">{fonts}{katex}<style>{rd.CSS} body{{width:182mm;margin:8mm}}</style></head><body>']
for i, it in enumerate(items, 1):
    h.append(rd.render_q(i, it))
h.append('<hr>')
for i, it in enumerate(items, 1):
    h.append(rd.render_ana(i, it))
h.append('<script>document.addEventListener("DOMContentLoaded",function(){if(window.renderMathInElement)renderMathInElement(document.body,{delimiters:[{left:"$",right:"$",display:false}],throwOnError:false});});</script></body></html>')
open('preview.html', 'w').write('\n'.join(h))
print('ok')
