import json, re
OUT = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B9.json"
TASK = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/B9.json"
data = json.load(open(OUT, encoding="utf-8"))
task = json.load(open(TASK, encoding="utf-8"))
assert [d["mat"] for d in data] == [t["mat"] for t in task], "mat order mismatch"
ok = True
cjk = re.compile(r'[一-鿿]')
def visible(s):
    # approximate visible length: drop latex commands and braces
    t = re.sub(r'\\(frac|times|approx|text|left|right)', '', s)
    t = t.replace('\\%', '%').replace('{','').replace('}','').replace('$','').replace('\\','')
    return len(t)
for d in data:
    assert len(d["q"]) == 5, d["mat"]
    for i, q in enumerate(d["q"]):
        assert q["n"] == i+1
        a = q["answer"]
        if a not in "ABCD" or len(a) != 1:
            print("bad answer", d["mat"], q["n"]); ok = False
        if not q["jiexi"].endswith(f"故正确答案为{a}。"):
            print("bad ending", d["mat"], q["n"]); ok = False
        if q["jiexi"].count("$") % 2:
            print("odd $", d["mat"], q["n"]); ok = False
        for seg in re.findall(r'\$(.*?)\$', q["jiexi"]):
            if cjk.search(seg):
                print("CJK in math", d["mat"], q["n"], seg); ok = False
        # ensure % inside math is escaped
        for seg in re.findall(r'\$(.*?)\$', q["jiexi"]):
            if re.search(r'(?<!\\)%', seg):
                print("unescaped % in math", d["mat"], q["n"], seg); ok = False
        if q["confidence"] not in ("high","medium","low"):
            print("bad conf", d["mat"], q["n"]); ok = False
        print(d["mat"], q["n"], a, q["confidence"], "raw", len(q["jiexi"]), "vis", visible(q["jiexi"]))
print("ALL OK" if ok else "PROBLEMS")
print("answers:", {d["mat"]: "".join(q["answer"] for q in d["q"]) for d in data})
