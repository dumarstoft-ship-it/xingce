import json, re
OUT = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A7.json"
TASK = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A7.json"
d = json.load(open(OUT, encoding="utf-8"))
t = json.load(open(TASK, encoding="utf-8"))
assert [m["mat"] for m in d] == [m["mat"] for m in t], "mat order/ids mismatch"
comp = {("MK2739X-M2",5),("MK2711X-M2",5),("MK2713X-M1",5),("MK2732X-M1",5)}
ok = True
for m in d:
    assert len(m["q"]) == 5, m["mat"]
    for q in m["q"]:
        a = q["answer"]; j = q["jiexi"]
        assert a in "ABCD" and len(a) == 1
        assert q["confidence"] in ("high","medium","low")
        mm = re.search(r"故正确答案为([A-D])。$", j)
        if not mm or mm.group(1) != a:
            print("BAD END", m["mat"], q["n"]); ok = False
        if j.count("$") % 2:
            print("ODD $", m["mat"], q["n"]); ok = False
        L = len(j)
        lim = 350 if (m["mat"], q["n"]) in comp else 250
        flag = "" if 80 <= L <= lim else "  <-- LENGTH"
        if flag: ok = False
        for bad in ["我的计算", "程序", "Python", "python"]:
            if bad in j: print("BAD WORD", bad, m["mat"], q["n"]); ok = False
        print(m["mat"], q["n"], a, q["confidence"], L, flag)
print("answers:", {m["mat"]: "".join(q["answer"] for q in m["q"]) for m in d})
print("ALL OK" if ok else "ISSUES")
