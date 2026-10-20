"""Extract 政治理论/常识/言语 sections from a 粉笔 PDF with blanks marked as ＿＿＿＿.
usage: python3 -I clean_paper.py <pdf> <out.txt>"""
import re, subprocess, sys
pdf, out = sys.argv[1], sys.argv[2]
raw = subprocess.run(['pdftotext', '-layout', '-enc', 'UTF-8', pdf, '-'], capture_output=True).stdout.decode('utf-8')
lines = []
for ln in raw.split('\n'):
    s = ln.rstrip()
    if not s.strip():
        continue
    if '本试卷由粉笔' in s or re.match(r'^\s*\d{4}年.*（.*网友回忆版）\s*$', s) or re.search(r'第 \d+ 页，共 \d+ 页', s):
        continue
    # option column separators: spaces followed by an option letter
    s = re.sub(r'\s{2,}(?=[A-D][\.．])', '\t', s)
    # blanks: long space runs inside text
    s = re.sub(r'(?<=\S) {4,}(?=\S)', '＿＿＿＿', s)
    s = re.sub(r'（\s*＿*\s*）', '（　）', s).replace('\t', '　　')
    lines.append(s.strip())
text = '\n'.join(lines)
# keep from start to just before 数量关系 section
m = re.search(r'\n[一二三四五六七]\.\s*数量关系', text)
if m:
    text = text[:m.start()]
open(out, 'w', encoding='utf-8').write(text + '\n')
print(out, len(text))
