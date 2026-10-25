# -*- coding: utf-8 -*-
"""5道无官方答案真题的独立求解（从题面出发穷举）＋两道答案存疑题复核。"""
import sys; sys.path.insert(0,'..')
from lib import *
from itertools import permutations, product, combinations
# 2026GD-62：一排6座，位置1..6从左到右（"右手边"=编号更大，选项同一视角）
N=['教育','住建','交通','农业','人社','财政']
S=line(N,6,[lambda s:s['财政']==s['人社']+1, lambda s:s['住建']-s['财政']>=2,
            lambda s:abs(s['教育']-s['交通'])==2, lambda s:abs(s['农业']-s['财政'])==1])
print('2026GD-62', [fmt_line(s) for s in S])
judge('2026GD-62',S,{'A':lambda s:7-s['教育']==3,'B':lambda s:7-s['住建']==2,'C':lambda s:s['交通']==3,'D':lambda s:s['人社']==2},'must')
# 2026ZJA-97
N=['A','B','C','D','E','F']
S=line(N,6,[lambda s:abs(s['A']-s['C'])!=1, lambda s:abs(s['F']-s['C'])!=1,
            lambda s:[s['A'] in (1,6), s['B'] in (1,6)].count(True)==1, lambda s:s['C']==2 and s['E']==4])
print('2026ZJA-97', [fmt_line(s) for s in S])
judge('2026ZJA-97',S,{'A':lambda s:s['B']==1,'B':lambda s:s['B']==5,'C':lambda s:s['D']==5,'D':lambda s:s['D']==6},'possible')
# 2026GK-110
P=['甲','乙','丙','丁','戊','己','庚']
S=[]
for c in combinations(P,4):
    s=set(c)
    if '甲' in s and '丁' in s: continue
    if ('丙' in s or '戊' in s) and not ('甲' in s and '己' not in s): continue
    if ('乙' in s or '庚' in s) and not ('丁' in s and '甲' not in s): continue
    S.append(s)
print('2026GK-110', S)
judge('2026GK-110',S,{'A':lambda s:{'乙','庚'}<=s,'B':lambda s:{'丙','丁'}<=s,'C':lambda s:{'己','戊'}<=s,'D':lambda s:{'甲','乙'}<=s},'must')
# 2026ZJA-98
P=['琪琪','依依','冰冰','鑫鑫','磊磊','静静']
S=[]
for a in permutations([1,2,2,3,3,3]):
    s=dict(zip(P,a))
    if tuple(sorted(a))!=(1,2,2,3,3,3): continue
    if not (s['琪琪']==2 or s['冰冰']==1): continue                                  # 除非琪二，否则冰一
    if (s['琪琪']==2 or s['依依']==2) and not (s['鑫鑫']==3 and s['静静']==2): continue  # 只有(鑫三且静二)，(琪二或依二)
    if s['鑫鑫']==3 and not (s['冰冰']==2 and s['依依']!=3): continue
    if s not in S: S.append(s)
print('2026ZJA-98', S)
judge('2026ZJA-98',S,{'A':lambda s:s['冰冰']!=1,'B':lambda s:s['琪琪']==2,'C':lambda s:s['鑫鑫']!=1,'D':lambda s:s['磊磊']==3},'must')
# 2026GD-63："相当"=收入相等（允许并列）；收入用0..3的等级
V=['甲','乙','丙','丁']; AW=['文旅','非遗','生态','数字']
S=[]
for a in permutations(AW):
    A=dict(zip(V,a)); W={v:k for k,v in A.items()}
    for inc in product(range(4),repeat=4):
        I=dict(zip(V,inc)); top=max(inc)
        if not I[W['文旅']]>I['丙']: continue
        if W['数字']=='甲' or I['甲']!=I[W['数字']] or I['甲']==top: continue
        if not I[W['生态']]>I['丁']: continue
        if not I['丙']>I[W['非遗']]: continue
        S.append((A,I))
print('2026GD-63 获奖分配', sorted({tuple(x[0][v] for v in V) for x in S}))
second=lambda I,v: sum(I[u]>I[v] for u in V)==1 and sum(I[u]==I[v] for u in V)==1   # 严格的"位列第二"(无并列)
judge('2026GD-63',S,{'A':lambda x:second(x[1],'甲'),'B':lambda x:x[0]['乙']=='文旅','C':lambda x:x[0]['丙']=='数字','D':lambda x:x[0]['丁']=='非遗'},'must')
# 稳健性：若"相当"不要求相等（只要求都不是最高），答案会怎样？
S2=[]
for a in permutations(AW):
    A=dict(zip(V,a)); W={v:k for k,v in A.items()}
    for inc in permutations(range(4)):
        I=dict(zip(V,inc)); top=3
        if not I[W['文旅']]>I['丙']: continue
        if W['数字']=='甲' or I['甲']==top or I[W['数字']]==top: continue
        if not I[W['生态']]>I['丁']: continue
        if not I['丙']>I[W['非遗']]: continue
        S2.append((A,I))
print('   若"相当"不作相等理解: B 是否必然?', all(x[0]['乙']=='文旅' for x in S2), '获奖分配数', len({tuple(x[0][v] for v in V) for x in S2}))
# 2024SC-85 闭世界 vs 开放职务
tab={'甲':('赵','男','馆员','借阅'),'乙':('钱','女','研究馆员','咨询'),'丙':('孙','男','馆员','借阅'),'丁':('李','女','研究馆员','采编'),'戊':('钱','女','副研究馆员','借阅')}
for mode in ('闭世界','职务/部门可在表外'):
    dims=[{'赵','钱','孙','李'},{'男','女'},{v[2] for v in tab.values()},{v[3] for v in tab.values()}]
    if mode!='闭世界': dims[2]|={'表外职务'}; dims[3]|={'表外部门'}
    S=[c for c in product(*dims) if all(sum(v[i]==c[i] for i in range(4))==1 for v in tab.values())]
    print('2024SC-85',mode,S)
# 2020SZS-73
feas={sum(c) for c in product([1,3,5,7,9],repeat=6)}
liars=[n for n in range(5) if any(sum(not t for t in tr)==n and all((not t) or (x in feas) for t,x in zip(tr,(10,30,33,58))) for tr in product([True,False],repeat=4))]
print('2020SZS-73 可能的说谎人数', liars, '-> C(至少一人)与D(至少两人)都必然为真')
