"""合订本: merge the finished workbook PDFs into a few volumes with two-level bookmarks (one per day / booklet, then
one per section, set or chapter, found from each page's first line). Usage: make_volumes.py <out_dir>"""
import os, re, subprocess, sys
from pypdf import PdfReader, PdfWriter
B = '/home/user/xingce/习题本'
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SECTION = re.compile(r'^((数字推理|数学运算|逻辑判断|综合推理) · .+|答案速查|解析 · .+|第 ?\d+ 章 · .+)$')
SET = re.compile(r'^第\s*(\d+)\s*套$')

def first_lines(path, n=2):
    """the first n non-empty lines of every page"""
    txt = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout
    pages = txt.split('\f')
    return [[l.strip() for l in p.splitlines() if l.strip()][:n] for p in pages[:len(PdfReader(path).pages)]]

def sections(path):
    """[(title, page index)] for the sections, sets or chapters that start on a page of this PDF"""
    out = []
    for i, ls in enumerate(first_lines(path)):
        if not ls: continue
        head = re.sub(r'\s{2,}.*$', '', ls[0])  # -layout puts the right-hand meta on the same line
        m = SET.match(head)
        if m:
            day = re.search(r'第\s*(\d+)\s*天', ' '.join(ls))  # the set's day sits on its header line
            out.append((f'第 {m.group(1)} 套' + (f'（第 {day.group(1)} 天）' if day else ''), i))
        elif SECTION.match(head):
            out.append((head, i))
    return out

def day_doc(d):
    week = '第一周' if d <= 7 else '第二周'
    return (f'第 {d} 天', f'{B}/{week}/第{d:02d}天.pdf')

VOLUMES = [
    ('第1册_第一周（第1-7天）', [('使用说明与日程总表', f'{S}/volumes/00_使用说明与日程总表.pdf')] + [day_doc(d) for d in range(1, 8)]),
    ('第2册_第二周（第8-14天）', [day_doc(d) for d in range(8, 15)]),
    ('第3册_资料分析打印册（第4-21天）', [('资料分析打印册 · 第 4–7 天（第 1–8 套）', f'{B}/资料分析/资料分析打印册_第4-7天.pdf'),
                                    ('资料分析打印册 · 第 8–14 天（第 9–22 套）', f'{B}/资料分析/资料分析打印册_第8-14天.pdf'),
                                    ('资料分析打印册 · 第 15–21 天（第 23–36 套）', f'{B}/资料分析/资料分析打印册_第15-21天.pdf')]),
    ('第4册_专项与背诵', [('图推固定题型专项', f'{B}/图推/图推固定题型专项.pdf'), ('幂次背诵表', f'{B}/背诵/幂次背诵表.pdf')]),
]

def build(name, docs, out_dir):
    w = PdfWriter()
    for title, path in docs:
        start = len(w.pages)
        w.append(path, import_outline=False)
        top = w.add_outline_item(title, start)
        subs = sections(path) if title != '幂次背诵表' else [('背诵版', 0), ('默写版', 1)]
        for t, i in subs:
            if i > 0 or title == '幂次背诵表': w.add_outline_item(t, start + i, parent=top)
    w.page_mode = '/UseOutlines'
    w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    out = f'{out_dir}/{name}.pdf'
    with open(out, 'wb') as f: w.write(f)
    return out, len(w.pages)

if __name__ == '__main__':
    out_dir = sys.argv[1]; os.makedirs(out_dir, exist_ok=True)
    for name, docs in VOLUMES:
        out, n = build(name, docs, out_dir)
        print(f'{name}: {n} 页, {os.path.getsize(out) // 1024} KB, 来源 {sum(len(PdfReader(p).pages) for _, p in docs)} 页')
