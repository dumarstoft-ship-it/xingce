"""把遮词句结果做成"考生卷"：原文里挖好空、列出选项，不给答案和说明。
用法：python3 -I make_solver_input.py <文章目录> <输出.md> <结果1.json> [结果2.json ...]
同时写出 <输出>.key.json（题号→答案），不要给作答的 agent 看。"""
import json, sys, os
src, out, files = sys.argv[1], sys.argv[2], sys.argv[3:]
L = 'ABCD'
lines, key = [], {}
for f in files:
    for art in json.load(open(f, encoding='utf-8'))['articles']:
        a = json.load(open(os.path.join(src, art['id'] + '.json'), encoding='utf-8'))
        paras = a['paras']
        qs = []
        for q in art['questions']:
            t = paras[q['p'] - 1]
            bl = []
            for b in q['blanks']:
                k = b.get('pre', '') + b['s']
                i = t.index(k) + len(b.get('pre', ''))
                bl.append((i, i + len(b['s'])))
            qs.append((q['p'], bl[0][0], q, bl))
        qs.sort(key=lambda x: (x[0], x[1]))
        marks = {}
        for n, (p, _, q, bl) in enumerate(qs, 1):
            for j, (b, e) in enumerate(bl):
                marks.setdefault(p, []).append((b, e, f"【{n}{'-'+str(j+1) if len(bl) > 1 else ''}＿＿】"))
        lines.append(f"## {art['id']}　{a['title']}（{a['src']} {a['col']} {a['date']}）\n")
        for pi, t in enumerate(paras, 1):
            for b, e, m in sorted(marks.get(pi, []), key=lambda x: -x[0]):
                t = t[:b] + m + t[e:]
            lines.append(f"[{pi}] {t}\n")
        lines.append("\n### 题目\n")
        for n, (p, _, q, bl) in enumerate(qs, 1):
            hint = f"，{len(bl)} 个空，依次填入" if len(bl) > 1 else ""
            lines.append(f"{n}.（{q['kind']}，第{p}段{hint}）")
            for i, o in enumerate(q['options']):
                lines.append(f"   {L[i]}. {o}")
            key[f"{art['id']}#{n}"] = q['answer']
            lines.append("")
        lines.append("\n---\n")
open(out, 'w', encoding='utf-8').write('\n'.join(lines))
json.dump(key, open(out + '.key.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(out, len(key), '题')
