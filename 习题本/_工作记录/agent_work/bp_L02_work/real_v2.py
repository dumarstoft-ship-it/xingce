# -*- coding: utf-8 -*-
"""L02 real questions: independent brute-force re-check against the official answers (this run).
All 17 truth/lie questions are encoded from the stems (crop images read in this run); 2024JSA-102 and
2020SC1206-84 get numeric checks. Run: python3 -I bp_L02_work/real_v2.py"""
import itertools, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_work')
from v2engine import (check, record, bools, choose_one, exactly_true, exactly_false, at_most_false, summary)
from fractions import Fraction as F

# ---------------- 2025SD-94: 甲 体或实；乙 非体且非实；丙 实或非教；只有一真 -> 用于建设什么 ----------------
check('2025SD-94', bools(['体', '实', '教']),
      [lambda w: w['体'] or w['实'], lambda w: not w['体'] and not w['实'], lambda w: w['实'] or not w['教']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['体'], 'B': lambda w, T: w['实'], 'C': lambda w, T: w['教'],
       'D': lambda w, T: w['体'] and w['教']}, 'C')

# ---------------- 2023ZJA-102: (1)魏→汉 (2)非秦且非魏 (3)秦或魏；两项错误 ----------------
check('2023ZJA-102', bools(['秦', '魏', '汉']),
      [lambda w: (not w['魏']) or w['汉'], lambda w: not w['秦'] and not w['魏'], lambda w: w['秦'] or w['魏']],
      exactly_false(2), 'must',
      {'A': lambda w, T: w['魏'] and w['汉'], 'B': lambda w, T: not w['魏'] and w['汉'],
       'C': lambda w, T: w['魏'] and not w['汉'], 'D': lambda w, T: not w['魏'] and not w['汉']}, 'C')

# ---------------- 2025HB-110: 五人决赛，冠亚季各一人；只有一人的回答与结果相符；问亚军 ----------------
P5 = ['周', '吴', '郑', '王', '钱']
W110 = []
for c, y, j in itertools.permutations(P5, 3):
    W110.append({'冠': c, '亚': y, '季': j})
top3 = lambda w, p: p in (w['冠'], w['亚'], w['季'])
check('2025HB-110', W110,
      [lambda w: w['冠'] == '郑', lambda w: w['冠'] in ('吴', '周', '钱'), lambda w: w['冠'] != '郑',
       lambda w: not top3(w, '钱'), lambda w: w['亚'] != '王'],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['亚'] == '王', 'B': lambda w, T: w['亚'] == '吴', 'C': lambda w, T: w['亚'] == '郑',
       'D': lambda w, T: w['亚'] == '钱'}, 'A')

# ---------------- 2022GK-109 ----------------
check('2022GK-109', bools(['陈', '李', '刘']),
      [lambda w: w['陈'] and w['李'], lambda w: not (w['陈'] and w['李']), lambda w: w['陈'] and not w['李'],
       lambda w: not w['陈'] and w['李'], lambda w: (not w['陈']) or w['刘']],
      exactly_true(1), 'must',
      {'A': lambda w, T: not w['陈'] and not w['李'], 'B': lambda w, T: w['陈'] and w['刘'],
       'C': lambda w, T: not w['李'] and not w['刘'], 'D': lambda w, T: w['陈'] and w['李']}, 'D')

# ---------------- 2023SC-85: 每人要么只看电影要么只购物（True=购物）；只有一项为真 ----------------
check('2023SC-85', bools(['甲', '乙', '丙', '丁']),
      [lambda w: w['丁'], lambda w: (not w['甲']) or (not w['乙']), lambda w: w['丁'] or (not w['丙']),
       lambda w: w['甲'] and w['乙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['乙'] and not w['甲'], 'B': lambda w, T: w['丙'] and not w['乙'],
       'C': lambda w, T: w['丙'] and not w['丁'], 'D': lambda w, T: not w['甲'] and not w['乙']}, 'C')

# ---------------- 2020SD-66: 四家企业捐赠；两真两假 ----------------
any4 = lambda w: w['甲'] or w['乙'] or w['丙'] or w['丁']
check('2020SD-66', bools(['甲', '乙', '丙', '丁']),
      [lambda w: not any4(w), lambda w: not w['丁'], lambda w: (not w['乙']) or (not w['丁']), any4],
      exactly_true(2), 'must',
      {'A': lambda w, T: not w['甲'], 'B': lambda w, T: w['乙'], 'C': lambda w, T: not w['丙'],
       'D': lambda w, T: w['丁']}, 'D')

# ---------------- 2022ZJA-101 ----------------
check('2022ZJA-101', bools(['甲', '乙']),
      [lambda w: (not w['甲']) or w['乙'], lambda w: w['甲'], lambda w: w['甲'] and not w['乙'],
       lambda w: w['甲'] or w['乙']],
      exactly_true(2), 'must',
      {'A': lambda w, T: w['甲'] and w['乙'], 'B': lambda w, T: not w['甲'] and not w['乙'],
       'C': lambda w, T: w['甲'] and not w['乙'], 'D': lambda w, T: not w['甲'] and w['乙']}, 'D')

# ---------------- 2024HB-102: 陈/林 带队；两对两错；问猜对的是谁 ----------------
check('2024HB-102', bools(['陈', '林']),
      [lambda w: w['陈'] or not w['林'], lambda w: w['陈'], lambda w: w['陈'] or w['林'],
       lambda w: w['林'] and not w['陈']],
      exactly_true(2), 'must',
      {'A': lambda w, T: T[1] and T[2], 'B': lambda w, T: T[0] and T[3], 'C': lambda w, T: T[0] and T[1],
       'D': lambda w, T: T[2] and T[3]}, 'D')

# ---------------- 2024SC-84: 王、郑和至少一名其他游客；每人买 白/青/其他瓷 的任意组合 ----------------
W84 = []
for wang in itertools.product([0, 1], repeat=3):          # (白, 青, 其他)
    for zheng in itertools.product([0, 1], repeat=3):
        for other in itertools.product([0, 1], repeat=3):
            W84.append({'王': wang, '郑': zheng, '他': other})
bought = lambda t: any(t)
check('2024SC-84', W84,
      [lambda w: all(bought(w[p]) for p in ('王', '郑', '他')), lambda w: w['王'][0] == 1,
       lambda w: not all(bought(w[p]) for p in ('王', '郑', '他')), lambda w: w['郑'][1] == 1 or w['王'][0] == 1],
      exactly_true(2), 'must',
      {'A': lambda w, T: not bought(w['王']), 'B': lambda w, T: w['郑'][1] == 1, 'C': lambda w, T: w['王'][0] == 1,
       'D': lambda w, T: any(w[p][1] == 0 for p in ('王', '郑', '他'))}, 'B')

# ---------------- 2020SZS-71: 六人（甲乙丙丁戊己），两人说谎；问甲乙丙中完成的人数 ----------------
P6 = ['甲', '乙', '丙', '丁', '戊', '己']
check('2020SZS-71', bools(P6),
      [lambda w: not w['甲'], lambda w: w['丙'], lambda w: not any(w[p] for p in P6), lambda w: not w['丙'],
       lambda w: w['乙'], lambda w: w['甲'] != w['丙']],
      exactly_false(2), 'must',
      {k: (lambda n: (lambda w, T: w['甲'] + w['乙'] + w['丙'] == n))(n) for k, n in zip('ABCD', range(4))}, 'C')

# ---------------- 2023SD-66: 冠军所在洲；只有一句为假 ----------------
CONT = {'法国': '欧', '克罗地亚': '欧', '阿根廷': '南美', '巴西': '南美', '摩洛哥': '非'}
W66 = [{'冠': c, '阿四强': a} for c in CONT for a in (False, True) if not (c == '阿根廷' and not a)]
check('2023SD-66', W66,
      [lambda w: CONT[w['冠']] == '欧', lambda w: w['冠'] == '法国', lambda w: CONT[w['冠']] == '南美',
       lambda w: not w['阿四强']],
      exactly_false(1), 'must',
      {'A': lambda w, T: not T[0], 'B': lambda w, T: w['冠'] != '法国', 'C': lambda w, T: CONT[w['冠']] != '南美',
       'D': lambda w, T: w['阿四强']}, 'C')

# ---------------- 2022SD-75 ----------------
check('2022SD-75', bools(['甲', '乙', '丙']),
      [lambda w: w['甲'], lambda w: not (w['甲'] and w['乙'] and w['丙']), lambda w: w['甲'] or w['乙'] or w['丙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['乙'] and not w['丙'], 'B': lambda w, T: w['甲'] and not w['乙'],
       'C': lambda w, T: not w['乙'] and not w['丙'], 'D': lambda w, T: w['丙'] and not w['甲']}, 'C')

# ---------------- 2021SD-66 (official answer now available: B) ----------------
# 6 runners in a strict order; "小夏的名次不好" is not checkable and is ignored (as in the official solution).
W2166 = []
for order in itertools.permutations(['张', '夏', '王', 'a', 'b', 'c']):
    W2166.append({p: i + 1 for i, p in enumerate(order)})
check('2021SD-66', W2166,
      [lambda r: r['张'] <= 5 and r['王'] == 6, lambda r: r['夏'] == r['王'] + 1,
       lambda r: r['张'] < r['王'] and r['夏'] < r['王']],
      at_most_false(1), 'must',
      {'A': lambda r, T: not T[0], 'B': lambda r, T: not T[1], 'C': lambda r, T: not T[2], 'D': lambda r, T: all(T)},
      'B', note='(official B; field size 6 here; sizes 3-8 were also tried: always "only 小夏 lies")')

# ---------------- 2023GD-63: 三人一人通过；只有一名专家预测正确；问必然错误 ----------------
check('2023GD-63', choose_one(['甲', '乙', '丙']),
      [lambda w: w['x'] != '甲', lambda w: w['x'] == '乙', lambda w: w['x'] != '丙'],
      exactly_true(1), 'never',
      {'A': lambda w, T: T[0], 'B': lambda w, T: T[2], 'C': lambda w, T: w['x'] == '甲', 'D': lambda w, T: w['x'] == '乙'},
      'D')

# ---------------- 2022GD-61 ----------------
check('2022GD-61', bools(['稻', '播']),
      [lambda w: w['稻'] and w['播'], lambda w: w['稻'] != w['播'], lambda w: not w['稻'], lambda w: w['播']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['稻'], 'B': lambda w, T: not w['稻'], 'C': lambda w, T: w['播'], 'D': lambda w, T: not w['播']},
      'D')

# ---------------- 2020SZS-67: 3号门的话为真 ----------------
check('2020SZS-67', choose_one([1, 2, 3]),
      [lambda w: ((w['x'] == 1) + (w['x'] != 2)) == 1],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['x'] == 1, 'B': lambda w, T: w['x'] == 2, 'C': lambda w, T: w['x'] == 3}, 'C')

# ---------------- 2020SZS-80: 元信息 ----------------
# Culprit X; each suspect accuses one of the other two; a suspect "说真话" iff his accusation names X.
S3 = ['甲', '乙', '丙']
worlds80 = [dict(X=X, 甲=a, 乙=b, 丙=c) for X in S3 for a in ('乙', '丙') for b in ('甲', '丙') for c in ('甲', '乙')]
truthful = lambda w, p: w[p] == w['X']
base80 = [w for w in worlds80 if truthful(w, '甲')]                       # (2) 甲说了真话
culprits_given = {s: {w['X'] for w in base80 if truthful(w, '丙') == s} for s in (True, False)}
told_status = [s for s, xs in culprits_given.items() if len(xs) == 1]    # (4)+当时推测出了真凶
final80 = [w for w in base80 if truthful(w, '丙') in told_status]
opts80 = {'A': lambda w: w['X'] == '乙', 'B': lambda w: truthful(w, '乙'), 'C': lambda w: not truthful(w, '丙'),
          'D': lambda w: w['X'] == '丙'}
hits80 = [k for k, f in opts80.items() if final80 and all(f(w) for w in final80)]
record('2020SZS-80', hits80 == ['A'],
       f'hits={hits80} expect=A | 丙真->{culprits_given[True]} 丙假->{culprits_given[False]} (only "丙真" lets 老赵 decide)')

# ---------------- 2024JSA-102 (numeric) ----------------
N, g = 100, 27                                   # 100 examinees, top / bottom 27 each
A_wrong = (F(g, g) - F(g, g)) != F(1, 10)        # difficulty 1 -> P_H = P_L = 1 -> D = 0
B_wrong = min(F(h, g) - F(l, g) for h in range(g + 1) for l in range(g + 1)) < 0
maxD = max(F(h, g) - F(l, g) for h in range(g + 1) for l in range(g + 1) if h + l <= 27)  # 27 correct overall
C_wrong = maxD != F(1, 2)
D_right = all(F(c * 5, N) / 5 == F(c, N) for c in range(N + 1))   # mean score / full mark = proportion correct
record('2024JSA-102', A_wrong and B_wrong and C_wrong and D_right, f'A错 B错 C错(max D={maxD}) D对 -> D')

# ---------------- 2020SC1206-84 (numeric direction) ----------------
counts = [1000, 900, 750, 600]
record('2020SC1206-84', all(2 * a > 2 * b for a, b in zip(counts, counts[1:])), '单价2元不变×数量逐年下降 -> 收入逐年下降 (C)')

ok = summary()
sys.exit(0 if ok else 1)
