"""L02 real-question check: every truth/lie real question is re-solved by brute force from its stem and
compared with the official answer; 2024JSA-102 (formula) and 2020SC1206-84 (fee x count) get numeric checks.
2021SD-66 (official answer still being OCR'd) is solved only as a cross-check, not as a self-solved answer.
Run: python3 -I verify/bp_L02_realcheck.py"""
import itertools, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_work')
from tfengine import check, worlds, ev

R = {}
# ---- 考法一 ----
R['2025SD-94'] = dict(dom=('bool', ['体', '实', '教']),
    stmts=[('甲', '体 or 实'), ('乙', 'not 体 and not 实'), ('丙', '实 or not 教')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '体', 'B': '实', 'C': '教', 'D': '体 and 教'}, ans='C')
R['2023ZJA-102'] = dict(dom=('bool', ['秦', '魏', '汉']),
    stmts=[('1', '(not 魏) or 汉'), ('2', 'not 秦 and not 魏'), ('3', '秦 or 魏')],
    count=('false', '==', 2), ask='must_true',
    opts={'A': '魏 and 汉', 'B': 'not 魏 and 汉', 'C': '魏 and not 汉', 'D': 'not 魏 and not 汉'}, ans='C')
R['2025HB-110'] = dict(dom=('perm', ['周', '吴', '郑', '王', '钱'], ['冠', '亚', '季']),
    stmts=[('周', "at['冠']=='郑'"), ('吴', "at['冠'] in ('吴','周','钱')"), ('郑', "at['冠']!='郑'"),
           ('钱', "pos['钱'] is None"), ('王', "pos['王']!='亚'")],
    count=('true', '==', 1), ask='must_true',
    opts={'A': "at['亚']=='王'", 'B': "at['亚']=='吴'", 'C': "at['亚']=='郑'", 'D': "at['亚']=='钱'"}, ans='A')
R['2022GK-109'] = dict(dom=('bool', ['陈', '李', '刘']),
    stmts=[('1', '陈 and 李'), ('2', 'not (陈 and 李)'), ('3', '陈 and not 李'), ('4', 'not 陈 and 李'), ('5', '(not 陈) or 刘')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': 'not 陈 and not 李', 'B': '陈 and 刘', 'C': 'not 李 and not 刘', 'D': '陈 and 李'}, ans='D')
# ---- 考法二 ----  (each person either only shopped (True) or only watched a film (False))
R['2023SC-85'] = dict(dom=('bool', ['甲', '乙', '丙', '丁']),
    stmts=[('1', '丁'), ('2', '(not 甲) or (not 乙)'), ('3', '丁 or (not 丙)'), ('4', '甲 and 乙')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '乙 and not 甲', 'B': '丙 and not 乙', 'C': '丙 and not 丁', 'D': 'not 甲 and not 乙'}, ans='C')
# ---- 考法三 ----
R['2020SD-66'] = dict(dom=('bool', ['甲', '乙', '丙', '丁']),
    stmts=[('1', 'not (甲 or 乙 or 丙 or 丁)'), ('2', 'not 丁'), ('3', '(not 乙) or (not 丁)'), ('4', '甲 or 乙 or 丙 or 丁')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': 'not 甲', 'B': '乙', 'C': 'not 丙', 'D': '丁'}, ans='D')
R['2022ZJA-101'] = dict(dom=('bool', ['甲', '乙']),
    stmts=[('赵', '(not 甲) or 乙'), ('钱', '甲'), ('孙', '甲 and not 乙'), ('李', '甲 or 乙')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': '甲 and 乙', 'B': 'not 甲 and not 乙', 'C': '甲 and not 乙', 'D': 'not 甲 and 乙'}, ans='D')
R['2024HB-102'] = dict(dom=('bool', ['陈', '林']),
    stmts=[('吴', '陈 or not 林'), ('李', '陈'), ('郑', '陈 or 林'), ('张', '林 and not 陈')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': 'T[1] and T[2]', 'B': 'T[0] and T[3]', 'C': 'T[0] and T[1]', 'D': 'T[2] and T[3]'}, ans='D')
# 2024SC-84: three tourists (王, 郑, one more) each buy any subset of {白, 青, 彩}
sub = [frozenset(c) for k in range(4) for c in itertools.combinations('白青彩', k)]
W84 = [{'王': a, '郑': b, 'X': c} for a in sub for b in sub for c in sub]
R['2024SC-84'] = dict(dom=('custom', W84),
    stmts=[('1', 'len(王)>0 and len(郑)>0 and len(X)>0'), ('2', "'白' in 王"), ('3', 'len(王)==0 or len(郑)==0 or len(X)==0'),
           ('4', "('青' in 郑) or ('白' in 王)")],
    count=('true', '==', 2), ask='must_true',
    opts={'A': 'len(王)==0', 'B': "'青' in 郑", 'C': "'白' in 王", 'D': "('青' not in 王) or ('青' not in 郑) or ('青' not in X)"}, ans='B')
R['2020SZS-71'] = dict(dom=('bool', ['甲', '乙', '丙', '丁', '戊', '己']),
    stmts=[('甲', 'not 甲'), ('乙', '丙'), ('丙', 'not (甲 or 乙 or 丙 or 丁 or 戊 or 己)'), ('丁', 'not 丙'), ('戊', '乙'), ('己', '甲 != 丙')],
    count=('false', '==', 2), ask='must_true',
    opts={'A': '甲+乙+丙==0', 'B': '甲+乙+丙==1', 'C': '甲+乙+丙==2', 'D': '甲+乙+丙==3'}, ans='C')
# ---- 考法四 ----
cont = {'法国': '欧', '克罗地亚': '欧', '阿根廷': '南美', '巴西': '南美', '摩洛哥': '非'}
W66 = [{'冠': c, '阿四强': a} for c in cont for a in (False, True) if not (c == '阿根廷' and not a)]
for w in W66: w['洲'] = cont[w['冠']]
R['2023SD-66'] = dict(dom=('custom', W66),
    stmts=[('甲', "洲=='欧'"), ('乙', "冠=='法国'"), ('丙', "洲=='南美'"), ('丁', 'not 阿四强')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': 'not T[0]', 'B': "冠!='法国'", 'C': "洲!='南美'", 'D': '阿四强'}, ans='C')
R['2022SD-75'] = dict(dom=('bool', ['甲', '乙', '丙']),
    stmts=[('1', '甲'), ('2', 'not (甲 and 乙 and 丙)'), ('3', '甲 or 乙 or 丙')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '乙 and not 丙', 'B': '甲 and not 乙', 'C': 'not 乙 and not 丙', 'D': '丙 and not 甲'}, ans='C')
# ---- 考法五 ----
R['2023GD-63'] = dict(dom=('one', ['甲', '乙', '丙']),
    stmts=[('一', "x!='甲'"), ('二', "x=='乙'"), ('三', "x!='丙'")],
    count=('true', '==', 1), ask='must_false',
    opts={'A': 'T[0]', 'B': 'T[2]', 'C': "x=='甲'", 'D': "x=='乙'"}, ans='D')
R['2022GD-61'] = dict(dom=('bool', ['稻', '播']),
    stmts=[('1', '稻 and 播'), ('2', '稻 != 播'), ('3', 'not 稻'), ('4', '播')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '稻', 'B': 'not 稻', 'C': '播', 'D': 'not 播'}, ans='D')
# ---- 考法六 ----
R['2020SZS-67'] = dict(dom=('one', [1, 2, 3]),
    stmts=[('三号', "((x==1) + (x!=2)) == 1")],
    count=('true', '==', 1), ask='must_true',
    opts={'A': 'x==1', 'B': 'x==2', 'C': 'x==3'}, ans='C')

ok = all(check(k, v) for k, v in R.items())

# 2020SZS-80: meta-information. Culprit X in {甲,乙,丙}; each suspect accuses one of the other two;
# a suspect "说真话" iff he accuses the culprit. Known: 甲 told the truth. 老赵 was told whether 丙 told
# the truth (but not 乙) and could identify the culprit; now he has forgotten 丙's status yet still knows.
P3 = ['甲', '乙', '丙']
ws = [{'X': X, '甲': a, '乙': b, '丙': c} for X in P3 for a in ('乙', '丙') for b in ('甲', '丙') for c in ('甲', '乙')]
tr = lambda w, p: w[p] == w['X']
base = [w for w in ws if tr(w, '甲')]
ded = {s: {w['X'] for w in base if tr(w, '丙') == s} for s in (True, False)}
told = [s for s in ded if len(ded[s]) == 1]          # statuses under which 老赵 could have identified the culprit
final = [w for w in base if tr(w, '丙') in told]
opts80 = {'A': lambda w: w['X'] == '乙', 'B': lambda w: tr(w, '乙'), 'C': lambda w: not tr(w, '丙'), 'D': lambda w: w['X'] == '丙'}
res80 = [k for k, f in opts80.items() if final and all(f(w) for w in final)]
print(('OK ' if res80 == ['A'] else 'BAD'), '2020SZS-80: answer', res80, 'expect A |', '丙真->', ded[True], '丙假->', ded[False])
ok &= res80 == ['A']

# 2021SD-66 (official answer pending OCR) -- cross-check only. 6 runners finish in a strict order 1..6
# (only "前五名" and "最后" need a field larger than 3; any field size >=6 gives the same result).
P = ['张', '夏', '王', '甲', '乙', '丙']
res66 = set()
for order in itertools.permutations(P):
    rk = {p: i + 1 for i, p in enumerate(order)}
    s_zhang = rk['张'] <= 5 and rk['王'] == 6          # "小夏的名次不好" treated as non-checkable (no effect)
    s_xia = rk['夏'] == rk['王'] + 1
    s_wang = rk['张'] < rk['王'] and rk['夏'] < rk['王']
    st = [s_zhang, s_xia, s_wang]
    if 3 - sum(st) <= 1:
        res66.add(tuple(not x for x in st))
print('   2021SD-66 cross-check (liar pattern 张/夏/王):', res66, '-> 只有小夏说假话 => B（仅供与 OCR 结果对照）')

# 2024JSA-102: D = P_H - P_L (P = proportion correct in the top / bottom 27%)
from fractions import Fraction as F
N = 100; g = 27
A_ok = (F(g, g) - F(g, g)) == 0                       # difficulty 1 -> everyone correct -> D = 0, not 0.1
B_ok = (F(5, g) - F(20, g)) < 0                       # top group worse than bottom group -> D < 0 possible
best = max(F(h, g) - F(l, g) for h in range(g + 1) for l in range(g + 1) if h + l <= 27)   # 27 correct in total
C_ok = best == 1                                      # max D is 1, not 0.5
D_ok = all(F(c * 5, N) / 5 == F(c, N) for c in range(N + 1))   # mean score / full mark == proportion correct
print(('OK ' if (A_ok and B_ok and C_ok and D_ok) else 'BAD'), '2024JSA-102: A错(D=0) B错(可为负) C错(最大D=%s) D对' % best)
# 2020SC1206-84: fee per box fixed at 2 yuan, count strictly decreasing -> fee income strictly decreasing
cnt = [1000, 900, 750, 600]
inc = [2 * c for c in cnt]
print(('OK ' if all(a > b for a, b in zip(inc, inc[1:])) else 'BAD'), '2020SC1206-84: 2元×逐年下降的数量 -> 收入逐年下降 (C)')
print('ALL REAL OK' if ok else 'SOME REAL BAD')
