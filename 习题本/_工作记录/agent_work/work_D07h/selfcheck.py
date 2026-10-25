import json, re
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
vs = json.load(open(S + '/gen/D07_math_h.json'))
hint = ['鸟头', '共角', '均值', '取等', '边界', '和定', '积定', '模型', '相似', '蝴蝶', '最近', '单调', '技巧', '改编', '真题', '考法']
keys = ["vid","group","seed","direction","kaofa","technique","difficulty","time_s","stem","options","answer","jiexi","figure_svg","verify"]
dec = json.load(open(S + '/harden/D07_decision.json'))
groups = [nv['group'] for nv in dec['new_variants']]
for v in vs:
    print(v['vid'], 'keys ok' if list(v.keys()) == keys else ('KEYS', list(v.keys())))
    print('  group in decision:', v['group'] in groups, '| jiexi len', len(v['jiexi']), '| kaofa', len(v['kaofa']), '| technique', len(v['technique']))
    txt = v['stem'] + ''.join(v['options'].values())
    print('  hint words in stem/options:', [h for h in hint if h in txt])
    print('  stem ending:', v['stem'][-12:], bool(re.search(r'（ ）[^（）]{1,6}。$', v['stem'])))
    print('  参考用时 in jiexi:', '参考用时' in v['jiexi'], '| answer letter in jiexi:', '选' + v['answer'] in v['jiexi'])
    print('  difficulty', v['difficulty'], 'time', v['time_s'], 'direction', v['direction'])
