"""Small helpers for writing clean problem figures as SVG strings."""
import math

STROKE = "#222"
FONT = "font-family=\"'Noto Sans SC','Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif\""

def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s

def svg(w, h, body, defs=""):
    d = f"<defs>{defs}</defs>" if defs else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}" height="{f(h)}" '
            f'viewBox="0 0 {f(w)} {f(h)}">{d}<rect width="100%" height="100%" fill="#fff"/>{body}</svg>')

def line(p, q, dash=False, w=1.4, color=STROKE):
    da = ' stroke-dasharray="5 4"' if dash else ''
    return (f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" '
            f'stroke="{color}" stroke-width="{w}"{da}/>')

def poly(pts, fill="none", stroke=STROKE, w=1.4, close=True, dash=False, extra=""):
    d = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
    tag = "polygon" if close else "polyline"
    da = ' stroke-dasharray="5 4"' if dash else ''
    st = f'stroke="{stroke}" stroke-width="{w}"' if stroke else 'stroke="none"'
    return f'<{tag} points="{d}" fill="{fill}" {st}{da} stroke-linejoin="round" {extra}/>'

def path(d, fill="none", stroke=STROKE, w=1.4, dash=False, extra=""):
    da = ' stroke-dasharray="5 4"' if dash else ''
    st = f'stroke="{stroke}" stroke-width="{w}"' if stroke else 'stroke="none"'
    return f'<path d="{d}" fill="{fill}" {st}{da} stroke-linejoin="round" {extra}/>'

def circle(c, r, fill="none", stroke=STROKE, w=1.4, dash=False):
    da = ' stroke-dasharray="5 4"' if dash else ''
    st = f'stroke="{stroke}" stroke-width="{w}"' if stroke else 'stroke="none"'
    return f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" fill="{fill}" {st}{da}/>'

def dot(c, r=2.6, color=STROKE):
    return f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" fill="{color}"/>'

def text(p, s, size=14, anchor="middle", color=STROKE, italic=False, weight="normal"):
    it = ' font-style="italic"' if italic else ''
    return (f'<text x="{f(p[0])}" y="{f(p[1])}" font-size="{size}" text-anchor="{anchor}" '
            f'dominant-baseline="central" fill="{color}" font-weight="{weight}" {FONT}{it}>{s}</text>')

def arrow_head(tip, frm, size=7, color=STROKE):
    ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    a1 = ang + math.radians(155); a2 = ang - math.radians(155)
    p1 = (tip[0] + size * math.cos(a1), tip[1] + size * math.sin(a1))
    p2 = (tip[0] + size * math.cos(a2), tip[1] + size * math.sin(a2))
    return poly([tip, p1, p2], fill=color, stroke=None)

def dim(p, q, label, off=(0, 0), size=13, w=1.0, both=True):
    """dimension line with arrow heads at both ends and a label at the midpoint+off"""
    s = line(p, q, w=w)
    s += arrow_head(q, p, 6)
    if both:
        s += arrow_head(p, q, 6)
    m = ((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1])
    s += text(m, label, size=size)
    return s

def ellipse(c, rx, ry, dash=False, fill="none", w=1.4, stroke=STROKE):
    da = ' stroke-dasharray="5 4"' if dash else ''
    return (f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{w}"{da}/>')

def half_ellipse(c, rx, ry, upper, dash=False, w=1.4):
    """upper=True: back (upper) half; False: front (lower) half"""
    x0, x1, y = c[0] - rx, c[0] + rx, c[1]
    sweep = 1 if upper else 0
    da = ' stroke-dasharray="5 4"' if dash else ''
    return (f'<path d="M {f(x0)} {f(y)} A {f(rx)} {f(ry)} 0 0 {sweep} {f(x1)} {f(y)}" fill="none" '
            f'stroke="{STROKE}" stroke-width="{w}"{da}/>')

def hatch_def(pid="hatch", gap=6, angle=45, color="#444", w=1):
    return (f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{gap}" height="{gap}" '
            f'patternTransform="rotate({angle})"><line x1="0" y1="0" x2="0" y2="{gap}" stroke="{color}" '
            f'stroke-width="{w}"/></pattern>')

def right_angle(v, p, q, s=9, w=1.1):
    """small right-angle mark at vertex v between directions to p and q"""
    def unit(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); return dx / L, dy / L
    u = unit(v, p); t = unit(v, q)
    a = (v[0] + u[0] * s, v[1] + u[1] * s)
    b = (a[0] + t[0] * s, a[1] + t[1] * s)
    c = (v[0] + t[0] * s, v[1] + t[1] * s)
    return poly([a, b, c], close=False, w=w)
