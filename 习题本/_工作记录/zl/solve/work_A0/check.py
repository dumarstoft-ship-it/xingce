import json, re
OUT="/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A0.json"
INP="/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A0.json"
d=json.load(open(OUT,encoding="utf-8"))
inp=json.load(open(INP,encoding="utf-8"))
assert [x["mat"] for x in d]==[x["mat"] for x in inp], "mat order mismatch"
ok=True
def visible(s):
    # strip latex: remove $ and commands, keep content roughly
    t=s
    t=re.sub(r"\\text\{([^}]*)\}", r"\1", t)
    t=re.sub(r"\\frac", "", t)
    t=re.sub(r"\\(times|approx|left|right|cdot)", "x", t)
    t=t.replace("\\%","%").replace("$","").replace("{","").replace("}","")
    return t
for m in d:
    qs=m["q"]
    if len(qs)!=5: print("BAD count", m["mat"]); ok=False
    for i,q in enumerate(qs):
        if q["n"]!=i+1: print("BAD n", m["mat"], q["n"]); ok=False
        if q["answer"] not in "ABCD" or len(q["answer"])!=1: print("BAD ans", m["mat"], q["n"]); ok=False
        if not q["jiexi"].endswith("故正确答案为%s。"%q["answer"]): print("BAD end", m["mat"], q["n"]); ok=False
        if q["jiexi"].count("故正确答案为")!=1: print("BAD multiple end", m["mat"], q["n"]); ok=False
        if q["confidence"] not in ("high","medium","low"): print("BAD conf"); ok=False
        js=q["jiexi"]
        if js.count("$")%2: print("ODD $", m["mat"], q["n"]); ok=False
        # check math segments: no unescaped % and no CJK outside \text
        segs=re.findall(r"\$([^$]*)\$", js)
        for s in segs:
            if re.search(r"(?<!\\)%", s): print("UNESCAPED % in math", m["mat"], q["n"], s); ok=False
            s2=re.sub(r"\\text\{[^}]*\}","",s)
            if re.search(r"[\u4e00-\u9fff]", s2): print("CJK in math", m["mat"], q["n"], s); ok=False
            if s.count("{")!=s.count("}"): print("BRACE", m["mat"], q["n"], s); ok=False
        outside=re.sub(r"\$[^$]*\$","",js)
        if "\\" in outside: print("BACKSLASH outside math", m["mat"], q["n"]); ok=False
        for bad in ["根据我的计算","程序","计算机","Python","python"]:
            if bad in js: print("BAD word", bad, m["mat"], q["n"]); ok=False
        print(m["mat"], q["n"], q["answer"], q["confidence"], "raw", len(js), "visible", len(visible(js)))
print("ALL OK" if ok else "PROBLEMS")
print("mats:", len(d))
