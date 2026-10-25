import sys; sys.path.insert(0,'..')
from lib import *
N=['会展','大学城','科技园','湿地','古镇','港口']
S=line(N,6,[lambda s:s['古镇']-s['湿地']==3, lambda s:s['古镇'] not in (1,6), lambda s:abs(s['会展']-s['大学城'])==2, lambda s:abs(s['古镇']-s['港口'])==1])
fixed=[x for x in N if len({s[x] for s in S})==1]
count_options('D10-一拖二小题1',len(fixed),{'A':1,'B':2,'C':3,'D':4},'B')
S2=[s for s in S if s['会展']==1]
judge('D10-一拖二小题2',S2,{'A':lambda s:s['港口']==6,'B':lambda s:s['科技园']==6,'C':lambda s:s['大学城']==3,'D':lambda s:abs(s['大学城']-s['古镇'])==1},'impossible','D')
N=['甲','乙','丙','丁','戊','己']
S=line(N,6,[lambda s:abs(s['甲']-s['乙'])==1, lambda s:s['丁']-s['丙']==3, lambda s:abs(s['甲']-s['戊'])==2, lambda s:s['己'] not in (1,6)])
judge('D6-一拖二小题1',S,{'A':lambda s:s['戊']==1,'B':lambda s:s['戊']==2,'C':lambda s:s['戊']==4,'D':lambda s:s['戊']==5},'possible','C')
S6=[s for s in S if s['乙']==6]
judge('D6-一拖二小题2',S6,{'A':lambda s:s['甲']==4,'B':lambda s:s['己']==2,'C':lambda s:s['丁']==3,'D':lambda s:s['戊']==4},'must','B')
