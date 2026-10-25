"""Write per-module task inputs (real questions + days) for blueprint agents, and the master schedule."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schedule import build, math_schedule, spaced, LOGIC_DAYS, LOGIC_ORDER, ZH_DAYS, ZH_ORDER, MATH, LOGIC, ZH
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
CR = S + '/crops/real2'
NO_OFFICIAL = ('2026GK', '2026GD', '2026ZJA')  # papers with no official answers anywhere

def clean(t, n):
    t = re.sub(r'[ \t]+', ' ', t or '')
    t = re.sub(r'\n\s*\n+', '\n', t).strip()
    return t[:n]

def main():
    pools, skipped, dups = build()
    fix = json.load(open(S + '/db/answer_fixes.json')) if os.path.exists(S + '/db/answer_fixes.json') else {}
    for m in pools:
        for r in pools[m]:
            if not r['answer_official'] and r['id'] in fix: r['answer_official'] = fix[r['id']]['answer']
    md = math_schedule(); ld = spaced(LOGIC_DAYS, LOGIC_ORDER, 42); zd = spaced(ZH_DAYS, ZH_ORDER, 42)
    sched = [{'day': d + 1, 'math': md[d], 'logic': ld[d], 'zh': zd[d]} for d in range(42)]
    json.dump({'schedule': sched, 'names': {**MATH, **LOGIC, **{k: '综合推理·' + v for k, v in ZH.items()}}, 'dups': dups,
               'skipped': skipped}, open(S + '/db/schedule.json', 'w'), ensure_ascii=False, indent=1)
    os.makedirs(S + '/tasks_in', exist_ok=True)
    # merge all C modules into one 综合推理 task
    groups = {m: pools[m] for m in pools if m[0] in 'ML'}
    groups['C'] = [r for m in pools if m[0] == 'C' for r in pools[m]]
    for m, rs in groups.items():
        days = [s['day'] for s in sched if s['math'] == m or s['logic'] == m] if m != 'C' else \
               [{'day': s['day'], 'sub': s['zh']} for s in sched]
        items = []
        for r in sorted(rs, key=lambda r: (r['module'], r['difficulty'], r['paper'])):
            q = {'id': r['id'], 'paper': r['paper_name'], 'module': r['module'], 'difficulty': r['difficulty'], 'kaofa': r['kaofa'], 'technique': r['technique'],
                 'answer_official': r['answer_official'], 'needs_self_solve': (not r['answer_official']) and r['paper'] in NO_OFFICIAL,
                 'answer_pending_ocr': (not r['answer_official']) and r['paper'] not in NO_OFFICIAL,
                 'q_crop': f"{CR}/{r['id']}_q.png", 'j_crop': f"{CR}/{r['id']}_j.png" if os.path.exists(f"{CR}/{r['id']}_j.png") else None,
                 's_crop': f"{CR}/{r['id']}_s.png" if r.get('stem_text') else None,
                 'needs_figure': r.get('needs_figure'), 'note': r.get('cls_note'),
                 'text': clean(r['text'], 700), 'stem_text': clean(r.get('stem_text'), 500) or None, 'jiexi_excerpt': clean(r.get('jiexi_raw'), 260) or None}
            items.append(q)
        json.dump({'module': m, 'name': MATH.get(m) or LOGIC.get(m) or '综合推理', 'days': days, 'n_real': len(items), 'real': items},
                  open(f'{S}/tasks_in/{m}.json', 'w'), ensure_ascii=False, indent=1)
        print(m, len(items), days if m != 'C' else len(days))

if __name__ == '__main__':
    main()
