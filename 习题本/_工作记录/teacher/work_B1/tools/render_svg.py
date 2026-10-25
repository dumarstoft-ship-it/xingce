# 极简 SVG 渲染（只支持本批用到的 line / circle / polyline / text），用于目检图形
import sys, re
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
S = 3
root = ET.parse(src).getroot()
ns = '{http://www.w3.org/2000/svg}'
vb = [float(v) for v in root.get('viewBox').split()]
W, H = int(vb[2] * S), int(vb[3] * S)
im = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(im)
fs = float(root.get('font-size', 15))
font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', int(fs * S))

def walk(el, inherited):
    attrs = dict(inherited); attrs.update(el.attrib)
    tag = el.tag.replace(ns, '')
    sw = float(attrs.get('stroke-width', 1)) * S
    if tag == 'line':
        d.line([float(attrs['x1']) * S, float(attrs['y1']) * S, float(attrs['x2']) * S, float(attrs['y2']) * S], fill='black', width=int(sw))
    elif tag == 'polyline':
        pts = [float(v) * S for v in re.split(r'[ ,]+', attrs['points'].strip())]
        d.line(pts, fill='black', width=int(sw))
    elif tag == 'circle':
        cx, cy, r = float(attrs['cx']) * S, float(attrs['cy']) * S, float(attrs['r']) * S
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill='black')
    elif tag == 'text':
        d.text((float(attrs['x']) * S, float(attrs['y']) * S), el.text or '', font=font, fill='black', anchor='ls')
    for ch in el:
        walk(ch, attrs)

walk(root, {})
im.save(out)
print('rendered', out, im.size)
