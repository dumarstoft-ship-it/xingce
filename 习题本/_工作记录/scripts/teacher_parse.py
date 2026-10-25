"""Split the teacher's notes (忧郁牛牛 26 数量关系笔记) into examples: black text = question, colored text = the
teacher's solution, light-gray text = OCR of embedded pictures. Writes teacher/examples.json and per-example
page crops (for review only; the crops still contain the teacher's annotations)."""
import json, re, collections, os, sys
import pdfplumber
SRC = '/home/user/xingce/忧郁牛牛丨26数量关系笔记（一期+二期）.pdf'
OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/teacher'

def kind(col):
    try: c = tuple(round(float(x), 2) for x in col)
    except Exception: return 'other'
    if c in ((0.0, 0.0, 0.0), (0.0,)): return 'black'
    if len(c) == 3 and all(abs(x - 0.82) < 0.03 for x in c): return 'ocr'
    return 'color'

def page_lines(p):
    rows = collections.defaultdict(list)
    for ch in p.chars:
        rows[round(ch['top'] / 2.5)].append(ch)
    out = []
    for k in sorted(rows):
        cs = sorted(rows[k], key=lambda c: c['x0'])
        # split a row into runs by kind (question text and solution text can share a row)
        runs = []
        for c in cs:
            kd = kind(c.get('non_stroking_color'))
            if runs and runs[-1]['kind'] == kd and c['x0'] - runs[-1]['x1'] < 25:
                runs[-1]['text'] += c['text']; runs[-1]['x1'] = c['x1']; runs[-1]['bottom'] = max(runs[-1]['bottom'], c['bottom'])
            else:
                runs.append({'kind': kd, 'text': c['text'], 'x0': c['x0'], 'x1': c['x1'], 'top': c['top'], 'bottom': c['bottom']})
        out += [r for r in runs if r['text'].strip()]
    return out

def main():
    pdf = pdfplumber.open(SRC)
    exs = []; section = None; cur = None
    for pno, p in enumerate(pdf.pages, 1):
        for r in page_lines(p):
            t = r['text'].strip()
            m_sec = re.match(r'^第[一二三四五六七八九十]+节\s*(.*)', t)
            if m_sec and len(t) < 30:
                section = t; cur = None; continue
            if r['kind'] == 'black':
                m_ex = re.match(r'^例\s*(\d+)\s*[:：]?\s*(.*)', t)
                opt_like = re.match(r'^[A-D][\.．、\s]?\S', t)
                new_ex = bool(m_ex) or bool(re.match(r'^[（(]\s*\d{4}', t)) or cur is None or \
                    (cur['sol'] and r['x0'] < 45 and not opt_like)
                if new_ex:
                    cur = {'tid': f'T{len(exs) + 1:03d}', 'section': section, 'ex_no': int(m_ex.group(1)) if m_ex else None, 'page': pno,
                           'top': r['top'], 'pages': [pno], 'q': [m_ex.group(2) if m_ex else t], 'sol': [], 'ocr': [], 'bottom': r['bottom'], 'last_page': pno}
                    exs.append(cur); continue
            if cur is None: continue
            if pno != cur['last_page']:
                cur['pages'].append(pno); cur['last_page'] = pno
            if r['kind'] == 'black': cur['q'].append(t)
            elif r['kind'] == 'color': cur['sol'].append(t)
            else: cur['ocr'].append(t)
            cur['bottom'] = r['bottom']
    for e in exs:
        q = '\n'.join(e['q'])
        e['question'] = q
        m = re.search(r'[（(]\s*(\d{4}[^）)]{0,14})[）)]', q[:30])
        e['source'] = m.group(1) if m else None
        e['has_options'] = bool(re.search(r'A[\.．、\s]*\S+.*B[\.．、\s]*\S+.*C[\.．、\s]*\S+.*D', q.replace('\n', ' ')))
        e['solution'] = '\n'.join(e['sol'])
        del e['q'], e['sol']
    json.dump(exs, open(OUT + '/examples.json', 'w'), ensure_ascii=False, indent=1)
    by = collections.Counter(e['section'] for e in exs)
    print(len(exs)); [print(k, v) for k, v in by.items()]
    print('with source', sum(1 for e in exs if e['source']), 'with options', sum(1 for e in exs if e['has_options']))

if __name__ == '__main__':
    main()
