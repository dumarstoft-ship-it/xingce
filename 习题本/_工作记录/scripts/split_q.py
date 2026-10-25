# Split question papers into questions with section labels, using line-level JSON
import json, os, re, sys, glob
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
LD = S + '/lines'
head_re = re.compile(r'^\s*(?:第\s*[一二三四五六七八]\s*部\S?|[一二三四五六七八]\s*[\.、．:：])?\s*(政治理论|常识判断|言语理解|数量关系|判断推理|科学推理|资料分[析折])')
qre = re.compile(r'^\s*(\d{1,3})\s*(?:[\.、．,，](?!\d)|\s{2,}|(?=[一-龥（(“]))')
JUNKRE = re.compile(r'本试卷由粉笔用户|认准淘宝|通关达人|TB：|TB:|Seeyee|淘宝店铺|获取持续更新|微信|公众号|QQ群|免费获取|考公资料|hijoe')
SHARED = re.compile(r'^\s*[（(]\s*(?:材料|[一二三四五六七八])\s*[)）]\s*$|\d+\s*[~～\-－—至]\s*\d+\s*题基于|根据(?:以下|下列|下面|如下)?(?:材料|题干|信息|资料|文字)[，,]?\s*回答\s*\d+|^\s*回答\s*\d+\s*[~～\-－—至]\s*\d+\s*题')
SUBSEC = re.compile(r'^\s*(?:[一二三四五六七八]\s*[、\.．]|第[一二三四五六七八]节)?\s*(?:图形推理|定义判断|类比推理|逻辑判断|数学运算|数字推理)\s*[。．\.：:]?\s*(?:每道题|请|本部分|根据|给出|在这部分|$)|^\s*每道题(?:先)?给出|^\s*给出一个数列|^\s*在这部分试题中')
def is_heading(t):
    t2 = t.strip()
    m = head_re.match(t2)
    if not m: return None
    if re.match(r'^\s*(?:第\s*[一二三四五六七八]\s*部|[一二三四五六七八]\s*[\.、．:：])', t2): return m.group(1).replace('资料分折', '资料分析')
    # heading lines are short or contain 部分/本部分/题
    if len(t2) < 40 or re.search(r'部分|本部分|每道题|根据题目要求|共\s*\d+\s*题', t2):
        return m.group(1)
    return None
def load(name):
    return json.load(open(os.path.join(LD, name + '.json')))
def flat_lines(doc):
    out = []
    for pg in doc['pages']:
        H = pg['height']
        for L in pg['lines']:
            t = L['text']
            # drop headers/footers
            if L['top'] < 0.075 * H and ('网友回忆版' in t or '行测' in t or '试卷' in t or '公务员' in t): continue
            if L['top'] > 0.88 * H and (re.search(r'第\s*\d+\s*[页⻚]|^\s*[-—]?\s*\d+\s*[-—]?\s*$|粉笔|\d+\s*/\s*\d+|共\s*\d+\s*页', t)): continue
            if JUNKRE.search(t) or not t.strip(): continue
            out.append(dict(L, page=pg['page']))
    return out
def split(name, sections_wanted=('数量关系', '判断推理')):
    doc = load(name)
    lines = flat_lines(doc)
    # find headings
    heads = []
    for i, L in enumerate(lines):
        h = is_heading(L['text'])
        if h and (not heads or heads[-1][1] != h): heads.append((i, h))
    res = []
    for k, (i, sec) in enumerate(heads):
        if sec not in sections_wanted: continue
        j = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        qs = []
        pending = None; pend_left = 0
        for L in lines[i + 1:j]:
            if SHARED.search(L['text']):
                if qs: qs[-1]['closed'] = True
                pending = {'lines': [L]}; pend_left = 2
                mm = re.search(r'(\d+)\s*[~～\-－—至]\s*(\d+)', L['text'])
                if mm: pend_left = max(1, int(mm.group(2)) - int(mm.group(1)) + 1)
                continue
            if SUBSEC.search(L['text']):
                if qs: qs[-1]['closed'] = True
                pending = None
                continue
            m = qre.match(L['text'])
            n = int(m.group(1)) if m else None
            if n is None:
                mb = re.match(r'^\s*(\d{1,3})\s*$', L['text']) or re.match(r'^\s*(\d{1,3})\s*[\.、．,，]', L['text'])
                if mb and (not qs or int(mb.group(1)) == qs[-1]['num'] + 1):
                    n = int(mb.group(1))
            if n is not None and (not qs or (0 < n - qs[-1]['num'] <= 3)) and n < 200:
                q = {'num': n, 'lines': [L]}
                if pending is not None and pend_left > 0:
                    q['stem_lines'] = pending['lines']; pending['used'] = True; pend_left -= 1
                    if pend_left == 0: pending = None
                elif pending is not None:
                    pending = None
                qs.append(q)
            elif pending is not None and not pending.get('used'):
                pending['lines'].append(L)
            elif qs and not qs[-1].get('closed'):
                qs[-1]['lines'].append(L)
        for q in qs:
            q['section'] = sec
            q['text'] = '\n'.join(L['text'] for L in q['lines'])
            res.append(q)
    return res, heads, lines
if __name__ == '__main__':
    for f in sorted(glob.glob(LD + '/*.json')):
        name = os.path.basename(f)[:-5]
        if re.search(r'解析|答案|方案', name) and '重庆省考' not in name and '314' not in name: continue
        res, heads, lines = split(name)
        secs = {}
        for q in res: secs.setdefault(q['section'], []).append(q['num'])
        print(name[:42].ljust(42), {k: f"{v[0]}-{v[-1]}({len(v)})" for k, v in secs.items()}, [h for _, h in heads][:9])
