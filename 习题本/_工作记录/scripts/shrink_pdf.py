"""Shrink a rendered workbook PDF: Chromium embeds our grayscale crops as 8-bit RGB. Re-encode every image as
4-bit grayscale (16 levels, plenty for scanned text) with Flate + PNG "Up" predictor, which cuts the file
several times without visible loss."""
import sys, zlib
import numpy as np
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject, DictionaryObject

def to_gray(o):
    w, h = int(o['/Width']), int(o['/Height'])
    bpc = int(o.get('/BitsPerComponent', 8))
    raw = o.get_data()
    cs = o.get('/ColorSpace')
    ncomp = 1 if cs == '/DeviceGray' else 3
    if isinstance(cs, list) or (hasattr(cs, '__getitem__') and not isinstance(cs, str)):
        try:
            if cs[0] == '/ICCBased': ncomp = int(cs[1].get_object().get('/N', 3))
        except Exception: pass
    if bpc != 8 or len(raw) < w * h * ncomp: return None
    a = np.frombuffer(raw[:w * h * ncomp], np.uint8).reshape(h, w, ncomp)
    g = a[:, :, 0] if ncomp == 1 else (0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2])
    if '/SMask' in o:  # composite on white
        sm = o['/SMask'].get_object()
        m = np.frombuffer(sm.get_data()[:w * h], np.uint8).reshape(h, w) / 255.0
        g = g * m + 255 * (1 - m)
    return np.clip(g, 0, 255).astype(np.uint8)

def encode4(g):
    a = g >> 4
    h, w = a.shape
    if w % 2: a = np.hstack([a, np.full((h, 1), 15, np.uint8)])
    packed = ((a[:, 0::2] << 4) | a[:, 1::2]).astype(np.uint8)
    prev = np.vstack([np.zeros((1, packed.shape[1]), np.uint8), packed[:-1]])
    up = ((packed.astype(np.int16) - prev.astype(np.int16)) % 256).astype(np.uint8)
    rows = np.hstack([np.full((h, 1), 2, np.uint8), up])
    return zlib.compress(rows.tobytes(), 9)

def shrink(src, dst):
    r = PdfReader(src); w = PdfWriter(clone_from=r)
    done = set(); before = after = 0; skipped = 0
    for page in w.pages:
        xo = (page.get('/Resources') or {}).get('/XObject') or {}
        for name, ref in xo.items():
            o = ref.get_object()
            if o.get('/Subtype') != '/Image' or id(o) in done: continue
            done.add(id(o))
            g = to_gray(o)
            if g is None: skipped += 1; continue
            data = encode4(g)
            before += len(o._data or b''); after += len(data)
            for k in ('/SMask', '/Intent', '/Decode', '/DecodeParms', '/Interpolate'):
                if k in o: del o[k]
            o[NameObject('/Filter')] = NameObject('/FlateDecode')
            o[NameObject('/ColorSpace')] = NameObject('/DeviceGray')
            o[NameObject('/BitsPerComponent')] = NumberObject(4)
            o[NameObject('/DecodeParms')] = DictionaryObject({NameObject('/Predictor'): NumberObject(12), NameObject('/Colors'): NumberObject(1),
                                                              NameObject('/BitsPerComponent'): NumberObject(4), NameObject('/Columns'): NumberObject(g.shape[1])})
            o._data = data
    with open(dst, 'wb') as f: w.write(f)
    return before, after, skipped

if __name__ == '__main__':
    b, a, s = shrink(sys.argv[1], sys.argv[2])
    print('images', round(b / 1048576, 1), 'MB ->', round(a / 1048576, 1), 'MB; skipped', s)
