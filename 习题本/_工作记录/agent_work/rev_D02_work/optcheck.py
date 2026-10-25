import json, re, sys
from fractions import Fraction as F
qpath, vdir = sys.argv[1], sys.argv[2]
qs = json.load(open(qpath, encoding='utf-8'))
for q in qs:
    src = open(f"{vdir}/{q['vid']}.py", encoding='utf-8').read()
    m = re.search(r"^(OPTS|OPTIONS)\s*=\s*(\{.*?\})\s*$", src, re.M)
    d = eval(m.group(2), {'F': F})
    ok = True
    for k, v in q['options'].items():
        sv = d[k]
        if isinstance(sv, str):
            ok &= (sv == v)
        else:
            ok &= (F(sv) == F(v))
    print(q['vid'], 'MATCH' if ok and set(d) == set(q['options']) else 'MISMATCH', d)
