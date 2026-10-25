import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from split_q import load, flat_lines, split
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
qnum_res = [re.compile(r'^\s*(\d{1,3})\s*(?:[\.、．](?!\d)|\s{2,}|(?=[一-龥（(“]))'), re.compile(r'^\s*【\s*(\d{1,3})\s*】'),
            re.compile(r'第\s*【\s*(\d{1,3})\s*】\s*题'), re.compile(r'【\s*题目\s*(\d{1,3})\s*】'), re.compile(r'^\s*题目\s*(\d{1,3})(?!\d)'),
            re.compile(r'【\s*解析\s*(\d{1,3})'), re.compile(r'^\s*第\s*(\d{1,3})\s*题'), re.compile(r'^\s*(\d{1,3})\s*$'), re.compile(r'^\s*(\d{1,3})\s*[～~、,，\.]?\s*正确答?案')]
SEARCH = {1, 2, 3, 5}
ans_res = [re.compile(r'【\s*解析\s*\d{1,3}\s*[—\-－–]+\s*正确答案\s*([A-D])'), re.compile(r'正确答?案?\s*(?:为|是)?\s*[：:=]?\s*([A-D])'), re.compile(r'【\s*答\s*\d*\s*案\s*\d*\s*】\s*([A-D])'),
           re.compile(r'因此[，,]\s*选择\s*([A-D])'), re.compile(r'(?:故|因此)[，,]?\s*本题(?:答案)?(?:选|为)\s*([A-D])'), re.compile(r'答案\s*(?:为|是)\s*([A-D])')]
def find_qstarts(lines):
    # candidates: (idx, n); choose longest strictly increasing subsequence (prefer consecutive)
    cands = []
    for i, L in enumerate(lines):
        t = L['text']
        for r in qnum_res:
            m = r.search(t) if qnum_res.index(r) in SEARCH else r.match(t)
            if m:
                n = int(m.group(1))
                if 0 < n < 200: cands.append((i, n))
                break
    if not cands: return []
    import bisect
    # LIS O(n log n) on n values with reconstruction
    tails, tails_idx, prev = [], [], [None] * len(cands)
    for k, (i, n) in enumerate(cands):
        pos = bisect.bisect_left(tails, n)
        if pos == len(tails): tails.append(n); tails_idx.append(k)
        else: tails[pos] = n; tails_idx[pos] = k
        prev[k] = tails_idx[pos - 1] if pos > 0 else None
    k = tails_idx[-1]; seq = []
    while k is not None: seq.append(cands[k]); k = prev[k]
    return seq[::-1]
def parse_answers(name):
    doc = load(name)
    lines = flat_lines(doc)
    starts = find_qstarts(lines)
    ans, seg = {}, {}
    global LINES
    LINES = {}
    global STARTS
    STARTS = [(n, lines[i]['page'], lines[i]['top']) for (i, n) in starts]
    for j, (i, n) in enumerate(starts):
        e = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
        block = [L['text'] for L in lines[i:e]]
        seg[n] = '\n'.join(block)
        LINES[n] = [(L['page'], L['top'], L['bottom']) for L in lines[i:e]]
        for t in block:
            for r in ans_res:
                m = r.search(t)
                if m: ans[n] = m.group(1); break
            if n in ans: break
    return ans, seg
if __name__ == '__main__':
    for f in sorted(glob.glob(S + '/lines/*.json')):
        name = os.path.basename(f)[:-5]
        if not re.search(r'解析|答案', name): continue
        ans, seg = parse_answers(name)
        ks = sorted(ans)
        print(name[:46].ljust(46), len(ans), (ks[0], ks[-1]) if ks else None, 'missing:', [k for k in range(ks[0], ks[-1]+1) if k not in ans][:15] if ks else '')
