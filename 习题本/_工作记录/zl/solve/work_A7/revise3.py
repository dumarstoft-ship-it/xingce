import json
OUT = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A7.json"
R = {
("MK2734X-M2",1): r"本题考查平均数比较。“十三五”为2016—2020年，单位面积产量=产量÷种植面积。2016、2018、2019、2020年分别约为4.79、4.90、5.04、5.11吨/亩，如2020年为 $\frac{12014}{2353}\approx5.11$。速算：2020年较2019年产量降约1.3%、面积降约2.6%，分母降得更多，比值上升；2019年较2018年产量增、面积减，比值也更大。故正确答案为D。",
("MK2707X-M3",3): r"本题考查平均数比较。每架订单交付额=交付额÷交付量，2016—2019年分别约为 $\frac{210.92}{2267}\approx0.093$、0.087、0.084、0.088亿美元，排序为2016年>2019年>2017年>2018年。速算：2017年较2016年分子减、分母增，必然更小，排除B、D；2019年交付额增速14.4%高于交付量增速8.8%，平均数高于2018年，排除C。故正确答案为A。",
}
d = json.load(open(OUT, encoding="utf-8"))
for m in d:
    for q in m["q"]:
        k = (m["mat"], q["n"])
        if k in R: q["jiexi"] = R[k]
json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
