# Render this batch with the book's CSS/fonts/KaTeX into an HTML preview (my work dir only).
import json, sys, re
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
sys.path.insert(0, S + '/scripts')
import render_day as rd  # read-only use of its CSS and helpers

vs = json.load(open(S + '/gen/D07_math_2.json'))
real = json.load(open(S + '/gen/real_D07-math-2.json'))
R = rd.R
fonts = ''.join(f'<link rel="stylesheet" href="file://{R}/node_modules/@fontsource/{f}/{w}.css">'
                for f in ('noto-serif-sc', 'noto-sans-sc') for w in (400, 700))
katex = (f'<link rel="stylesheet" href="file://{R}/node_modules/katex/dist/katex.min.css">'
         f'<script src="file://{R}/node_modules/katex/dist/katex.min.js"></script>'
         f'<script src="file://{R}/node_modules/katex/dist/contrib/auto-render.min.js"></script>')
h = [f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">{fonts}{katex}<style>{rd.CSS} body{{width:182mm;margin:8mm}}</style></head><body>']
for i, v in enumerate(vs, 1):
    it = {'type': 'var', 'stem': v['stem'], 'options': v['options'], 'figure': v.get('figure_svg')}
    h.append(rd.render_q(i, it))
for i, v in enumerate(vs, 1):
    it = {'type': 'var', 'answer': v['answer'], 'kaofa': v['kaofa'], 'technique': v['technique'],
          'jiexi': v['jiexi'] + f"（参考用时 {v['time_s']} 秒）"}
    h.append(rd.render_ana(i, it))
h.append(rd.render_ana('真题', {'type': 'real', 'answer': real[0]['answer'], 'src_label': '2026广东 第41题（自解）',
                                'jiexi_text': real[0]['jiexi']}))
h.append('<script>document.addEventListener("DOMContentLoaded",function(){renderMathInElement(document.body,'
         '{delimiters:[{left:"$",right:"$",display:false}],throwOnError:false});});</script></body></html>')
open(S + '/work_D07m2/preview.html', 'w').write('\n'.join(h))
print('ok')
