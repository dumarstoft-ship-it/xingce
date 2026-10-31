"""动图: 第 3 天数学运算第 3 题 (相遇后甲再走 16 分钟到 B、乙再走 25 分钟到 A, 甲 200 米/分, 求全程).
Shows the two cars meeting, the road splitting into the stretch each car covered before meeting, each car then driving
the other's stretch, and the derivation t^2 = 16 x 25. Drawn at 2x and downsampled. Usage: anim_meet.py <out.gif>"""
import sys
from PIL import Image, ImageDraw, ImageFont

SC, W, H = 2, 800, 540
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED, BLUE, GRAY, INK, MUTED, PANEL = (214, 64, 54), (40, 104, 210), (200, 200, 200), (30, 30, 30), (105, 105, 105), (244, 245, 247)
X0, X1, ROAD_Y = 110, 690, 150                  # road ends and height, in final pixels
TOTAL, VA, VB, T = 7200, 200, 160, 20           # metres, 甲 and 乙 m/min, minutes to the meeting (checked: t*t = 16*25)
XP = X0 + (X1 - X0) * VA * T / TOTAL            # meeting point
fonts = {}

def F(size):
    if size not in fonts: fonts[size] = ImageFont.truetype(FONT, size * SC)
    return fonts[size]

def xm(metres):
    return X0 + (X1 - X0) * metres / TOTAL

class Canvas:
    def __init__(self):
        self.im = Image.new('RGB', (W * SC, H * SC), 'white'); self.d = ImageDraw.Draw(self.im)
    def line(self, x0, y0, x1, y1, fill, w):
        self.d.line([(x0 * SC, y0 * SC), (x1 * SC, y1 * SC)], fill=fill, width=round(w * SC))
    def rect(self, x0, y0, x1, y1, r, fill):
        self.d.rounded_rectangle([x0 * SC, y0 * SC, x1 * SC, y1 * SC], r * SC, fill=fill)
    def text(self, x, y, s, size, fill=INK, anchor='la', bold=False):
        self.d.text((x * SC, y * SC), s, font=F(size), fill=fill, anchor=anchor, stroke_width=1 if bold else 0, stroke_fill=fill)
    def runs(self, x, y, parts, size, anchor_mid=False, bold=False):
        """a line made of differently coloured pieces: [(text, colour), ...]"""
        widths = [self.d.textlength(s, font=F(size)) / SC for s, _ in parts]
        if anchor_mid: x -= sum(widths) / 2
        for (s, c), w in zip(parts, widths):
            self.text(x, y, s, size, c, 'lm', bold); x += w
    def done(self):
        return self.im.resize((W, H), Image.LANCZOS)

def car(c, x, y, colour, name):
    c.rect(x - 23, y - 12, x + 23, y + 12, 6, colour)
    c.text(x, y, name, 14, (255, 255, 255), 'mm', True)

CAPTIONS = {
    'intro': [[('甲从 A、乙从 B 同时出发，相向而行。甲每分钟 200 米。', INK)],
              [('相遇后，甲再走 ', INK), ('16 分钟', RED), ('到 B，乙再走 ', INK), ('25 分钟', BLUE), ('到 A。全程多长？', INK)]],
    'p1': [[('相遇前，两车走的时间一样，记作 ', INK), ('t', INK), (' 分钟。', INK)],
           [('红色', RED), ('是甲走过的路，', INK), ('蓝色', BLUE), ('是乙走过的路。', INK)]],
    'meet': [[('相遇了！相遇点把全程分成两段：', INK)],
             [('红段', RED), ('是甲相遇前走的，', INK), ('蓝段', BLUE), ('是乙相遇前走的，都用了 t 分钟。', INK)]],
    'p2': [[('相遇后，两车去走对方刚走过的那一段：', INK)],
           [('甲走', INK), ('蓝段', BLUE), ('用 16 分钟，乙走', INK), ('红段', RED), ('用 25 分钟。', INK)]],
    'end': [[('每一段路，两辆车都各走了一遍：', INK)],
            [('红段', RED), ('：甲 t 分钟，乙 25 分钟；', INK), ('蓝段', BLUE), ('：乙 t 分钟，甲 16 分钟。', INK)]],
}
DERIVE = [
    [('同一段路，用时之比就是速度的反比：', INK)],
    [('红段', RED), ('  甲 : 乙 = 25 : t        ', INK), ('蓝段', BLUE), ('  甲 : 乙 = t : 16', INK)],
    [('两个都是甲 : 乙的速度比，所以  25 : t = t : 16', INK)],
    [('t × t = 16 × 25 = 400，所以 t = 20 分钟', RED)],
    [('16 → 20 → 25，每一步都 ×5/4：甲的速度是乙的 5/4', MUTED)],
    [('甲全程 20 + 16 = 36 分钟，36 × 200 = 7200 米，选 B', INK)],
]

def frame(m, phase, n=0):
    """m: minutes since the start (0-45); phase: intro / p1 / meet / p2 / end / derive; n: derivation lines shown"""
    c = Canvas()
    c.text(W / 2, 26, '第 3 天 · 数学运算第 3 题：相遇后各走 16、25 分钟，全程多长？', 19, INK, 'mm', True)
    c.text(X0 - 30, ROAD_Y, 'A 站', 16, INK, 'rm', True)
    c.text(X1 + 30, ROAD_Y, 'B 站', 16, INK, 'lm', True)
    c.line(X0, ROAD_Y, X1, ROAD_Y, GRAY, 8)
    a_pos, b_pos = min(VA * m, TOTAL), max(TOTAL - VB * m, 0)
    met = m >= T
    if met:                                                    # the two stretches keep their colours after the meeting
        c.line(X0, ROAD_Y, XP, ROAD_Y, RED, 8); c.line(XP, ROAD_Y, X1, ROAD_Y, BLUE, 8)
        for y in range(ROAD_Y - 38, ROAD_Y + 40, 8):           # dashed meeting mark
            c.line(XP, y, XP, y + 4, MUTED, 1.5)
        c.text((X0 + XP) / 2, ROAD_Y - 52, '红段：甲相遇前走的', 15, RED, 'mm', True)
        c.text((XP + X1) / 2, ROAD_Y - 52, '蓝段：乙相遇前走的', 15, BLUE, 'mm', True)
    else:
        c.line(X0, ROAD_Y, xm(a_pos), ROAD_Y, RED, 8); c.line(xm(b_pos), ROAD_Y, X1, ROAD_Y, BLUE, 8)
    for x in (X0, X1):
        c.line(x, ROAD_Y - 10, x, ROAD_Y + 10, INK, 2)
    car(c, xm(a_pos), ROAD_Y - 22, RED, '甲')
    car(c, xm(b_pos), ROAD_Y + 22, BLUE, '乙')
    # under each stretch: the clock while the cars drive it after meeting, then who took how long
    yl = ROAD_Y + 56
    if phase in ('p2',) or (phase == 'meet'):
        ta, tb = min(m - T, 16), min(m - T, 25)
        c.runs((X0 + XP) / 2, yl, [('乙 走红段：', BLUE), (f'{int(tb)} / 25 分钟', BLUE)], 15, True, True)
        c.runs((XP + X1) / 2, yl, [('甲 走蓝段：', RED), (f'{int(ta)} / 16 分钟', RED)], 15, True, True)
    elif phase in ('end', 'derive'):
        c.runs((X0 + XP) / 2, yl, [('甲 t 分钟', RED), ('  ·  ', MUTED), ('乙 25 分钟', BLUE)], 15, True, True)
        c.runs((XP + X1) / 2, yl, [('乙 t 分钟', BLUE), ('  ·  ', MUTED), ('甲 16 分钟', RED)], 15, True, True)
        if phase == 'derive' and n >= 6:
            c.text((X0 + XP) / 2, yl + 26, '20 × 200 = 4000 米', 14, MUTED, 'mm')
            c.text((XP + X1) / 2, yl + 26, '16 × 200 = 3200 米', 14, MUTED, 'mm')
    # explanation panel
    c.rect(30, 262, W - 30, H - 16, 10, PANEL)
    if phase == 'derive':
        for k, parts in enumerate(DERIVE[:n]):
            c.runs(54, 296 + k * 38, parts, 17, bold=(k in (3, 5)))
    else:
        for k, parts in enumerate(CAPTIONS[phase]):
            c.runs(54, 310 + k * 44, parts, 17)
    return c.done()

def build(out):
    frames = [(frame(0, 'intro'), 2600)]
    frames += [(frame(T * i / 30, 'p1'), 80) for i in range(1, 30)]
    frames += [(frame(T, 'meet'), 3200)]
    frames += [(frame(T + 25 * i / 40, 'p2'), 80) for i in range(1, 41)]
    frames += [(frame(45, 'end'), 3000)]
    frames += [(frame(45, 'derive', n), d) for n, d in zip(range(1, 7), (1800, 2400, 2200, 2600, 2600, 5000))]
    pal = frames[-1][0].quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    ims = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f, _ in frames]
    ims[0].save(out, save_all=True, append_images=ims[1:], duration=[d for _, d in frames], loop=0, optimize=True)
    for name, idx in (('meet', 30), ('p2', 50), ('end', -1)):
        frames[idx][0].save(out[:-4] + f'_{name}.png')
    print('ok', out, len(frames), 'frames', sum(d for _, d in frames) / 1000, 's')

if __name__ == '__main__':
    build(sys.argv[1])
