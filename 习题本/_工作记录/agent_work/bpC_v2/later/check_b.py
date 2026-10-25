import sys; sys.path.insert(0,'..')
from lib import *
from itertools import permutations, product, combinations
N=['会展','大学城','科技园','湿地','古镇','港口']
base=[lambda s:s['会展']-s['大学城']==2, lambda s:abs(s['科技园']-s['会展'])==1, lambda s:s['湿地'] not in (1,6)]
extras={
 '古镇在港口北边且相邻':lambda s:s['古镇']-s['港口']==1,
 '古镇在港口北边，两站中间隔两站':lambda s:s['古镇']-s['港口']==3,
 '港口站在最南端或最北端':lambda s:s['港口'] in (1,6),
 '古镇站与湿地站相邻':lambda s:abs(s['古镇']-s['湿地'])==1,
 '科技园站在会展站北边':lambda s:s['科技园']>s['会展'],
 '古镇站在会展站南边':lambda s:s['古镇']<s['会展'],
}
for k1,k2 in combinations(extras,2):
    S=line(N,6,base+[extras[k1],extras[k2]])
    if 3<=len(S)<=5:
        fixed=[x for x in N if len({s[x] for s in S})==1]
        if 1<=len(fixed)<=2:
            print(k1,'|',k2,'解数',len(S),'确定',fixed)
            for s in S: print('     ',fmt_line(s))
