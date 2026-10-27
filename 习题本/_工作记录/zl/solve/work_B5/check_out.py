import json, re
OUT = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B5.json"
IN = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/B5.json"
d = json.load(open(OUT, encoding="utf-8"))
inp = json.load(open(IN, encoding="utf-8"))
assert [m["mat"] for m in d] == [m["mat"] for m in inp], "mat order mismatch"
ok = True
for m in d:
    qs = m["q"]
    if len(qs) != 5: print("BAD count", m["mat"]); ok = False
    for i, q in enumerate(qs):
        tag = f'{m["mat"]} Q{q["n"]}'
        if q["n"] != i + 1: print("BAD n", tag); ok = False
        if q["answer"] not in "ABCD" or len(q["answer"]) != 1: print("BAD answer", tag); ok = False
        if not q["jiexi"].endswith(f'故正确答案为{q["answer"]}。'): print("BAD ending", tag); ok = False
        if q["jiexi"].count("故正确答案为") != 1: print("BAD multiple endings", tag); ok = False
        if q["confidence"] not in ("high", "medium", "low"): print("BAD conf", tag); ok = False
        if q["jiexi"].count("$") % 2: print("BAD odd $", tag); ok = False
        # flag bare % inside math
        for seg in re.findall(r"\$(.*?)\$", q["jiexi"]):
            if re.search(r"(?<!\\)%", seg): print("BARE % in math", tag, seg); ok = False
            if re.search(r"[一-鿿]", seg): print("CJK in math", tag, seg); ok = False
        L = len(q["jiexi"])
        zh = "综合分析" in q["jiexi"][:12]
        lim = 350 if zh else 250
        flag = "" if 80 <= L <= lim else "  <-- LENGTH"
        if flag: ok = False
        print(f'{tag} ans={q["answer"]} conf={q["confidence"]} len={L} (lim {lim}){flag}')
print("ALL OK" if ok else "ISSUES")
