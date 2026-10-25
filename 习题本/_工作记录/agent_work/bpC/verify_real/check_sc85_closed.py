from itertools import product
tab = {'甲': ('赵','男','馆员','借阅'), '乙': ('钱','女','研究馆员','咨询'), '丙': ('孙','男','馆员','借阅'),
       '丁': ('李','女','研究馆员','采编'), '戊': ('钱','女','副研究馆员','借阅')}
for mode in ('closed', 'surname_from_options_only'):
    dims = [set(v[i] for v in tab.values()) for i in range(4)]
    if mode == 'surname_from_options_only':
        dims[2] |= {'表外职务'}; dims[3] |= {'表外部门'}
    S = [c for c in product(*dims) if all(sum(1 for i in range(4) if v[i] == c[i]) == 1 for v in tab.values())]
    print(mode, S)
