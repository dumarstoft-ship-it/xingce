import json, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/scripts')
from render_day import render_day, to_pdf
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
vs = json.load(open(S + '/gen/D06_math_2.json'))
items = [{'type': 'variant', 'vid': v['vid'], 'group': v['group'], 'stem': v['stem'], 'options': v['options'], 'answer': v['answer'],
          'jiexi': v['jiexi'] + f"（参考用时 {v['time_s']} 秒）", 'kaofa': v['kaofa'], 'technique': v['technique'],
          'figure': v.get('figure_svg'), 'shared_stem_text': None} for v in vs]
r = json.load(open(S + '/gen/real_D06-math-2.json'))[0]
items.insert(3, {'type': 'real', 'id': r['id'], 'src_label': '2026广东 第40题（答案自解）', 'q_img': S + '/crops/real2/2026GD-40_q.png',
                 'answer': r['answer'], 'kaofa': None, 'technique': None, 'jiexi_text': r['jiexi'], 'extra': None, 'group': ''})
day = {'day': 6, 'subtitle': 'preview D06 math 2', 'note': '', 'parts': [{'title': '数学运算', 'module': 'M07 概率问题', 'time_min': 90, 'items': items}]}
hp = S + '/work_D06m2/preview.html'
render_day(day, hp)
to_pdf(hp, S + '/work_D06m2/preview.pdf')
print('ok')
