# 本批自检：字段长度、解析字数、题干结尾格式、题干禁用词、答案分布
import json, re, sys
from collections import Counter
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
V = json.load(open(S + '/gen/D07_math_1.json'))
R = json.load(open(S + '/gen/real_D07-math-1.json'))

def visible(t):
    t = re.sub(r'\\(frac|dfrac)\{([^{}]*)\}\{([^{}]*)\}', r'\2/\3', t)
    t = re.sub(r'\\sqrt\{([^{}]*)\}', r'√\1', t)
    t = re.sub(r'\\(triangle|times|div|pi|approx|le|ge)', 'x', t)
    t = re.sub(r'\\[a-zA-Z]+', '', t)
    return len(t.replace('$', '').replace('{', '').replace('}', '').replace('^', ''))

BAN = ['勾股', '射影', '外心', '内心', '相似', '赋值', '等积', '模型', '本题', '技巧', '公式', '改编', '真题', '直角']
probs = []
for v in V:
    vid = v['vid']
    if len(v['kaofa']) > 20: probs.append((vid, 'kaofa too long', len(v['kaofa'])))
    if len(v['technique']) > 12: probs.append((vid, 'technique too long', len(v['technique'])))
    n_raw, n_vis = len(v['jiexi']), visible(v['jiexi'])
    if n_vis > 250: probs.append((vid, 'jiexi visible length', n_vis))
    if '参考用时' in v['jiexi']: probs.append((vid, 'jiexi has 参考用时'))
    if not re.search(r'（ ）[^（）。]{0,6}。$', v['stem']) and not v['stem'].endswith('（$\\pi$ 取 3.14）'):
        probs.append((vid, 'stem ending', v['stem'][-20:]))
    for w in BAN:
        if (w in v['stem'] or any(w in o for o in v['options'].values())) and not (w == '直角' and vid == 'D07-math-1-v11'):
            probs.append((vid, 'banned word in stem/options', w))
    if f"选 {v['answer']}" not in v['jiexi']: probs.append((vid, 'jiexi does not state 选 ' + v['answer']))
    print(vid, v['answer'], 'jiexi raw/visible', n_raw, n_vis, '| kaofa', len(v['kaofa']), '| tech', len(v['technique']))
for r in R:
    print(r['id'], r['answer'], 'jiexi raw/visible', len(r['jiexi']), visible(r['jiexi']))
    if visible(r['jiexi']) > 250: probs.append((r['id'], 'jiexi visible length'))
print('answers', dict(sorted(Counter(v['answer'] for v in V).items())))
print('groups', dict(Counter(v['group'] for v in V)))
print('directions', dict(Counter((v['group'][:3], v['direction']) for v in V)))
for p in probs: print('PROBLEM', p)
print('lint problems', len(probs))
