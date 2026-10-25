# -*- coding: utf-8 -*-
"""L02 blueprint -- planning-stage verification (this run, written from scratch from the idea texts in
blueprints/L02.json; it supersedes the interrupted run's verify/bp_L02_ideas.py, which is stale).

Every truth/lie design and every quantitative induction design is checked here under the id quoted at the
end of its idea (〔验算 Dxx-g-k〕 = day xx, group g, k-th variant entry of that group). A check passes only if
exactly the intended option satisfies the question; for unusual question types (identity, self-reference,
meta-information, supplement, "max simultaneously true") a dedicated enumeration is used.
Writers must still write their own solver per finished item (briefs/generate.md).
Run: python3 -I bp_L02_work/ideas_v2.py
"""
import itertools, sys
from fractions import Fraction as F
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_work')
from v2engine import (check, record, bools, choose_one, subsets_of_size, exactly_true, exactly_false,
                      at_most_false, at_most_true, more_true_than_false, summary)

B = lambda *names: bools(list(names))
cnt = lambda w, names: sum(1 for n in names if w[n])

# =====================================================================================================
# DAY 7
# =====================================================================================================
# ---- G1 考法一 ----
check('D07-1-1', B('污', '路', '场'),
      [lambda w: w['污'] or w['路'], lambda w: not w['污'] and not w['路'], lambda w: (not w['路']) or w['场'],
       lambda w: not w['场']],
      exactly_false(1), 'must',
      {'A': lambda w, T: w['污'], 'B': lambda w, T: w['路'], 'C': lambda w, T: not w['路'] and not w['场'],
       'D': lambda w, T: not (w['污'] or w['路'] or w['场'])}, 'C')
check('D07-1-2', choose_one('ABCD'),
      [lambda w: w['x'] == 'A', lambda w: w['x'] != 'A', lambda w: w['x'] in 'BC', lambda w: w['x'] != 'D'],
      exactly_true(1), 'must',
      {'A': lambda w, T: T[1] and w['x'] == 'B', 'B': lambda w, T: T[1] and w['x'] == 'D',
       'C': lambda w, T: T[3] and w['x'] == 'A', 'D': lambda w, T: T[0] and w['x'] == 'A'}, 'B')
check('D07-1-3', B('甲', '乙'),
      [lambda w: w['甲'] and w['乙'], lambda w: not w['甲'] or not w['乙'], lambda w: w['乙'] or not w['甲']],
      exactly_false(2), 'never',
      {'A': lambda w, T: w['甲'], 'B': lambda w, T: not w['乙'], 'C': lambda w, T: T[1], 'D': lambda w, T: w['乙']}, 'D')
check('D07-1-4', B('甲', '乙', '丙'),
      [lambda w: not (w['甲'] or w['乙'] or w['丙']), lambda w: w['甲'] or w['乙'] or w['丙'],
       lambda w: w['甲'] or not w['乙'], lambda w: (not w['丙']) or (not w['乙']), lambda w: not w['丙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['甲'] and w['乙'], 'B': lambda w, T: not w['甲'] and w['乙'] and w['丙'],
       'C': lambda w, T: w['甲'] and w['丙'] and not w['乙'], 'D': lambda w, T: w['甲'] and w['乙'] and w['丙']}, 'B')
check('D07-1-5', B('体', '饭', '托'),
      [lambda w: w['体'] or w['饭'], lambda w: not w['体'] and not w['饭'], lambda w: not w['托'],
       lambda w: (not w['托']) or w['饭']],
      exactly_true(1), 'undet',
      {'A': lambda w, T: w['托'], 'B': lambda w, T: w['饭'], 'C': lambda w, T: T[3], 'D': lambda w, T: w['体']}, 'D')
P4 = ['甲', '乙', '丙', '丁']
check('D07-1-6', bools(P4),
      [lambda w: cnt(w, P4) == 4, lambda w: cnt(w, P4) < 4, lambda w: w['甲'], lambda w: (not w['乙']) or w['丙'],
       lambda w: not w['丁']],
      exactly_true(1), 'must',
      {k: (lambda n: (lambda w, T: cnt(w, P4) == n))(n) for k, n in zip('ABCD', (1, 2, 3, 4))}, 'B')
# ---- G2 考法三 ----
check('D07-2-1', bools(P4),
      [lambda w: cnt(w, P4) == 0, lambda w: w['乙'] and w['丙'], lambda w: w['乙'], lambda w: cnt(w, P4) > 0],
      exactly_true(2), 'must',
      {'A': lambda w, T: T[0] and T[1], 'B': lambda w, T: T[1] and T[2], 'C': lambda w, T: T[2] and T[3],
       'D': lambda w, T: T[1] and T[3]}, 'C')
check('D07-2-2', B('甲', '乙', '丙'),
      [lambda w: w['甲'] and w['乙'] and w['丙'], lambda w: not (w['甲'] and w['乙'] and w['丙']), lambda w: w['甲'],
       lambda w: (not w['乙']) or (not w['丙'])],
      exactly_false(1), 'must',
      {'A': lambda w, T: w['甲'] and not w['乙'], 'B': lambda w, T: w['甲'] and not (w['乙'] and w['丙']),
       'C': lambda w, T: not w['丙'], 'D': lambda w, T: w['甲'] and w['乙'] and w['丙']}, 'B')
check('D07-2-3', B('A', 'B', 'C'),
      [lambda w: w['A'], lambda w: not w['A'], lambda w: (not w['B']) or w['C'], lambda w: w['B'] and not w['C'],
       lambda w: w['C']],
      exactly_true(2), 'must',
      {'A': lambda w, T: w['A'], 'B': lambda w, T: w['B'], 'C': lambda w, T: not w['C'], 'D': lambda w, T: w['B'] and w['C']},
      'C')
check('D07-2-4', bools(P4),
      [lambda w: cnt(w, P4) == 4, lambda w: cnt(w, P4) < 4, lambda w: w['甲'], lambda w: w['甲'] or w['乙']],
      exactly_true(2), 'may',
      {'A': lambda w, T: w['甲'], 'B': lambda w, T: not w['乙'], 'C': lambda w, T: cnt(w, P4) == 4,
       'D': lambda w, T: not w['丙'] and not w['丁']}, 'D')
check('D07-2-5', B('甲', '乙'),
      [lambda w: w['甲'], lambda w: not w['乙'], lambda w: w['乙'], lambda w: w['甲'] and w['乙']],   # 小陈：“小李说的不对”
      exactly_true(2), 'must',
      {'A': lambda w, T: w['甲'] and w['乙'], 'B': lambda w, T: w['甲'] and not w['乙'],
       'C': lambda w, T: not w['甲'] and w['乙'], 'D': lambda w, T: not w['甲'] and not w['乙']}, 'B')
# ---- G3 考法四 ----
check('D07-3-1', choose_one(['老林', '小吴', '小陈', '小郑']),
      [lambda w: w['x'] == '老林', lambda w: w['x'] == '小吴', lambda w: w['x'] != '小陈',
       lambda w: w['x'] not in ('小郑', '老林')],
      exactly_false(1), 'must',
      {k: (lambda i: (lambda w, T: not T[i]))(i) for k, i in zip('ABCD', range(4))}, 'A')
check('D07-3-2', B('甲', '乙', '丙'),
      [lambda w: w['甲'] or w['乙'] or w['丙'], lambda w: not (w['甲'] and w['乙'] and w['丙']), lambda w: not w['甲']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['甲'] and w['乙'] and w['丙'], 'B': lambda w, T: not (w['甲'] or w['乙'] or w['丙']),
       'C': lambda w, T: w['甲'] and not w['乙'], 'D': lambda w, T: w['甲'] and not w['乙'] and not w['丙']}, 'A')
check('D07-3-3', B('广', '潮', '醒'),
      [lambda w: cnt(w, '广潮醒') >= 2, lambda w: w['广'] and not w['潮'] and not w['醒'], lambda w: not w['潮'],
       lambda w: w['醒']],
      at_most_false(1), 'must',
      {'A': lambda w, T: w['广'] and not w['潮'] and not w['醒'], 'B': lambda w, T: w['广'] and w['醒'] and not w['潮'],
       'C': lambda w, T: cnt(w, '广潮醒') == 3, 'D': lambda w, T: w['醒'] and not w['广'] and not w['潮']}, 'B')
check('D07-3-4', B('甲', '乙', '丙'),
      [lambda w: w['甲'] or w['乙'], lambda w: not w['甲'] or not w['乙'], lambda w: w['甲'] and not w['丙'],
       lambda w: w['丙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: cnt(w, '甲乙丙') == 0, 'B': lambda w, T: w['甲'] and not w['乙'] and not w['丙'],
       'C': lambda w, T: w['乙'] and not w['甲'] and not w['丙'], 'D': lambda w, T: w['甲'] and w['乙']}, 'A')
check('D07-3-5', B('A', 'B', 'C'),
      [lambda w: w['A'] or w['B'] or w['C'], lambda w: not w['A'], lambda w: w['B'], lambda w: w['A'] and w['B'] and w['C']],
      exactly_true(1), 'must',
      {'A': lambda w, T: not w['B'], 'B': lambda w, T: w['A'], 'C': lambda w, T: cnt(w, 'ABC') == 0,
       'D': lambda w, T: w['C']}, 'A')
# ---- G4 考法五 ----
check('D07-4-1', choose_one(['甲', '乙', '丙']),
      [lambda w: w['x'] == '甲', lambda w: w['x'] != '乙', lambda w: w['x'] != '丙'],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['x'] == '乙', 'B': lambda w, T: w['x'] == '丙', 'C': lambda w, T: w['x'] != '甲',
       'D': lambda w, T: T[2]}, 'C')
check('D07-4-2', subsets_of_size(P4, 2),
      [lambda w: '甲' in w['S'], lambda w: '甲' in w['S'] or '乙' in w['S'], lambda w: not ({'丙', '丁'} & w['S']),
       lambda w: ('丁' not in w['S']) or ('甲' in w['S'])],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['S'] == {'甲', '丁'}, 'B': lambda w, T: w['S'] == {'乙', '丙'},
       'C': lambda w, T: w['S'] == {'乙', '丁'}, 'D': lambda w, T: w['S'] == {'丙', '丁'}}, 'C')
check('D07-4-3', choose_one(P4),
      [lambda w: w['x'] != '甲', lambda w: w['x'] == '乙', lambda w: w['x'] in ('乙', '丙'), lambda w: w['x'] != '丁'],
      exactly_true(1), 'never',
      {'A': lambda w, T: T[0], 'B': lambda w, T: T[3], 'C': lambda w, T: w['x'] == '甲', 'D': lambda w, T: T[2]}, 'D')
check('D07-4-4', B('骑', '狮', '侨'),
      [lambda w: cnt(w, ['骑', '狮', '侨']) == 3, lambda w: cnt(w, ['骑', '狮', '侨']) == 1, lambda w: not w['骑'],
       lambda w: w['狮']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['骑'], 'B': lambda w, T: not w['狮'], 'C': lambda w, T: not w['侨'],
       'D': lambda w, T: cnt(w, ['骑', '狮', '侨']) == 1}, 'C', show=True)

# ---- G7 考法十一（数量） ----
record('D07-7-2', 1.08 * 0.97 > 1 and abs(1.08 * 0.97 - 1.11) > 0.05, f'总额倍数 1.08×0.97={1.08 * 0.97:.4f}（增加约4.8%，不是11%）')
new, tot = F(50, 100) * F(9, 10), 1          # 2025 new-energy share × total (2024 total = 1)
record('D07-7-3', new > F(40, 100) and new / F(40, 100) == F(9, 8) and (F(50, 100) * F(9, 10)) / F(60, 100) == F(3, 4),
       f'新能源 0.45/0.40=1.125（+12.5%）；燃油 0.45/0.60=0.75（-25%）')
avg = F(82 * 1 + 78 * 2, 3)
record('D07-7-4', avg < 80, f'加权平均 (82+78×2)/3={float(avg):.2f} < 80')

# =====================================================================================================
# DAY 14
# =====================================================================================================
# ---- G1 考法一 ----
check('D14-1-1', B('甲', '乙', '丙'),
      [lambda w: w['甲'] and w['乙'], lambda w: not (w['甲'] and w['乙']), lambda w: not w['甲'] and w['乙'],
       lambda w: (not w['乙']) or w['丙'], lambda w: w['丙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: T[0], 'B': lambda w, T: T[1], 'C': lambda w, T: T[3], 'D': lambda w, T: T[4]}, 'A')
T5 = ['甲', '乙', '丙', '丁', '戊']
W5 = []
for p in itertools.permutations(T5, 3):
    W5.append({'一': p[0], '二': p[1], '三': p[2]})
prized = lambda w, t: t in (w['一'], w['二'], w['三'])
check('D14-1-2', W5,
      [lambda w: w['一'] == '丙', lambda w: w['一'] in ('甲', '乙', '丁', '戊'), lambda w: not prized(w, '甲'),
       lambda w: w['二'] == '戊', lambda w: w['一'] != '乙'],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['一'] == '乙', 'B': lambda w, T: w['二'] == '甲', 'C': lambda w, T: not prized(w, '戊'),
       'D': lambda w, T: w['三'] == '丙'}, 'A')
# ---- G2 考法二 ----
check('D14-2-1', B('研', '宿', '展'),
      [lambda w: (not w['研']) or w['宿'], lambda w: w['研'] and not w['宿'], lambda w: not w['宿'], lambda w: w['展']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['研'] and w['宿'], 'B': lambda w, T: w['宿'] and not w['展'],
       'C': lambda w, T: w['研'] and not w['宿'], 'D': lambda w, T: not (w['研'] or w['宿'] or w['展'])}, 'B')
check('D14-2-2', B('海', '龙'),
      [lambda w: (not w['龙']) or w['海'], lambda w: w['龙'] and not w['海'], lambda w: w['海'] and w['龙'],
       lambda w: not w['海']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['海'] and not w['龙'], 'B': lambda w, T: w['龙'] and not w['海'],
       'C': lambda w, T: w['海'] and w['龙'], 'D': lambda w, T: not w['海'] and not w['龙']}, 'A')
check('D14-2-3', B('选', '三'),
      [lambda w: w['选'] != w['三'], lambda w: w['选'] == w['三'], lambda w: w['选'], lambda w: (not w['选']) or w['三'],
       lambda w: not w['三']],
      exactly_true(2), 'must',
      {'A': lambda w, T: w['选'] and w['三'], 'B': lambda w, T: w['选'] and not w['三'],
       'C': lambda w, T: w['三'] and not w['选'], 'D': lambda w, T: not w['选'] and not w['三']}, 'C')
check('D14-2-4', B('甲', '乙', '丙'),
      [lambda w: cnt(w, '甲乙丙') >= 2, lambda w: cnt(w, '甲乙丙') <= 1, lambda w: w['甲'],
       lambda w: (not w['乙']) or w['丙'], lambda w: not w['乙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['乙'] and not w['甲'] and not w['丙'], 'B': lambda w, T: w['乙'] and w['丙'] and not w['甲'],
       'C': lambda w, T: w['甲'] and w['乙'] and not w['丙'], 'D': lambda w, T: cnt(w, '甲乙丙') == 0}, 'A')
T5b = ['A', 'B', 'C', 'D', 'E']
check('D14-2-5', bools(T5b),
      [lambda w: cnt(w, T5b) < 5, lambda w: cnt(w, T5b) == 5, lambda w: cnt(w, T5b) > 0, lambda w: not w['A']],
      exactly_false(1), 'must',
      {'A': lambda w, T: cnt(w, T5b) == 5, 'B': lambda w, T: not w['A'] and cnt(w, 'BCDE') >= 1,
       'C': lambda w, T: cnt(w, T5b) == 0, 'D': lambda w, T: not w['A'] and cnt(w, 'BCDE') == 4}, 'B')
# ---- G3 考法三 ----
check('D14-3-1', B('张', '王'),
      [lambda w: (not w['王']) or w['张'], lambda w: w['张'] and w['王'], lambda w: w['张'], lambda w: w['王'] and not w['张']],
      exactly_true(2), 'must',
      {'A': lambda w, T: T[0] and T[1], 'B': lambda w, T: T[2] and T[3], 'C': lambda w, T: T[1] and T[2],
       'D': lambda w, T: T[0] and T[2]}, 'D')
check('D14-3-2', B('甲', '乙', '丙'),
      [lambda w: cnt(w, '甲乙丙') == 0, lambda w: (not w['乙']) or w['丙'], lambda w: w['乙'] and w['丙'],
       lambda w: cnt(w, '甲乙丙') > 0],
      exactly_true(2), 'undet',
      {'A': lambda w, T: not w['乙'], 'B': lambda w, T: T[1], 'C': lambda w, T: w['甲'], 'D': lambda w, T: T[2]}, 'C',
      show=True)
check('D14-3-3', B('甲', '乙', '丙', '丁', '戊'),     # 完成情况；说真话＝话为真（每人只说一句）
      [lambda w: w['乙'], lambda w: not w['丙'], lambda w: w['丙'], lambda w: w['甲'] and w['丙'], lambda w: not w['甲']],
      exactly_false(2), 'must',
      {'A': lambda w, T: w['乙'], 'B': lambda w, T: w['丙'], 'C': lambda w, T: not w['甲'],
       'D': lambda w, T: w['甲'] and w['丙']}, 'A')
check('D14-3-4', choose_one('ABCD'),
      [lambda w: w['x'] == 'A', lambda w: w['x'] != 'A', lambda w: w['x'] == 'B', lambda w: w['x'] in 'BC'],
      exactly_true(2), 'must',
      {k: (lambda c: (lambda w, T: w['x'] == c))(k) for k in 'ABCD'}, 'C')
# ---- G4 考法四 ----
check('D14-4-1', B('林', '周', '吴'),
      [lambda w: w['林'] and w['周'], lambda w: not w['林'] and not w['周'], lambda w: w['周'], lambda w: (not w['周']) or w['吴']],
      exactly_false(1), 'must',
      {'A': lambda w, T: cnt(w, '林周吴') == 3, 'B': lambda w, T: w['林'] and w['周'] and not w['吴'],
       'C': lambda w, T: not w['林'], 'D': lambda w, T: not w['吴']}, 'A')
check('D14-4-2', B('甲', '乙', '丙'),
      [lambda w: cnt(w, '甲乙丙') >= 2, lambda w: cnt(w, '甲乙丙') <= 2, lambda w: not w['甲'], lambda w: w['乙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['甲'] and not w['乙'] and not w['丙'], 'B': lambda w, T: w['甲'] and w['丙'] and not w['乙'],
       'C': lambda w, T: cnt(w, '甲乙丙') == 3, 'D': lambda w, T: w['甲'] and w['乙'] and not w['丙']}, 'A')
check('D14-4-3', choose_one(['甲', '乙', '丙', '丁', '戊']),
      [lambda w: w['x'] == '甲', lambda w: w['x'] == '乙', lambda w: w['x'] != '丙', lambda w: w['x'] in ('甲', '丁'),
       lambda w: w['x'] != '戊'],
      at_most_false(1), 'must',
      {k: (lambda c: (lambda w, T: w['x'] == c))(c) for k, c in zip('ABCD', ['甲', '乙', '丙', '丁'])}, 'A')
# ---- G5 考法五 ----
check('D14-5-1', B('渔', '茶'),
      [lambda w: w['渔'], lambda w: not w['茶'], lambda w: w['渔'] or w['茶'], lambda w: w['渔'] and w['茶']],
      exactly_true(1), 'must',
      {'A': lambda w, T: not w['渔'], 'B': lambda w, T: w['茶'], 'C': lambda w, T: not w['渔'] and not w['茶'],
       'D': lambda w, T: w['渔'] != w['茶']}, 'A', show=True)
check('D14-5-2', choose_one(P4),
      [lambda w: w['x'] == '甲', lambda w: w['x'] in ('甲', '乙'), lambda w: w['x'] == '丙', lambda w: w['x'] == '丁'],
      exactly_true(1), 'may',
      {'A': lambda w, T: w['x'] == '甲', 'B': lambda w, T: T[0] and T[1], 'C': lambda w, T: not T[1] and not T[2],
       'D': lambda w, T: T[2] and T[3]}, 'C')
check('D14-5-3', B('A', 'B', 'C'),
      [lambda w: not w['C'], lambda w: (not w['A']) or w['B'], lambda w: (not w['C']) or w['B'], lambda w: w['A'] and w['B']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['C'] and not w['A'] and not w['B'], 'B': lambda w, T: w['A'] and not w['B'] and not w['C'],
       'C': lambda w, T: w['A'] and w['B'] and not w['C'], 'D': lambda w, T: w['A'] and w['B'] and w['C']}, 'A')
# ---- G6 考法六 ----
check('D14-6-1', choose_one([1, 2, 3]),
      [lambda w: ((w['x'] != 3) + (w['x'] == 1)) == 1],          # 3号箱的话
      exactly_true(0), 'must',                                   # 3号箱上的话是假的
      {'A': lambda w, T: w['x'] == 1, 'B': lambda w, T: w['x'] == 3, 'C': lambda w, T: w['x'] != 2,
       'D': lambda w, T: w['x'] != 3}, 'C', show=True)
# chain accusation: truth values t must satisfy t_i == content_i(t)
def fixed(n, contents):
    return [t for t in itertools.product([False, True], repeat=n) if all(t[i] == contents[i](t) for i in range(n))]
fp = fixed(3, [lambda t: not t[1], lambda t: not t[2], lambda t: (not t[0]) and (not t[1])])
record('D14-6-2', fp == [(False, True, False)], f'链式指控 3人 不动点={fp} -> 只有乙说真话 (A)')
fp = fixed(3, [lambda t: sum(t) == 1, lambda t: sum(t) == 2, lambda t: sum(t) == 0])
record('D14-6-3', fp == [(True, False, False)], f'自指计数 3句 不动点={fp} -> 只有①为真 (A)')
# ---- G7 考法七 ----
D5 = ['甲', '乙', '丙', '丁', '戊']
ok = [x for x in D5 if all(((a) + (b)) == 1 for a, b in [(x == '甲', x != '乙'), (x == '甲', x != '丙'), (x != '甲', x == '丁')])]
record('D14-7-1', ok == ['戊'], f'每人两句恰一真 -> {ok} (D 戊区)')
def knights(people, says, kinds=('H', 'L')):
    out = []
    for tp in itertools.product(kinds, repeat=len(people)):
        a = dict(zip(people, tp))
        if all((a[p] != 'H' or f(a)) and (a[p] != 'L' or not f(a)) for p, f in says.items()):
            out.append(a)
    return out
sol = knights(['甲', '乙'], {'甲': lambda a: a['乙'] == 'L', '乙': lambda a: a['甲'] == a['乙']})
record('D14-7-2', sol == [{'甲': 'H', '乙': 'L'}], f'身份型2人 -> {sol} (A 甲真乙假)')
sol = knights(['甲', '乙', '丙'], {'甲': lambda a: 'L' in a.values(), '乙': lambda a: a['丙'] == 'H', '丙': lambda a: a['甲'] == 'L'})
record('D14-7-3', sol == [{'甲': 'H', '乙': 'L', '丙': 'L'}], f'身份型3人 -> {sol} (A)')
# ---- G9 / G11 数量 ----
record('D14-9-3', F(40, 100) * F(12, 10) > F(30, 100) and F(60, 100) * F(12, 10) > F(70, 100),
       '海外仓 0.4×1.2=0.48>0.30（增加）；非海外仓 0.6×1.2=0.72>0.70（也增加，故C错）')
record('D14-11-1', 40 * F(3, 2) < 80, '门票 40×1.5=60<80')
avg = F(92 * 100 + 86 * 300, 400)
record('D14-11-2', avg < 89 and avg == F(175, 2), f'加权平均={float(avg)}<89；简单平均89')
def five_scores(cond, lo=60, hi=95, total=400, distinct=False):
    # five integer scores in [lo,hi], max exactly hi, sum total; return whether some multiset satisfies cond
    for c in itertools.combinations_with_replacement(range(lo, hi + 1), 4):
        s = list(c) + [hi]
        if sum(s) != total or max(s) != hi:
            continue
        if distinct and len(set(s)) < 5:
            continue
        if cond(sorted(s, reverse=True)):
            return True
    return False
poss = {'A': five_scores(lambda s: sum(x < 80 for x in s) >= 3),
        'B': five_scores(lambda s: sum(x >= 90 for x in s) == 1),
        'C': five_scores(lambda s: min(s) == 60),
        'D': five_scores(lambda s: sum(x >= 90 for x in s) >= 4)}
record('D14-11-3', [k for k, v in poss.items() if not v] == ['D'], f'可能性={poss} -> 不可能的只有D')

# =====================================================================================================
# DAY 27
# =====================================================================================================
# ---- G1 考法二 ----  (True = 线上)
check('D27-1-1', bools(P4),
      [lambda w: w['甲'] == w['乙'], lambda w: (w['甲'] + w['乙']) == 1, lambda w: w['丁'],
       lambda w: w['丙'] or (not w['丁'])],                       # 丙线下 -> 丁线下
      exactly_false(1), 'must',
      {'A': lambda w, T: w['丙'] and w['丁'], 'B': lambda w, T: w['甲'] and w['乙'],
       'C': lambda w, T: w['甲'] and not w['乙'], 'D': lambda w, T: not w['丙'] and w['丁']}, 'A')
check('D27-1-2', choose_one('ABC'),
      [lambda w: w['x'] == 'A', lambda w: w['x'] in 'BC', lambda w: w['x'] != 'B', lambda w: w['x'] == 'C'],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['x'] == 'A', 'B': lambda w, T: w['x'] == 'B', 'C': lambda w, T: w['x'] == 'C',
       'D': lambda w, T: T[2]}, 'B')
check('D27-1-3', B('夜', '券', '志'),
      [lambda w: (not w['夜']) or w['券'], lambda w: w['夜'] and not w['券'], lambda w: (not w['志']) or w['夜'],
       lambda w: w['志'], lambda w: not w['券']],
      exactly_false(1), 'must',
      {'A': lambda w, T: w['夜'] and w['志'] and not w['券'], 'B': lambda w, T: w['夜'] and w['券'] and w['志'],
       'C': lambda w, T: w['志'] and not w['夜'] and not w['券'], 'D': lambda w, T: w['券'] and not w['夜']}, 'A')
check('D27-1-4', B('甲广', '乙广'),                                # False = 深圳
      [lambda w: w['甲广'] or not w['乙广'], lambda w: (not w['甲广']) and w['乙广'], lambda w: w['甲广'],
       lambda w: not w['乙广']],
      exactly_true(2), 'must',
      {'A': lambda w, T: w['甲广'], 'B': lambda w, T: not w['乙广'], 'C': lambda w, T: w['甲广'] == w['乙广'],
       'D': lambda w, T: w['甲广'] != w['乙广']}, 'C')
# ---- G2 考法三 ----
check('D27-2-1', B('王', '郑', '林'),
      [lambda w: cnt(w, '王郑林') == 3, lambda w: w['王'], lambda w: cnt(w, '王郑林') < 3, lambda w: w['郑'] or not w['林']],
      exactly_false(1), 'may',
      {'A': lambda w, T: not w['王'], 'B': lambda w, T: not w['郑'] and w['林'], 'C': lambda w, T: not w['郑'] and not w['林'],
       'D': lambda w, T: w['郑'] and not w['王'] and not w['林']}, 'C', show=True)
check('D27-2-2', B('甲', '乙'),
      [lambda w: (not w['甲']) or w['乙'], lambda w: not w['甲'] and not w['乙'], lambda w: w['甲'] and not w['乙'],
       lambda w: w['甲'] or not w['乙']],                          # 除非甲进，否则乙也进不了：非甲→非乙
      exactly_true(2), 'must',
      {'A': lambda w, T: w['甲'], 'B': lambda w, T: w['乙'], 'C': lambda w, T: not w['乙'], 'D': lambda w, T: T[0]}, 'A',
      show=True)
check('D27-2-3', B('甲', '乙', '丙'),
      [lambda w: not (w['甲'] and w['乙']), lambda w: w['甲'] and not w['丙'], lambda w: w['甲'] and w['乙'],
       lambda w: (not w['甲']) or w['丙'], lambda w: not w['乙']],
      exactly_true(3), 'must',
      {'A': lambda w, T: w['甲'], 'B': lambda w, T: not w['乙'], 'C': lambda w, T: w['丙'],
       'D': lambda w, T: w['甲'] and not w['丙']}, 'B')
P6 = ['甲', '乙', '丙', '丁', '戊', '己']
check('D27-2-4', bools(P6),
      [lambda w: not w['乙'], lambda w: w['乙'], lambda w: w['丁'], lambda w: w['丙'] and w['丁'], lambda w: w['乙'],
       lambda w: not w['丁']],                                     # 乙：“甲说的是假话”＝乙完成了
      exactly_false(2), 'must',
      {'A': lambda w, T: w['乙'] and w['丙'] and w['丁'], 'B': lambda w, T: w['甲'], 'C': lambda w, T: not w['丁'],
       'D': lambda w, T: (not T[0]) and (not T[4]) and sum(T) == 4}, 'A')
check('D27-2-5', B('甲', '乙', '丙'),
      [lambda w: w['甲'], lambda w: not w['甲'], lambda w: w['乙'] and w['丙'], lambda w: not w['乙'] or not w['丙'],
       lambda w: w['乙'], lambda w: w['甲'] or w['乙']],
      exactly_true(3), 'must',
      {'A': lambda w, T: w['甲'] and not w['乙'], 'B': lambda w, T: w['丙'], 'C': lambda w, T: w['乙'],
       'D': lambda w, T: not w['甲'] and not w['乙']}, 'A')
# ---- G3 考法四 ----
check('D27-3-1', B('甲', '乙', '丙'),
      [lambda w: not w['甲'], lambda w: not w['乙'], lambda w: w['甲'] or w['乙'] or w['丙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['甲'] and w['乙'], 'B': lambda w, T: cnt(w, '甲乙丙') == 3, 'C': lambda w, T: not w['丙'],
       'D': lambda w, T: w['甲'] and not w['乙'] and not w['丙']}, 'A', show=True)
check('D27-3-2', B('A', 'B', 'C'),
      [lambda w: cnt(w, 'ABC') == 3, lambda w: cnt(w, 'ABC') == 0, lambda w: w['A'], lambda w: w['B']],
      at_most_false(1), 'must',
      {'A': lambda w, T: cnt(w, 'ABC') == 3, 'B': lambda w, T: w['A'] and w['B'] and not w['C'], 'C': lambda w, T: not w['C'],
       'D': lambda w, T: not T[0]}, 'A')
check('D27-3-3', B('甲', '乙', '丙'),
      [lambda w: w['甲'] and w['乙'], lambda w: not w['甲'] and not w['乙'], lambda w: w['甲'] or w['丙'],
       lambda w: not w['甲'] or not w['丙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['甲'], 'B': lambda w, T: w['乙'], 'C': lambda w, T: w['乙'] != w['丙'],
       'D': lambda w, T: cnt(w, '甲乙丙') == 3}, 'C')
check('D27-3-4', choose_one(T5),
      [lambda w: w['x'] == '甲', lambda w: w['x'] == '乙', lambda w: w['x'] in ('甲', '丙'), lambda w: w['x'] != '丙',
       lambda w: w['x'] in ('乙', '戊')],
      exactly_true(2), 'must',
      {k: (lambda c: (lambda w, T: w['x'] == c))(c) for k, c in zip('ABCD', ['甲', '丙', '丁', '戊'])}, 'D')
# ---- G4 考法五 ----
check('D27-4-1', subsets_of_size(P4, 2),
      [lambda w: '丁' in w['S'], lambda w: bool({'乙', '丁'} & w['S']), lambda w: not ({'甲', '丁'} & w['S']),
       lambda w: ('乙' not in w['S']) or ('丁' in w['S'])],
      exactly_true(2), 'must',
      {'A': lambda w, T: w['S'] == {'甲', '乙'}, 'B': lambda w, T: w['S'] == {'乙', '丙'},
       'C': lambda w, T: w['S'] == {'乙', '丁'}, 'D': lambda w, T: w['S'] == {'丙', '丁'}}, 'B', show=True)
check('D27-4-2', B('广', '潮', '陶'),
      [lambda w: cnt(w, '广潮陶') == 3, lambda w: cnt(w, '广潮陶') == 1, lambda w: not w['广'], lambda w: w['潮']],
      exactly_true(2), 'must',
      {'A': lambda w, T: w['广'], 'B': lambda w, T: not w['潮'], 'C': lambda w, T: w['陶'], 'D': lambda w, T: cnt(w, '广潮陶') == 3},
      'C', show=True)
check('D27-4-3', B('甲', '乙', '丙'),
      [lambda w: (not w['甲']) or w['乙'], lambda w: w['乙'] or (not w['甲']), lambda w: w['甲'],
       lambda w: w['乙'] and w['丙'], lambda w: not w['丙']],
      exactly_true(2), 'must',
      {'A': lambda w, T: not w['乙'], 'B': lambda w, T: w['甲'], 'C': lambda w, T: w['丙'],
       'D': lambda w, T: not w['甲'] and not w['丙']}, 'A', show=True)
# ---- G5 考法六 ----
check('D27-5-1', choose_one([1, 2, 3, 4]),
      [lambda w: ((w['x'] == 1) + (w['x'] != 1) + (w['x'] != 3)) == 1],     # 4号门的话（为真）
      exactly_true(1), 'must',
      {k: (lambda c: (lambda w, T: w['x'] == c))(c) for k, c in zip('ABCD', [1, 2, 3, 4])}, 'C')
fp = fixed(4, [lambda t: not t[1], lambda t: not t[2], lambda t: not t[3], lambda t: (not t[0]) and (not t[1])])
record('D27-5-2', fp == [(True, False, True, False)], f'4人链式指控 不动点={fp} -> 甲、丙说真话 (A)')
sols = []
for loc in 'AB':
    for t in itertools.product([False, True], repeat=3):
        if t[0] == (t[1] != t[2]) and t[1] == (t[0] and loc == 'A') and t[2] == (sum(t) <= 1):
            sols.append((t, loc))
record('D27-5-3', sols == [((True, True, False), 'A')], f'自指＋内容 解={sols} -> A')
# ---- G6 考法七 ----
ok = [x for x in D5 if all((a + b) == 1 for a, b in [(x == '甲', x != '乙'), (x == '乙', x in ('丙', '戊')), (x == '丁', x in ('乙', '戊'))])]
record('D27-6-1', ok == ['戊'], f'每人两句恰一真 -> {ok} (D)')
sols = []
for exit_ in ('左', '右'):
    for a in knights(['甲', '乙'], {'甲': lambda a: 'L' in a.values(), '乙': (lambda e: (lambda a: e == '左'))(exit_)}):
        sols.append((a, exit_))
record('D27-6-2', sols == [({'甲': 'H', '乙': 'L'}, '右')], f'身份＋内容 -> {sols} (A)')
def hlr(says):
    out = []
    for tp in itertools.permutations(['H', 'L', 'R']):
        a = dict(zip(['甲', '乙', '丙'], tp))
        if all((a[p] != 'H' or f(a)) and (a[p] != 'L' or not f(a)) for p, f in says.items()):
            out.append(a)
    return out
sol = hlr({'甲': lambda a: a['乙'] == 'H', '乙': lambda a: a['甲'] == 'H', '丙': lambda a: a['甲'] == 'L'})
record('D27-6-3', sol == [{'甲': 'L', '乙': 'R', '丙': 'H'}], f'诚实/说谎/随意 -> {sol} (A)')
# ---- G9 / G10 / G11 数量与规则 ----
record('D27-9-1', F(6, 8) == F(3, 4), '收入持平：时长比 6/8 = 3/4')
dig = F(35, 100) * F(9, 10); non = F(65, 100) * F(9, 10)
record('D27-9-2', dig > F(30, 100) and non / F(70, 100) < F(9, 10),
       f'数字岗位 0.315>0.300；非数字 0.585/0.70={float(non / F(70, 100)):.3f}（降约16%，B错）')
def vol_possible(cond):
    for c in itertools.product(range(3, 9), repeat=7):
        s = list(c) + [8]
        if sum(s) == 40 and max(s) == 8 and cond(s):
            return True
    return False
poss = {'A': vol_possible(lambda s: 3 in s), 'B': vol_possible(lambda s: s.count(8) >= 3),
        'C': vol_possible(lambda s: min(s) >= 5), 'D': vol_possible(lambda s: s.count(4) >= 5)}
record('D27-9-3', [k for k, v in poss.items() if not v] == ['C'], f'可能性={poss} -> 不可能的只有C')
record('D27-9-4', F(60 + 55 - 100, 100) == F(15, 100) and F(15, 55) < F(1, 2),
       '粤英重叠至少15%；英语者中会粤语最少15/55≈27%（B错）；都不会可为0（C错）')
record('D27-10-1', F(2 + 2, 100) <= F(5, 100) and F(2, 50) <= F(5, 100), '合计4/100=4%≤5%，不召回；首次2/50=4%也不召回（C错）')
bmi = 60 / 1.6 ** 2
record('D27-10-2', 18.5 <= bmi <= 23.9, f'BMI=60/1.6²={bmi:.2f}，属正常（D错）')
def crafts_possible(cond):
    for a in range(1, 13):
        for b in range(1, 13):
            c = 12 - a - b
            if c >= 1 and a > b > c and cond(a, b, c):   # a 竹编 > b 木雕 > c 陶艺
                return True
    return False
poss = {'A': crafts_possible(lambda a, b, c: a == 6), 'B': crafts_possible(lambda a, b, c: b == 5),
        'C': crafts_possible(lambda a, b, c: c == 4), 'D': crafts_possible(lambda a, b, c: b == 2)}
record('D27-11-3', [k for k, v in poss.items() if not v] == ['C'], f'可能性={poss} -> 不可能的只有C')

# =====================================================================================================
# DAY 36
# =====================================================================================================
# ---- G1 考法三 ----
check('D36-1-1', B('甲', '乙', '丙', '丁', '戊'),
      [lambda w: not w['丙'], lambda w: w['丙'], lambda w: w['丁'] and w['戊'], lambda w: w['甲'] and not w['乙'],
       lambda w: not w['丙'] or not w['丁']],
      exactly_false(1), 'must',
      {'A': lambda w, T: not T[1] and cnt(w, '甲乙丙丁戊') == 3, 'B': lambda w, T: not T[0] and cnt(w, '甲乙丙丁戊') == 3,
       'C': lambda w, T: not T[1] and cnt(w, '甲乙丙丁戊') == 4, 'D': lambda w, T: not T[2] and cnt(w, '甲乙丙丁戊') == 2},
      'A')
check('D36-1-2', bools(P6),
      [lambda w: (w['甲'] + w['乙']) == 1, lambda w: cnt(w, P6) == 0, lambda w: (w['乙'] + w['丙']) == 1,
       lambda w: w['甲'] and w['丙'],                                   # 丁：“戊说的是假话”
       lambda w: not w['甲'] or not w['丙'], lambda w: w['甲']],
      exactly_false(2), 'must',
      {'A': lambda w, T: not T[1] and not T[4] and sum(T) == 4, 'B': lambda w, T: not T[3] and not T[5] and sum(T) == 4,
       'C': lambda w, T: not T[1] and not T[3] and sum(T) == 4, 'D': lambda w, T: not T[0] and not T[4] and sum(T) == 4},
      'A')
check('D36-1-3', bools(P4),
      [lambda w: w['丙'], lambda w: not w['丙'], lambda w: w['甲'] or w['丙'], lambda w: not w['甲'] and not w['丙'],
       lambda w: not w['甲'] or not w['丁'], lambda w: (not w['乙']) or w['丁'], lambda w: (not w['丙']) or w['乙']],
      exactly_true(3), 'must',
      {'A': lambda w, T: w['甲'] and w['丙'] and w['丁'] and not w['乙'], 'B': lambda w, T: cnt(w, P4) == 4,
       'C': lambda w, T: w['乙'] and w['丙'] and w['丁'] and not w['甲'],
       'D': lambda w, T: w['甲'] and w['丙'] and not w['乙'] and not w['丁']}, 'A')
check('D36-1-4', bools(P4),
      [lambda w: w['甲'] or w['丙'], lambda w: not w['甲'] and not w['丙'], lambda w: w['甲'] and w['丙'],
       lambda w: w['乙'] and w['丁'], lambda w: not w['乙'] and not w['丙']],
      more_true_than_false(), 'must',
      {'A': lambda w, T: cnt(w, P4) == 4, 'B': lambda w, T: w['甲'] and w['丙'] and not w['乙'] and not w['丁'],
       'C': lambda w, T: not w['乙'] and not w['丙'], 'D': lambda w, T: w['乙'] and w['丁'] and not w['甲'] and not w['丙']},
      'A')
# ---- G2 考法二 ----
check('D36-2-1', bools(P4),
      [lambda w: (not w['甲']) or w['乙'], lambda w: w['甲'] and not w['乙'], lambda w: cnt(w, P4) == 4,
       lambda w: cnt(w, P4) < 4, lambda w: w['丙'], lambda w: not w['丁']],
      exactly_true(2), 'must',
      {'A': lambda w, T: w['甲'], 'B': lambda w, T: not w['乙'], 'C': lambda w, T: not w['丙'] and w['丁'],
       'D': lambda w, T: cnt(w, P4) == 4}, 'C')
check('D36-2-2', B('A', 'B', 'C'),
      [lambda w: w['A'] != w['B'], lambda w: w['A'] == w['B'], lambda w: w['C'], lambda w: (not w['B']) or w['C']],
      exactly_true(2), 'must',
      {'A': lambda w, T: not w['B'] and not w['C'], 'B': lambda w, T: w['A'], 'C': lambda w, T: w['B'],
       'D': lambda w, T: cnt(w, 'ABC') == 3}, 'A')
check('D36-2-3', bools(T5),
      [lambda w: cnt(w, T5) == 2, lambda w: cnt(w, T5) != 2, lambda w: w['甲'] and w['乙'],
       lambda w: not (w['丙'] or w['丁'] or w['戊'])],
      exactly_true(2), 'must',
      {'A': lambda w, T: cnt(w, T5) == 2, 'B': lambda w, T: w['甲'], 'C': lambda w, T: cnt(w, T5) != 2,
       'D': lambda w, T: w['丙']}, 'C')
# ---- G3 考法四 ----
check('D36-3-1', B('甲', '乙', '丙'),
      [lambda w: w['甲'] and w['乙'], lambda w: not w['甲'] and not w['乙'], lambda w: w['乙'] or w['丙'],
       lambda w: not w['乙'] or not w['丙'], lambda w: (not w['甲']) or w['丙']],
      exactly_true(2), 'must',
      {'A': lambda w, T: w['乙'] and w['丙'] and not w['甲'], 'B': lambda w, T: w['甲'] and not w['乙'] and not w['丙'],
       'C': lambda w, T: cnt(w, '甲乙丙') == 3, 'D': lambda w, T: w['甲'] and w['乙'] and not w['丙']}, 'A', show=True)
check('D36-3-2', B('A', 'B', 'C'),
      [lambda w: cnt(w, 'ABC') > 0, lambda w: cnt(w, 'ABC') < 3, lambda w: not w['A'], lambda w: not w['C']],
      at_most_true(1), 'must',
      {'A': lambda w, T: cnt(w, 'ABC') == 3, 'B': lambda w, T: cnt(w, 'ABC') == 0,
       'C': lambda w, T: w['A'] and w['C'] and not w['B'], 'D': lambda w, T: not w['B']}, 'A')
# ---- G4 考法五 ----
check('D36-4-1', B('A', 'B', 'C'),
      [lambda w: w['A'] and w['B'], lambda w: (not w['C']) or w['A'], lambda w: not w['B'], lambda w: w['A'] or w['C']],
      exactly_true(3), 'never',
      {'A': lambda w, T: w['A'] and not w['B'] and not w['C'], 'B': lambda w, T: w['C'] and not w['A'] and not w['B'],
       'C': lambda w, T: w['A'] and w['C'] and not w['B'], 'D': lambda w, T: cnt(w, 'ABC') == 3}, 'B')
base = [lambda w: w['甲'] and w['乙'], lambda w: not w['甲'], lambda w: (not w['乙']) or w['丙']]
cands = {'A': lambda w: not w['乙'], 'B': lambda w: not w['丙'], 'C': lambda w: w['甲'], 'D': lambda w: w['乙'] and w['丙']}
info = {}
for k, f4 in cands.items():
    vw = [w for w in B('甲', '乙', '丙') if sum(bool(s(w)) for s in base + [f4]) == 1]
    info[k] = [''.join(n for n in '甲乙丙' if w[n]) or '无' for w in vw]
good = [k for k, v in info.items() if v and all('丙' in s for s in v)]
record('D36-4-2', good == ['B'] and info['A'] == ['乙', '甲乙'] and info['C'] == ['乙'] and len(info['D']) == 4,
       f'各补充项下的情况={info} -> 只有补B能确定丙入选')
mx = max(sum([x == '乙', x in ('丙', '丁'), x != '丁', x != '甲']) for x in P4)
record('D36-4-3', mx == 3, f'四句最多同真 {mx} 句 (C)')
# ---- G5 考法六 ----
fp = fixed(4, [lambda t: sum(t) == 1, lambda t: sum(t) == 2, lambda t: sum(t) == 3, lambda t: sum(t) == 0])
record('D36-5-1', fp == [(True, False, False, False)], f'自指计数 4句 不动点={fp} -> A')
S3 = ['甲', '乙', '丙']
ws = [dict(X=X, 甲=a, 乙=b, 丙=c) for X in S3 for a in ('乙', '丙') for b in ('甲', '丙') for c in ('甲', '乙')]
tr = lambda w, p: w[p] == w['X']
base_w = [w for w in ws if tr(w, '甲')]
by = {s: {w['X'] for w in base_w if tr(w, '丙') == s} for s in (True, False)}
told = [s for s, xs in by.items() if len(xs) > 1]                 # 被告知后仍无法确定
fin = [w for w in base_w if tr(w, '丙') in told]
o = {'A': lambda w: w['X'] == '乙', 'B': lambda w: not tr(w, '丙'), 'C': lambda w: w['X'] == '丙', 'D': lambda w: tr(w, '乙')}
hits = [k for k, f in o.items() if fin and all(f(w) for w in fin)]
record('D36-5-2', hits == ['B'], f'元信息反转 hits={hits} | 丙真->{by[True]} 丙假->{by[False]}')
stm = lambda x: x == '黄'                                          # 红盒上的话
deduce = {s: [x for x in ('红', '黄', '蓝') if stm(x) == s] for s in (True, False)}
told = [s for s, xs in deduce.items() if len(xs) == 1]
record('D36-5-3', told == [True] and deduce[True] == ['黄'], f'红盒为真->{deduce[True]}，为假->{deduce[False]} -> 奖品在黄盒 (B)')
# ---- G6 考法七 ----
def sayable(f):
    return any((a['甲'] == 'H' and f(a)) or (a['甲'] == 'L' and not f(a)) for a in
               [dict(zip(['甲', '乙'], tp)) for tp in itertools.product('HL', repeat=2)])
cands = {'A': lambda a: a['甲'] == 'L', 'B': lambda a: a['甲'] == 'H', 'C': lambda a: a['乙'] == 'L',
         'D': lambda a: a['甲'] == 'L' and a['乙'] == 'L'}
never = [k for k, f in cands.items() if not sayable(f)]
record('D36-6-1', never == ['A'], f'任何情况下都说不出的话 -> {never}')
res = []
for x in D5:
    pats = sorted([(x == '甲') + (x != '乙'), (x == '甲') + (x != '丁'), (x == '乙') + (x != '丙')])
    if pats == [0, 1, 2]:
        res.append(x)
record('D36-6-2', res == ['乙'], f'一人全对一人全错一人半对 -> {res} (B)')
sol = hlr({'甲': lambda a: a['乙'] != 'H', '乙': lambda a: a['甲'] == 'H', '丙': lambda a: a['甲'] == 'L'})
record('D36-6-3', sol == [{'甲': 'H', '乙': 'R', '丙': 'L'}], f'诚实/说谎/随意 -> {sol} -> 随意者乙 (B)')
# ---- G7 / G9 / G10 数量与规则 ----
record('D36-7-3', F(105, 150) == F(7, 10) and F(45, 150) == F(3, 10) and F(7, 10) / F(3, 10) > 2,
       '保持改善 70% 对 30%，2倍多')
tot25 = F(100); fx25 = F(60); dm25 = tot25 - fx25
tot24 = tot25 / F(108, 100); fx24 = fx25 / F(112, 100); dm24 = tot24 - fx24
g_dm = dm25 / dm24 - 1
record('D36-9-1', 0 < g_dm < F(8, 100) and fx24 / tot24 < F(60, 100) and abs((fx25 - fx24) / (dm25 - dm24) - F(3, 2)) > 1,
       f'内贸增速={float(g_dm) * 100:.2f}%；2024外贸占比={float(fx24 / tot24) * 100:.2f}%；外贸/内贸增量比={float((fx25 - fx24) / (dm25 - dm24)):.2f}')
poss = {'A': five_scores(lambda s: min(s) == 60, lo=0, distinct=True),
        'B': five_scores(lambda s: sum(x < 60 for x in s) >= 2, lo=0, distinct=True),
        'C': five_scores(lambda s: s[1] == 94, lo=0, distinct=True),
        'D': five_scores(lambda s: sum(x > 80 for x in s) >= 3, lo=0, distinct=True)}
record('D36-9-2', [k for k, v in poss.items() if not v] == ['B'], f'互不相同整数 可能性={poss} -> 不可能的只有B')
# Simpson: grid search for counterexamples to "甲 overall lower => 甲 has larger heavy share"
bad = 0; example = None
grid = [F(i, 20) for i in range(1, 20)]
for a1 in grid:
    for b1 in grid:
        if not b1 < a1: continue
        for a2 in grid:
            for b2 in grid:
                if not (b2 < a2 and a1 > a2 and b1 > b2): continue
                for p1 in (F(1, 10), F(3, 10), F(5, 10), F(7, 10), F(9, 10)):
                    for p2 in (F(1, 10), F(3, 10), F(5, 10), F(7, 10), F(9, 10)):
                        t1 = p1 * b1 + (1 - p1) * a1; t2 = p2 * b2 + (1 - p2) * a2
                        if t1 < t2:
                            if not p1 > p2: bad += 1
                            elif example is None: example = (a1, b1, a2, b2, p1, p2)
record('D36-9-3', bad == 0 and example is not None, f'辛普森：反例数={bad}；示例 {example}')
fee = lambda t: 3 * min(t, 15) + 5 * max(t - 15, 0)
record('D36-10-1', fee(20) == 70 and fee(10) == 30 and fee(20) > 2 * fee(10) and F(fee(20), 20) == F(7, 2) and fee(15) == 45,
       '甲20吨=70元，乙10吨=30元；均价3.5元；乙15吨=45元')
z = lambda x: F(x - 70, 10)
record('D36-10-2', z(70) == 0 and z(69) < 0 and z(80) - z(70) == 1 and z(90) == 2, '标准分：70->0；差10分->差1；标准分2->90分')
record('D36-12-6', F(120, 1) / F(12, 10) == 100 and F(15, 10) / F(12, 10) == F(5, 4), '去年100期；每期平均人次为1.25倍')
# ---- G12 混练（真假部分） ----
check('D36-12-1', bools(T5),
      [lambda w: cnt(w, T5) >= 3, lambda w: cnt(w, T5) <= 2, lambda w: w['甲'] and w['乙'],
       lambda w: not (w['丙'] or w['丁'] or w['戊']), lambda w: (not w['甲']) or w['丙']],
      exactly_true(1), 'must',
      {'A': lambda w, T: w['甲'] and w['乙'], 'B': lambda w, T: w['甲'] and not w['乙'] and not w['丙'],
       'C': lambda w, T: w['丁'] and w['戊'], 'D': lambda w, T: cnt(w, T5) == 2}, 'B')
check('D36-12-2', B('甲', '乙', '丙'),
      [lambda w: cnt(w, '甲乙丙') == 1, lambda w: cnt(w, '甲乙丙') == 2, lambda w: w['甲'],
       lambda w: not w['乙'] or not w['丙'], lambda w: w['乙']],
      at_most_false(1), 'must',
      {'A': lambda w, T: w['甲'] and w['乙'] and not w['丙'], 'B': lambda w, T: w['甲'] and not w['乙'] and not w['丙'],
       'C': lambda w, T: cnt(w, '甲乙丙') == 3, 'D': lambda w, T: w['甲'] and w['丙'] and not w['乙']}, 'A')
check('D36-12-3', subsets_of_size(P4, 2),
      [lambda w: '甲' in w['S'], lambda w: '乙' in w['S'], lambda w: '丙' not in w['S'],
       lambda w: ('丁' not in w['S']) or ('甲' in w['S'])],
      exactly_false(1), 'must',
      {'A': lambda w, T: w['S'] == {'甲', '乙'}, 'B': lambda w, T: w['S'] == {'甲', '丁'},
       'C': lambda w, T: w['S'] == {'乙', '丙'}, 'D': lambda w, T: w['S'] == {'丙', '丁'}}, 'B')
sol = knights(['甲', '乙', '丙'], {'甲': lambda a: a['甲'] == 'L' and a['乙'] == 'L',
                                  '乙': lambda a: a['甲'] == 'L' or a['丙'] == 'L', '丙': lambda a: a['乙'] == 'L'})
record('D36-12-4', sol == [{'甲': 'L', '乙': 'H', '丙': 'L'}], f'身份型3人（含自指） -> {sol} (A)')

ok = summary()
sys.exit(0 if ok else 1)
