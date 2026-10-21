"""审阅用：每题打印所在段落（空处用【】标出原文）、选项（*为原文）、说明。
用法：python3 -I review.py <文章目录> <结果.json> [文章id]"""
import json, sys, os
src, f = sys.argv[1], sys.argv[2]
only = sys.argv[3] if len(sys.argv) > 3 else None
L = 'ABCD'
r = json.load(open(f, encoding='utf-8'))
for art in r['articles']:
    if only and art['id'] != only: continue
    a = json.load(open(os.path.join(src, art['id'] + '.json'), encoding='utf-8'))
    print('#' * 8, art['id'], a['title'], f"（{len(art['questions'])} 题）")
    qs = sorted(art['questions'], key=lambda q: (q['p'], a['paras'][q['p']-1].index(q['blanks'][0].get('pre','') + q['blanks'][0]['s'])))
    for n, q in enumerate(qs, 1):
        t = a['paras'][q['p'] - 1]
        spans = []
        for b in q['blanks']:
            i = t.index(b.get('pre', '') + b['s']) + len(b.get('pre', ''))
            spans.append((i, i + len(b['s'])))
        for b, e in sorted(spans, reverse=True):
            t = t[:b] + '【' + t[b:e] + '】' + t[e:]
        print(f"\n[{n}] {q['kind']} 第{q['p']}段：{t}")
        for i, o in enumerate(q['options']):
            print(f"    {'*' if L[i] == q['answer'] else ' '}{L[i]}. {o}")
        print('    说明：' + q['note'])
    if art.get('comments'): print('\n  【agent 对这篇的意见】' + art['comments'])
    print()
if r.get('comments'): print('【整体意见】' + r['comments'])
