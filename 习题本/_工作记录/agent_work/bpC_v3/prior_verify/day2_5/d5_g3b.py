from itertools import product, combinations
U=['A','B','C']; K=['党员','退役军人','志愿者']
W=[dict(zip(U,p)) for p in product(K,repeat=3)]
designs={
 'X':[lambda w:(w['A']!='志愿者') or w['B']=='党员',          # 只有B党员，A才志愿者
      lambda w:(w['A']!='党员') or w['C']=='退役军人',         # 除非C退役军人，否则A不党员 (A党员->C退役)
      lambda w:(w['B']=='志愿者') or w['C']=='志愿者'],        # 如果B不志愿者，那么C志愿者
 'Y':[lambda w:(w['A']!='志愿者') or w['B']=='党员',
      lambda w:(w['C']!='党员') or w['A']=='退役军人',         # 如果C党员，那么A退役军人
      lambda w:(w['B']!='退役军人') or (w['A']=='党员' or w['C']=='党员')],  # 如果B退役军人，那么A或C有党员
}
for name,ps in designs.items():
    S=[w for w in W if all(p(w) for p in ps)]
    S1=[w for w in S if len(set(w.values()))==3]
    print(name,'全部',len(S)); [print('   ',w) for w in S]
    print('  各不相同',S1)
