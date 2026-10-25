import json, re, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
segs = []
for i in r["items"]:
    segs += re.findall(r"\$([^$]+)\$", i["problem"])
segs += re.findall(r"\$([^$]+)\$", r["overall"])
json.dump(segs, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
print(len(segs), "segments; dollar count even per item:",
      all(i["problem"].count("$") % 2 == 0 for i in r["items"]))
