"""按模块刷题顺序: a printable checklist for working through the printed books one module at a time (the number-crunching
modules first, then the reasoning ones), with a box per day, set or chapter. Topics, set-to-day mapping and question
counts are read from the finished PDFs. Usage: make_module_order.py <out.pdf>"""
import os, re, subprocess, sys
from pypdf import PdfReader
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_volumes import sections, B
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
R = S + '/render'

# days grouped by 考法 for the modules whose topics repeat across the two weeks; a note marks a day that mixes in another 考法
LOGIC = [('翻译推理', [1, 8]), ('加强论证', [2, 10]), ('削弱论证', [3, 11]), ('前提假设', [4, 12]),
         ('原因解释', [5, (9, '含削弱')]), ('结构相似与论证评价', [6, 13]), ('真假推理与归纳推理', [7, (14, '含翻译推理')])]
ZONGHE = [('排序与位置', [1, (6, '含分组'), 11]), ('匹配对应', [2, 7, 12]), ('分组与选择', [3, 8, 13]),
          ('数量与大小比较', [4, (9, '含真假综合')]), ('真假综合与多维混合', [5, 10, 14])]

def day_pdf(d):
    return f'{B}/{"第一周" if d <= 7 else "第二周"}/第{d:02d}天.pdf'

def counted(path, secs, title):
    """number of answered questions in the 解析 section `title` of a PDF"""
    n = len(PdfReader(path).pages); starts = [i for _, i in secs] + [n]
    k = [t for t, _ in secs].index(title)
    txt = subprocess.run(['pdftotext', '-layout', '-f', str(secs[k][1] + 1), '-l', str(starts[k + 1]), path, '-'],
                         capture_output=True, text=True).stdout
    return len(set(re.findall(r'^\s*(\d+)\.\s*答案', txt, re.M)))

def gather():
    days = {}
    for d in range(1, 15):
        p = day_pdf(d); secs = sections(p)
        days[d] = {'topic': {t.split(' · ')[0]: t.split(' · ', 1)[1] for t, _ in secs if ' · ' in t and not t.startswith('解析')},
                   'n': {m: counted(p, secs, f'解析 · {m}') for m in ('数学运算', '数字推理', '逻辑判断', '综合推理')}}
    sets = []
    for name in ('资料分析打印册_第4-7天', '资料分析打印册_第8-14天'):
        for t, _ in sections(f'{B}/资料分析/{name}.pdf'):
            m = re.match(r'第 (\d+) 套（第 (\d+) 天）', t)
            if m: sets.append((int(m.group(1)), int(m.group(2)), name.split('_')[1]))
    tu = f'{B}/图推/图推固定题型专项.pdf'; secs = sections(tu)
    chapters = [(t, counted(tu, secs, f'解析 · {t.split(" · ")[0]}')) for t, _ in secs if re.match(r'第 \d+ 章 · ', t)]
    return days, sets, chapters

def box(label, note=''):
    return f'<span class="it"><i class="box"></i>{label}{f"<em>{note}</em>" if note else ""}</span>'

def block(no, name, where, total, body):
    return (f'<section><div class="hd"><span class="no">{no}</span><b>{name}</b><span class="where">{where}</span>'
            f'<span class="tot">{total}</span></div>{body}</section>')

def grouped(groups):
    rows = []
    for kf, ds in groups:
        items = ''.join(box(f'第 {x} 天') if isinstance(x, int) else box(f'第 {x[0]} 天', x[1]) for x in ds)
        rows.append(f'<div class="grp"><span class="kf">{kf}</span><span class="items">{items}</span></div>')
    return ''.join(rows)

def page(days, sets, chapters):
    tot = lambda m, ds: sum(days[d]['n'][m] for d in ds)
    out = ['<h1>按模块刷题顺序</h1>',
           '<div class="sub">先打要算的三块，再打推理的三块，中间只换一次脑子。第 1、2 天做过的跳过，做完一格打一个勾。</div>',
           '<div class="flow">' + ' → '.join(f'<span>{s}</span>' for s in
                                            ['0 申论', '1 数学运算', '2 数字推理', '3 资料分析', '4 逻辑判断', '5 综合推理', '6 图推']) + '</div>',
           '<div class="how">每做完一格：先对那天本子里的“答案速查”，再看对应的解析。被题目绕进去的，记进《易错陷阱记录》。</div>']
    math_days = range(3, 15)
    out.append(block(1, '数学运算', '每天本子里的“数学运算”，按天往下做，一天一个考法', f'第 3–14 天 · 共 {tot("数学运算", math_days)} 题',
                     '<div class="cols c3">' + ''.join(box(f'第 {d} 天 · {days[d]["topic"]["数学运算"]}') for d in math_days) + '</div>'))
    out.append(block(2, '数字推理', '每天本子里的“数字推理”，每天 10 道，一口气做完', f'第 1–14 天 · 共 {tot("数字推理", range(1, 15))} 题',
                     '<div class="cols c7">' + ''.join(box(f'第 {d} 天') for d in range(1, 15)) + '</div>'))
    book = {}
    for n, d, b in sets: book.setdefault(b, []).append((n, d))
    zl = ''.join(f'<div class="grp"><span class="kf">{re.sub(r"第(\d+)-(\d+)天", r"第 \1–\2 天", b)}那本</span><span class="items">'
                 + ''.join(box(f'第 {n} 套', f'第 {d} 天') for n, d in ss) + '</span></div>'
                 for b, ss in book.items())
    zl += '<div class="note">答案在对应那天本子里的“解析 · 资料分析”。第 15–21 天那本（第 23–36 套）的答案还没出，做到之前补上。</div>'
    out.append(block(3, '资料分析', '资料分析打印册，按套往下做', f'第 1–{len(sets)} 套', zl))
    out.append(block(4, '逻辑判断', '每天本子里的“逻辑判断”，按考法把天数凑在一起做', f'共 {tot("逻辑判断", range(1, 15))} 题', grouped(LOGIC)))
    out.append(block(5, '综合推理', '每天本子里的“综合推理”，按考法把天数凑在一起做', f'共 {tot("综合推理", range(1, 15))} 题', grouped(ZONGHE)))
    out.append(block(6, '图推', '《图推固定题型专项》，按章往下做', f'7 章 · 共 {sum(c for _, c in chapters)} 题',
                     '<div class="cols c2">' + ''.join(box(t.replace(' · ', ' '), f'{c} 题') for t, c in chapters) + '</div>'))
    return ''.join(out)

CSS = """
@page { size: A4; margin: 13mm 14mm 12mm 14mm; }
body { font-family: 'Noto Sans SC', sans-serif; color: #111; margin: 0; font-size: 10.5pt; line-height: 1.5; }
h1 { font-size: 18pt; margin: 0 0 1mm 0; }
.sub { color: #444; margin-bottom: 2.5mm; }
.flow { background: #f2f2f2; border-radius: 2px; padding: 2mm 3mm; font-weight: 700; margin-bottom: 2mm; }
.flow span { white-space: nowrap; }
.how { font-size: 9.5pt; color: #444; margin-bottom: 4mm; }
section { border: 1px solid #bbb; border-radius: 3px; margin-bottom: 3.5mm; break-inside: avoid; }
.hd { display: flex; align-items: baseline; gap: 2.5mm; background: #eee; border-bottom: 1px solid #ccc; padding: 1.4mm 3mm; }
.hd .no { background: #333; color: #fff; border-radius: 2px; padding: 0 1.8mm; font-weight: 700; font-size: 9.5pt; }
.hd b { font-size: 11.5pt; }
.hd .where { color: #444; font-size: 9.5pt; }
.hd .tot { margin-left: auto; color: #666; font-size: 9pt; white-space: nowrap; }
.cols { display: grid; gap: 1.2mm 3mm; padding: 2mm 3mm; }
.c2 { grid-template-columns: repeat(2, 1fr); }
.c3 { grid-template-columns: repeat(3, 1fr); font-size: 10pt; }
.c3 .it { white-space: normal; padding-left: 4.7mm; text-indent: -4.7mm; }
.c7 { grid-template-columns: repeat(7, 1fr); }
.grp { display: flex; align-items: baseline; padding: 1.2mm 3mm; border-bottom: 1px dashed #ddd; }
.items { flex: 1; display: flex; flex-wrap: wrap; gap: 1mm 5mm; }
.grp:last-of-type { border-bottom: none; }
.kf { width: 39mm; flex: none; font-weight: 600; color: #333; }
.it { white-space: nowrap; }
.it em { font-style: normal; color: #777; font-size: 8.5pt; margin-left: 1mm; }
.box { display: inline-block; width: 3.2mm; height: 3.2mm; border: 1px solid #333; border-radius: 0.4mm; margin-right: 1.5mm; vertical-align: -0.5mm; }
.note { font-size: 9pt; color: #555; padding: 0.5mm 3mm 2mm 3mm; }
"""

if __name__ == '__main__':
    out_pdf = sys.argv[1]
    days, sets, chapters = gather()
    fonts = ''.join(f'<link rel="stylesheet" href="file://{R}/node_modules/@fontsource/noto-sans-sc/{w}.css">' for w in (400, 700))
    doc = (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>按模块刷题顺序</title>{fonts}'
           f'<style>{CSS}</style></head><body>{page(days, sets, chapters)}</body></html>')
    hp = S + '/module_order.html'
    open(hp, 'w').write(doc)
    subprocess.run(['node', R + '/print.js', hp, os.path.abspath(out_pdf)], check=True, cwd=R)
    print('ok', out_pdf, '图推各章:', chapters)
