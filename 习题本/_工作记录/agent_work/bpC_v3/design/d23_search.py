import sys; sys.path.insert(0, '..')
from lib import *
import random

# (a) 工序带时长：A2 B1 C3 D1 E2（共9天），每天只做一道工序，第1天开工连续施工
DUR = {'A': 2, 'B': 1, 'C': 3, 'D': 1, 'E': 2}
def schedule(order):
    day = {}; t = 1
    for x in order:
        for k in range(DUR[x]): day[t + k] = x
        t += DUR[x]
    return day
sols = []
for order in permutations('ABCDE'):
    pos = {x: i for i, x in enumerate(order)}
    if not pos['A'] < pos['B']: continue          # B 在 A 完成后才开始
    if pos['D'] != pos['C'] + 1: continue          # D 紧接在 C 之后
    if pos['E'] == 4: continue                     # E 不是最后做
    if pos['A'] == 0: continue                     # A 不是第一道
    sols.append(order)
print('(a) 顺序', [''.join(o) for o in sols])
for d in range(1, 10):
    print('   第', d, '天', sorted({schedule(o)[d] for o in sols}))

# (b) 6人一排，3条条件，问甲乙之间最多隔几人
P = ['甲', '乙', '丙', '丁', '戊', '己']
S = line(P, 6, [lambda s: s['甲'] < s['乙'], lambda s: abs(s['丙'] - s['丁']) == 1, lambda s: s['戊'] not in (1, 6),
                lambda s: abs(s['己'] - s['甲']) == 2, lambda s: s['丙'] < s['甲']])
print('(b) 解数', len(S), '甲乙间隔人数分布', sorted({s['乙'] - s['甲'] - 1 for s in S}))

# (c) 7人名次：甲比乙高2个名次；丙在丁之前；戊不在前三；己在庚之后；乙最高可能第几
P = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
S = line(P, 7, [lambda r: r['乙'] - r['甲'] == 2, lambda r: r['丙'] < r['丁'], lambda r: r['戊'] > 3,
                lambda r: r['己'] > r['庚'], lambda r: r['丁'] < r['乙'], lambda r: r['庚'] < r['甲']])
print('(c) 解数', len(S), '乙可能名次', sorted({r['乙'] for r in S}), '甲可能名次', sorted({r['甲'] for r in S}))

# (d) 6人圆桌（0..5俯视顺时针，左手边=+1），3对夫妻：甲-A、乙-B、丙-C（甲乙丙为丈夫），每位丈夫坐在妻子的左手边（相邻）
H = ['甲', '乙', '丙']; W = ['A', 'B', 'C']
sols = []
for p in permutations(range(1, 6)):
    st = dict(zip(H + W, (0,) + p))
    if any(st[h] != (st[w] + 1) % 6 for h, w in zip(H, W)): continue
    if (st['乙'] - st['甲']) % 6 != 3 and False: continue
    if (st['C'] - st['甲']) % 6 != 3: continue      # 甲的对面是丙的妻子
    sols.append(st)
at = lambda st, i: {v: k for k, v in st.items()}[i % 6]
print('(d) 解', [[at(s, i) for i in range(6)] for s in sols])

# (e) 两排对坐长桌：北侧自西向东1-3，南侧自西向东4-6；1-4、2-5、3-6正对；"斜对面"=隔桌且相差一个座位
P = ['甲', '乙', '丙', '丁', '戊', '己']
side = lambda x: 0 if x <= 3 else 1
col = lambda x: (x - 1) % 3
opp = lambda a, b: side(a) != side(b) and col(a) == col(b)
diag = lambda a, b: side(a) != side(b) and abs(col(a) - col(b)) == 1
S = line(P, 6, [lambda s: opp(s['甲'], s['乙']), lambda s: side(s['丙']) == side(s['甲']) and abs(col(s['丙']) - col(s['甲'])) == 1,
                lambda s: diag(s['丁'], s['戊']), lambda s: col(s['己']) == 1, lambda s: side(s['甲']) == 0])
print('(e) 解数', len(S), [fmt_line(s) for s in S])

# (f) 6人一排，4条陈述恰有1条不成立 + 确定信息 甲在3号
P = ['甲', '乙', '丙', '丁', '戊', '己']
stm = [lambda s: abs(s['甲'] - s['乙']) == 1, lambda s: abs(s['丙'] - s['丁']) == 3, lambda s: s['戊'] < s['甲'],
       lambda s: abs(s['己'] - s['乙']) == 2]
S = [s for s in line(P, 6, [lambda s: s['甲'] == 3]) if sum(f(s) for f in stm) == 3]
print('(f) 解数', len(S), '不成立的是第', sorted({[i for i, f in enumerate(stm) if not f(s)][0] + 1 for s in S}), '条')
