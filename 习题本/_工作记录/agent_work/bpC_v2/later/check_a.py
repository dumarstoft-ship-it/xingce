import sys; sys.path.insert(0,'..')
from lib import *
from itertools import permutations, product, combinations
# D6 龙舟泊位（由北向南1-6号）：①甲乙相邻 ②丙在丁北边，中间隔两个泊位 ③甲与戊之间隔着一个泊位 ④己不在两端
N=['甲','乙','丙','丁','戊','己']
S=line(N,6,[lambda s:abs(s['甲']-s['乙'])==1, lambda s:s['丁']-s['丙']==3, lambda s:abs(s['甲']-s['戊'])==2, lambda s:s['己'] not in (1,6)])
print('D6 龙舟 解数',len(S)); [print('  ',fmt_line(s)) for s in S]
print('   戊可能位置', sorted({s['戊'] for s in S}))
S6=[s for s in S if s['乙']==6]
print('   乙在最南端:', [fmt_line(s) for s in S6])
# D10 城际线（由南向北1-6号）：①会展在大学城北边，两站中间隔一站 ②科技园与会展相邻 ③湿地不在两端 ④古镇在港口北边
N=['会展','大学城','科技园','湿地','古镇','港口']
S=line(N,6,[lambda s:s['会展']-s['大学城']==2, lambda s:abs(s['科技园']-s['会展'])==1, lambda s:s['湿地'] not in (1,6), lambda s:s['古镇']>s['港口']])
print('D10 城际线 解数',len(S)); [print('  ',fmt_line(s)) for s in S]
fixed=[x for x in N if len({s[x] for s in S})==1]; print('   确定位置的站',fixed)
S2=[s for s in S if abs(s['湿地']-s['大学城'])==1]; print('   湿地与大学城相邻:',[fmt_line(s) for s in S2])
# D8 六品种至少选4：'选荔枝则不选龙眼和菠萝''香蕉和芒果至少选一种''要么选杨桃，要么选龙眼'
T=['荔枝','龙眼','菠萝','香蕉','芒果','杨桃']
S=[]
for b in product([0,1],repeat=6):
    s=dict(zip(T,b))
    if sum(b)<4: continue
    if s['荔枝'] and (s['龙眼'] or s['菠萝']): continue
    if not (s['香蕉'] or s['芒果']): continue
    if s['杨桃']+s['龙眼']!=1: continue
    S.append(s)
print('D8 六品种 方案',[ [t for t in T if s[t]] for s in S])
print('   一定不选',[t for t in T if all(not s[t] for s in S)],'一定选',[t for t in T if all(s[t] for s in S)])
