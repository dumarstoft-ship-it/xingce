# 生成 T204 / T204b / T204c 的 SVG（坐标取自原图放大后的测量值），并输出预览 HTML
import json, math, sys

FONT = "'Noto Sans SC', sans-serif"


def svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}">')


def fmt(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


# ---------- T204 最小生成树 ----------
def fig_mst():
    s, ox, oy = 0.5, 4, 0
    raw = {'F': (45, 190), 'A': (228, 182), 'B': (620, 48), 'C': (380, 320), 'D': (530, 325), 'E': (305, 465)}
    P = {k: (x * s + ox, y * s + oy) for k, (x, y) in raw.items()}
    edges = [('F', 'A', '3', (148, 160)), ('A', 'B', '10', (410, 95)), ('A', 'C', '4', (312, 240)),
             ('B', 'C', '8', (472, 176)), ('B', 'D', '6', (620, 213)), ('F', 'C', '6.5', (222, 299)),
             ('C', 'D', '2.5', (456, 300)), ('F', 'E', '7.5', (158, 370)), ('C', 'E', '3', (322, 385)),
             ('D', 'E', '5', (420, 442))]
    w, h = 330, 250
    out = [svg_open(w, h, '6栋住宅楼F、A、B、C、D、E之间可铺设管道的线路图，线上数字为长度（百米）')]
    out.append('<g stroke="#111" stroke-width="1.6">')
    for u, v, _, _ in edges:
        (x1, y1), (x2, y2) = P[u], P[v]
        out.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}"/>')
    out.append('</g>')
    out.append(f'<g font-family="{FONT}" font-size="13" fill="#111" text-anchor="middle">')
    for _, _, t, (x, y) in edges:
        out.append(f'<text x="{fmt(x * s + ox)}" y="{fmt(y * s + oy + 4)}">{t}</text>')
    out.append('</g>')
    out.append(f'<g stroke="#111" stroke-width="1.6" fill="#fff">')
    for k, (x, y) in P.items():
        out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="11"/>')
    out.append('</g>')
    out.append(f'<g font-family="{FONT}" font-size="14" fill="#111" text-anchor="middle">')
    for k, (x, y) in P.items():
        out.append(f'<text x="{fmt(x)}" y="{fmt(y + 5)}">{k}</text>')
    out.append('</g></svg>')
    return ''.join(out)


# ---------- T204b M到N线路图 ----------
def fig_grid():
    s, ox, oy = 0.32, -10, -8
    raw = {'M': (105, 100), 'T1': (300, 100), 'T2': (598, 100), 'T3': (885, 100),
           'L': (205, 285), 'ML': (300, 285), 'C': (598, 285), 'MR': (885, 285), 'R': (990, 285),
           'BL': (300, 465), 'B2': (598, 465), 'B3': (885, 465), 'N': (1100, 465)}
    P = {k: (x * s + ox, y * s + oy) for k, (x, y) in raw.items()}
    edges = [('M', 'T1', '3', (195, 72)), ('T1', 'T2', '5', (455, 72)), ('T2', 'T3', '2', (765, 72)),
             ('M', 'L', '4', (118, 190)), ('L', 'BL', '2', (205, 375)), ('T3', 'R', '3', (975, 180)),
             ('R', 'N', '6', (995, 380)), ('BL', 'B2', '7', (425, 530)), ('B2', 'B3', '9', (705, 530)),
             ('B3', 'N', '4', (965, 530)), ('L', 'ML', '1', (245, 262)), ('ML', 'C', '3', (378, 248)),
             ('C', 'MR', '5', (770, 255)), ('MR', 'R', '4', (930, 255)), ('T1', 'ML', '2', (275, 185)),
             ('ML', 'BL', '4', (278, 355)), ('T2', 'C', '3', (568, 180)), ('C', 'B2', '5', (568, 372)),
             ('T3', 'MR', '1', (862, 178)), ('MR', 'B3', '3', (852, 372)), ('T1', 'C', '7', (372, 180)),
             ('BL', 'C', '8', (432, 345)), ('C', 'T3', '6', (722, 172)), ('C', 'B3', '2', (672, 378))]
    w, h = 360, 170
    out = [svg_open(w, h, 'M到N之间的电缆线路图，线上数字为该段线路的电量损耗')]
    out.append('<g stroke="#111" stroke-width="1.5">')
    for u, v, _, _ in edges:
        (x1, y1), (x2, y2) = P[u], P[v]
        out.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}"/>')
    out.append('</g>')
    out.append(f'<g font-family="{FONT}" font-size="13" fill="#111" text-anchor="middle">')
    for _, _, t, (x, y) in edges:
        out.append(f'<text x="{fmt(x * s + ox)}" y="{fmt(y * s + oy + 4.5)}">{t}</text>')
    out.append('</g>')
    out.append('<g fill="#111">')
    for k in ('M', 'N'):
        x, y = P[k]
        out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="3"/>')
    out.append('</g>')
    out.append(f'<g font-family="{FONT}" font-size="15" fill="#111">')
    mx, my = P['M']
    nx, ny = P['N']
    out.append(f'<text x="{fmt(mx - 14)}" y="{fmt(my - 4)}">M</text>')
    out.append(f'<text x="{fmt(nx + 5)}" y="{fmt(ny + 5)}">N</text>')
    out.append('</g></svg>')
    return ''.join(out)


# ---------- T204c 菱形道路图（按真实比例） ----------
def fig_rhombus():
    k = 0.75
    hh = 100 * math.sqrt(3)
    cx, cy = 150, 100
    raw = {'A': (-hh, 0), 'B': (0, 100), 'C': (hh, 0), 'D': (0, -100)}
    raw['E'] = ((raw['A'][0] + raw['B'][0]) / 2, (raw['A'][1] + raw['B'][1]) / 2)   # D在AB上的垂足即AB中点
    raw['F'] = ((raw['C'][0] + raw['D'][0]) / 2, (raw['C'][1] + raw['D'][1]) / 2)
    P = {n: (cx + x * k, cy - y * k) for n, (x, y) in raw.items()}
    roads = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('A', 'C'), ('B', 'D'), ('D', 'E'), ('B', 'F')]
    w, h = 300, 200
    out = [svg_open(w, h, '由两个正三角形拼成的菱形ABCD，内部道路为AC、BD、DE、BF')]
    out.append('<g stroke="#111" stroke-width="1.8" stroke-linecap="round">')
    for u, v in roads:
        (x1, y1), (x2, y2) = P[u], P[v]
        out.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}"/>')
    out.append('</g>')
    off = {'A': (-14, 5), 'B': (0, -8), 'C': (13, 5), 'D': (0, 19), 'E': (-9, -7), 'F': (9, 16)}
    out.append(f'<g font-family="{FONT}" font-size="16" font-weight="700" fill="#111" text-anchor="middle">')
    for n, (dx, dy) in off.items():
        x, y = P[n]
        out.append(f'<text x="{fmt(x + dx)}" y="{fmt(y + dy)}">{n}</text>')
    out.append('</g></svg>')
    return ''.join(out)


figs = {'T204': fig_mst(), 'T204x1': fig_grid(), 'T204x2': fig_rhombus()}
json.dump(figs, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
html = '<!doctype html><html><head><meta charset="utf-8"><style>body{background:#fff;margin:10px;font-family:sans-serif} .f{display:inline-block;border:1px dashed #ccc;margin:6px;padding:6px;vertical-align:top}</style></head><body>'
for k, v in figs.items():
    html += f'<div class="f"><div>{k}</div>{v}</div>'
html += '</body></html>'
open(sys.argv[2], 'w').write(html)
print({k: len(v) for k, v in figs.items()})
