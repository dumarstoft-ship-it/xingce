"""L07 真题形式化核查：自解答案（2026GD-61/2026GK-115/2026GD-57/2026GD-65）+ 可形式化的官方答案题。
每道题：把题干和四个选项按考试惯例翻译成箭头式（见 bp_L07_work/logic_sig.py 顶部说明），
计算"结构签名"（原子改名、单原子取反、前提顺序都不影响），要求恰好一个选项与题干签名相同，且就是答案。
None = 非形式（类比、关系推理、无法翻译），视为与题干不同。
"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L07_work')
from logic_sig import check_question

I = lambda a, c: ('imp', a if isinstance(a, list) else [a], c)
Q = []

# ---------------- 自解 ----------------
Q.append(('2026GD-61 (自解)', dict(rules=[I('A', 'B'), I('B', 'C')], concl=I('A', 'C')), {
    'A': dict(rules=[I('A', 'B'), I('B', 'C')], concl=I('~A', '~C')),            # 否定式结论
    'B': dict(rules=[I('B', 'C'), I('A', 'B')], concl=I('A', 'C')),              # 前提顺序互换的串联
    'C': dict(rules=[I('B', 'C'), I('C', 'A')], concl=I('A', 'B')),              # 结论倒推
    'D': dict(rules=[I('A', 'B'), I('C', 'B')], concl=I('C', 'A')),              # 共享后件
}, 'B', False))
Q.append(('2026GK-115 (自解)', dict(rules=[I('L', 'R')], facts=['R'], concl='L'), {
    'A': dict(rules=[I('S', 'Y'), I('Y', 'G')], facts=['S'], concl='G'),
    'B': None,                                                                     # "不会导致…可见无关"，非条件推理
    'C': dict(rules=[I('D', 'Y')], facts=['Y'], concl='D'),
    'D': dict(rules=[I('K', 'W')], facts=['K'], concl='W'),                       # "大多"按全称也只是肯前
}, 'C', False))
Q.append(('2026GD-57 (自解)', dict(rules=[I('B', 'A')], facts=['A'], concl='B'), {   # 不A就不B => B>A
    'A': dict(rules=[I('Y', 'X'), I('S', 'Y')], concl=I('S', 'X'), case='S'),    # 只有X才Y，某社区Y => X（肯前，有效）
    'B': dict(rules=[I('Y', 'X')], facts=['~Y'], concl='~X'),                     # 同句式，但已知~Y推~X
    'C': dict(rules=[I('Y', 'X')], concl=I('X', 'Y')),                           # 因为不X就无法Y，所以X则Y
    'D': dict(rules=[I('X', 'Y')], facts=['Z'], concl='Y'),                       # 禁止过度开采≠合理开采
}, 'C', False))
Q.append(('2026GD-65 (自解)', dict(rules=[I('J', ('or', ['Q', 'Z']))], facts=['~Q'], concl=I('J', 'Z')), {
    'A': dict(rules=[I('S', ('or', ['E', 'T']))], facts=['~T'], concl='E'),        # 丢了"申请认证"这个条件
    'B': None,                                                                     # 有的…有的…，不是选言
    'C': dict(rules=[I('P', ('or', ['O', 'F']))], facts=['O'], concl='~F'),        # 肯定一支否定另一支
    'D': dict(rules=[I('K', ('or', ['M', 'T']))], facts=['K', '~T'], concl='M'),   # 先肯定条件再否定一支
}, 'D', False))

# ---------------- 官方答案核对 ----------------
Q.append(('2022GD-69', dict(rules=[I('S', 'H'), I('H', 'M')], concl=I('S', 'M')), {
    'A': dict(rules=[('most', 'Y', 'L'), ('some', 'L', 'G')], concl=('most', 'Y', 'G'), quant=True),
    'B': dict(rules=[I('V', 'R'), I('P', 'R')], concl=I('V', 'P')),
    'C': dict(rules=[I('K', 'L'), I('L', 'Z')], concl=I('K', 'Z')),
    'D': dict(rules=[I('E', 'M'), I('M', 'H')], concl=I('E', 'C')),
}, 'C', False))
Q.append(('2022GD-73', dict(rules=[I('N', 'I'), I('X', '~I')], concl=I('X', '~N')), {
    'A': dict(rules=[I('T', 'O'), I('G', '~O')], concl=I('G', '~T')),
    'B': dict(rules=[I('J', 'Y'), I('W', 'Y')], concl=I(['J', 'W'], 'Y')),
    'C': dict(rules=[('most', 'E', '~R'), I('V', 'R')], concl=('most', 'E', '~V'), quant=True),  # "往往…较难…"
    'D': dict(rules=[I('A', 'B'), I('C', 'D')], concl=('and', ['B', 'D'])),
}, 'A', False))
Q.append(('2023GD-69', dict(rules=[I('W', 'P')], facts=['~W'], concl='~P'), {
    'A': dict(rules=[I('U', 'C')], facts=['~U'], concl='~C'),
    'B': dict(rules=[I('S', 'Y')], facts=['S'], concl='Y'),
    'C': dict(rules=[I('R', 'L')], facts=['~L'], concl='~R'),
    'D': dict(rules=[I('J', 'X')], facts=['~X'], concl='~J'),
}, 'A', False))
Q.append(('2024GD-57', dict(rules=[I('F', 'Q'), I('H', '~F')], concl=I('H', '~Q')), {
    'A': dict(rules=[I('S', 'W'), I('M', 'W')], concl=I('M', 'S')),
    'B': dict(rules=[I('K', 'Y'), I('K', 'E')], concl=I('G', 'Y')),
    'C': None,
    'D': dict(rules=[I('~O', 'P'), I('C', 'O')], concl=I('C', '~P')),
}, 'D', False))
Q.append(('2024GD-60', dict(rules=[I('A', 'B'), I('B', 'C')], concl=I('A', 'C')), {
    'A': dict(rules=[I('H', 'Z'), I('~H', 'Y')], concl=I('H', '~Y')),
    'B': dict(rules=[I('Y', 'J'), I('P', 'J')], concl=I('P', 'Y')),
    'C': dict(rules=[I('N', 'Q'), I('Q', 'G')], concl=I('N', 'G')),
    'D': dict(rules=[I('Z', 'F'), I('~F', '~Z')], concl=('and', [I('F', 'Z'), I('Z', 'F')])),
}, 'C', False))
Q.append(('2024SC-77', dict(rules=[I('J', 'X')], concl=I(['Y', 'J'], 'X'), case='Y'), {
    'A': dict(rules=[I('Q', 'Z'), I('Z', 'D')], concl=I('D', 'I')),
    'B': dict(rules=[I('G', 'R'), I('M', 'R')], concl=I('W', 'T')),
    'C': dict(rules=[I('P', 'S')], concl=I('Z', 'S')),
    'D': dict(rules=[I('K', 'L')], concl=I(['E', 'K'], 'L'), case='E'),
}, 'D', False))
Q.append(('2024SD-95', dict(rules=[I('F', 'K'), I('K', 'R')], concl=I('F', 'R')), {
    'A': dict(rules=[I('H', 'W'), I('T', 'D')], concl=I('H', '~D')),
    'B': dict(rules=[I('V', 'C'), I('C', 'O')], concl=I('V', 'C')),
    'C': None,                                                                     # 高矮关系的传递，不是条件/直言
    'D': dict(rules=[I('Y', 'Q'), I('Q', 'Z')], concl=I('Y', 'Z')),
}, 'D', False))
Q.append(('2022GD-70', dict(rules=[I('K', 'T'), I('G', 'K')], concl=I('G', 'T')), {
    'A': dict(rules=[I('P', 'H')], concl=I('H', 'P')),
    'B': dict(rules=[I('C', 'R'), I('D', 'C')], concl=I('D', 'R')),
    'C': dict(rules=[I('C', 'T')], concl='B'),
    'D': None,
}, 'B', False))
Q.append(('2023GD-64', dict(rules=[I('W', 'B'), I('H', '~W')], concl=I('H', '~B')), {
    'A': dict(rules=[I('M', 'R'), I('F', '~R')], concl=I('F', '~M')),
    'B': dict(rules=[I('S', 'J'), I('X', '~J')], concl=I('X', '~S')),
    'C': None,
    'D': dict(rules=[I('G', 'X'), I('T', '~G')], concl=I('T', '~X')),
}, 'D', False))
Q.append(('2023GD-72', dict(rules=[I('E', ('and', ['L', 'S']))], concl=I(['L', '~S'], '~E')), {
    'A': dict(rules=[I('M', ('and', ['W', 'X']))], concl=I('X', 'W')),
    'B': dict(rules=[I('G', 'Y')], concl=I('~Y', ('and', ['~Q', '~G']))),
    'C': dict(rules=[I('P', ('and', ['C', 'D']))], concl=I(['C', '~D'], '~P')),   # 按官方解析的理解
    'D': dict(rules=[I('M', ('and', ['J', 'W']))], concl=I(['J', '~W'], 'N')),
}, 'C', False))
Q.append(('2024SZ-41', dict(rules=[I('F', 'N'), I('F', 'K')], concl=I('N', 'K')), {
    'A': dict(rules=[I('T', 'U'), I('T', 'J')], concl=I('U', 'J')),
    'B': dict(rules=[I('F', 'D'), I('D', 'M')], concl=I('F', 'M')),
    'C': dict(rules=[I('L', 'R')], concl=I(['X', 'R'], 'L'), case='X'),
    'D': dict(rules=[I('F', 'Y'), I('Y', 'Z')], concl=I('F', 'Z')),
}, 'A', False))
Q.append(('2025GD-56', dict(rules=[I('W', 'Z'), ('some', 'G', 'W')], concl=('some', 'G', 'Z')), {
    'A': dict(rules=[('most', 'M', '~F'), ('some', 'S', 'F')], concl=('some', 'S', '~M'), quant=True),
    'B': dict(rules=[I('H', 'J'), ('most', 'E', 'H')], concl=('some', 'E', 'J'), quant=True),
    'C': dict(rules=[('most', 'R', 'Q'), ('most', 'R', 'B')], concl=('some', 'B', 'Q'), quant=True),
    'D': dict(rules=[I('K', 'P')], concl=I('A', 'X'), quant=True),
}, 'B', True))
Q.append(('2025GD-62', dict(rules=[I('P', 'V')], concl=I('~V', '~P')), {
    'A': dict(rules=[I('N', 'J')], concl=I('J', '~H')),
    'B': dict(rules=[I('G', 'J')], concl=I('~J', '~G')),
    'C': dict(rules=[I('S', 'E')], concl=I('~S', '~E')),
    'D': dict(rules=[I('N', 'W')], concl=I('W', 'N')),
}, 'B', False))
# 待识别答案的参考（不进 self_solved）
Q.append(('2022SC1-76 (参考)', dict(rules=[I('X', 'D'), I('D', 'L')], concl=I('X', 'L')), {
    'A': None,
    'B': dict(rules=[I('Q', 'J'), I('J', 'Z')], concl='K'),
    'C': dict(rules=[I('H', 'A'), I('R', 'A')], concl=I('H', 'R')),
    'D': dict(rules=[I('S', 'N'), I('N', 'E')], concl=I('S', 'E')),
}, 'D', False))

if __name__ == '__main__':
    all_errs = []
    for name, stem, opts, ans, quant in Q:
        all_errs += check_question(name, stem, opts, ans, verbose=True, quant=quant)
        print()
    print('TOTAL questions', len(Q), '| errors', len(all_errs))
    for e in all_errs: print('  ', e)
