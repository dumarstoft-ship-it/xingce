"""幂次背诵表 for 数字推理 (幂次修正): squares 1–31 (every square under 1000), cubes 1–12, powers of 2–7, numbers with
several power forms, and the numbers one away from a power. Page 1 has the values, page 2 is the same sheet blank
for recall. Every value is computed here. Usage: make_powers.py <out.pdf>"""
import os, subprocess, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
R = S + '/render'
BASES = {2: 12, 3: 7, 4: 6, 5: 5, 6: 4, 7: 4}  # base: highest exponent listed (values up to a few thousand)
LIMIT = 5000

def power_forms(limit=LIMIT):
    """{value: ['2<sup>6</sup>', '4<sup>3</sup>', '8<sup>2</sup>'], ...} for perfect powers (exponent >= 2) up to limit"""
    forms = {}
    for b in range(2, 71):
        e = 2
        while b ** e <= limit:
            forms.setdefault(b ** e, []).append(f'{b}<sup>{e}</sup>')
            e += 1
    return forms

def table(rows, blank):
    """rows: [(head, [cells...]), ...]; the second row of each pair is the answer row"""
    h = ['<table>']
    for k, (head, cells) in enumerate(rows):
        ans = k % 2 == 1
        tds = ''.join(f'<td class="{"a" if ans else "n"}">{"" if (ans and blank) else c}</td>' for c in cells)
        h.append(f'<tr><th>{head}</th>{tds}</tr>')
    h.append('</table>')
    return ''.join(h)

def sheet(blank):
    sq = [(n, n * n) for n in range(1, 32)]
    cu = [(n, n ** 3) for n in range(1, 13)]
    out = [f'<h1>幂次背诵表{"（默写版）" if blank else ""}</h1>'
           '<div class="sub">数字推理 · 幂次修正。数列里的数等于或接近这些数时，先想幂次。</div>']
    out.append('<h2>平方（1000 以内的平方数全在这里）</h2>')
    out.append(table([('n', [n for n, _ in sq[:16]]), ('n²', [v for _, v in sq[:16]]),
                      ('n', [n for n, _ in sq[16:]] + ['']), ('n²', [v for _, v in sq[16:]] + [''])], blank))
    out.append('<h2>立方</h2>')
    out.append(table([('n', [n for n, _ in cu]), ('n³', [v for _, v in cu])], blank))
    out.append('<h2>各次方（底数 2–7）</h2>')
    w = max(BASES.values()) + 1
    h = ['<table class="pw"><tr><th>底数＼指数</th>' + ''.join(f'<td class="n">{e}</td>' for e in range(w)) + '</tr>']
    for b, top in BASES.items():
        cells = ''.join(f'<td class="a">{"" if blank or e > top else b ** e}</td>' if e <= top else '<td class="x"></td>' for e in range(w))
        h.append(f'<tr><th>{b}</th>{cells}</tr>')
    h.append('</table>')
    out.append(''.join(h))
    out.append('<div class="note">任何数的 0 次方都是 1；负一次方是倒数（2<sup>−1</sup> = 1/2），数列里出现分数、1 时也可能是幂次。</div>')
    forms = power_forms()
    multi = [(v, f) for v, f in sorted(forms.items()) if len(f) >= 2]
    out.append('<h2>一个数有几种幂次写法（最容易考的）</h2><div class="multi">')
    out.append(''.join(f'<span><b>{v}</b> = {"<i class=gap></i>" if blank else " = ".join(f)}</span>' for v, f in multi))
    out.append('</div>')
    # squares up to 100 and every higher power up to 1100 (the squares above 100 are in the first table)
    near = sorted({n * n for n in range(3, 11)} | {b ** e for b in range(2, 11) for e in range(3, 11) if b ** e <= 1100})
    out.append('<h2>幂次 ±1 速认（看到左右两个数，先想中间的幂次）</h2><div class="near">')
    out.append(''.join(f'<span>{v - 1} ・ <b class="{"gap" if blank else ""}">{"" if blank else v}</b> ・ {v + 1}</span>' for v in near))
    out.append('</div>')
    return '<div class="page">' + ''.join(out) + '</div>'

CSS = """
@page { size: A4; margin: 12mm; }
body { font-family: 'Noto Sans SC', sans-serif; color: #111; margin: 0; font-size: 10pt; }
.page { break-after: page; }
.page:last-child { break-after: auto; }
h1 { font-size: 17pt; margin: 0 0 1mm 0; }
.sub { color: #555; font-size: 9pt; margin-bottom: 3mm; }
h2 { font-size: 11pt; margin: 4mm 0 1.5mm 0; border-left: 3px solid #333; padding-left: 2mm; }
table { border-collapse: collapse; width: 100%; table-layout: fixed; }
th, td { border: 1px solid #aaa; text-align: center; padding: 1.2mm 0; font-size: 10pt; }
th { background: #eee; font-weight: 600; width: 13mm; }
td.n { background: #f7f7f7; color: #555; }
td.a { font-weight: 700; height: 6mm; }
td.x { background: #fafafa; }
table.pw th { width: 20mm; }
.note { font-size: 8.5pt; color: #444; margin-top: 1.2mm; }
.multi, .near { display: flex; flex-wrap: wrap; gap: 1.5mm 3mm; font-size: 10pt; }
.multi span { border: 1px solid #ccc; border-radius: 2px; padding: 0.8mm 2mm; min-width: 40mm; }
.near span { border: 1px solid #ccc; border-radius: 2px; padding: 0.8mm 2mm; min-width: 24mm; text-align: center; }
.gap { display: inline-block; min-width: 9mm; border-bottom: 1px solid #333; vertical-align: -1mm; }
i.gap { min-width: 26mm; }
sup { font-size: 70%; }
"""

if __name__ == '__main__':
    out_pdf = sys.argv[1]
    fonts = ''.join(f'<link rel="stylesheet" href="file://{R}/node_modules/@fontsource/noto-sans-sc/{w}.css">' for w in (400, 700))
    html = f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>幂次背诵表</title>{fonts}<style>{CSS}</style></head><body>{sheet(False)}{sheet(True)}</body></html>'
    hp = out_pdf[:-4] + '.html'
    open(hp, 'w').write(html)
    subprocess.run(['node', R + '/print.js', os.path.abspath(hp), os.path.abspath(out_pdf)], check=True, cwd=R)
    print('ok', out_pdf)
