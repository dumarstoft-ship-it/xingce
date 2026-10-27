"""Text-level checks on rendered day PDFs: every typed 解析 / note reaches its end in the PDF (catches HTML swallowing
text), no production words leak, mock 资料 items are labelled 模考. Usage: final_check.py day..."""
import json, re, subprocess, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
LEAK = re.compile(r'排版|截图|数据包|请以本解析为准|重裁|db_match|\bT\d{3}\b|reserve|分类员|笔记例|待定|核对一致后采用|补充：补充|\$')

def tail(s, n=6):
    """the last n characters of plain text outside $...$ (what pdftotext can see)"""
    plain = re.sub(r'\$[^$]*\$', ' ', s or '')
    plain = re.sub(r'[\s，。、；：！？“”（）()]+', '', plain)
    return plain[-n:]

def main(days):
    bad = 0
    for d in days:
        D = json.load(open(f'{S}/out/final/D{d}.json'))
        txt = subprocess.run(['pdftotext', f'{S}/out/final/D{d}.pdf', '-'], capture_output=True, text=True).stdout
        flat = re.sub(r'[\s，。、；：！？“”（）()]+', '', txt)
        probs = []
        for m in LEAK.finditer(txt):
            probs.append('leak ' + repr(txt[max(0, m.start() - 15):m.end() + 15]))
        for pt in D['parts']:
            for it in pt['items']:
                k = it.get('id') or it.get('tid') or it.get('vid')
                for f in ('jiexi', 'jiexi_text', 'extra'):
                    t = tail(it.get(f))
                    if len(t) >= 4 and t not in flat:
                        probs.append(f'{pt["title"]} {k} {f} ending not found: {t}')
                if pt['title'] == '资料分析' and it.get('mock') and f'模考·{it["src_label"]}'.replace(' ', '')[:12] not in flat:
                    probs.append(f'{k} not labelled 模考')
        print(d, 'pages', subprocess.run(['pdfinfo', f'{S}/out/final/D{d}.pdf'], capture_output=True, text=True).stdout.split('Pages:')[1].split()[0],
              'problems', len(probs))
        for p in probs[:15]: print('   ', p)
        bad += len(probs)
    return bad

if __name__ == '__main__':
    sys.exit(1 if main([int(x) for x in sys.argv[1:]]) else 0)
