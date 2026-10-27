"""图推固定题型专项本: pick the candidate questions by their stem (规律 and 图形分类 questions are left out), crop question
and 解析 like the other real questions (number masked, display scale), and write tu/candidates.json for the type check."""
import json, os, re, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop import crop
import mask_qnum
from rescale_crops import rescale_one
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = S + '/crops/real2'
RULES = [('六面体/折纸盒', r'纸盒|折成|折叠|展开图|外表面|六面体|正方体.*(展开|折)|多面体'),
         ('三视图', r'视图|从.{0,6}(方向|上方|正面|侧面)看|俯视|主视|左视'),
         ('截面', r'截面|截得|截去|切面|剖面|剖开|切割|切开|横截'),
         ('立体拼合', r'(立体|方块|小正方体|多面体).{0,30}(拼|组合|组成)|拼合.{0,20}立体'),
         ('平面拼合', r'拼合|拼成|拼接|组成.{0,10}(图形|正方形|长方形)|分割|剪'),
         ('图形分类', r'分为两类|分成两类|分类'),
         ('规律', r'问号|规律性|规律')]

def guess(r):
    t = (r.get('text') or '') + (r.get('stem_text') or '')
    for name, p in RULES:
        if re.search(p, t): return name
    return '其他'

if __name__ == '__main__':
    raw = [r for r in json.load(open(S + '/db/real_raw.json')) if r.get('kind') == '图推']
    cands = [r for r in raw if guess(r) not in ('图形分类', '规律')]
    os.makedirs(S + '/tu', exist_ok=True)
    out = []
    for r in cands:
        i = r['id']; qp, jp = f'{OUT}/{i}_q.png', f'{OUT}/{i}_j.png'
        try:
            if r['regions'] and not os.path.exists(qp): crop(r['qfile'], r['regions'], qp)
            if r.get('jiexi_regions') and not os.path.exists(jp): crop(r['jfile'], r['jiexi_regions'], jp)
        except Exception as e:
            print('ERR', i, repr(e)[:100]); continue
        if os.path.exists(qp) and not os.path.exists(f'{OUT}_nonum/{i}_q.png'):
            if mask_qnum.mask(i, r.get('text'), shift=True) != 'ok':
                shutil.copy(qp, f'{OUT}_nonum/{i}_q.png'); shutil.copy(qp + '.json', f'{OUT}_nonum/{i}_q.png.json')
        for p in (qp, f'{OUT}_nonum/{i}_q.png', jp):
            if os.path.exists(p): rescale_one(p)
        q = f'{OUT}_nonum/{i}_q.png' if os.path.exists(f'{OUT}_nonum/{i}_q.png') else qp
        out.append({'id': i, 'paper': r['paper'], 'paper_name': r['paper_name'], 'num': r['num'], 'guess': guess(r),
                    'answer': r.get('answer_official'), 'text': (r.get('text') or '')[:200],
                    'q_img': q if os.path.exists(q) else None, 'j_img': jp if os.path.exists(jp) else None,
                    'jiexi_raw': (r.get('jiexi_raw') or '')[:600]})
    json.dump(out, open(S + '/tu/candidates.json', 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(out), Counter(c['guess'] for c in out), 'no q', sum(1 for c in out if not c['q_img']),
          'no j', sum(1 for c in out if not c['j_img']), 'no answer', sum(1 for c in out if not c['answer']))
