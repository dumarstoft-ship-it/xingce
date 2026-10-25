import json, re, sys
key = json.load(open(sys.argv[1], encoding="utf-8"))
qs = {q["vid"]: q for q in json.load(open(sys.argv[2], encoding="utf-8"))}
# 1) each jiexi names exactly the keyed option
for q in key:
    m = re.findall(r"选([A-D])", q["jiexi"])
    if m != [q["answer"]]:
        print(q["vid"], "选 mentions", m, "answer", q["answer"])
# 2) stems/options in key identical to the blind question file
for q in key:
    b = qs[q["vid"]]
    if b["stem"] != q["stem"] or b["options"] != q["options"]:
        print("MISMATCH between key and question file:", q["vid"])
# 3) collect KaTeX segments
segs = []
for q in key:
    texts = [q["stem"], q["jiexi"], *q["options"].values()]
    for t in texts:
        segs += re.findall(r"\$([^$]+)\$", t)
json.dump(segs, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False)
print("checked", len(key), "items;", len(segs), "KaTeX segments ->", sys.argv[3])
