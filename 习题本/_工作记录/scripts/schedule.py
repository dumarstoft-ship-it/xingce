"""Merge classification, dedupe, build module pools and the 42-day module schedule."""
import json, glob, re, os
from collections import Counter, defaultdict
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

MATH = {'M01': '基础应用：和差倍比与比例', 'M02': '不定方程与数字特性', 'M03': '工程问题', 'M04': '行程问题', 'M05': '经济利润',
        'M06': '排列组合', 'M07': '概率问题', 'M08': '几何问题', 'M09': '最值问题（抽屉与构造）', 'M10': '统筹优化与线性规划',
        'M11': '容斥问题', 'M12': '溶液混合与平均数', 'M13': '周期、日期与杂题', 'M14': '数论与计算'}
LOGIC = {'L01': '翻译推理', 'L02': '真假推理与归纳推理', 'L03': '加强论证', 'L04': '削弱论证', 'L05': '前提假设', 'L06': '原因解释', 'L07': '结构相似与论证评价'}
ZH = {'C01': '排序与位置', 'C02': '匹配对应', 'C03': '分组与选择', 'C04': '数量与大小比较', 'C05': '真假综合与多维混合'}
MATH_DAYS = {'M01': 4, 'M02': 3, 'M03': 3, 'M04': 4, 'M05': 3, 'M06': 4, 'M07': 3, 'M08': 4, 'M09': 3, 'M10': 3, 'M11': 2, 'M12': 2, 'M13': 2, 'M14': 2}
LOGIC_DAYS = {'L01': 7, 'L02': 4, 'L03': 6, 'L04': 6, 'L05': 6, 'L06': 7, 'L07': 6}
ZH_DAYS = {'C01': 10, 'C02': 10, 'C03': 8, 'C04': 7, 'C05': 7}
MATH_ORDER_R1 = ['M01', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M02', 'M09', 'M10', 'M11', 'M12', 'M13', 'M14']
MATH_ORDER_R3 = ['M01', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M02', 'M09', 'M10', 'M01', 'M04', 'M06', 'M08']
LOGIC_ORDER = ['L01', 'L03', 'L04', 'L05', 'L06', 'L07', 'L02']
ZH_ORDER = ['C01', 'C02', 'C03', 'C04', 'C05']
PRIO = {'GD': 0, 'GK': 1, 'ZJA': 2, 'ZJB': 2, 'SZ': 3, 'SZS': 3, 'SZ1': 3, 'JSA': 4, 'CQ': 5}

def src_prio(pid):
    code = re.sub(r'^\d{4}', '', pid)
    code = re.sub(r'\d+$', '', code)
    year = int(pid[:4])
    return (PRIO.get(code, 6), -year)

def math_schedule():
    days = MATH_ORDER_R1 + MATH_ORDER_R1 + MATH_ORDER_R3
    assert Counter(days) == Counter(MATH_DAYS), Counter(days)
    return days

def spaced(counts, order, n):
    """greedy: each day pick module with largest remaining/ideal ratio, avoid repeats within 2 days"""
    rem = dict(counts); out = []
    for d in range(n):
        best = None
        for m in order:
            if rem[m] == 0: continue
            if m in out[-2:] and sum(rem.values()) > rem[m]: continue
            # ideal spacing: next due time
            used = counts[m] - rem[m]
            due = used * n / counts[m]
            key = (due, order.index(m))
            if best is None or key < best[0]: best = (key, m)
        if best is None:
            best = (None, max(rem, key=rem.get))
        m = best[1]; out.append(m); rem[m] -= 1
    return out

def load_all():
    db = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    cls = {}
    for f in glob.glob(S + '/cls/out_*.jsonl'):
        for l in open(f):
            l = l.strip()
            if l:
                d = json.loads(l); cls[d['id']] = d
    return db, cls

def norm(t):
    t = re.sub(r'^\s*\d{1,3}\s*[\.、．]?', '', t or '')
    return re.sub(r'[^一-龥A-Za-z0-9]', '', t)

def dedupe(items):
    def sh(s, k=6): return {s[i:i + k] for i in range(max(1, len(s) - k + 1))}
    items = sorted(items, key=lambda r: src_prio(r['paper']))
    kept, kept_sh, dups = [], [], {}
    for r in items:
        s = norm(r['text'])[:160]
        if len(s) < 30:
            kept.append(r); kept_sh.append(None); continue
        g = sh(s)
        hit = None
        for k, kg in zip(kept, kept_sh):
            if kg is None: continue
            if len(g & kg) / max(1, min(len(g), len(kg))) > 0.75:
                hit = k; break
        if hit is not None:
            dups[r['id']] = hit['id']
        else:
            kept.append(r); kept_sh.append(g)
    return kept, dups

def build():
    db, cls = load_all()
    pools = defaultdict(list); skipped = []
    cand = []
    for qid, r in db.items():
        if r['kind'] not in ('数学运算', '逻辑'): continue
        c = cls.get(qid)
        if c is None: skipped.append((qid, 'unclassified')); continue
        if c.get('kind') not in ('数学运算', '逻辑') or not c.get('module'): skipped.append((qid, 'kind=' + str(c.get('kind')))); continue
        if c.get('incomplete') and not r.get('stem_text'): skipped.append((qid, 'incomplete')); continue
        cand.append(dict(r, **{'module': c['module'], 'kaofa': c.get('kaofa'), 'technique': c.get('technique'), 'difficulty': c.get('difficulty') or 2,
                               'needs_figure': c.get('needs_figure'), 'cls_note': c.get('note')}))
    kept, dups = dedupe(cand)
    for r in kept: pools[r['module']].append(r)
    return pools, skipped, dups

if __name__ == '__main__':
    pools, skipped, dups = build()
    print('skipped', len(skipped), Counter(s[1] for s in skipped))
    print('dups', len(dups))
    tot = Counter()
    for m in sorted(pools):
        rs = pools[m]
        name = MATH.get(m) or LOGIC.get(m) or ZH.get(m)
        nd = MATH_DAYS.get(m) or LOGIC_DAYS.get(m) or ZH_DAYS.get(m)
        per = 45 if m[0] in 'ML' else 15
        noans = sum(1 for r in rs if not r['answer_official'])
        gd = sum(1 for r in rs if 'GD' in r['paper'])
        print(f'{m} {name:<16} real={len(rs):4d} days={nd} real/day={len(rs)/nd:5.1f} var/day={per - len(rs)/nd:5.1f} noans={noans} GD={gd}')
        tot[m[0]] += len(rs)
    print(tot)
    print('math days', math_schedule())
    print('logic days', spaced(LOGIC_DAYS, LOGIC_ORDER, 42))
    print('zh days', spaced(ZH_DAYS, ZH_ORDER, 42))
