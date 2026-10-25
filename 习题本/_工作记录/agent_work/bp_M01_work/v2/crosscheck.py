# Compare options/answers written in idea texts with those checked in verify_variants.py
import re, sys, io, contextlib
from fractions import Fraction as F
sys.path.insert(0, '.')
from bp_data import DAYS
CAP = {}
src = open('verify_variants.py', encoding='utf-8').read()
g = {}
def fake_check(vid, value, options, answer, tol=None, note=''):
    CAP[vid] = (options, answer)
src = src.replace('def check(', 'def _orig_check(')
g['check'] = fake_check
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, 'verify_variants.py', 'exec'), g)
def norm(x):
    if isinstance(x, str):
        s = x.replace('＋', '+').replace('~', '～').strip()
        m = re.fullmatch(r'(-?\d+(?:\.\d+)?)%', s)
        if m: return round(float(m.group(1)) / 100, 6)
        m = re.fullmatch(r'(\d+)/(\d+)', s)
        if m: return round(int(m.group(1)) / int(m.group(2)), 6)
        m = re.fullmatch(r'(-?\d+(?:\.\d+)?)(?:岁|万)?', s)
        if m: return round(float(m.group(1)), 6)
        return s
    return round(float(F(x)), 6)
bad = 0
for d in DAYS:
    for gr in d['groups']:
        for vid, dirn, seed, idea in gr['variants']:
            m = re.search(r'选项：(.*?)；答案(.*?)（', idea)
            if not m: print('NO-OPTS', vid); bad += 1; continue
            opts_txt = [o.strip() for o in m.group(1).split('／')]
            ans_txt = m.group(2).strip()
            vopts, vans = CAP[vid]
            if vid == '29-1-1':
                ok = ans_txt == 'C' and vans == 'C'
            elif vid == '39-8-2':
                ok = ans_txt.startswith('50～60') and vans == '50~60万元' and len(opts_txt) == 4
            else:
                a = sorted(map(str, map(norm, opts_txt))); b = sorted(map(str, map(norm, vopts)))
                ok = (a == b) and (norm(ans_txt) == norm(vans))
                if not ok: print('MISMATCH', vid, opts_txt, ans_txt, '| verify:', vopts, vans)
            bad += (not ok)
print('checked', sum(len(gr['variants']) for d in DAYS for gr in d['groups']), 'mismatches', bad)
