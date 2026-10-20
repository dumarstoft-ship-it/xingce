"""检查遮词句结果能否在原文里定位。
用法：python3 -I check_masks.py <结果.json> <文章目录>
结果格式：{"articles":[{"id":..., "questions":[{"kind","p","blanks":[{"s","pre"}],"options":[4个],"answer":"A-D","note"}]}]}"""
import json, sys, os
res = json.load(open(sys.argv[1], encoding='utf-8'))
src = sys.argv[2]
bad = 0
for art in res.get('articles', []):
    path = os.path.join(src, art['id'] + '.json')
    if not os.path.exists(path):
        print('找不到文章', art['id']); bad += 1; continue
    paras = json.load(open(path, encoding='utf-8'))['paras']
    nq = nb = 0
    for qi, q in enumerate(art.get('questions', [])):
        tag = f"{art['id']} 第{qi+1}题"
        err = []
        if q.get('kind') not in ('选词填空', '语句填空'):
            err.append('kind 只能是 选词填空 或 语句填空')
        p = q.get('p')
        if not isinstance(p, int) or not 1 <= p <= len(paras):
            err.append(f'段号 p={p} 不在 1..{len(paras)}')
            print(tag, '；'.join(err)); bad += 1; continue
        text = paras[p - 1]
        spans = []
        for bi, b in enumerate(q.get('blanks', [])):
            s, pre = b.get('s', ''), b.get('pre', '')
            if not s:
                err.append(f'第{bi+1}空 s 为空'); continue
            key = pre + s
            n = text.count(key)
            if n != 1:
                err.append(f'第{bi+1}空 pre+s「{key}」在第{p}段出现 {n} 次（要恰好 1 次）'); continue
            i = text.index(key) + len(pre)
            if pre == '' and i != 0 and text.count(s) != 1:
                err.append(f'第{bi+1}空 pre 为空但「{s}」不在段首且不唯一')
            spans.append((i, i + len(s), s))
        if spans and [x[0] for x in spans] != sorted(x[0] for x in spans):
            err.append('blanks 要按在文中出现的先后排列')
        for (b1, e1, _), (b2, e2, _) in zip(sorted(spans), sorted(spans)[1:]):
            if b2 < e1:
                err.append('两个空重叠')
        opts = q.get('options', [])
        if len(opts) != 4 or len(set(opts)) != 4:
            err.append('options 要有 4 个互不相同的选项')
        ans = q.get('answer')
        if ans not in ('A', 'B', 'C', 'D'):
            err.append('answer 要是 A/B/C/D')
        elif len(opts) == 4 and spans and len(spans) == len(q.get('blanks', [])):
            right = opts['ABCD'.index(ans)]
            want = ' '.join(x[2] for x in spans)
            if right != want:
                err.append(f'正确项「{right}」和原文「{want}」不一致（多空用一个半角空格隔开）')
            parts = [o.split(' ') for o in opts]
            if q.get('kind') == '选词填空' and any(len(x) != len(spans) for x in parts):
                err.append('选词填空每个选项的词数要等于空数')
        if not q.get('note'):
            err.append('缺 note')
        if err:
            print(tag, '；'.join(err)); bad += 1
        nq += 1; nb += len(spans)
    print(f"{art['id']}：{nq} 题，{nb} 个空")
print('有问题的题：', bad)
sys.exit(1 if bad else 0)
