import json, re, collections
KF = {
 '一': ['2020JSA-55','2023ZJA-66','2020ZJB-18','2026ZJA-59','2020SC1206-44','2025HB-74','2021GK-70'],
 '二': ['2020SD-41','2024GK-70','2023SC-47','2023JSA-59','2023ZJA-62','2023GK-67','2020SC1206-49','2024HB-71','2021SD-36','2025ZJA-69'],
 '三': ['2024GD-38','2026ZJA-55','2020HB-74','2022JSA-67','2026CQ-66'],
 '四': ['2023JSA-53','2020ZJB-12','2022GD-39','2025JSA-59','2022JSA-59'],
 '五': ['2025ZJA-66','2026GD-41','2025GK-78','2023GK-64','2022ZJA-65','2025SC-49','2026CQ-65'],
 '六': ['2023SC-53','2024ZJA-65','2022SC1-53','2025HB-80','2024HB-69','2024GK-71'],
 '七': ['2023HB-70','2024HB-64','2020HB-68','2026GK-75','2024SC-53'],
 '八': ['2022ZJA-67','2025HB-78','2024SC-55'],
 '九': ['2020HB-69','2023GD-34','2023JSA-57','2023HB-69','2023SZ-51'],
 '十': ['2025HB-77','2020SC0725-55','2024JSA-58','2022GK-73','2026GK-72'],
 '十一': ['2025HB-79','2021GK-74','2025GK-80','2024HB-70','2020SC0725-54','2023GK-75'],
 '十二': ['2021JSA-65','2022ZJA-68','2021SD-41','2025JSA-65','2026ZJA-64'],
 '十三': ['2022SD-36','2024ZJA-67','2022ZJA-69','2022SC2-44','2025SC-48'],
 '十四': ['2025HB-67','2024JSA-65'],
 '十五': [],
}
EXCL = ['2022JSA-55','2023JSA-55']
d = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/tasks_in/M08.json'))
Q = {q['id']: q for q in d['real']}
allk = [i for v in KF.values() for i in v]
assert len(allk) == len(set(allk))
assert set(allk) | set(EXCL) == set(Q), (set(Q) - set(allk) - set(EXCL), set(allk) - set(Q))
def paper(i):
    y, p = re.match(r'(\d{4})([A-Z]+)', i).groups()
    p = {'ZJA':'浙江','ZJB':'浙江B','GK':'国考','GD':'广东','JSA':'江苏','HB':'河北','SD':'山东','SC':'四川','SZ':'深圳','CQ':'重庆'}.get(p, p)
    return p, y
for k, v in KF.items():
    by = collections.defaultdict(list)
    for i in v:
        p, y = paper(i); by[p].append(y)
    diffs = collections.Counter(Q[i]['difficulty'] for i in v)
    print(f'考法{k}: {len(v)}题 难度{dict(sorted(diffs.items()))} ', {p: sorted(ys) for p, ys in by.items()})
cnt = collections.Counter(paper(i) for i in Q)
print()
for p in ['广东','国考','浙江','浙江B','江苏','河北','山东','四川','深圳','重庆']:
    print(p, sorted([(y, c) for (pp, y), c in cnt.items() if pp == p]))
json.dump({'KF': KF, 'EXCL': EXCL}, open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M08_work/assign.json', 'w'), ensure_ascii=False, indent=1)
