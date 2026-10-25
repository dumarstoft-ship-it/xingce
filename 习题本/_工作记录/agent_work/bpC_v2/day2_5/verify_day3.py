# -*- coding: utf-8 -*-
"""第3天（C03 首次）改编骨架验算。"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bpC_v2')
from lib import *
from itertools import permutations, product, combinations

# ---------- G1-a 名额筛选：一定入选
cand = {'甲': ('街道办', '法律'), '乙': ('街道办', '农学'), '丙': ('街道办', '法律'),
        '丁': ('区直', '农学'), '戊': ('区直', '财会'), '己': ('事业', '财会'), '庚': ('事业', '规划')}
quota = {'街道办': 2, '区直': 1, '事业': 1}
S = []
for c in combinations(cand, 4):
    units = [cand[x][0] for x in c]; majors = [cand[x][1] for x in c]
    if any(units.count(u) != q for u, q in quota.items()): continue
    if len(set(majors)) != 4: continue
    S.append(set(c))
print('G1-a 方案', S)
judge('D3-G1a', S, {'A': lambda s: '甲' in s, 'B': lambda s: '丁' in s, 'C': lambda s: '戊' in s, 'D': lambda s: '己' in s}, 'must', 'C')

# ---------- G1-b 数合规组合（2名机关+1名社区，主题各不相同）
jg = {'甲': '党史', '乙': '法治', '丙': '党史', '丁': '生态'}
sq = {'戊': '法治', '己': '民生', '庚': '生态'}
cnt = 0
for a, b in combinations(jg, 2):
    for c in sq:
        th = [jg[a], jg[b], sq[c]]
        if len(set(th)) == 3: cnt += 1
count_options('D3-G1b', cnt, {'A': 7, 'B': 8, 'C': 9, 'D': 10}, 'C')

# ---------- G1-c 名额+科目+条件句：四个完整组合，各暴露一类错误
cand = {'甲': ('高一', '历史'), '乙': ('高一', '地理'), '丙': ('高一', '数学'), '丁': ('高二', '语文'),
        '戊': ('高二', '历史'), '己': ('高三', '政治'), '庚': ('高三', '英语')}
quota = {'高一': 2, '高二': 1, '高三': 1}
def valid(c, why=False):
    units = [cand[x][0] for x in c]; subj = [cand[x][1] for x in c]
    r = []
    if any(units.count(u) != q for u, q in quota.items()): r.append('名额')
    if len(set(subj)) != len(subj): r.append('科目重复')
    if '地理' in subj and '己' in c: r.append('条件句')   # 如果抽调地理老师，则不抽调高三的政治老师
    return r if why else not r
opts = {'A': ('甲', '乙', '丁', '己'), 'B': ('乙', '丙', '戊', '庚'), 'C': ('甲', '丙', '戊', '庚'), 'D': ('甲', '丁', '己', '庚')}
res = {k: valid(v, True) for k, v in opts.items()}
print('G1-c 各选项违反', res)
assert [k for k, v in res.items() if not v] == ['B']
print('[OK] D3-G1c -> B（A违反条件句，C科目重复，D名额不对）')

# ---------- G2-a 1男2女 + "如果选周或吴，那么选孙"
M = ['赵', '钱', '孙']; F = ['李', '周', '吴', '郑']
S = []
for m in M:
    for f in combinations(F, 2):
        s = {m, *f}
        if ('周' in s or '吴' in s) and '孙' not in s: continue
        S.append(s)
print('G2-a 方案', S)
judge('D3-G2a', S, {'A': lambda s: '赵' in s or '李' in s, 'B': lambda s: '孙' in s or '郑' in s,
                    'C': lambda s: '钱' in s or '吴' in s, 'D': lambda s: '周' in s or '郑' in s}, 'must', 'B')

# ---------- G2-b 2男2女；(1)如果推选王，那么钱和孙都推选；(2)如果推选吴，那么不推选孙；问不可能
M = ['赵', '钱', '孙']; F = ['李', '刘', '王', '吴']
S = []
for m in combinations(M, 2):
    for f in combinations(F, 2):
        s = {*m, *f}
        if '王' in s and not ({'钱', '孙'} <= s): continue
        if '吴' in s and '孙' in s: continue
        S.append(s)
print('G2-b 方案', S)
judge('D3-G2b', S, {'A': lambda s: {'赵', '李'} <= s, 'B': lambda s: {'孙', '王'} <= s,
                    'C': lambda s: {'赵', '王'} <= s, 'D': lambda s: {'钱', '吴'} <= s}, 'impossible', 'C')

# ---------- G2-c 两个条件句 + 名额 -> 三支：7人选2男2女
M = ['甲', '乙', '丙']; F = ['丁', '戊', '己', '庚']
S = []
for m in combinations(M, 2):
    for f in combinations(F, 2):
        s = {*m, *f}
        if '甲' in s and '丁' in s: continue                       # 如果选甲，则不选丁
        if '丙' not in s and not ({'戊', '己'} <= s): continue     # 如果不选丙，则选戊和己
        S.append(s)
print('G2-c 方案', sorted(map(sorted, S)))
judge('D3-G2c', S, {'A': lambda s: '丙' in s or '戊' in s, 'B': lambda s: '乙' in s or '丁' in s,
                    'C': lambda s: '甲' in s or '庚' in s, 'D': lambda s: '戊' in s or '己' in s}, 'must', 'A')

# ---------- G2-d 项目入库：东(A1,A2,A3) 西(B1,B2) 北(C1,C2) 选4个，每片至少1个
proj = {'A1': '东', 'A2': '东', 'A3': '东', 'B1': '西', 'B2': '西', 'C1': '北', 'C2': '北'}
S = []
for c in combinations(proj, 4):
    s = set(c); regs = [proj[x] for x in c]
    if any(regs.count(r) < 1 for r in ('东', '西', '北')): continue
    if 'A1' in s and regs.count('西') != 1: continue        # 如果选A1，则西片只选1个
    if 'B2' in s and 'C1' in s: continue                    # B2和C1不能都选
    if ('A2' in s or 'A3' in s) and 'C2' not in s: continue   # 只要选A2或A3，就必须选C2
    S.append(s)
print('G2-d 方案', sorted(map(sorted, S)))
judge('D3-G2d', S, {'A': lambda s: 'C2' in s, 'B': lambda s: 'A1' in s, 'C': lambda s: 'B1' in s, 'D': lambda s: 'C1' not in s}, 'must')

# ---------- G3-a 新人/老员工分到A–D（无"每点至少1人"）；问不可能
NEW = ['甲', '乙', '丙']; OLD = ['张', '李', '王']; PP = NEW + OLD
def okb(s, cap=None):
    for p in 'ABCD':
        here = [x for x in PP if s[x] == p]
        if cap and len(here) > cap: return False
        if any(x in NEW for x in here) and not any(x in OLD for x in here): return False
    return True
S = [s for s in (dict(zip(PP, a)) for a in product('ABCD', repeat=6)) if okb(s) and s['张'] in 'AB' and s['乙'] == 'D']
print('G3-a 方案数', len(S))
judge('D3-G3a', S, {'A': lambda s: s['李'] == 'C' and s['王'] == 'C', 'B': lambda s: s['甲'] == 'B' and s['张'] == 'B',
                    'C': lambda s: s['丙'] == 'D', 'D': lambda s: s['王'] == 'A'}, 'impossible', 'A')

# ---------- G3-b 深化：每个点最多2人；张去A或B，乙去D，甲不去A；如果张去A，则必然
S = [s for s in (dict(zip(PP, a)) for a in product('ABCD', repeat=6)) if okb(s, cap=2) and s['张'] in 'AB' and s['乙'] == 'D' and s['甲'] != 'A']
S1 = [s for s in S if s['张'] == 'A']
print('G3-b 方案', S1)
judge('D3-G3b', S1, {'A': lambda s: s['丙'] == 'A', 'B': lambda s: s['李'] == 'D', 'C': lambda s: s['甲'] == 'C', 'D': lambda s: s['王'] == 'B'}, 'must', 'A')

# ---------- G3-c 3男3女分成3个2人组，每组一男一女
Mm = ['甲', '乙', '丙']; Ff = ['张', '李', '王']
S = []
for p in permutations(Ff):
    pair = dict(zip(Mm, p))      # 男 -> 同组女
    if pair['甲'] == '张': continue                                   # 甲不与张同组
    if pair['乙'] == '李' and pair['丙'] != '王': continue           # 如果乙与李同组，则丙与王同组
    if pair['丙'] == '李': continue                                   # 丙不与李同组
    S.append(pair)
print('G3-c 方案', S)
S2 = [p for p in S if p['乙'] == '张'] if False else S
judge('D3-G3c', S, {'A': lambda p: p['甲'] == '李', 'B': lambda p: p['乙'] == '张', 'C': lambda p: p['丙'] == '张', 'D': lambda p: p['乙'] == '李'}, 'must', 'A')

# ---------- G3-d 派车：9人3车每车3人，会开车的4人（甲乙丙丁），每车至少1名驾驶员
PP = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬']; DRV = {'甲', '乙', '丙', '丁'}
S = []
for a in product('123', repeat=9):
    if any(a.count(c) != 3 for c in '123'): continue
    s = dict(zip(PP, a))
    if any(not any(s[d] == c for d in DRV) for c in '123'): continue
    if s['甲'] == s['乙']: continue                 # 甲乙不同车
    if s['戊'] != s['丙']: continue                 # 戊与丙同车
    if s['己'] != s['丁'] and s['己'] != s['甲']: pass
    if s['壬'] != '3': continue                     # 壬坐3号车（去最远的村）
    if sum(1 for d in DRV if s[d] == '3') != 2: continue   # 去最远村的3号车需2名驾驶员轮换
    if s['丙'] == '3': continue                     # 丙不去最远的村
    S.append(s)
print('G3-d 方案数', len(S))
judge('D3-G3d', S, {'A': lambda s: s['丁'] == '3', 'B': lambda s: s['甲'] == '3', 'C': lambda s: s['戊'] == '3', 'D': lambda s: s['乙'] != '3'}, 'must')
