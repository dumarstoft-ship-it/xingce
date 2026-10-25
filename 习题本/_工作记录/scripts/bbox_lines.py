# Replace pdfplumber lines with pdftotext -bbox-layout lines for problem files (keeps images/vec)
import json, re, subprocess, sys, os, html as H
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SRC = '/home/user/xingce'
def convert(stem):
    out = subprocess.run(['pdftotext', '-bbox-layout', os.path.join(SRC, stem + '.pdf'), '-'], capture_output=True, text=True).stdout
    doc = json.load(open(f'{S}/lines/{stem}.json'))
    pages = out.split('<page ')[1:]
    for pi, pg in enumerate(pages):
        lines = []
        for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', pg, re.S):
            ws = re.findall(r'<word xMin="([\d.]+)" yMin="[\d.]+" xMax="([\d.]+)" yMax="[\d.]+">([^<]*)</word>', m.group(5))
            text = ''; x1 = None
            for a, b, w in ws:
                a = float(a); b = float(b)
                if x1 is not None and a - x1 > 3: text += ' ' * max(1, int((a - x1) / 6))
                text += H.unescape(w); x1 = b
            lines.append({'top': round(float(m.group(2)), 1), 'bottom': round(float(m.group(4)), 1), 'x0': round(float(m.group(1)), 1), 'x1': round(float(m.group(3)), 1), 'text': text})
        lines.sort(key=lambda L: (L['top'], L['x0']))
        if pi < len(doc['pages']): doc['pages'][pi]['lines'] = lines
    json.dump(doc, open(f'{S}/lines/{stem}.json', 'w'), ensure_ascii=False)
    print('converted', stem, sum(len(p['lines']) for p in doc['pages']))
if __name__ == '__main__':
    for st in sys.argv[1:]: convert(st)
