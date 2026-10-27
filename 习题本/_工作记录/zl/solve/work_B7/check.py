import json, re
p = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B7.json"
task = json.load(open("/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/B7.json"))
d = json.load(open(p))
assert [m["mat"] for m in d] == [m["mat"] for m in task], "mat order mismatch"
ok = True
for m in d:
    assert len(m["q"]) == 5, m["mat"]
    assert [q["n"] for q in m["q"]] == [1,2,3,4,5]
    for q in m["q"]:
        a = q["answer"]
        if a not in "ABCD" or len(a)!=1:
            print("bad answer", m["mat"], q["n"]); ok=False
        j = q["jiexi"]
        mm = re.search(r"故正确答案为([A-D])。$", j)
        if not mm or mm.group(1)!=a:
            print("bad ending", m["mat"], q["n"]); ok=False
        if q["confidence"] not in ("high","medium","low"):
            print("bad conf", m["mat"], q["n"]); ok=False
        # math delimiters balanced
        if j.count("$")%2:
            print("unbalanced $", m["mat"], q["n"]); ok=False
        # no Chinese inside math
        for seg in re.findall(r"\$(.+?)\$", j):
            if re.search(r"[一-鿿]", seg):
                print("CJK in math", m["mat"], q["n"], seg); ok=False
        L = len(j)
        print(m["mat"], q["n"], a, q["confidence"], "len", L, "(over)" if L>350 or (L>250 and "综合" not in j[:12]) else "")
print("ALL OK" if ok else "PROBLEMS")
