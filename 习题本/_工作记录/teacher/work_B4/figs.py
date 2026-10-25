# 生成本批需要的题图（SVG），写到 work_B4/fig/ 下，并供 build.py 导入
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = '<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Noto Sans SC, Arial, sans-serif" font-size="15" fill="#111">'

def f(v):
    s = ('%.1f' % v).rstrip('0').rstrip('.')
    return s

# ---------- T128 L形道路网 ----------
def t128():
    X = lambda i: 30 + 40 * i
    Y = lambda j: 195 - 40 * j
    node = lambda i, j: (0 <= i <= 4 and 0 <= j <= 2) or (2 <= i <= 4 and 2 <= j <= 4)
    p = []
    for j in range(5):
        xs = [i for i in range(5) if node(i, j)]
        p.append('M%s,%s H%s' % (X(xs[0]), Y(j), X(xs[-1])))
    for i in range(5):
        ys = [j for j in range(5) if node(i, j)]
        p.append('M%s,%s V%s' % (X(i), Y(ys[0]), Y(ys[-1])))
    s = [HEAD.format(w=230, h=225)]
    s.append('<path d="%s" fill="none" stroke="#111" stroke-width="1.5"/>' % ' '.join(p))
    for i in range(5):
        for j in range(5):
            if node(i, j):
                s.append('<circle cx="%s" cy="%s" r="3"/>' % (X(i), Y(j)))
    s.append('<text x="196" y="28">甲</text>')
    s.append('<text x="10" y="216">乙</text>')
    s.append('<text x="155" y="176">丙</text>')
    s.append('</svg>')
    return ''.join(s)

# ---------- T151 立方体堆垛（正面看到的6个立方体） ----------
def t151():
    w, h, v = 40, 20, 46
    tops = [(130, 10), (90, 76), (170, 76), (50, 142), (130, 142), (210, 142)]
    s = [HEAD.format(w=260, h=240)]
    for x, y in tops:
        top = [(x, y), (x + w, y + h), (x, y + 2 * h), (x - w, y + h)]
        left = [(x - w, y + h), (x, y + 2 * h), (x, y + 2 * h + v), (x - w, y + h + v)]
        right = [(x, y + 2 * h), (x + w, y + h), (x + w, y + h + v), (x, y + 2 * h + v)]
        for poly in (top, left, right):
            s.append('<polygon points="%s" fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/>'
                     % ' '.join('%s,%s' % pt for pt in poly))
    s.append('</svg>')
    return ''.join(s)

# ---------- T152 空心圆/实心圆树形图（第1~6行） ----------
def t152():
    sc, ox, oy = 0.36, 0, 2
    P = lambda x, y: (x * sc + ox, y * sc + oy)
    # (x, y, 是否空心) —— 坐标按原图量取
    rows = {
        1: [(222, 65, 1)],
        2: [(222, 155, 0)],
        3: [(180, 265, 0), (400, 265, 1)],
        4: [(138, 380, 0), (285, 380, 1), (590, 380, 0)],
        5: [(103, 485, 0), (208, 485, 1), (387, 485, 0), (575, 485, 0), (762, 485, 1)],
        6: [(60, 600, 0), (180, 600, 1), (287, 600, 0), (355, 600, 0), (487, 600, 1), (565, 600, 0), (708, 600, 1), (950, 600, 0)],
    }
    edges = [((1, 0), (2, 0)), ((2, 0), (3, 0)), ((2, 0), (3, 1)),
             ((3, 0), (4, 0)), ((3, 0), (4, 1)), ((3, 1), (4, 2)),
             ((4, 0), (5, 0)), ((4, 0), (5, 1)), ((4, 1), (5, 2)), ((4, 2), (5, 3)), ((4, 2), (5, 4)),
             ((5, 0), (6, 0)), ((5, 0), (6, 1)), ((5, 1), (6, 2)), ((5, 2), (6, 3)), ((5, 2), (6, 4)),
             ((5, 3), (6, 5)), ((5, 3), (6, 6)), ((5, 4), (6, 7))]
    s = [HEAD.format(w=440, h=226).replace('font-size="15"', 'font-size="13"')]
    d = []
    for (r1, i1), (r2, i2) in edges:
        x1, y1 = P(*rows[r1][i1][:2]); x2, y2 = P(*rows[r2][i2][:2])
        d.append('M%s,%s L%s,%s' % (f(x1), f(y1), f(x2), f(y2)))
    for r in range(3, 7):                       # 每行的横线
        x1, y1 = P(*rows[r][0][:2]); x2, y2 = P(*rows[r][-1][:2])
        d.append('M%s,%s L%s,%s' % (f(x1), f(y1), f(x2), f(y2)))
    s.append('<path d="%s" fill="none" stroke="#111" stroke-width="1.3"/>' % ' '.join(d))
    lab_x = 1072 * sc + ox
    for r in range(1, 7):
        xr, yr = P(*rows[r][-1][:2])
        s.append('<path d="M%s,%s H%s" stroke="#666" stroke-width="1" stroke-dasharray="4,3"/>' % (f(xr + 9), f(yr), f(lab_x - 5)))
        s.append('<text x="%s" y="%s">第%d行</text>' % (f(lab_x), f(yr + 4.5), r))
    for r in rows:
        for x, y, hollow in rows[r]:
            cx, cy = P(x, y)
            if hollow:
                s.append('<circle cx="%s" cy="%s" r="4.6" fill="#fff" stroke="#111" stroke-width="1.3"/>' % (f(cx), f(cy)))
            else:
                s.append('<circle cx="%s" cy="%s" r="4.6"/>' % (f(cx), f(cy)))
    s.append('</svg>')
    return ''.join(s)

# ---------- T153 管材堆示意图（中间部分用虚线省略） ----------
def t153():
    R, STEP, DY = 9.5, 20, 17.3
    shift = -30
    s = [HEAD.format(w=380, h=175)]
    circ = lambda x, y: '<circle cx="%s" cy="%s" r="%s" fill="#fff" stroke="#555" stroke-width="1.2"/>' % (f(x + shift), f(y), R)
    dash = lambda x1, y1, x2, y2: '<path d="M%s,%s L%s,%s" stroke="#777" stroke-width="1" stroke-dasharray="3,3"/>' % (f(x1 + shift), f(y1), f(x2 + shift), f(y2))
    # 最上层
    y0 = 14
    top_left = [130, 150, 170]; top_right = [290, 310]
    s.append(dash(top_left[-1] + R + 2, y0, top_right[0] - R - 2, y0))
    for x in top_left + top_right:
        s.append(circ(x, y0))
    # 下面可见的5层
    y1 = 82
    first_left = None
    for k in range(5):
        y = y1 + DY * k
        left = [90 - 10 * k + STEP * i for i in range(4 + k)]
        right = [330 + 10 * k, 350 + 10 * k]
        if k == 0:
            first_left, first_right = left, right
        s.append(dash(left[-1] + R + 2, y, right[0] - R - 2, y))
        for x in left + right:
            s.append(circ(x, y))
    # 中间省略的若干层（虚线连接）
    for xt, xb in zip(top_left, first_left):
        s.append(dash(xt, y0 + R + 2, xb, y1 - R - 2))
    for xt, xb in zip(top_right, first_right):
        s.append(dash(xt, y0 + R + 2, xb, y1 - R - 2))
    s.append('</svg>')
    return ''.join(s)

# ---------- T160 撕页台历 ----------
def t160():
    s = [HEAD.format(w=180, h=135)]
    s.append('<rect x="12" y="24" width="156" height="102" rx="12" fill="#fff" stroke="#111" stroke-width="1.6"/>')
    s.append('<path d="M12,40 H168 M12,45 H168" stroke="#111" stroke-width="1.1"/>')
    for x in (52, 76, 104, 128):
        s.append('<rect x="%d" y="10" width="9" height="30" rx="4.5" fill="#fff" stroke="#111" stroke-width="1.3"/>' % (x - 4))
    s.append('<text x="90" y="88" text-anchor="middle" font-size="30" font-weight="700">13日</text>')
    s.append('<text x="90" y="110" text-anchor="middle" font-size="10" font-weight="700">庚子年十月廿九</text>')
    s.append('</svg>')
    return ''.join(s)

FIGS = {'T128': t128(), 'T151': t151(), 'T152': t152(), 'T153': t153(), 'T160': t160()}

if __name__ == '__main__':
    for k, v in FIGS.items():
        with open(os.path.join(HERE, 'fig', k + '.svg'), 'w') as fh:
            fh.write(v)
        print(k, len(v))
