"""Hand-located 解析 for 资料 questions the automatic start detection skipped ("119、2011年…" reads as a number run)."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from split_q import load, flat_lines
import zl_build as Z
import zl_crop as C
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
def locate(jf, n):
    lines = flat_lines(load(jf))
    st = [i for i, L in enumerate(lines) if re.match(rf'^\s*{n}\s*[、\.．]', L['text'])]
    nx = [i for i, L in enumerate(lines) if re.match(rf'^\s*{n + 1}\s*[、\.．]', L['text'])]
    if not st: return None
    a = lines[st[0]]
    b = lines[nx[0]] if nx and nx[0] > st[0] else None
    jdoc = load(jf)
    if b: regs = Z.span(jdoc, a['page'], a['top'], b['page'], b['top'])
    else:
        end = min(len(lines), st[0] + 40)
        seg = lines[st[0]:end]
        regs = Z.span(jdoc, a['page'], a['top'], seg[-1]['page'], seg[-1]['bottom'] + 2)
    return Z.cut_jiexi(jdoc, regs)
if __name__ == '__main__':
    todo = {'2015GK-Z119': 'C', '2017JSA-Z135': 'C', '2019ZJA-Z126': 'C'}
    raw = json.load(open(S + '/db/zl_raw.json'))
    by = {r['id']: r for r in raw}
    fix = json.load(open(S + '/db/zl_fixes.json'))
    for i, ans in todo.items():
        r = by[i]
        regs = locate(r['jfile'], r['num'])
        r['jiexi_regions'] = regs
        C.build_jiexi([r], force=True)
        fix[i] = {'answer': ans, 'source': '官方解析（手动定位）'}
        print(i, regs)
    json.dump(raw, open(S + '/db/zl_raw.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(fix, open(S + '/db/zl_fixes.json', 'w'), ensure_ascii=False, indent=1)
