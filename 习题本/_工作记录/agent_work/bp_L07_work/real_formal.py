"""回归测试：把本模块的形式类真题编码后跑核对器，检查“官方答案（或自解答案）恰好唯一同构”。
同时给 6 道无官方答案的真题出自解答案。运行：python3 -I real_formal.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checker import check_question, validity

def A(rules=(), facts=(), concl=None, case=None):
    return dict(rules=list(rules), facts=list(facts), concl=concl, case=case)

def imp(a, c, *fl):
    return ('imp', a if isinstance(a, list) else [a], c) + tuple(fl)

Q = {}

# ---------------- 考法一 串联
Q['2022GD-69'] = ('C',
    A([imp('Z', 'Y'), imp('Y', 'J')], concl=imp('Z', 'J')),
    {'A': A([imp('K', 'L', 'w'), ('some', 'L', 'G')], concl=imp('K', 'G', 'w')),
     'B': A([imp('S', 'R'), imp('H', 'R')], concl=imp('S', 'H')),
     'C': A([imp('k', 'l'), imp('l', 'z')], concl=imp('k', 'z')),
     'D': A([imp('L', 'M'), imp('M', 'H')], concl=imp('L', 'C'))})
Q['2026GD-61'] = ('B',   # 自解
    A([imp('G', 'X'), imp('X', 'W')], concl=imp('G', 'W')),
    {'A': A([imp('F', 'B'), imp('B', 'J')], concl=imp('~F', '~J')),
     'B': A([imp('M', 'L'), imp('K', 'M')], concl=imp('K', 'L')),
     'C': A([imp('C', 'E'), imp('E', 'R')], concl=imp('R', 'C')),
     'D': A([imp('S', 'Y'), imp('H', 'Y')], concl=imp('H', 'S'))})
Q['2024GD-60'] = ('C',
    A([imp('J', 'B'), imp('B', 'L')], concl=imp('J', 'L')),
    {'A': A([imp('C', 'Z'), imp('~C', 'S')], concl=imp('C', '~S')),
     'B': A([imp('Y', 'H'), imp('P', 'H')], concl=imp('P', 'Y')),
     'C': A([imp('X', 'Q'), imp('Q', 'G')], concl=imp('X', 'G')),
     'D': None})
Q['2024SD-95'] = ('D',
    A([imp('F', 'K'), imp('K', 'R')], concl=imp('F', 'R')),
    {'A': A([imp('a', 'm'), imp('b', 'd')], concl=imp('a', '~d')),
     'B': A([imp('X', 'C'), imp('C', 'Z')], concl=imp('X', 'C')),
     'C': A([('rel', 'T', 'z', 'w'), ('rel', 'T', 'w', 'l')], concl=('rel', 'T', 'z', 'l')),
     'D': A([imp('C', 'Q'), imp('Q', 'Y')], concl=imp('C', 'Y'))})
Q['2022GD-70'] = ('B',
    A([imp('S', 'T'), imp('x', 'S')], concl=imp('x', 'T'), case='x'),
    {'A': A([imp('P', 'H')], concl=imp('H', 'P')),
     'B': A([imp('K', 'R'), imp('L', 'K')], concl=imp('L', 'R')),
     'C': None,
     'D': A([imp('K', 'B'), imp('Y', 'G')], concl=imp('Y', 'B'))})
Q['2022SC1-76'] = ('D',  # 自解
    A([imp('N', 'P'), imp('P', 'L')], concl=imp('N', 'L')),
    {'A': None,
     'B': A([imp('Q', 'J'), imp('F', 'J')], concl=imp('Q', 'Z')),
     'C': A([imp('H', 'S'), imp('R', 'S')], concl=imp('H', 'R')),
     'D': A([imp('M', 'H'), imp('H', 'E')], concl=imp('M', 'E'))})

# ---------------- 考法二 量词
Q['2025GD-56'] = ('B',
    A([imp('W', 'Z'), ('most', 'H', 'W')], concl=('most', 'H', 'Z')),
    {'A': A([imp('X', '~F', 'w'), ('most', 'S', 'F')], concl=('some', 'S', '~X')),
     'B': A([imp('G', 'J'), ('most', 'M', 'G')], concl=('some', 'M', 'J')),
     'C': A([('most', 'R', 'Q'), ('most', 'R', 'B')], concl=('some', 'B', 'Q')),
     'D': A([imp('K', 'P')], concl=imp('D', 'N'))})
Q['2024SZ-41'] = ('A',
    A([imp('F', 'L'), imp('F', 'K')], concl=imp('L', 'K')),
    {'A': A([imp('T', 'D'), imp('T', 'J')], concl=imp('D', 'J')),
     'B': A([imp('Z', 'Y'), imp('Y', 'W')], concl=imp('Z', 'W')),
     'C': A([imp('L', 'D'), imp('x', 'D')], concl=imp('x', 'L'), case='x'),
     'D': A([imp('Z', 'Y'), imp('Y', 'J')], concl=imp('Z', 'J'))})

# ---------------- 考法三 有效式
Q['2024SC-77'] = ('D',
    A([imp('G', 'X')], concl=imp(['y', 'G'], 'X'), case='y'),
    {'A': A([imp('J', 'Z'), imp('Z', 'C')], concl=imp('C', 'I')),
     'B': A([imp('F', 'R'), imp('M', 'R')], concl=imp('Z', 'W')),
     'C': A([imp('Z', 'P')], concl=imp('S', 'J')),
     'D': A([imp('K', 'D')], concl=imp(['d', 'K'], 'D'), case='d')})
Q['2022GD-73'] = ('A',
    A([imp('a', 'b'), imp('c', '~b')], concl=imp('c', '~a')),
    {'A': A([imp('d', 'k'), imp('g', '~k')], concl=imp('g', '~d')),
     'B': A([imp('~y', '~j'), imp('~y', '~w')], concl=imp(['j', 'w'], 'y')),
     # C 的“往往……较难……”按非必然处理；若把它当必然，C 与题干同构（见问题清单）
     'C': A([imp('a', 'b', 'w'), imp('c', '~b')], concl=imp('a', '~c', 'w')),
     'D': A([imp('Y', 'B'), imp('S', 'D')], concl=('and', ['B', 'D']))})
Q['2022GD-73/C按必然'] = ('C',
    A([imp('a', 'b'), imp('c', '~b')], concl=imp('c', '~a')),
    {'C': A([imp('e', 'q'), imp('v', '~q')], concl=imp('e', '~v'))})
Q['2025GD-62'] = ('B',
    A([imp('G', 'W')], concl=imp('~W', '~G')),
    {'A': A([imp('I', 'M')], concl=imp('M', 'I')),
     'B': A([imp('Y', 'J')], concl=imp('~J', '~Y')),
     'C': A([imp('N', 'E')], concl=imp('~N', '~E')),
     'D': A([imp('T', 'F')], concl=imp('F', 'T'))})

# ---------------- 考法四 无效式
Q['2023GD-69'] = ('A',
    A([imp('W', 'L'), imp('x', '~W')], concl=imp('x', '~L'), case='x'),
    {'A': A([imp('U', 'D'), imp('x', '~U')], concl=imp('x', '~D'), case='x'),
     'B': A([imp('~Y', '~X', 'dn'), imp('x', 'X')], concl=imp('x', 'Y'), case='x'),
     'C': A([imp('J', 'D'), imp('x', '~D')], concl=imp('x', '~J'), case='x'),
     'D': A([imp('P', 'S'), imp('x', '~S')], concl=imp('x', '~P'), case='x')})
Q['2026GK-115'] = ('C',  # 自解
    A([imp('x', 'Y'), imp('J', 'Y')], concl=imp('x', 'J'), case='x'),
    {'A': A([imp('x', 'M'), imp('M', 'N'), imp('N', 'F')], concl=imp('x', 'F'), case='x'),
     'B': None,
     'C': A([imp('S', 'G'), imp('x', 'G')], concl=imp('x', 'S'), case='x'),
     'D': A([imp('K', 'W', 'w'), imp('x', 'K')], concl=imp('x', 'W'), case='x')})
Q['2024GD-57'] = ('D',
    A([imp('S', 'W'), imp('R', '~S')], concl=imp('R', '~W')),
    {'A': A([imp('Y', 'B'), imp('x', 'B')], concl=imp('x', 'Y'), case='x'),
     'B': None,
     'C': None,
     'D': A([imp('~Z', 'P'), imp('x', 'Z')], concl=imp('x', '~P'), case='x')})
Q['2023GD-64'] = ('D',
    A([imp('T', 'B'), imp('H', '~T')], concl=imp('H', '~B')),
    {'A': A([imp('R', 'H'), imp('x', '~H')], concl=imp('x', '~R'), case='x'),
     'B': A([imp('Y', 'J'), imp('x', '~J')], concl=imp('x', '~Y'), case='x'),
     'C': None,
     'D': A([imp('M', 'X'), imp('x', '~M')], concl=imp('x', '~X'), case='x')})
Q['2026GD-57'] = ('C',   # 自解
    A([imp('~A', '~B', 'dn')], facts=['A'], concl='B'),
    {'A': A([imp('H', 'M')], facts=['H'], concl='M'),
     'B': A([imp('~F', '~Q', 'dn')], facts=['~Q'], concl='~F'),
     'C': A([imp('~E', '~R', 'dn')], concl=imp('E', 'R')),
     'D': A([imp('H', 'S')], facts=['G'], concl='S')})

# ---------------- 考法五 联言、选言
Q['2025GD-58'] = ('C',
    A([imp('M', ('and', ['E', 'C']))], concl=imp(['E', '~C'], '~M')),
    {'A': A([imp('Z', 'R')], concl=imp('C', 'H')),
     'B': A([imp('F', ('and', ['S', 'G']))], concl=imp('Q', 'F')),
     'C': A([imp('H', ('and', ['S', 'T']))], concl=imp(['S', '~T'], '~H')),
     'D': A([imp('T', 'C')], concl=imp('~C', '~T'))})
Q['2023GD-72'] = ('C',
    A([imp('Y', ('and', ['L', 'R']))], concl=imp(['L', '~R'], '~Y')),
    {'A': A([imp('M', ('and', ['W', 'X']))], concl=imp('X', 'W')),
     'B': A([imp('Y', 'S')], concl=imp('~S', ('and', ['B', '~Y']))),
     'C': A([imp('P', ('and', ['G', 'D']))], concl=imp(['G', 'P'], 'D')),
     'D': A([imp('L', ('and', ['J', 'S']))], concl=imp(['J', '~S'], 'K'))})
Q['2026GD-65'] = ('D',   # 自解
    A([imp('J', ('or', ['P', 'Z'])), imp('x', '~P')], concl=imp(['x', 'J'], 'Z'), case='x'),
    {'A': A([imp('S', ('or', ['E', 'T'])), imp('x', '~T')], concl=imp('x', 'E'), case='x'),
     'B': A([('some', 'D', 'H'), ('some', 'D', 'Q'), imp('x', 'Q')], concl=imp('x', '~H'), case='x'),
     'C': A([imp('S', ('or', ['O', 'F'])), imp('x', 'O')], concl=imp('x', '~F'), case='x'),
     'D': A([imp('K', ('or', ['M', 'T'])), imp('x', 'K'), imp('x', '~T')], concl=imp('x', 'M'), case='x')})

# ---------------- 考法八（形式部分）集合概念题的官方形式化
Q['2020HB-110'] = ('C',
    A([imp('S', 'Q'), imp('J', 'S')], concl=imp('J', 'Q')),
    {'A': A([imp('N', '~R'), imp('L', '~N')], concl=imp('L', '~R')),
     'B': A([imp('F', 'Y'), imp('x', 'Y')], concl=imp('x', 'F'), case='x'),
     'C': A([imp('P', 'B'), imp('Y', 'P')], concl=imp('Y', 'B')),
     'D': A([imp('W', 'L'), ('some', 'G', 'L')], concl=('some', 'G', 'W'))})

if __name__ == '__main__':
    bad = 0
    for name, (ans, stem, opts) in Q.items():
        errs = check_question(name, stem, opts, ans)
        bad += bool(errs)
        print()
    print('questions with problems:', bad)
