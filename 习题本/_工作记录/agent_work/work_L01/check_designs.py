# 快速核对蓝图里写明了结论的几处改编设计（不是正式验算脚本，只为保证 idea 本身无逻辑错误）
import itertools
def imp(a,b): return (not a) or b
def models(names, prem):
    for v in itertools.product([False,True], repeat=len(names)):
        m=dict(zip(names,v))
        if all(p(m) for p in prem): yield m
def necessary(names, prem):
    ms=list(models(names,prem)); assert ms
    return {k:(all(m[k] for m in ms) and 'T') or (all(not m[k] for m in ms) and 'F') or '?' for k in names}, ms

# D15 G4 v1
n=list("ABCD")
P=[lambda m: imp(not m['A'] and not m['B'], m['C']), lambda m: imp(m['B'] or m['C'], m['D']),
   lambda m: imp(m['A'] or m['B'], (not m['C']) and m['D'])]
print('D15G4v1', necessary(n,P)[0])

# D15 G4 v2 南沙N 前海Q 横琴H 河套T 松山湖S
n=list("NQHTS")
P=[lambda m: m['N'] or m['Q'], lambda m: m['H'] or m['N'] or m['T'],
   lambda m: m['Q']+m['T']+m['S']>=2, lambda m: imp(not m['N'], not m['H'])]
nec, ms = necessary(n,P)
print('D15G4v2', nec, 'min count', min(sum(m.values()) for m in ms))
# 两两"至少一个"的必然性
for a,b in itertools.combinations(n,2):
    if all(m[a] or m[b] for m in ms): print('  必然至少一个:',a,b)

# D15 G4 v4 / D28 G5 v1
n=list("ABCDEFG")
P=[lambda m: m['A']+m['B']+m['C']>=2, lambda m: imp(m['D'] or m['A'], not m['E'] and not m['B']),
   lambda m: imp(m['F'] or m['A'] or m['B'], m['E'] and not m['D'])]
print('D15G4v4', necessary(n,P)[0])
P=[lambda m: m['A']+m['B']+m['C']>=2, lambda m: imp(m['D'] or m['E'] or m['A'], not m['F'] and not m['B']),
   lambda m: imp(m['G'] or m['A'] or m['B'], m['F'] and not m['D'])]
print('D28G5v1', necessary(n,P)[0])

# D8 G3 v6 环形链
n=list("ABC")
P=[lambda m: imp(m['A'],m['B']), lambda m: imp(m['B'],m['C']), lambda m: imp(m['C'],m['A'])]
ms=list(models(n,P)); print('D8G3v6 models', ms)

# D34 G2 v3: 甲∨乙; 丙 xor 丁; ¬甲→丙; 已知丁
n=['J','Y','B','D']
P=[lambda m: m['J'] or m['Y'], lambda m: m['B']!=m['D'], lambda m: imp(not m['J'], m['B']), lambda m: m['D']]
print('D34G2v3', necessary(n,P)[0])

# D15 G5 v1 模板A否定目标：义诊Y或宣讲X；义诊→¬后勤H；小周后勤；目标 ¬摄影S
n=['Y','X','H','S']
P=[lambda m: m['Y'] or m['X'], lambda m: imp(m['Y'], not m['H']), lambda m: m['H']]
T=lambda m: not m['S']
opts={'宣讲→¬摄影':lambda m: imp(m['X'], not m['S']), '¬摄影→宣讲':lambda m: imp(not m['S'], m['X']),
      '小周¬义诊':lambda m: not m['Y'], '摄影→义诊':lambda m: imp(m['S'], m['Y']), '摄影→宣讲':lambda m: imp(m['S'], m['X'])}
for k,f in opts.items():
    ms=list(models(n,P+[f])); print('D15G5v1', k, bool(ms) and all(T(m) for m in ms))

# D34 G1 v4 12村：通气≥7，广场≥9 → 重叠最小
print('D34G1v4 min overlap', min(a+b-12 for a in range(7,13) for b in range(9,13) if a+b-12>=0))
# D21 G3 v4 40人：急救≥25，手语≥20
print('D21G3v4 min overlap', max(0, 25+20-40))
